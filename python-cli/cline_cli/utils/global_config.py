"""Global configuration management."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class GlobalConfig:
    """Global configuration for the CLI."""
    verbose: bool = False
    output_format: str = 'rich'
    core_address: str = 'localhost:51051'
    config_path: str = ''


_config: Optional[GlobalConfig] = None


def initialize_global_config(verbose: bool = False, 
                            output_format: str = 'rich',
                            core_address: str = 'localhost:51051') -> GlobalConfig:
    """Initialize the global configuration."""
    global _config
    
    config_path = os.environ.get('CLINE_CONFIG_PATH', 
                                 os.path.expanduser('~/.cline'))
    
    _config = GlobalConfig(
        verbose=verbose,
        output_format=output_format,
        core_address=core_address,
        config_path=config_path
    )
    
    return _config


def get_config() -> GlobalConfig:
    """Get the global configuration."""
    if _config is None:
        return initialize_global_config()
    return _config
