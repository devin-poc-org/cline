"""Authentication commands."""

import sys
import click


@click.command(name='auth')
@click.option('-p', '--provider', default='', 
              help='Provider ID for quick setup (e.g., openai-native, anthropic)')
@click.option('-k', '--apikey', default='', 
              help='API key for the provider')
@click.option('-m', '--modelid', default='', 
              help='Model ID to configure (e.g., gpt-4o, claude-sonnet-4-5-20250929)')
@click.option('-b', '--baseurl', default='', 
              help='Base URL (optional, only for openai provider)')
def auth_command(provider, apikey, modelid, baseurl):
    """Authenticate a provider and configure what model is used.
    
    Interactive Mode:
      Run without flags to open an interactive menu where you can:
      - Sign in to your Cline account
      - Configure other LLM providers (Anthropic, OpenAI, etc.)
      - Select and switch between AI models
      - Manage provider settings
    
    Quick Setup Mode:
      Use flags to quickly configure a BYO provider non-interactively:
      
      Examples:
        cline-py auth --provider openai-native --apikey sk-xxx --modelid gpt-5
        cline-py auth -p anthropic -k sk-ant-xxx -m claude-sonnet-4-5-20250929
        cline-py auth -p openai-compatible -k xxx -m gpt-4 -b https://api.example.com/v1
        
      Supported providers: openai-native, openai, anthropic, gemini, openrouter, xai, cerebras, ollama
      Note: Bedrock provider requires interactive setup due to complex auth fields
    """
    from cline_cli.core.auth_manager import AuthManager
    
    try:
        manager = AuthManager()
        
        if provider or apikey or modelid or baseurl:
            if not provider or not apikey or not modelid:
                click.echo("Error: Quick setup requires --provider, --apikey, and --modelid flags", err=True)
                sys.exit(1)
            
            manager.quick_setup(provider, apikey, modelid, baseurl)
        else:
            manager.run_auth_flow()
    
    except KeyboardInterrupt:
        click.echo("\nAuth setup cancelled")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
