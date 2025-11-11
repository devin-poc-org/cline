#!/usr/bin/env python3
"""Main entry point for Cline Python CLI."""

import sys
import click
from typing import Optional, List

from cline_cli import __version__
from cline_cli.commands import task, instance, config, auth, version, logs, doctor
from cline_cli.utils.global_config import GlobalConfig, initialize_global_config


@click.group(invoke_without_command=True)
@click.argument('prompt', nargs=-1, type=str, required=False)
@click.option('--address', default='localhost:51051', 
              help='Cline Core gRPC address')
@click.option('-v', '--verbose', is_flag=True, 
              help='Verbose output')
@click.option('-F', '--output-format', 
              type=click.Choice(['rich', 'json', 'plain']), 
              default='rich',
              help='Output format')
@click.option('-i', '--image', 'images', multiple=True, 
              help='Attach image files')
@click.option('-f', '--file', 'files', multiple=True, 
              help='Attach files')
@click.option('-m', '--mode', 
              type=click.Choice(['act', 'plan']), 
              default='plan',
              help='Mode (act|plan)')
@click.option('-s', '--setting', 'settings', multiple=True, 
              help='Task settings (key=value format)')
@click.option('-y', '--yolo', is_flag=True, 
              help='Enable yolo mode (non-interactive)')
@click.option('--no-interactive', is_flag=True, 
              help='Enable yolo mode (non-interactive)')
@click.option('-o', '--oneshot', is_flag=True, 
              help='Full autonomous mode')
@click.pass_context
def cli(ctx, prompt, address, verbose, output_format, images, files, 
        mode, settings, yolo, no_interactive, oneshot):
    """Cline CLI - AI-powered coding assistant.
    
    Start a new task by providing a prompt:
      cline-py "Create a new Python script that prints hello world"
    
    Or pipe a prompt via stdin:
      echo "Create a todo app" | cline-py
      cat prompt.txt | cline-py --yolo
    
    Or run with no arguments to enter interactive mode:
      cline-py
    
    This CLI also provides task management, configuration, and monitoring capabilities.
    """
    initialize_global_config(
        verbose=verbose,
        output_format=output_format,
        core_address=address
    )
    
    if ctx.invoked_subcommand is not None:
        return
    
    from cline_cli.commands.task import create_and_follow_task
    
    yolo = yolo or no_interactive
    
    if oneshot:
        mode = 'plan'
        yolo = True
    
    prompt_text = ' '.join(prompt) if prompt else ''
    
    if not sys.stdin.isatty():
        stdin_content = sys.stdin.read().strip()
        if stdin_content:
            if prompt_text:
                prompt_text += ' ' + stdin_content
            else:
                prompt_text = stdin_content
    
    if not prompt_text:
        from cline_cli.utils.interactive import prompt_for_initial_task
        prompt_text = prompt_for_initial_task(address, mode)
        if not prompt_text:
            click.echo("Prompt required")
            sys.exit(1)
    
    try:
        create_and_follow_task(
            prompt=prompt_text,
            images=list(images),
            files=list(files),
            mode=mode,
            settings=list(settings),
            yolo=yolo,
            address=address,
            verbose=verbose
        )
    except KeyboardInterrupt:
        click.echo("\nTask cancelled by user")
        sys.exit(0)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


cli.add_command(task.task_group)
cli.add_command(instance.instance_group)
cli.add_command(config.config_group)
cli.add_command(auth.auth_command)
cli.add_command(version.version_command)
cli.add_command(logs.logs_group)
cli.add_command(doctor.doctor_command)


if __name__ == '__main__':
    cli()
