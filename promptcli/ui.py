"""Interactive UI components for CLI with number-based selection."""

import os
import sys

# Check if we're in a interactive terminal
IS_TTY = sys.stdin.isatty()


def select_option_with_explain(
    question: str,
    options: list[str],
    explanations: dict[str, str],
    question_explanation: str,
    default_index: int = 0,
) -> str:
    """
    Interactive selection with number keys and explain option.

    Args:
        question: The question to display
        options: List of available options (including "Explain" as last option)
        explanations: Dict mapping option -> explanation
        question_explanation: Explanation of what the question is asking
        default_index: Index of default selection

    Returns:
        The selected option
    """
    # Add "Explain" as the last option
    all_options = options + ["Explain"]
    selected = default_index

    while True:
        # Clear screen
        print("\033[2J\033[H", end="")

        print(f"\n{question}\n")
        print("=" * len(question))
        print(f"\n{question_explanation}\n")
        print("Enter a number to select:\n")

        for i, opt in enumerate(all_options):
            num = f"{i + 1}."
            if i == default_index:
                marker = "→"
                default_tag = " (default)"
            else:
                marker = " "
                default_tag = ""

            # Show explanation for selected option OR for Explain
            if i == selected:
                if opt == "Explain":
                    exp = "Learn more about this question"
                else:
                    exp = explanations.get(opt, "")
                if exp:
                    print(f"  {marker} [{num}] {opt}{default_tag}")
                    print(f"       └─ {exp}")
                else:
                    print(f"  {marker} [{num}] {opt}{default_tag}")
            else:
                print(f"  {marker} [{num}] {opt}{default_tag}")

        print("\nPress number to select, Enter to confirm default")

        try:
            if os.name == "nt":
                import msvcrt

                key = msvcrt.getch()
                if key == b"\r":  # Enter - confirm current selection
                    if selected == len(all_options) - 1:
                        # Explain selected, show full explanation
                        print("\033[2J\033[H", end="")
                        print(f"\n{question}\n")
                        print("=" * len(question))
                        print(f"\n{question_explanation}\n")
                        print("Available options:\n")
                        for opt in options:
                            exp = explanations.get(opt, "")
                            print(f"  • {opt}")
                            if exp:
                                print(f"    {exp}")
                            print()
                        print("\nPress any key to return...")
                        msvcrt.getch()
                    else:
                        return options[selected]
                elif key == b"\xe0":  # Arrow key prefix on Windows
                    key2 = msvcrt.getch()
                    if key2 == b"H":  # Up
                        selected = max(0, selected - 1)
                    elif key2 == b"P":  # Down
                        selected = min(len(all_options) - 1, selected + 1)
                else:
                    # Number keys
                    try:
                        num = int(key.decode()) - 1
                        if 0 <= num < len(all_options):
                            selected = num
                    except (ValueError, UnicodeDecodeError):
                        pass
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
                        if selected == len(all_options) - 1:
                            # Explain
                            print("\033[2J\033[H", end="")
                            print(f"\n{question}\n")
                            print("=" * len(question))
                            print(f"\n{question_explanation}\n")
                            print("Available options:\n")
                            for opt in options:
                                exp = explanations.get(opt, "")
                                print(f"  • {opt}")
                                if exp:
                                    print(f"    {exp}")
                                print()
                            print("\nPress any key to return...")
                            sys.stdin.read(1)
                        else:
                            return options[selected]
                    elif key == "\x1b":  # Escape
                        next1 = sys.stdin.read(1)
                        if next1 == "[":
                            next2 = sys.stdin.read(1)
                            if next2 == "A":  # Up
                                selected = max(0, selected - 1)
                            elif next2 == "B":  # Down
                                selected = min(len(all_options) - 1, selected + 1)
                    else:
                        # Number keys
                        try:
                            num = int(key) - 1
                            if 0 <= num < len(all_options):
                                selected = num
                        except ValueError:
                            pass
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            # Fallback
            print("\nEnter number:")
            choice = input(f" [{default_index + 1}]: ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(all_options):
                    if idx == len(all_options) - 1:
                        # Explain
                        print(f"\n{question_explanation}\n")
                        input("Press Enter to continue...")
                    else:
                        return options[idx]
            except ValueError:
                pass
            return options[default_index]


def confirm_interactive(prompt: str, default: bool = True) -> bool:
    """Yes/no confirmation."""
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
    """Prompt with default."""
    suffix = f" [{default}]" if default else ""
    response = input(f"{prompt}{suffix}: ").strip()
    return response if response else default
