"""Tests for ConfigManager."""

import pytest
from cline_cli.core.config_manager import ConfigManager


class TestConfigManager:
    """Tests for ConfigManager class."""
    
    def test_parse_settings_simple(self):
        """Test parsing simple settings."""
        manager = ConfigManager('localhost:51051')
        settings = ['key1=value1', 'key2=value2']
        parsed = manager._parse_settings(settings)
        
        assert parsed == {'key1': 'value1', 'key2': 'value2'}
    
    def test_parse_settings_nested(self):
        """Test parsing nested settings with dot notation."""
        manager = ConfigManager('localhost:51051')
        settings = ['auto-approval.actions.read-files=true']
        parsed = manager._parse_settings(settings)
        
        assert 'auto-approval' in parsed
        assert 'actions' in parsed['auto-approval']
        assert parsed['auto-approval']['actions']['read-files'] is True
    
    def test_parse_settings_json_value(self):
        """Test parsing JSON values."""
        manager = ConfigManager('localhost:51051')
        settings = ['enabled=true', 'count=42']
        parsed = manager._parse_settings(settings)
        
        assert parsed['enabled'] is True
        assert parsed['count'] == 42
    
    def test_get_current_instance(self):
        """Test getting current instance address."""
        address = 'localhost:51051'
        manager = ConfigManager(address)
        
        assert manager.get_current_instance() == address
