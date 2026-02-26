"""
builders/kilo.py
Builds the .kilo/ directory structure for Kilo Code.

Output layout:
  {output}/.kilo/rules/              ← always-on (all modes)
  {output}/.kilo/rules-{mode}/       ← per-mode files
  {output}/.kilocodemodes           ← manifest defining custom modes
"""

import shutil
from pathlib import Path

from promptcli.builders.builder import Builder
from promptcli.registry import registry


class KiloBuilder(Builder):
    """Builder for Kilo Code .kilo/ directory structure."""

    def build(self, output: Path, dry_run: bool = False) -> list[str]:
        """
        Write the Kilo .kilo/ structure under `output`.
        Returns a list of action strings for display.
        """
        actions: list[str] = []
        base = output / ".kilo"

        # Always-on rules
        for filename in registry.always_on:
            dst = base / "rules" / filename
            actions.append(self._copy(registry.prompt_path(filename), dst, dry_run))

        # Per-mode rules
        for mode_key, files in registry.mode_files.items():
            for filename in files:
                dst = base / f"rules-{mode_key}" / registry.dest_name(mode_key, filename)
                actions.append(self._copy(registry.prompt_path(filename), dst, dry_run))

        # Generate .kilocodemodes manifest
        actions.append(self._write_manifest(output / ".kilocodemodes", dry_run))

        return actions

    def _write_manifest(self, dst: Path, dry_run: bool) -> str:
        """Write the .kilocodemodes manifest file."""
        lines = ["# .kilocodemodes", "customModes:", ""]

        for mode_key, mode_info in registry.kilo_modes.items():
            slug = mode_key
            name = mode_info.get("name", mode_key.title())
            description = mode_info.get("description", "")
            role_definition = mode_info.get("roleDefinition", "")
            when_to_use = mode_info.get("whenToUse", "")
            groups = mode_info.get("groups", ["read", "edit", "command"])

            lines.append(f"  - slug: {slug}")
            lines.append(f"    name: {name}")
            lines.append(f"    description: {description}")
            lines.append(f"    roleDefinition: {role_definition}")
            lines.append(f"    whenToUse: {when_to_use}")
            lines.append("    groups:")

            for group in groups:
                if isinstance(group, str):
                    lines.append(f"      - {group}")
                elif isinstance(group, dict):
                    for group_name, group_config in group.items():
                        if group_config is None:
                            lines.append(f"      - {group_name}")
                        else:
                            file_regex = group_config.get("fileRegex", "")
                            lines.append(f"      - {group_name}:")
                            lines.append(f"          fileRegex: {file_regex}")

            lines.append("")

        content = "\n".join(lines)
        label = ".kilocodemodes"

        if dry_run:
            return f"[dry-run] {label}"
        dst.write_text(content, encoding="utf-8")
        return f"✓ {label}"

    def _copy(self, src: Path, dst: Path, dry_run: bool) -> str:
        rel = str(dst).split(".kilo/", 1)[-1]
        label = f".kilo/{rel}"
        if dry_run:
            return f"[dry-run] {src.name} → {label}"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return f"✓ {src.name} → {label}"
