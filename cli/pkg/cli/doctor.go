package cli

import (
	"context"
	"fmt"
	"net"
	"os"
	"strings"
	"time"

	"github.com/cline/cli/pkg/cli/display"
	"github.com/cline/cli/pkg/cli/global"
	"github.com/cline/cli/pkg/cli/terminal"
	"github.com/cline/cli/pkg/cli/updater"
	"github.com/cline/cli/pkg/common"
	"github.com/spf13/cobra"
)

// NewDoctorCommand creates the doctor command
func NewDoctorCommand() *cobra.Command {
	cmd := &cobra.Command{
		Use:     "doctor",
		Aliases: []string{"d"},
		Short:   "Check system health and diagnose problems",
		Long: `Check the health of your Cline CLI installation and diagnose problems.

Currently this command performs the following checks and fixes:

Terminal Configuration:
  - Detects your terminal emulator (VS Code, Cursor, Ghostty, Kitty, WezTerm, Alacritty)
  - Configures shift+enter to insert newlines in multiline input
  - Creates backups before modifying configuration files
  - Supported terminals: VS Code, Cursor, Ghostty, Kitty, WezTerm, Alacritty
  - iTerm2 works by default, Terminal.app requires manual setup

CLI Updates:
  - Checks npm registry for the latest version
  - Automatically installs updates via npm if available
  - Respects NO_AUTO_UPDATE environment variable
  - Skipped in CI environments

Note: Future versions will include additional health checks for Node.js version,
npm availability, Cline Core connectivity, database integrity, and more.`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runDoctorChecks()
		},
	}

	return cmd
}

// runDoctorChecks performs all doctor diagnostics and configuration
func runDoctorChecks() error {
	renderer := display.NewRenderer(global.Config.OutputFormat)

	fmt.Printf("\n%s\n\n", renderer.Bold("Cline Doctor - System Health Check"))

	fmt.Printf("%s\n\n", renderer.Dim("━━━ Network & Proxy Configuration ━━━"))
	checkNetworkAndProxy(renderer)

	// Configure terminal keybindings (terminal.go prints its own status)
	fmt.Printf("\n%s\n\n", renderer.Dim("━━━ Terminal Configuration ━━━"))
	terminal.SetupKeyboardSync()

	// Check for updates (updater.go prints its own status)
	fmt.Printf("\n%s\n\n", renderer.Dim("━━━ CLI Updates ━━━"))
	updater.CheckAndUpdateSync(global.Config.Verbose, true)

	// Summary
	fmt.Printf("\n%s\n", renderer.Dim("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
	fmt.Printf("\n%s\n\n", renderer.SuccessWithCheckmark("Health check complete"))

	return nil
}

func checkNetworkAndProxy(renderer *display.Renderer) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	fmt.Println("Checking localhost resolution and connectivity...")

	hasIssues := false

	localhostAddrs, err := net.LookupHost("localhost")
	if err != nil {
		fmt.Printf("%s Failed to resolve localhost: %v\n", renderer.Red("✗"), err)
		hasIssues = true
	} else {
		fmt.Printf("%s localhost resolves to: %s\n", renderer.Green("✓"), strings.Join(localhostAddrs, ", "))
		
		hasIPv4 := false
		hasIPv6 := false
		for _, addr := range localhostAddrs {
			ip := net.ParseIP(addr)
			if ip != nil {
				if ip.To4() != nil {
					hasIPv4 = true
				} else {
					hasIPv6 = true
				}
			}
		}
		
		if hasIPv4 && hasIPv6 {
			fmt.Printf("%s localhost has both IPv4 and IPv6 addresses (dual-stack)\n", renderer.Green("✓"))
		} else if hasIPv4 {
			fmt.Printf("%s localhost has IPv4 only\n", renderer.Yellow("⚠"))
		} else if hasIPv6 {
			fmt.Printf("%s localhost has IPv6 only\n", renderer.Yellow("⚠"))
		}
	}

	proxyVars := []string{"http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "no_proxy"}
	activeProxies := []string{}
	for _, varName := range proxyVars {
		if val := os.Getenv(varName); val != "" {
			activeProxies = append(activeProxies, fmt.Sprintf("%s=%s", varName, val))
		}
	}

	if len(activeProxies) > 0 {
		fmt.Printf("\n%s Proxy environment variables detected:\n", renderer.Yellow("⚠"))
		for _, proxy := range activeProxies {
			fmt.Printf("  %s\n", proxy)
		}

		noProxy := os.Getenv("NO_PROXY")
		if noProxy == "" {
			noProxy = os.Getenv("no_proxy")
		}

		if noProxy == "" {
			fmt.Printf("%s NO_PROXY is not set. This may cause issues with localhost connections on VPN.\n", renderer.Red("✗"))
			fmt.Printf("  Recommendation: Set NO_PROXY=localhost,127.0.0.1,[::1]\n")
			hasIssues = true
		} else {
			hasLocalhost := strings.Contains(noProxy, "localhost")
			has127 := strings.Contains(noProxy, "127.0.0.1")
			hasIPv6Loopback := strings.Contains(noProxy, "::1")

			if !hasLocalhost || !has127 {
				fmt.Printf("%s NO_PROXY does not include all loopback addresses\n", renderer.Yellow("⚠"))
				fmt.Printf("  Current: NO_PROXY=%s\n", noProxy)
				missing := []string{}
				if !hasLocalhost {
					missing = append(missing, "localhost")
				}
				if !has127 {
					missing = append(missing, "127.0.0.1")
				}
				if !hasIPv6Loopback {
					missing = append(missing, "[::1]")
				}
				fmt.Printf("  Recommendation: Add %s to NO_PROXY\n", strings.Join(missing, ", "))
				hasIssues = true
			} else {
				fmt.Printf("%s NO_PROXY includes localhost and 127.0.0.1\n", renderer.Green("✓"))
			}
		}
	} else {
		fmt.Printf("\n%s No proxy environment variables detected\n", renderer.Green("✓"))
	}

	registry := global.Clients.GetRegistry()
	if registry != nil {
		instances, err := registry.ListInstancesCleaned(ctx)
		if err == nil && len(instances) > 0 {
			fmt.Printf("\nTesting connectivity to running Cline instances...\n")
			
			for _, instance := range instances {
				testAddress := instance.Address
				
				status, err := common.PerformHealthCheck(ctx, testAddress)
				if err != nil {
					fmt.Printf("%s Failed to connect to %s: %v\n", renderer.Red("✗"), testAddress, err)
					hasIssues = true
				} else if status.String() == "SERVING" {
					fmt.Printf("%s Successfully connected to %s\n", renderer.Green("✓"), testAddress)
				} else {
					fmt.Printf("%s Instance %s status: %s\n", renderer.Yellow("⚠"), testAddress, status.String())
				}
			}
		}
	}

	if hasIssues {
		fmt.Printf("\n%s Network configuration issues detected. See recommendations above.\n", renderer.Yellow("⚠"))
		fmt.Printf("  These issues may cause healthcheck timeouts, especially when using VPN.\n")
	} else {
		fmt.Printf("\n%s Network configuration looks good\n", renderer.Green("✓"))
	}
}
