"""Configuration management functionality."""

import json
from typing import Dict, Any
from cline_cli.core.grpc_client import GrpcClient
from cline_cli.utils.display import Display


class ConfigManager:
    """Manages Cline configuration."""
    
    def __init__(self, address: str):
        """Initialize config manager.
        
        Args:
            address: Cline Core gRPC address
        """
        self.address = address
        self.client = GrpcClient(address)
    
    def get_current_instance(self) -> str:
        """Get the current instance address."""
        return self.address
    
    def list_settings(self):
        """List all configuration settings."""
        settings = self.client.get_all_settings()
        display = Display()
        display.show_settings(settings)
    
    def get_setting(self, key: str):
        """Get a specific setting value.
        
        Args:
            key: Setting key (supports dot notation)
        """
        settings = self.client.get_all_settings()
        
        value = settings
        for part in key.split('.'):
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                raise ValueError(f"Setting '{key}' not found")
        
        display = Display()
        display.show_setting_value(key, value)
    
    def update_settings(self, settings: list):
        """Update configuration settings.
        
        Args:
            settings: List of settings in key=value format
        """
        parsed_settings = self._parse_settings(settings)
        
        self.client.update_settings(parsed_settings)
        
        print("Settings updated successfully")
    
    def _parse_settings(self, settings: list) -> Dict[str, Any]:
        """Parse settings from key=value format.
        
        Args:
            settings: List of settings in key=value format
        
        Returns:
            Dictionary of parsed settings
        """
        parsed = {}
        for setting in settings:
            if '=' not in setting:
                raise ValueError(f"Invalid setting format: {setting}. Expected key=value")
            
            key, value = setting.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                pass
            
            if '.' in key:
                parts = key.split('.')
                current = parsed
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = value
            else:
                parsed[key] = value
        
        return parsed
