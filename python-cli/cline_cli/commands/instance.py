"""Instance management commands."""

import sys
import click


@click.group(name='instance')
def instance_group():
    """Manage Cline instances."""
    pass


@instance_group.command(name='list')
def instance_list():
    """List all registered Cline instances."""
    from cline_cli.core.instance_manager import InstanceManager
    
    try:
        manager = InstanceManager()
        manager.list_instances()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@instance_group.command(name='default')
@click.argument('address', type=str)
def instance_default(address):
    """Set the default Cline instance."""
    from cline_cli.core.instance_manager import InstanceManager
    
    try:
        manager = InstanceManager()
        manager.set_default_instance(address)
        click.echo(f"Switched to instance: {address}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@instance_group.command(name='new')
@click.option('-d', '--default', 'set_default', is_flag=True, 
              help='Set as default instance')
def instance_new(set_default):
    """Create a new Cline instance."""
    from cline_cli.core.instance_manager import InstanceManager
    
    try:
        manager = InstanceManager()
        click.echo("Starting new Cline instance...")
        
        instance = manager.start_new_instance()
        
        click.echo("Successfully started new instance:")
        click.echo(f"  Address: {instance['address']}")
        click.echo(f"  Core Port: {instance['core_port']}")
        click.echo(f"  Host Bridge Port: {instance['host_port']}")
        
        if set_default:
            manager.set_default_instance(instance['address'])
            click.echo("  Status: Set as default instance")
        elif manager.is_default_instance(instance['address']):
            click.echo("  Status: Default instance")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@instance_group.command(name='kill')
@click.argument('address', type=str, required=False)
@click.option('-a', '--all-cli', is_flag=True, 
              help='Kill all running CLI instances (excludes JetBrains)')
def instance_kill(address, all_cli):
    """Kill a Cline instance by address."""
    from cline_cli.core.instance_manager import InstanceManager
    
    if all_cli and address:
        click.echo("Error: cannot specify both --all-cli flag and address argument", err=True)
        sys.exit(1)
    
    if not all_cli and not address:
        click.echo("Error: requires exactly one address argument when --all-cli is not specified", err=True)
        sys.exit(1)
    
    try:
        manager = InstanceManager()
        
        if all_cli:
            manager.kill_all_cli_instances()
        else:
            manager.kill_instance_by_address(address)
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
