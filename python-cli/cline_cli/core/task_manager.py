"""Task management functionality."""

import os
import json
from typing import List, Optional
from cline_cli.core.grpc_client import GrpcClient
from cline_cli.utils.display import Display


class TaskManager:
    """Manages Cline tasks."""
    
    def __init__(self, address: str):
        """Initialize task manager.
        
        Args:
            address: Cline Core gRPC address
        """
        self.address = address
        self.client = GrpcClient(address)
    
    def get_current_instance(self) -> str:
        """Get the current instance address."""
        return self.address
    
    def create_task(self, prompt: str, images: List[str], 
                   files: List[str], settings: List[str]) -> str:
        """Create a new task.
        
        Args:
            prompt: Task prompt
            images: List of image file paths
            files: List of file paths
            settings: List of settings in key=value format
        
        Returns:
            Task ID
        """
        parsed_settings = self._parse_settings(settings)
        
        task_id = self.client.create_task(prompt, images, files, parsed_settings)
        return task_id
    
    def cancel_task(self):
        """Cancel the current task."""
        self.client.cancel_task()
    
    def send_message(self, message: str, images: List[str], 
                    files: List[str], approve: Optional[str] = None):
        """Send a message to the current task.
        
        Args:
            message: Message text
            images: List of image file paths
            files: List of file paths
            approve: Approval status ('true', 'false', or None)
        """
        self.client.send_message(message, images, files, approve)
    
    def set_mode(self, mode: str):
        """Set the task mode.
        
        Args:
            mode: Mode ('act' or 'plan')
        """
        self.client.set_mode(mode)
    
    def set_mode_and_send_message(self, mode: str, message: str, 
                                  images: List[str], files: List[str]):
        """Set mode and send message.
        
        Args:
            mode: Mode ('act' or 'plan')
            message: Message text
            images: List of image file paths
            files: List of file paths
        """
        self.set_mode(mode)
        if message or images or files:
            self.send_message(message, images, files)
    
    def check_send_enabled(self):
        """Check if sending messages is enabled."""
        self.client.check_send_enabled()
    
    def update_settings(self, settings: List[str]):
        """Update task settings.
        
        Args:
            settings: List of settings in key=value format
        """
        parsed_settings = self._parse_settings(settings)
        self.client.update_settings(parsed_settings)
    
    def update_task_settings(self, task_id: str, settings: List[str]):
        """Update task-specific settings.
        
        Args:
            task_id: Task ID
            settings: List of settings in key=value format
        """
        parsed_settings = self._parse_settings(settings)
        self.client.update_task_settings(task_id, parsed_settings)
    
    def resume_task(self, task_id: str):
        """Resume a task by ID.
        
        Args:
            task_id: Task ID
        """
        self.client.resume_task(task_id)
    
    def validate_checkpoint_exists(self, checkpoint_id: int):
        """Validate that a checkpoint exists.
        
        Args:
            checkpoint_id: Checkpoint ID
        """
        self.client.validate_checkpoint_exists(checkpoint_id)
    
    def restore_checkpoint(self, checkpoint_id: int, restore_type: str):
        """Restore a checkpoint.
        
        Args:
            checkpoint_id: Checkpoint ID
            restore_type: Restore type ('task', 'workspace', 'taskAndWorkspace')
        """
        self.client.restore_checkpoint(checkpoint_id, restore_type)
    
    def follow_conversation(self, interactive: bool = False):
        """Follow the conversation in real-time.
        
        Args:
            interactive: Whether to enable interactive input
        """
        display = Display()
        
        if interactive:
            display.follow_conversation_interactive(self.client)
        else:
            display.follow_conversation(self.client)
    
    def follow_conversation_until_completion(self):
        """Follow conversation until task completion."""
        display = Display()
        display.follow_until_completion(self.client)
    
    def show_conversation(self):
        """Show a snapshot of the conversation."""
        display = Display()
        display.show_conversation_snapshot(self.client)
    
    @staticmethod
    def list_tasks_from_disk():
        """List tasks from disk."""
        config_path = os.path.expanduser('~/.cline')
        history_path = os.path.join(config_path, 'task_history.json')
        
        if not os.path.exists(history_path):
            print("No task history found.")
            return
        
        with open(history_path, 'r') as f:
            history = json.load(f)
        
        if not history:
            print("No tasks in history.")
            return
        
        display = Display()
        display.show_task_list(history)
    
    def _parse_settings(self, settings: List[str]) -> dict:
        """Parse settings from key=value format.
        
        Args:
            settings: List of settings in key=value format
        
        Returns:
            Dictionary of parsed settings
        """
        parsed = {}
        for setting in settings:
            if '=' not in setting:
                raise ValueError(f"Invalid setting format: {setting}. Expected key=value")
            
            key, value = setting.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                pass
            
            if '.' in key:
                parts = key.split('.')
                current = parsed
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = value
            else:
                parsed[key] = value
        
        return parsed
