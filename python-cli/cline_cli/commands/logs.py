"""Log management commands."""

import sys
import click


@click.group(name='logs')
def logs_group():
    """Manage Cline log files."""
    pass


@logs_group.command(name='list')
def logs_list():
    """List all log files."""
    from cline_cli.core.logs_manager import LogsManager
    
    try:
        manager = LogsManager()
        manager.list_logs()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@logs_group.command(name='clean')
@click.option('--older-than', default=7, type=int, 
              help='Delete logs older than N days')
@click.option('--all', 'delete_all', is_flag=True, 
              help='Delete all log files')
@click.option('--dry-run', is_flag=True, 
              help='Show what would be deleted without deleting')
def logs_clean(older_than, delete_all, dry_run):
    """Delete old log files."""
    from cline_cli.core.logs_manager import LogsManager
    
    try:
        manager = LogsManager()
        manager.clean_logs(older_than, delete_all, dry_run)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@logs_group.command(name='path')
def logs_path():
    """Print the logs directory path."""
    from cline_cli.core.logs_manager import LogsManager
    
    try:
        manager = LogsManager()
        click.echo(manager.get_logs_path())
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
