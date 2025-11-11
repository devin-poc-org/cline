"""Configuration management commands."""

import sys
import click


@click.group(name='config')
def config_group():
    """Manage Cline configuration."""
    pass


@config_group.command(name='list')
@click.option('--address', default='', help='Specific Cline instance address to use')
def config_list(address):
    """List all configuration settings."""
    from cline_cli.core.config_manager import ConfigManager
    from cline_cli.utils.global_config import get_config
    
    config = get_config()
    
    try:
        manager = ConfigManager(address or config.core_address)
        manager.list_settings()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@config_group.command(name='get')
@click.argument('key', type=str)
@click.option('--address', default='', help='Specific Cline instance address to use')
def config_get(key, address):
    """Get a specific configuration value."""
    from cline_cli.core.config_manager import ConfigManager
    from cline_cli.utils.global_config import get_config
    
    config = get_config()
    
    try:
        manager = ConfigManager(address or config.core_address)
        manager.get_setting(key)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@config_group.command(name='set')
@click.argument('settings', nargs=-1, type=str, required=True)
@click.option('--address', default='', help='Specific Cline instance address to use')
def config_set(settings, address):
    """Set configuration variables.
    
    Set one or more global configuration variables using key=value format.
    This command merges the provided settings with existing values, preserving
    unspecified fields. Only the fields you explicitly set will be updated.
    """
    from cline_cli.core.config_manager import ConfigManager
    from cline_cli.utils.global_config import get_config
    
    config = get_config()
    
    try:
        manager = ConfigManager(address or config.core_address)
        manager.update_settings(list(settings))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
