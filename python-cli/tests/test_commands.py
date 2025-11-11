"""Tests for CLI commands."""

import pytest
from click.testing import CliRunner
from cline_cli.main import cli
from cline_cli.commands.version import version_command
from cline_cli.commands.task import task_group
from cline_cli.commands.instance import instance_group
from cline_cli.commands.config import config_group
from cline_cli.commands.auth import auth_command
from cline_cli.commands.logs import logs_group
from cline_cli.commands.doctor import doctor_command


class TestRootCommand:
    """Tests for root command."""
    
    def test_help(self):
        """Test --help flag."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Cline CLI - AI-powered coding assistant' in result.output
    
    def test_version_command(self):
        """Test version command directly."""
        runner = CliRunner()
        result = runner.invoke(version_command, [])
        assert result.exit_code == 0
        assert 'Cline CLI' in result.output


class TestTaskCommands:
    """Tests for task commands."""
    
    def test_task_help(self):
        """Test task --help."""
        runner = CliRunner()
        result = runner.invoke(task_group, ['--help'])
        assert result.exit_code == 0
        assert 'Manage Cline tasks' in result.output
    
    def test_task_new_help(self):
        """Test task new --help."""
        runner = CliRunner()
        result = runner.invoke(task_group, ['new', '--help'])
        assert result.exit_code == 0
        assert 'Create a new task' in result.output
    
    def test_task_pause_help(self):
        """Test task pause --help."""
        runner = CliRunner()
        result = runner.invoke(task_group, ['pause', '--help'])
        assert result.exit_code == 0
        assert 'Pause the current task' in result.output
    
    def test_task_send_help(self):
        """Test task send --help."""
        runner = CliRunner()
        result = runner.invoke(task_group, ['send', '--help'])
        assert result.exit_code == 0
        assert 'Send a followup message' in result.output
    
    def test_task_chat_help(self):
        """Test task chat --help."""
        runner = CliRunner()
        result = runner.invoke(task_group, ['chat', '--help'])
        assert result.exit_code == 0
        assert 'Chat with the current task' in result.output
    
    def test_task_view_help(self):
        """Test task view --help."""
        runner = CliRunner()
        result = runner.invoke(task_group, ['view', '--help'])
        assert result.exit_code == 0
        assert 'View task conversation' in result.output
    
    def test_task_list_help(self):
        """Test task list --help."""
        runner = CliRunner()
        result = runner.invoke(task_group, ['list', '--help'])
        assert result.exit_code == 0
        assert 'List recent task history' in result.output
    
    def test_task_open_help(self):
        """Test task open --help."""
        runner = CliRunner()
        result = runner.invoke(task_group, ['open', '--help'])
        assert result.exit_code == 0
        assert 'Open an existing task' in result.output
    
    def test_task_restore_help(self):
        """Test task restore --help."""
        runner = CliRunner()
        result = runner.invoke(task_group, ['restore', '--help'])
        assert result.exit_code == 0
        assert 'Restore task to a specific checkpoint' in result.output


class TestInstanceCommands:
    """Tests for instance commands."""
    
    def test_instance_help(self):
        """Test instance --help."""
        runner = CliRunner()
        result = runner.invoke(instance_group, ['--help'])
        assert result.exit_code == 0
        assert 'Manage Cline instances' in result.output
    
    def test_instance_list_help(self):
        """Test instance list --help."""
        runner = CliRunner()
        result = runner.invoke(instance_group, ['list', '--help'])
        assert result.exit_code == 0
        assert 'List all registered' in result.output
    
    def test_instance_default_help(self):
        """Test instance default --help."""
        runner = CliRunner()
        result = runner.invoke(instance_group, ['default', '--help'])
        assert result.exit_code == 0
        assert 'Set the default' in result.output
    
    def test_instance_new_help(self):
        """Test instance new --help."""
        runner = CliRunner()
        result = runner.invoke(instance_group, ['new', '--help'])
        assert result.exit_code == 0
        assert 'Create a new' in result.output
    
    def test_instance_kill_help(self):
        """Test instance kill --help."""
        runner = CliRunner()
        result = runner.invoke(instance_group, ['kill', '--help'])
        assert result.exit_code == 0
        assert 'Kill a Cline instance' in result.output


class TestConfigCommands:
    """Tests for config commands."""
    
    def test_config_help(self):
        """Test config --help."""
        runner = CliRunner()
        result = runner.invoke(config_group, ['--help'])
        assert result.exit_code == 0
        assert 'Manage Cline configuration' in result.output
    
    def test_config_list_help(self):
        """Test config list --help."""
        runner = CliRunner()
        result = runner.invoke(config_group, ['list', '--help'])
        assert result.exit_code == 0
        assert 'List all configuration' in result.output
    
    def test_config_get_help(self):
        """Test config get --help."""
        runner = CliRunner()
        result = runner.invoke(config_group, ['get', '--help'])
        assert result.exit_code == 0
        assert 'Get a specific' in result.output
    
    def test_config_set_help(self):
        """Test config set --help."""
        runner = CliRunner()
        result = runner.invoke(config_group, ['set', '--help'])
        assert result.exit_code == 0
        assert 'Set configuration' in result.output


class TestAuthCommand:
    """Tests for auth command."""
    
    def test_auth_help(self):
        """Test auth --help."""
        runner = CliRunner()
        result = runner.invoke(auth_command, ['--help'])
        assert result.exit_code == 0
        assert 'Authenticate a provider' in result.output


class TestVersionCommand:
    """Tests for version command."""
    
    def test_version(self):
        """Test version command."""
        runner = CliRunner()
        result = runner.invoke(version_command, [])
        assert result.exit_code == 0
        assert 'Cline CLI' in result.output
    
    def test_version_short(self):
        """Test version --short."""
        runner = CliRunner()
        result = runner.invoke(version_command, ['--short'])
        assert result.exit_code == 0
        assert 'Cline CLI' not in result.output


class TestLogsCommands:
    """Tests for logs commands."""
    
    def test_logs_help(self):
        """Test logs --help."""
        runner = CliRunner()
        result = runner.invoke(logs_group, ['--help'])
        assert result.exit_code == 0
        assert 'Manage Cline log files' in result.output
    
    def test_logs_list_help(self):
        """Test logs list --help."""
        runner = CliRunner()
        result = runner.invoke(logs_group, ['list', '--help'])
        assert result.exit_code == 0
        assert 'List all log files' in result.output
    
    def test_logs_clean_help(self):
        """Test logs clean --help."""
        runner = CliRunner()
        result = runner.invoke(logs_group, ['clean', '--help'])
        assert result.exit_code == 0
        assert 'Delete old log files' in result.output
    
    def test_logs_path_help(self):
        """Test logs path --help."""
        runner = CliRunner()
        result = runner.invoke(logs_group, ['path', '--help'])
        assert result.exit_code == 0
        assert 'Print the logs directory' in result.output


class TestDoctorCommand:
    """Tests for doctor command."""
    
    def test_doctor_help(self):
        """Test doctor --help."""
        runner = CliRunner()
        result = runner.invoke(doctor_command, ['--help'])
        assert result.exit_code == 0
        assert 'Check system health' in result.output


class TestGlobalFlags:
    """Tests for global flags."""
    
    def test_verbose_flag(self):
        """Test -v/--verbose flag."""
        runner = CliRunner()
        result = runner.invoke(cli, ['-v', '--help'])
        assert result.exit_code == 0
    
    def test_output_format_rich(self):
        """Test -F rich."""
        runner = CliRunner()
        result = runner.invoke(cli, ['-F', 'rich', '--help'])
        assert result.exit_code == 0
    
    def test_output_format_json(self):
        """Test -F json."""
        runner = CliRunner()
        result = runner.invoke(cli, ['-F', 'json', '--help'])
        assert result.exit_code == 0
    
    def test_output_format_plain(self):
        """Test -F plain."""
        runner = CliRunner()
        result = runner.invoke(cli, ['-F', 'plain', '--help'])
        assert result.exit_code == 0
    
    def test_address_flag(self):
        """Test --address flag."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--address', 'localhost:51052', '--help'])
        assert result.exit_code == 0
