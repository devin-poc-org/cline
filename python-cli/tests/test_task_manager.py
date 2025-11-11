"""Tests for TaskManager."""

import pytest
from cline_cli.core.task_manager import TaskManager


class TestTaskManager:
    """Tests for TaskManager class."""
    
    def test_parse_settings_simple(self):
        """Test parsing simple settings."""
        manager = TaskManager('localhost:51051')
        settings = ['key1=value1', 'key2=value2']
        parsed = manager._parse_settings(settings)
        
        assert parsed == {'key1': 'value1', 'key2': 'value2'}
    
    def test_parse_settings_nested(self):
        """Test parsing nested settings with dot notation."""
        manager = TaskManager('localhost:51051')
        settings = ['auto-approval.read=true', 'auto-approval.write=false']
        parsed = manager._parse_settings(settings)
        
        assert 'auto-approval' in parsed
        assert parsed['auto-approval']['read'] is True
        assert parsed['auto-approval']['write'] is False
    
    def test_parse_settings_json_value(self):
        """Test parsing JSON values."""
        manager = TaskManager('localhost:51051')
        settings = ['enabled=true', 'count=42', 'list=[1,2,3]']
        parsed = manager._parse_settings(settings)
        
        assert parsed['enabled'] is True
        assert parsed['count'] == 42
        assert parsed['list'] == [1, 2, 3]
    
    def test_parse_settings_invalid_format(self):
        """Test parsing invalid setting format."""
        manager = TaskManager('localhost:51051')
        settings = ['invalid_setting_without_equals']
        
        with pytest.raises(ValueError, match='Invalid setting format'):
            manager._parse_settings(settings)
    
    def test_get_current_instance(self):
        """Test getting current instance address."""
        address = 'localhost:51051'
        manager = TaskManager(address)
        
        assert manager.get_current_instance() == address
