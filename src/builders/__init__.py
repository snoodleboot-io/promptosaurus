"""Builders module for tool-specific output generation.

This module provides abstract builder base classes, factory patterns, and
mixin interfaces for generating tool-specific configurations from the
Intermediate Representation (IR) Agent models.
"""

from src.builders.base import AbstractBuilder, BuildOptions
from src.builders.interfaces import (
    SupportsSkills,
    SupportsWorkflows,
    SupportsRules,
    SupportsSubagents,
)
from src.builders.factory import BuilderFactory
from src.builders.registry import BuilderRegistry
from src.builders.errors import (
    BuilderException,
    BuilderNotFoundError,
    BuilderValidationError,
    UnsupportedFeatureError,
)

__all__ = [
    "AbstractBuilder",
    "BuildOptions",
    "SupportsSkills",
    "SupportsWorkflows",
    "SupportsRules",
    "SupportsSubagents",
    "BuilderFactory",
    "BuilderRegistry",
    "BuilderException",
    "BuilderNotFoundError",
    "BuilderValidationError",
    "UnsupportedFeatureError",
]
