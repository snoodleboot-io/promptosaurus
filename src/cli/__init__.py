"""CLI module for prompt-build tool.

This module provides the command-line interface for building tool-specific
agent configurations from unified IR models.
"""

from src.cli.prompt_build_cli import PromptBuildCLI, main

__all__ = ["PromptBuildCLI", "main"]
