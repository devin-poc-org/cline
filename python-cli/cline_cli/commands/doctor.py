"""System health check command."""

import sys
import click


@click.command(name='doctor')
def doctor_command():
    """Check system health and diagnose problems.
    
    Check the health of your Cline CLI installation and diagnose problems.
    
    Currently this command performs the following checks and fixes:
    
    Terminal Configuration:
      - Detects your terminal emulator (VS Code, Cursor, Ghostty, Kitty, WezTerm, Alacritty)
      - Configures shift+enter to insert newlines in multiline input
      - Creates backups before modifying configuration files
      - Supported terminals: VS Code, Cursor, Ghostty, Kitty, WezTerm, Alacritty
      - iTerm2 works by default, Terminal.app requires manual setup
    
    CLI Updates:
      - Checks PyPI for the latest version
      - Automatically installs updates via pip if available
      - Respects NO_AUTO_UPDATE environment variable
      - Skipped in CI environments
    
    Note: Future versions will include additional health checks for Python version,
    pip availability, Cline Core connectivity, database integrity, and more.
    """
    from cline_cli.core.doctor import Doctor
    
    try:
        doctor = Doctor()
        doctor.run_checks()
    except KeyboardInterrupt:
        click.echo("\nHealth check cancelled")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
