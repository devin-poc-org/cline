"""Instance management functionality."""

import os
import json
import subprocess
import signal
from typing import List, Dict, Optional
from cline_cli.core.grpc_client import GrpcClient
from cline_cli.utils.display import Display


class InstanceManager:
    """Manages Cline instances."""
    
    def __init__(self):
        """Initialize instance manager."""
        self.config_path = os.path.expanduser('~/.cline')
        self.registry_path = os.path.join(self.config_path, 'instance_registry.json')
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Ensure config directory exists."""
        os.makedirs(self.config_path, exist_ok=True)
    
    def _load_registry(self) -> Dict:
        """Load instance registry from disk."""
        if not os.path.exists(self.registry_path):
            return {'instances': [], 'default': None}
        
        with open(self.registry_path, 'r') as f:
            return json.load(f)
    
    def _save_registry(self, registry: Dict):
        """Save instance registry to disk."""
        with open(self.registry_path, 'w') as f:
            json.dump(registry, f, indent=2)
    
    def list_instances(self):
        """List all registered instances."""
        registry = self._load_registry()
        instances = registry.get('instances', [])
        default_instance = registry.get('default')
        
        if not instances:
            print("No Cline instances found.")
            print("Run 'cline-py instance new' to start a new instance, or 'cline-py task new \"...\"' to auto-start one.")
            return
        
        display = Display()
        display.show_instance_list(instances, default_instance)
    
    def set_default_instance(self, address: str):
        """Set the default instance.
        
        Args:
            address: Instance address
        """
        registry = self._load_registry()
        
        instances = registry.get('instances', [])
        if not any(inst['address'] == address for inst in instances):
            raise ValueError(f"Instance {address} not found. Run 'cline-py instance list' to see available instances")
        
        registry['default'] = address
        self._save_registry(registry)
    
    def is_default_instance(self, address: str) -> bool:
        """Check if an instance is the default.
        
        Args:
            address: Instance address
        
        Returns:
            True if default, False otherwise
        """
        registry = self._load_registry()
        return registry.get('default') == address
    
    def start_new_instance(self) -> Dict:
        """Start a new Cline instance.
        
        Returns:
            Instance information dictionary
        """
        core_port = self._find_available_port(51051)
        host_port = self._find_available_port(52051)
        
        address = f"localhost:{core_port}"
        
        
        
        instance = {
            'address': address,
            'core_port': core_port,
            'host_port': host_port,
            'status': 'SERVING',
            'version': 'unknown',
            'platform': 'CLI'
        }
        
        registry = self._load_registry()
        instances = registry.get('instances', [])
        instances.append(instance)
        registry['instances'] = instances
        
        if not registry.get('default'):
            registry['default'] = address
        
        self._save_registry(registry)
        
        return instance
    
    def kill_instance_by_address(self, address: str):
        """Kill an instance by address.
        
        Args:
            address: Instance address
        """
        registry = self._load_registry()
        instances = registry.get('instances', [])
        
        instance = None
        for inst in instances:
            if inst['address'] == address:
                instance = inst
                break
        
        if not instance:
            raise ValueError(f"Instance {address} not found")
        
        try:
            client = GrpcClient(address)
            process_info = client.get_process_info()
            pid = process_info.get('pid')
            
            if pid:
                os.kill(pid, signal.SIGTERM)
                print(f"✓ Killed {address} (PID {pid})")
            else:
                print(f"⚠ Instance {address} appears to be already dead")
        except Exception as e:
            print(f"✗ Failed to kill {address}: {e}")
        
        instances = [inst for inst in instances if inst['address'] != address]
        registry['instances'] = instances
        
        if registry.get('default') == address:
            registry['default'] = instances[0]['address'] if instances else None
        
        self._save_registry(registry)
    
    def kill_all_cli_instances(self):
        """Kill all CLI instances."""
        registry = self._load_registry()
        instances = registry.get('instances', [])
        
        cli_instances = [inst for inst in instances if inst.get('platform') == 'CLI']
        
        if not cli_instances:
            print("No CLI instances found to kill.")
            return
        
        print(f"Killing {len(cli_instances)} CLI instance(s)...")
        
        for instance in cli_instances:
            try:
                self.kill_instance_by_address(instance['address'])
            except Exception as e:
                print(f"Failed to kill {instance['address']}: {e}")
    
    def _find_available_port(self, start_port: int) -> int:
        """Find an available port starting from start_port.
        
        Args:
            start_port: Starting port number
        
        Returns:
            Available port number
        """
        import socket
        
        port = start_port
        while port < start_port + 100:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('localhost', port))
                sock.close()
                return port
            except OSError:
                port += 1
        
        raise RuntimeError(f"Could not find available port starting from {start_port}")
