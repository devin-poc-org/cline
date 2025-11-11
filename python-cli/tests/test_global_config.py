"""Tests for global configuration."""

import pytest
from cline_cli.utils.global_config import GlobalConfig, initialize_global_config, get_config


class TestGlobalConfig:
    """Tests for GlobalConfig."""
    
    def test_initialize_global_config(self):
        """Test initializing global config."""
        config = initialize_global_config(
            verbose=True,
            output_format='json',
            core_address='localhost:51052'
        )
        
        assert config.verbose is True
        assert config.output_format == 'json'
        assert config.core_address == 'localhost:51052'
    
    def test_get_config(self):
        """Test getting global config."""
        initialize_global_config(verbose=True)
        
        config = get_config()
        
        assert config.verbose is True
    
    def test_default_values(self):
        """Test default configuration values."""
        config = initialize_global_config()
        
        assert config.verbose is False
        assert config.output_format == 'rich'
        assert config.core_address == 'localhost:51051'
