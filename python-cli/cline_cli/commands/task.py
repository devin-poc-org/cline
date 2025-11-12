"""Task management commands."""

import sys
import click
from typing import List, Optional


@click.group(name='task')
def task_group():
    """Manage Cline tasks."""
    pass


@task_group.command(name='new')
@click.argument('prompt', nargs=-1, type=str, required=False)
@click.option('-i', '--image', 'images', multiple=True, help='Attach image files')
@click.option('-f', '--file', 'files', multiple=True, help='Attach files')
@click.option('--address', default='', help='Specific Cline instance address to use')
@click.option('-m', '--mode', type=click.Choice(['act', 'plan']), help='Mode (act|plan)')
@click.option('-s', '--setting', 'settings', multiple=True, 
              help='Task settings (key=value format)')
@click.option('-y', '--yolo', is_flag=True, help='Enable yolo mode (non-interactive)')
@click.option('--no-interactive', is_flag=True, help='Enable yolo mode (non-interactive)')
def task_new(prompt, images, files, address, mode, settings, yolo, no_interactive):
    """Create a new task."""
    from cline_cli.core.task_manager import TaskManager
    from cline_cli.utils.global_config import get_config
    
    config = get_config()
    
    prompt_text = ' '.join(prompt) if prompt else ''
    
    if not sys.stdin.isatty():
        stdin_content = sys.stdin.read().strip()
        if stdin_content:
            if prompt_text:
                prompt_text += ' ' + stdin_content
            else:
                prompt_text = stdin_content
    
    if not prompt_text:
        click.echo("Error: prompt required: provide as argument or pipe via stdin", err=True)
        sys.exit(1)
    
    yolo = yolo or no_interactive
    
    settings_list = list(settings)
    if yolo:
        settings_list.append('yolo_mode_toggled=true')
    
    try:
        manager = TaskManager(address or config.core_address)
        
        if mode:
            manager.set_mode(mode)
            if config.verbose:
                click.echo(f"Mode set to: {mode}")
        
        task_id = manager.create_task(
            prompt=prompt_text,
            images=list(images),
            files=list(files),
            settings=settings_list
        )
        
        if config.verbose:
            click.echo(f"Task created successfully with ID: {task_id}")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@task_group.command(name='pause')
