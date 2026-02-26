"""Interactive UI components using prompt_toolkit for rich CLI interactions."""

import os
import sys

# Check if we're in a interactive terminal
IS_TTY = sys.stdin.isatty()


def select_option_interactive(
    question: str,
    options: list[str],
    explanations: dict[str, str],
    default_index: int = 0,
) -> str:
    """
    Interactive selection using arrow keys, numbers, or Enter.

    Args:
        question: The question to display
        options: List of available options
        explanations: Dict mapping option -> explanation
        default_index: Index of default selection

    Returns:
        The selected option
    """
    if not IS_TTY:
        # Fallback to simple input when not interactive
        return options[default_index]

    try:
        from prompt_toolkit import Application
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.layout.containers import VSplit
        from prompt_toolkit.layout.layout import Layout
        from prompt_toolkit.widgets import Label, RadioList

        # Use RadioList for interactive selection
        radio = RadioList(
            values=[(opt, f"{opt}") for opt in options],
            default=default_index,
        )

        # Create a simple label for the question
        label = Label(text=question, dont_extend_height=False)

        # Build the application
        container = VSplit([label, radio])

        app = Application(
            layout=Layout(container),
            key_bindings=KeyBindings(),
            mouse_support=True,
        )

        # Run the application
        app.run()
        return options[default_index]  # Fallback

    except Exception:
        # If prompt_toolkit fails, fall back to simple selector
        return _simple_select(question, options, explanations, default_index)


def _simple_select(
    question: str,
    options: list[str],
    explanations: dict[str, str],
    default_index: int = 0,
) -> str:
    """
    Simple terminal-based selection with number keys.
    """
    selected = default_index

    while True:
        # Clear screen (works on most terminals)
        print("\033[2J\033[H", end="")

        print(f"\n{question}\n")
        print("=" * len(question))
        print("\nUse number keys to select, Enter to confirm:\n")

        for i, opt in enumerate(options):
            marker = "→" if i == selected else " "
            num = f"{i + 1}."
            exp = explanations.get(opt, "")
            default_tag = " (default)" if i == default_index else ""
            current = "◉" if i == selected else "○"
            print(f"  {marker} {current} [{num}] {opt}{default_tag}")
            if exp and i == selected:
                print(f"       → {exp}")
            print()

        print("\nControls: ↑/↓ = navigate, Enter = select, q = quit")

        try:
            if os.name == "nt":
                import msvcrt

                key = msvcrt.getch()
                if key == b"\r":  # Enter
                    return options[selected]
                elif key == b"q":
                    return options[default_index]
                elif key == b"\xe0":  # Arrow key prefix on Windows
                    key2 = msvcrt.getch()
                    if key2 == b"H":  # Up
                        selected = max(0, selected - 1)
                    elif key2 == b"P":  # Down
                        selected = min(len(options) - 1, selected + 1)
                elif key in [b"1", b"2", b"3", b"4", b"5", b"6", b"7", b"8", b"9"]:
                    idx = int(key) - 1
                    if idx < len(options):
                        return options[idx]
            else:
                # Unix-like systems
                import termios
                import tty

                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    key = sys.stdin.read(1)
                    if key == "\r":  # Enter
                        return options[selected]
                    elif key == "q":
                        return options[default_index]
                    elif key == "\x1b":  # Escape sequence
                        next1 = sys.stdin.read(1)
                        if next1 == "[":
                            next2 = sys.stdin.read(1)
                            if next2 == "A":  # Up
                                selected = max(0, selected - 1)
                            elif next2 == "B":  # Down
                                selected = min(len(options) - 1, selected + 1)
                    elif key in "123456789":
                        idx = int(key) - 1
                        if idx < len(options):
                            return options[idx]
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            # Fallback to input() if terminal handling fails
            print("\nEnter number or press Enter for default:")
            choice = input(f" [{default_index + 1}]: ").strip()
            if not choice:
                return options[default_index]
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    return options[idx]
            except ValueError:
                pass
            return options[default_index]


def confirm_interactive(prompt: str, default: bool = True) -> bool:
    """
    Interactive yes/no confirmation.

    Args:
        prompt: The prompt to display
        default: Default value if user just presses Enter

    Returns:
        True if confirmed, False otherwise
    """
    suffix = " [Y/n]" if default else " [y/N]"
    while True:
        response = input(f"{prompt}{suffix}: ").strip().lower()
        if not response:
            return default
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        print("Please enter y or n")


def prompt_with_default(prompt: str, default: str) -> str:
    """
    Prompt with a default value.

    Args:
        prompt: The prompt to display
        default: Default value if user just presses Enter

    Returns:
        User's input or the default
    """
    suffix = f" [{default}]" if default else ""
    response = input(f"{prompt}{suffix}: ").strip()
    return response if response else default


def display_explanation(title: str, content: str) -> None:
    """
    Display an explanation to the user.

    Args:
        title: Title of the explanation
        content: Content of the explanation
    """
    separator = "=" * 60
    print(f"\n{separator}")
    print(f"  {title}")
    print(separator)
    print(f"\n{content}\n")
    if IS_TTY:
        input("Press Enter to continue...")
    else:
        print("(Press Enter to continue...)")
