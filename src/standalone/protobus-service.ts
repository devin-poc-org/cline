import { Controller } from "@core/controller"
import { StreamingResponseHandler } from "@core/controller/grpc-handler"
import { addProtobusServices } from "@generated/hosts/standalone/protobus-server-setup"
import * as grpc from "@grpc/grpc-js"

import { ReflectionService } from "@grpc/reflection"
import { GrpcHandler, GrpcStreamingResponseHandler } from "@hosts/external/grpc-types"
import * as health from "grpc-health-check"
import { getPackageDefinition, log } from "./utils"

export const PROTOBUS_PORT = 26040

export function startProtobusService(controller: Controller): Promise<string> {
	return new Promise((resolve, reject) => {
		const server = new grpc.Server()

		// Set up health check.
		const healthImpl = new health.HealthImplementation({ "": "SERVING" })
		healthImpl.addToServer(server)

		// Add all the handlers for the ProtoBus services to the server.
		addProtobusServices(server, controller, wrapHandler, wrapStreamingResponseHandler)

		// Create reflection service with protobus service names
		const packageDefinition = getPackageDefinition()
		const reflection = new ReflectionService(packageDefinition, {
			services: getProtobusServiceNames(packageDefinition),
		})
		reflection.addToServer(server)

		const bindMode = process.env.PROTOBUS_BIND || "auto"

		// Start the server with appropriate bind addresses
		if (process.env.PROTOBUS_ADDRESS) {
			const host = process.env.PROTOBUS_ADDRESS
			bindAndStart(server, host, resolve, reject)
		} else if (bindMode === "ipv6") {
			const host = `[::1]:${PROTOBUS_PORT}`
			bindAndStart(server, host, resolve, reject)
		} else if (bindMode === "ipv4") {
			const host = `127.0.0.1:${PROTOBUS_PORT}`
			bindAndStart(server, host, resolve, reject)
		} else {
			bindDualStack(server, PROTOBUS_PORT, resolve, reject)
		}
	})
}

function bindAndStart(server: grpc.Server, host: string, resolve: (value: string) => void, reject: (reason: Error) => void) {
	server.bindAsync(host, grpc.ServerCredentials.createInsecure(), (err) => {
		if (err) {
			log(`Could not start ProtoBus service: Failed to bind to ${host}, port may be unavailable. ${err.message}`)
			reject(new Error(`Failed to bind ProtoBus to ${host}: ${err.message}`))
			return
		}
		server.start()
		log(`ProtoBus gRPC server listening on ${host}`)

		const proxyVars = ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "no_proxy"]
		const activeProxies = proxyVars.filter((v) => process.env[v])
		if (activeProxies.length > 0) {
			log(`Proxy environment variables detected: ${activeProxies.join(", ")}`)
			const noProxy = process.env.NO_PROXY || process.env.no_proxy || ""
			if (!noProxy.includes("127.0.0.1") && !noProxy.includes("localhost")) {
				log(
					"WARNING: Proxy is configured but 127.0.0.1 and localhost are not in NO_PROXY. " +
						"This may cause connection issues, especially on VPN. " +
						"Consider setting NO_PROXY=localhost,127.0.0.1,[::1]",
				)
			}
		}

		resolve(host)
	})
}