@click.option('--address', default='', help='Specific Cline instance address to use')
def task_pause(address):
    """Pause the current task."""
    from cline_cli.core.task_manager import TaskManager
    from cline_cli.utils.global_config import get_config
    
    config = get_config()
    
    try:
        manager = TaskManager(address or config.core_address)
        manager.cancel_task()
        click.echo("Task paused successfully")
        click.echo(f"Instance: {manager.get_current_instance()}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@task_group.command(name='send')
@click.argument('message', nargs=-1, type=str, required=False)
@click.option('-i', '--image', 'images', multiple=True, help='Attach image files')
@click.option('-f', '--file', 'files', multiple=True, help='Attach files')
@click.option('--address', default='', help='Specific Cline instance address to use')
@click.option('-m', '--mode', type=click.Choice(['act', 'plan']), help='Mode (act|plan)')
@click.option('-a', '--approve', is_flag=True, help='Approve pending request')
@click.option('-d', '--deny', is_flag=True, help='Deny pending request')
@click.option('-y', '--yolo', is_flag=True, help='Enable yolo mode (non-interactive)')
@click.option('--no-interactive', is_flag=True, help='Enable yolo mode (non-interactive)')
def task_send(message, images, files, address, mode, approve, deny, yolo, no_interactive):
    """Send a followup message to the current task and/or update mode/approve."""
    from cline_cli.core.task_manager import TaskManager
    from cline_cli.utils.global_config import get_config
    
    config = get_config()
    
    message_text = ' '.join(message) if message else ''
    
    if not sys.stdin.isatty():
        stdin_content = sys.stdin.read().strip()
        if stdin_content:
            if message_text:
                message_text += ' ' + stdin_content
            else:
                message_text = stdin_content
    
    if not message_text and not images and not files and not mode and not approve and not deny:
        click.echo("Error: content (message, files, images) required unless using --mode, --approve, or --deny flags", err=True)
        sys.exit(1)
    
    if approve and deny:
        click.echo("Error: cannot use both --approve and --deny flags", err=True)
        sys.exit(1)
    
    if (approve or deny) and mode:
        click.echo("Error: cannot use --approve/--deny and --mode together", err=True)
        sys.exit(1)
    
    yolo = yolo or no_interactive
    
    try:
        manager = TaskManager(address or config.core_address)
        
        manager.check_send_enabled()
        
        if yolo:
            manager.update_settings(['yolo_mode_toggled=true'])
        
        if mode:
            manager.set_mode_and_send_message(mode, message_text, list(images), list(files))
            click.echo(f"Mode set to {mode} and message sent successfully.")
        else:
            approve_str = None
            if approve:
                approve_str = 'true'
            elif deny:
                approve_str = 'false'
            
            manager.send_message(message_text, list(images), list(files), approve_str)
            click.echo("Message sent successfully.")
        
        click.echo(f"Instance: {manager.get_current_instance()}")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@task_group.command(name='chat')
@click.option('--address', default='', help='Specific Cline instance address to use')
def task_chat(address):
    """Chat with the current task in interactive mode."""
    from cline_cli.core.task_manager import TaskManager
    from cline_cli.utils.global_config import get_config
    
    config = get_config()
    
    try:
        manager = TaskManager(address or config.core_address)
        
        try:
            manager.check_send_enabled()
        except Exception as e:
            if "no active task" in str(e).lower():
                click.echo("No active task found. Use 'cline-py task new' to create a task first.")
                return
        
        manager.follow_conversation(interactive=True)
    
    except KeyboardInterrupt:
        click.echo("\nChat session ended")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@task_group.command(name='view')
@click.option('-f', '--follow', is_flag=True, help='Follow conversation forever')
@click.option('-c', '--follow-complete', is_flag=True, help='Follow until completion')
@click.option('--address', default='', help='Specific Cline instance address to use')
def task_view(follow, follow_complete, address):
    """View task conversation."""
    from cline_cli.core.task_manager import TaskManager
    from cline_cli.utils.global_config import get_config
    
    config = get_config()
    
    try:
        manager = TaskManager(address or config.core_address)
        click.echo(f"Using instance: {manager.get_current_instance()}")
        
        if follow:
            manager.follow_conversation(interactive=False)
        elif follow_complete:
            manager.follow_conversation_until_completion()
        else:
            manager.show_conversation()
    
    except KeyboardInterrupt:
        click.echo("\nView session ended")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@task_group.command(name='list')
def task_list():
    """List recent task history."""
    from cline_cli.core.task_manager import TaskManager
    
    try:
        TaskManager.list_tasks_from_disk()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@task_group.command(name='open')
@click.argument('task_id', type=str)
@click.option('--address', default='', help='Specific Cline instance address to use')
@click.option('-m', '--mode', type=click.Choice(['act', 'plan']), help='Mode (act|plan)')
@click.option('-s', '--setting', 'settings', multiple=True, 
              help='Task settings (key=value format)')
@click.option('-y', '--yolo', is_flag=True, help='Enable yolo mode (non-interactive)')
@click.option('--no-interactive', is_flag=True, help='Enable yolo mode (non-interactive)')
def task_open(task_id, address, mode, settings, yolo, no_interactive):
    """Open an existing task by ID and optionally update settings or mode."""
    from cline_cli.core.task_manager import TaskManager
    from cline_cli.utils.global_config import get_config
    
    config = get_config()
    
    yolo = yolo or no_interactive
    
    settings_list = list(settings)
    if yolo:
        settings_list.append('yolo_mode_toggled=true')
    
    try:
        manager = TaskManager(address or config.core_address)
        click.echo(f"Using instance: {manager.get_current_instance()}")
        
        manager.resume_task(task_id)
        
        if mode:
            manager.set_mode(mode)
            if config.verbose:
                click.echo(f"Mode set to: {mode}")
        
        if settings_list:
            manager.update_task_settings(task_id, settings_list)
            if config.verbose:
                click.echo("Task-specific settings applied successfully")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@task_group.command(name='restore')
@click.argument('checkpoint_id', type=str)
@click.option('-t', '--type', 'restore_type', 
              type=click.Choice(['task', 'workspace', 'taskAndWorkspace']),
              default='task',
              help='Restore type')
@click.option('--address', default='', help='Specific Cline instance address to use')
def task_restore(checkpoint_id, restore_type, address):
    """Restore task to a specific checkpoint."""
    from cline_cli.core.task_manager import TaskManager
    from cline_cli.utils.global_config import get_config
    
    config = get_config()
    
    try:
        checkpoint_id_int = int(checkpoint_id)
    except ValueError:
        click.echo(f"Error: invalid checkpoint ID '{checkpoint_id}': must be a valid number", err=True)
        sys.exit(1)
    
    try:
        manager = TaskManager(address or config.core_address)
        
        manager.validate_checkpoint_exists(checkpoint_id_int)
        
        click.echo(f"Using instance: {manager.get_current_instance()}")
        click.echo(f"Restoring to checkpoint {checkpoint_id_int} (type: {restore_type})")
        
        manager.restore_checkpoint(checkpoint_id_int, restore_type)
        click.echo("Checkpoint restored successfully")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def create_and_follow_task(prompt: str, images: List[str], files: List[str],
                          mode: str, settings: List[str], yolo: bool,
                          address: str, verbose: bool):
    """Create a new task and immediately follow it in interactive mode.
    
    This is used by the root command to provide a streamlined UX.
    """
    from cline_cli.core.task_manager import TaskManager
    
    if not mode:
        mode = 'plan'
    
    if yolo:
        settings.append('yolo_mode_toggled=true')
    
    manager = TaskManager(address)
    
    manager.set_mode(mode)
    if verbose:
        click.echo(f"Mode set to: {mode}")
    
    task_id = manager.create_task(
        prompt=prompt,
        images=images,
        files=files,
        settings=settings
    )
    
    if verbose:
        click.echo(f"Task created successfully with ID: {task_id}\n")
    
    if yolo:
        manager.follow_conversation_until_completion()
    else:
        manager.follow_conversation(interactive=True)
