"""Display and output formatting utilities."""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax


class Display:
    """Handles display and output formatting."""
    
    def __init__(self):
        """Initialize display."""
        self.console = Console()
    
    def bold(self, text: str) -> str:
        """Format text as bold."""
        return f"[bold]{text}[/bold]"
    
    def dim(self, text: str) -> str:
        """Format text as dim."""
        return f"[dim]{text}[/dim]"
    
    def success(self, text: str) -> str:
        """Format text as success (green)."""
        return f"[green]{text}[/green]"
    
    def error(self, text: str) -> str:
        """Format text as error (red)."""
        return f"[red]{text}[/red]"
    
    def warning(self, text: str) -> str:
        """Format text as warning (yellow)."""
        return f"[yellow]{text}[/yellow]"
    
    def show_task_list(self, tasks: List[Dict[str, Any]]):
        """Display task list.
        
        Args:
            tasks: List of task dictionaries
        """
        table = Table(title="Task History")
        
        table.add_column("Task ID", style="cyan")
        table.add_column("Created", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Prompt", style="white")
        
        for task in tasks:
            table.add_row(
                task.get('id', 'unknown'),
                task.get('created', 'unknown'),
                task.get('status', 'unknown'),
                task.get('prompt', '')[:50] + '...' if len(task.get('prompt', '')) > 50 else task.get('prompt', '')
            )
        
        self.console.print(table)
    
    def show_instance_list(self, instances: List[Dict[str, Any]], default_instance: Optional[str]):
        """Display instance list.
        
        Args:
            instances: List of instance dictionaries
            default_instance: Default instance address
        """
        table = Table(title="Cline Instances")
        
        table.add_column("ADDRESS", style="cyan")
        table.add_column("STATUS", style="green")
        table.add_column("VERSION", style="magenta")
        table.add_column("PLATFORM", style="blue")
        table.add_column("DEFAULT", style="yellow")
        
        for instance in instances:
            is_default = "✓" if instance['address'] == default_instance else ""
            
            table.add_row(
                instance.get('address', 'unknown'),
                instance.get('status', 'unknown'),
                instance.get('version', 'unknown'),
                instance.get('platform', 'unknown'),
                is_default
            )
        
        self.console.print(table)
    
    def show_settings(self, settings: Dict[str, Any]):
        """Display configuration settings.
        
        Args:
            settings: Settings dictionary
        """
        self.console.print("\n[bold]Configuration Settings:[/bold]\n")
        self.console.print_json(json.dumps(settings, indent=2))
    
    def show_setting_value(self, key: str, value: Any):
        """Display a specific setting value.
        
        Args:
            key: Setting key
            value: Setting value
        """
        self.console.print(f"\n[bold]{key}:[/bold]")
        
        if isinstance(value, (dict, list)):
            self.console.print_json(json.dumps(value, indent=2))
        else:
            self.console.print(f"  {value}")
    
    def show_auth_config(self, config: Dict[str, Any]):
        """Display authentication configuration.
        
        Args:
            config: Auth config dictionary
        """
        table = Table(title="Authentication Configuration")
        
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="white")
        
        for key, value in config.items():
            table.add_row(key, str(value))
        
        self.console.print(table)
    
    def show_log_files(self, log_files: List[Dict[str, Any]], mark_for_deletion: bool = False):
        """Display log files.
        
        Args:
            log_files: List of log file dictionaries
            mark_for_deletion: Whether to mark files for deletion
        """
        table = Table(title="Log Files")
        
        table.add_column("FILENAME", style="cyan")
        table.add_column("SIZE", style="magenta")
        table.add_column("CREATED", style="blue")
        table.add_column("AGE", style="yellow")
        
        for log_file in log_files:
            created_str = log_file['created'].strftime("%Y-%m-%d %H:%M:%S")
            age = self._format_age(log_file['created'])
            size = self._format_size(log_file['size'])
            
            style = "red" if mark_for_deletion else None
            
            table.add_row(
                log_file['name'],
                size,
                created_str,
                age,
                style=style
            )
        
        self.console.print(table)
    
    def follow_conversation(self, client):
        """Follow conversation in non-interactive mode.
        
        Args:
            client: gRPC client
        """
        self.console.print("\n[bold]Following conversation...[/bold]")
        self.console.print("[dim]Press Ctrl+C to stop[/dim]\n")
        
        try:
            for message in client.stream_conversation():
                self._display_message(message)
        except KeyboardInterrupt:
            pass
    
    def follow_conversation_interactive(self, client):
        """Follow conversation in interactive mode.
        
        Args:
            client: gRPC client
        """
        from prompt_toolkit import prompt
        
        self.console.print("\n[bold]Interactive chat mode[/bold]")
        self.console.print("[dim]Type your messages and press Enter. Press Ctrl+C to exit.[/dim]\n")
        
        try:
            while True:
                for message in client.stream_conversation():
                    self._display_message(message)
                    
                    if message.get('waiting_for_input'):
                        break
                
                user_input = prompt("\n> ")
                if user_input.strip():
                    client.send_message(user_input, [], [], None)
        
        except KeyboardInterrupt:
            pass
    
    def follow_until_completion(self, client):
        """Follow conversation until task completion.
        
        Args:
            client: gRPC client
        """
        self.console.print("\n[bold]Following until completion...[/bold]\n")
        
        try:
            for message in client.stream_conversation():
                self._display_message(message)
                
                if message.get('type') == 'completion':
                    break
        except KeyboardInterrupt:
            pass
    
    def show_conversation_snapshot(self, client):
        """Show a snapshot of the conversation.
        
        Args:
            client: gRPC client
        """
        self.console.print("\n[bold]Conversation Snapshot:[/bold]\n")
        
        self.console.print("[dim]Conversation snapshot not yet implemented[/dim]")
    
    def _display_message(self, message: Dict[str, Any]):
        """Display a conversation message.
        
        Args:
            message: Message dictionary
        """
        msg_type = message.get('type', 'unknown')
        
        if msg_type == 'say':
            text = message.get('text', '')
            self.console.print(f"[bold cyan]Cline:[/bold cyan] {text}")
        
        elif msg_type == 'ask':
            text = message.get('text', '')
            self.console.print(f"[bold yellow]Cline (asking):[/bold yellow] {text}")
        
        elif msg_type == 'tool':
            tool_name = message.get('tool_name', 'unknown')
            self.console.print(f"[bold magenta]Tool:[/bold magenta] {tool_name}")
        
        elif msg_type == 'completion':
            self.console.print("[bold green]✓ Task completed[/bold green]")
    
    def _format_age(self, created: datetime) -> str:
        """Format age of a file.
        
        Args:
            created: Creation datetime
        
        Returns:
            Formatted age string
        """
        delta = datetime.now() - created
        
        if delta.days > 0:
            return f"{delta.days}d ago"
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            return f"{hours}h ago"
        elif delta.seconds >= 60:
            minutes = delta.seconds // 60
            return f"{minutes}m ago"
        else:
            return "just now"
    
    def _format_size(self, size: int) -> str:
        """Format file size.
        
        Args:
            size: Size in bytes
        
        Returns:
            Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
