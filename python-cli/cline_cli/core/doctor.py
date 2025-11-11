"""System health check functionality."""

import os
import sys
import platform
from cline_cli.utils.display import Display


class Doctor:
    """Performs system health checks."""
    
    def __init__(self):
        """Initialize doctor."""
        self.display = Display()
    
    def run_checks(self):
        """Run all health checks."""
        print("\n" + self.display.bold("Cline Doctor - System Health Check") + "\n")
        
        print(self.display.dim("━━━ Terminal Configuration ━━━") + "\n")
        self._check_terminal()
        
        print("\n" + self.display.dim("━━━ Python Environment ━━━") + "\n")
        self._check_python()
        
        print("\n" + self.display.dim("━━━ CLI Updates ━━━") + "\n")
        self._check_updates()
        
        print("\n" + self.display.dim("━" * 60))
        print("\n" + self.display.success("✓ Health check complete") + "\n")
    
    def _check_terminal(self):
        """Check terminal configuration."""
        term = os.environ.get('TERM_PROGRAM', 'unknown')
        
        print(f"Terminal: {term}")
        
        if term in ['vscode', 'cursor']:
            print("✓ VS Code/Cursor terminal detected")
            print("  Shift+Enter should work for multiline input")
        elif term in ['iTerm.app', 'iTerm2']:
            print("✓ iTerm2 detected")
            print("  Shift+Enter works by default")
        elif term == 'Apple_Terminal':
            print("⚠ Terminal.app detected")
            print("  Manual setup required for Shift+Enter")
        else:
            print(f"ℹ Terminal: {term}")
            print("  Multiline input may require manual configuration")
    
    def _check_python(self):
        """Check Python environment."""
        python_version = platform.python_version()
        print(f"Python version: {python_version}")
        
        major, minor, _ = python_version.split('.')
        if int(major) >= 3 and int(minor) >= 8:
            print("✓ Python version is compatible")
        else:
            print("✗ Python 3.8 or higher is required")
        
        try:
            import pip
            print("✓ pip is available")
        except ImportError:
            print("✗ pip is not available")
        
        required_packages = ['click', 'grpcio', 'prompt_toolkit', 'rich']
        for package in required_packages:
            try:
                __import__(package)
                print(f"✓ {package} is installed")
            except ImportError:
                print(f"✗ {package} is not installed")
    
    def _check_updates(self):
        """Check for CLI updates."""
        if os.environ.get('NO_AUTO_UPDATE'):
            print("⊘ Auto-update disabled (NO_AUTO_UPDATE set)")
            return
        
        if os.environ.get('CI'):
            print("⊘ Skipping update check (CI environment)")
            return
        
        print("Checking for updates...")
        
        
        from cline_cli import __version__
        print(f"Current version: {__version__}")
        print("ℹ Update check not yet implemented")
        print("  Run 'pip install --upgrade cline-cli-python' to update manually")