function bindDualStack(server: grpc.Server, port: number, resolve: (value: string) => void, reject: (reason: Error) => void) {
	const ipv4Host = `127.0.0.1:${port}`
	server.bindAsync(ipv4Host, grpc.ServerCredentials.createInsecure(), (err) => {
		if (err) {
			log(`Could not bind ProtoBus to IPv4 (${ipv4Host}): ${err.message}`)
			reject(new Error(`Failed to bind ProtoBus to ${ipv4Host}: ${err.message}`))
			return
		}

		const ipv6Host = `[::1]:${port}`
		server.bindAsync(ipv6Host, grpc.ServerCredentials.createInsecure(), (err) => {
			if (err) {
				log(`Could not bind ProtoBus to IPv6 (${ipv6Host}): ${err.message}`)
				log(`ProtoBus will only be available on IPv4 (${ipv4Host})`)
			} else {
				log(`ProtoBus bound to both IPv4 (${ipv4Host}) and IPv6 (${ipv6Host})`)
			}

			server.start()
			log(`ProtoBus gRPC server listening on ${ipv4Host}`)

			const proxyVars = ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "no_proxy"]
			const activeProxies = proxyVars.filter((v) => process.env[v])
			if (activeProxies.length > 0) {
				log(`Proxy environment variables detected: ${activeProxies.join(", ")}`)
				const noProxy = process.env.NO_PROXY || process.env.no_proxy || ""
				if (!noProxy.includes("127.0.0.1") && !noProxy.includes("localhost")) {
					log(
						"WARNING: Proxy is configured but 127.0.0.1 and localhost are not in NO_PROXY. " +
							"This may cause connection issues, especially on VPN. " +
							"Consider setting NO_PROXY=localhost,127.0.0.1,[::1]",
					)
				}
			}

			resolve(ipv4Host)
		})
	})
}

function getProtobusServiceNames(packageDefinition: { [x: string]: any }): string[] {
	// Filter service names to only include cline services
	const protobusServiceNames = Object.keys(packageDefinition).filter(
		(name) => name.startsWith("cline.") || name.startsWith("grpc.health"),
	)
	return protobusServiceNames
}

/**
 * Wraps a Promise-based handler function to make it compatible with gRPC's callback-based API.
 * This function converts an async handler that returns a Promise into a function that uses
 * the gRPC callback pattern.
 *
 * @template TRequest - The type of the request object
 * @template TResponse - The type of the response object
 * @param handler - The Promise-based handler function to wrap
 * @param controllerInstance - The controller instance to pass to the handler
 * @returns A gRPC-compatible callback-style handler function
 */
function wrapHandler<TRequest, TResponse>(
	handler: GrpcHandler<TRequest, TResponse>,
	controller: Controller,
): grpc.handleUnaryCall<TRequest, TResponse> {
	return async (call: grpc.ServerUnaryCall<TRequest, TResponse>, callback: grpc.sendUnaryData<TResponse>) => {
		try {
			log(`ProtoBus request: ${call.getPath()}`)
			const result = await handler(controller, call.request)
			callback(null, result)
		} catch (err: any) {
			log(`ProtoBus handler error: ${call.getPath()}\n${err.stack}`)
			callback({
				code: grpc.status.INTERNAL,
				message: err.message || "Internal error",
			} as grpc.ServiceError)
		}
	}
}

function wrapStreamingResponseHandler<TRequest, TResponse>(
	handler: GrpcStreamingResponseHandler<TRequest, TResponse>,
	controller: Controller,
): grpc.handleServerStreamingCall<TRequest, TResponse> {
	return async (call: grpc.ServerWritableStream<TRequest, TResponse>) => {
		try {
			const requestId = call.metadata.get("request-id").pop()?.toString()
			log(`ProtoBus gRPC streaming request: ${call.getPath()}`)

			const responseHandler: StreamingResponseHandler<TResponse> = (response, isLast, _sequenceNumber) => {
				try {
					call.write(response) // Use a bound version of call.write to maintain proper 'this' context

					if (isLast === true) {
						log(`Closing ProtoBus stream for ${requestId}`)
						call.end()
					}
					return Promise.resolve()
				} catch (error) {
					return Promise.reject(error)
				}
			}
			await handler(controller, call.request, responseHandler, requestId)
		} catch (err: any) {
			log(`ProtoBus handler error: ${call.getPath()}\n${err.stack}`)
			call.destroy({
				code: grpc.status.INTERNAL,
				message: err.message || "Internal error",
			} as grpc.ServiceError)
		}
	}
}
