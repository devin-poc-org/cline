"""Interactive input utilities."""

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style


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
    
    try:
        user_input = prompt(
            "Start a new Cline task\n"
            "What would you like Cline to help you with?\n"
            "> ",
            multiline=True,
            style=style
        )
        return user_input.strip()
    except KeyboardInterrupt:
        return ""
