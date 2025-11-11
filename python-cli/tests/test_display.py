"""Tests for Display utilities."""

import pytest
from datetime import datetime, timedelta
from cline_cli.utils.display import Display


class TestDisplay:
    """Tests for Display class."""
    
    def test_format_age_just_now(self):
        """Test formatting age for recent files."""
        display = Display()
        created = datetime.now()
        age = display._format_age(created)
        
        assert age == 'just now'
    
    def test_format_age_minutes(self):
        """Test formatting age in minutes."""
        display = Display()
        created = datetime.now() - timedelta(minutes=5)
        age = display._format_age(created)
        
        assert 'm ago' in age
    
    def test_format_age_hours(self):
        """Test formatting age in hours."""
        display = Display()
        created = datetime.now() - timedelta(hours=2)
        age = display._format_age(created)
        
        assert 'h ago' in age
    
    def test_format_age_days(self):
        """Test formatting age in days."""
        display = Display()
        created = datetime.now() - timedelta(days=3)
        age = display._format_age(created)
        
        assert 'd ago' in age
    
    def test_format_size_bytes(self):
        """Test formatting size in bytes."""
        display = Display()
        size = display._format_size(500)
        
        assert 'B' in size
    
    def test_format_size_kb(self):
        """Test formatting size in KB."""
        display = Display()
        size = display._format_size(2048)
        
        assert 'KB' in size
    
    def test_format_size_mb(self):
        """Test formatting size in MB."""
        display = Display()
        size = display._format_size(2 * 1024 * 1024)
        
        assert 'MB' in size
    
    def test_format_size_gb(self):
        """Test formatting size in GB."""
        display = Display()
        size = display._format_size(2 * 1024 * 1024 * 1024)
        
        assert 'GB' in size
    
    def test_bold(self):
        """Test bold formatting."""
        display = Display()
        text = display.bold('test')
        
        assert '[bold]' in text
        assert '[/bold]' in text
    
    def test_dim(self):
        """Test dim formatting."""
        display = Display()
        text = display.dim('test')
        
        assert '[dim]' in text
        assert '[/dim]' in text
    
    def test_success(self):
        """Test success formatting."""
        display = Display()
        text = display.success('test')
        
        assert '[green]' in text
        assert '[/green]' in text
    
    def test_error(self):
        """Test error formatting."""
        display = Display()
        text = display.error('test')
        
        assert '[red]' in text
        assert '[/red]' in text
    
    def test_warning(self):
        """Test warning formatting."""
        display = Display()
        text = display.warning('test')
        
        assert '[yellow]' in text
        assert '[/yellow]' in text
