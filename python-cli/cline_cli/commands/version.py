"""Version command."""

import sys
import click
import platform


@click.command(name='version')
@click.option('--short', is_flag=True, help='Show only version number')
def version_command(short):
    """Show version information."""
    from cline_cli import __version__
    
    if short:
        click.echo(__version__)
    else:
        click.echo("Cline CLI (Python)")
        click.echo(f"Cline CLI Version:  {__version__}")
        click.echo(f"Python version:     {platform.python_version()}")
        click.echo(f"OS/Arch:            {platform.system()}/{platform.machine()}")
