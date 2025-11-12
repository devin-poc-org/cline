"""Interactive input utilities."""

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings


def prompt_for_initial_task(address: str, mode: str) -> str:
    """Prompt user for initial task input.
    
    Args:
        address: Instance address
        mode: Current mode (act or plan)
    
    Returns:
        User's prompt text
    """
    print("\n" + "="*60)
    print("Cline CLI - AI-powered coding assistant")
    print(f"Mode: {mode}")
    print(f"Instance: {address}")
    print("="*60 + "\n")
    
    style = Style.from_dict({
        'prompt': '#ffcc00 bold',
    })
    
    kb = KeyBindings()
    
    @kb.add('enter')
    def _(event):
        """Accept input on Enter."""
        event.current_buffer.validate_and_handle()
    
    @kb.add('escape', 'enter')
    def _(event):
        """Insert newline on Esc+Enter."""
        event.current_buffer.insert_text('\n')
    
    try:
        print("Start a new Cline task")
        print("What would you like Cline to help you with?")
        print("(Press Enter to submit, Esc+Enter for new line, Ctrl+C to cancel)\n")
        
        user_input = prompt(
            "> ",
            multiline=True,
            style=style,
            key_bindings=kb
        )
        return user_input.strip()
    except (KeyboardInterrupt, EOFError):
        return ""
