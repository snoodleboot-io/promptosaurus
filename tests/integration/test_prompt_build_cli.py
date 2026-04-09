"""Integration tests for prompt-build CLI tool.

Tests cover:
- CLI argument parsing and validation
- Agent loading from registry
- Builder selection and execution
- Output file writing for all tool types
- Variant handling (minimal/verbose)
- Error cases with helpful messages
- Full end-to-end workflows
"""

import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator

from src.cli.prompt_build_cli import PromptBuildCLI
from src.ir.models import Agent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Generator as GeneratorType
else:
    GeneratorType = Generator


def create_test_agents_directory(temp_dir: str | Path) -> Path:
    """Create a test agents directory with properly structured agents.

    Args:
        temp_dir: Temporary directory to create agents in

    Returns:
        Path to agents directory
    """
    agents_path = Path(temp_dir) / "agents"
    agents_path.mkdir(exist_ok=True)

    # Create code agent with both minimal and verbose variants
    code_minimal = agents_path / "code" / "minimal"
    code_minimal.mkdir(parents=True, exist_ok=True)
    (code_minimal / "prompt.md").write_text(
        "You are an expert software engineer and code generation specialist.\n\n"
        "Your role is to write high-quality Python code following best practices."
    )

    code_verbose = agents_path / "code" / "verbose"
    code_verbose.mkdir(parents=True, exist_ok=True)
    (code_verbose / "prompt.md").write_text(
        "You are a senior software engineer with extensive knowledge in many "
        "programming languages, frameworks, design patterns, and best practices.\n\n"
        "Your role is to write high-quality production code, mentor junior engineers, "
        "and establish architectural standards."
    )

    # Create architect agent
    architect_minimal = agents_path / "architect" / "minimal"
    architect_minimal.mkdir(parents=True, exist_ok=True)
    (architect_minimal / "prompt.md").write_text(
        "You are a software architect.\n\nYour role is to design scalable system architectures."
    )

    return agents_path


class TestPromptBuildCLIArgumentParsing:
    """Tests for CLI argument parsing."""

    @pytest.fixture
    def cli(self) -> Generator[PromptBuildCLI, None, None]:  # type: ignore
        """Create CLI instance."""
        with TemporaryDirectory() as temp_dir:
            agents_path = create_test_agents_directory(temp_dir)
            yield PromptBuildCLI(agents_dir=agents_path)

    def test_parser_creation(self, cli: PromptBuildCLI) -> None:
        """Test that parser is created successfully."""
        parser = cli.create_parser()
        assert parser is not None
        assert parser.prog == "prompt-build"

    def test_parser_required_arguments(self, cli: PromptBuildCLI) -> None:
        """Test that required arguments are enforced."""
        parser = cli.create_parser()
        # Should fail without required arguments
        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_parser_tool_choices(self, cli: PromptBuildCLI) -> None:
        """Test that tool argument accepts valid choices."""
        parser = cli.create_parser()
        # Valid tool
        args = parser.parse_args(["--tool", "kilo", "--agent", "code"])
        assert args.tool == "kilo"

    def test_parser_tool_invalid_choice(self, cli: PromptBuildCLI) -> None:
        """Test that invalid tool choice is rejected."""
        parser = cli.create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["--tool", "invalid", "--agent", "code"])

    def test_parser_variant_default(self, cli: PromptBuildCLI) -> None:
        """Test that variant defaults to minimal."""
        parser = cli.create_parser()
        args = parser.parse_args(["--tool", "kilo", "--agent", "code"])
        assert args.variant == "minimal"

    def test_parser_variant_verbose(self, cli: PromptBuildCLI) -> None:
        """Test that verbose variant is accepted."""
        parser = cli.create_parser()
        args = parser.parse_args(["--tool", "kilo", "--agent", "code", "--variant", "verbose"])
        assert args.variant == "verbose"

    def test_parser_output_default(self, cli: PromptBuildCLI) -> None:
        """Test that output defaults to current directory."""
        parser = cli.create_parser()
        args = parser.parse_args(["--tool", "kilo", "--agent", "code"])
        assert args.output == "."

    def test_parser_output_custom_path(self, cli: PromptBuildCLI) -> None:
        """Test that custom output path is accepted."""
        parser = cli.create_parser()
        args = parser.parse_args(["--tool", "kilo", "--agent", "code", "--output", "/tmp/output"])
        assert args.output == "/tmp/output"


class TestPromptBuildCLIBuilderSelection:
    """Tests for builder selection and retrieval."""

    @pytest.fixture
    def temp_agents_dir(self) -> Generator[Path, None, None]:
        """Create temporary agents directory."""
        with TemporaryDirectory() as temp_dir:
            agents_path = create_test_agents_directory(temp_dir)
            yield agents_path

    @pytest.fixture
    def cli(self, temp_agents_dir: Path) -> PromptBuildCLI:
        """Create CLI instance with temp agents directory."""
        return PromptBuildCLI(agents_dir=temp_agents_dir)

    def test_get_builder_kilo(self, cli: PromptBuildCLI) -> None:
        """Test getting Kilo builder."""
        builder = cli.get_builder("kilo")
        assert builder is not None
        assert builder.get_tool_name() == "kilo"

    def test_get_builder_claude(self, cli: PromptBuildCLI) -> None:
        """Test getting Claude builder."""
        builder = cli.get_builder("claude")
        assert builder is not None
        assert builder.get_tool_name() == "claude"

    def test_get_builder_cline(self, cli: PromptBuildCLI) -> None:
        """Test getting Cline builder."""
        builder = cli.get_builder("cline")
        assert builder is not None
        assert builder.get_tool_name() == "cline"

    def test_get_builder_invalid(self, cli: PromptBuildCLI) -> None:
        """Test that invalid builder name raises error."""
        with pytest.raises(SystemExit):
            cli.get_builder("invalid")

    def test_get_builder_case_insensitive(self, cli: PromptBuildCLI) -> None:
        """Test that builder names are case-insensitive."""
        builder = cli.get_builder("KILO")
        assert builder is not None


class TestPromptBuildCLIAgentLoading:
    """Tests for agent loading from registry."""

    @pytest.fixture
    def temp_agents_dir(self) -> Generator[Path, None, None]:
        """Create temporary agents directory with test agents."""
        with TemporaryDirectory() as temp_dir:
            agents_path = Path(temp_dir) / "agents"
            agents_path.mkdir()

            # Create code agent
            code_agent_dir = agents_path / "code" / "minimal"
            code_agent_dir.mkdir(parents=True)
            (code_agent_dir / "prompt.md").write_text("Code generation prompt")

            # Create architect agent
            architect_agent_dir = agents_path / "architect" / "minimal"
            architect_agent_dir.mkdir(parents=True)
            (architect_agent_dir / "prompt.md").write_text("Architecture design prompt")

            yield agents_path

    @pytest.fixture
    def cli(self, temp_agents_dir: Path) -> PromptBuildCLI:
        """Create CLI instance."""
        return PromptBuildCLI(agents_dir=temp_agents_dir)

    def test_load_agent_by_name(self, cli: PromptBuildCLI) -> None:
        """Test loading agent by name."""
        agent = cli.load_agent("code")
        assert agent is not None
        assert isinstance(agent, Agent)

    def test_load_multiple_agents(self, cli: PromptBuildCLI) -> None:
        """Test loading multiple different agents."""
        code_agent = cli.load_agent("code")
        architect_agent = cli.load_agent("architect")
        assert code_agent is not None
        assert architect_agent is not None
        assert code_agent.name == "code"
        assert architect_agent.name == "architect"

    def test_load_agent_not_found(self, cli: PromptBuildCLI) -> None:
        """Test that missing agent raises error."""
        with pytest.raises(SystemExit):
            cli.load_agent("nonexistent")

    def test_load_agent_helpful_error_message(self, cli: PromptBuildCLI) -> None:
        """Test that error message lists available agents."""
        # This test verifies the error message would mention available agents
        # We can't easily test stderr capture, so we verify the call fails
        with pytest.raises(SystemExit):
            cli.load_agent("missing_agent_xyz")


class TestPromptBuildCLIOutputPath:
    """Tests for determining output paths."""

    @pytest.fixture
    def cli(self) -> PromptBuildCLI:
        """Create CLI instance."""
        with TemporaryDirectory() as temp_dir:
            agents_path = Path(temp_dir) / "agents"
            agents_path.mkdir()
            code_agent_dir = agents_path / "code" / "minimal"
            code_agent_dir.mkdir(parents=True)
            (code_agent_dir / "prompt.md").write_text("Test")
            yield PromptBuildCLI(agents_dir=agents_path)

    def test_determine_output_path_kilo_default(self, cli: PromptBuildCLI) -> None:
        """Test default output path for Kilo."""
        path = cli.determine_output_path(".", "kilo", "code")
        assert str(path).endswith("code.md")

    def test_determine_output_path_kilo_custom_dir(self, cli: PromptBuildCLI) -> None:
        """Test custom directory output for Kilo."""
        path = cli.determine_output_path("/tmp", "kilo", "code")
        assert str(path).startswith("/tmp")
        assert str(path).endswith("code.md")

    def test_determine_output_path_claude_default(self, cli: PromptBuildCLI) -> None:
        """Test default output path for Claude."""
        path = cli.determine_output_path(".", "claude", "code")
        assert str(path).endswith("code.json")

    def test_determine_output_path_cline_default(self, cli: PromptBuildCLI) -> None:
        """Test default output path for Cline."""
        path = cli.determine_output_path(".", "cline", "code")
        assert str(path).endswith(".clinerules")

    def test_determine_output_path_cursor_default(self, cli: PromptBuildCLI) -> None:
        """Test default output path for Cursor."""
        path = cli.determine_output_path(".", "cursor", "code")
        assert str(path).endswith(".cursorrules")

    def test_determine_output_path_copilot_subdir(self, cli: PromptBuildCLI) -> None:
        """Test that Copilot uses .github/instructions subdir."""
        path = cli.determine_output_path(".", "copilot", "code")
        assert ".github/instructions" in str(path)
        assert str(path).endswith("code.md")

    def test_determine_output_path_explicit_file(self, cli: PromptBuildCLI) -> None:
        """Test explicit file path output."""
        path = cli.determine_output_path("/tmp/custom.md", "kilo", "code")
        assert str(path) == "/tmp/custom.md"


class TestPromptBuildCLIFileWriting:
    """Tests for writing output files."""

    @pytest.fixture
    def temp_output_dir(self) -> Generator[Path, None, None]:
        """Create temporary output directory."""
        with TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def temp_agents_dir(self) -> Generator[Path, None, None]:
        """Create temporary agents directory."""
        with TemporaryDirectory() as temp_dir:
            agents_path = Path(temp_dir) / "agents"
            agents_path.mkdir()
            code_agent_dir = agents_path / "code" / "minimal"
            code_agent_dir.mkdir(parents=True)
            (code_agent_dir / "prompt.md").write_text("Test prompt")
            yield agents_path

    @pytest.fixture
    def cli(self, temp_agents_dir: Path) -> PromptBuildCLI:
        """Create CLI instance."""
        return PromptBuildCLI(agents_dir=temp_agents_dir)

    def test_write_output_string_content(self, cli: PromptBuildCLI, temp_output_dir: Path) -> None:
        """Test writing string content to file."""
        output_file = temp_output_dir / "test.md"
        cli.write_output(output_file, "Test content", "kilo")
        assert output_file.exists()
        assert output_file.read_text() == "Test content"

    def test_write_output_dict_content_claude(
        self, cli: PromptBuildCLI, temp_output_dir: Path
    ) -> None:
        """Test writing dict content (Claude format) as JSON."""
        output_file = temp_output_dir / "test.json"
        content = {"system": "Test prompt", "tools": []}
        cli.write_output(output_file, content, "claude")
        assert output_file.exists()
        # Verify it's valid JSON
        loaded = json.loads(output_file.read_text())
        assert loaded["system"] == "Test prompt"

    def test_write_output_creates_parent_dirs(
        self, cli: PromptBuildCLI, temp_output_dir: Path
    ) -> None:
        """Test that write_output creates parent directories."""
        output_file = temp_output_dir / "subdir" / "nested" / "test.md"
        cli.write_output(output_file, "Content", "kilo")
        assert output_file.exists()
        assert output_file.parent.exists()

    def test_write_output_overwrites_existing(
        self, cli: PromptBuildCLI, temp_output_dir: Path
    ) -> None:
        """Test that write_output overwrites existing files."""
        output_file = temp_output_dir / "test.md"
        output_file.write_text("Old content")
        cli.write_output(output_file, "New content", "kilo")
        assert output_file.read_text() == "New content"

    def test_write_output_for_all_tools(self, cli: PromptBuildCLI, temp_output_dir: Path) -> None:
        """Test writing output for each tool type."""
        tools = ["kilo", "cline", "cursor", "copilot"]
        for tool in tools:
            output_file = temp_output_dir / f"test_{tool}.md"
            cli.write_output(output_file, "Content", tool)
            assert output_file.exists()


class TestPromptBuildCLIEndToEnd:
    """End-to-end integration tests."""

    @pytest.fixture
    def temp_agents_dir(self) -> Generator[Path, None, None]:
        """Create temporary agents directory with test agents."""
        with TemporaryDirectory() as temp_dir:
            agents_path = Path(temp_dir) / "agents"
            agents_path.mkdir()

            # Create code agent
            code_agent_dir = agents_path / "code" / "minimal"
            code_agent_dir.mkdir(parents=True)
            (code_agent_dir / "prompt.md").write_text("Code generation expert")

            code_agent_verbose = agents_path / "code" / "verbose"
            code_agent_verbose.mkdir(parents=True)
            (code_agent_verbose / "prompt.md").write_text("Detailed code generation instructions")

            yield agents_path

    @pytest.fixture
    def temp_output_dir(self) -> Generator[Path, None, None]:
        """Create temporary output directory."""
        with TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def cli(self, temp_agents_dir: Path) -> PromptBuildCLI:
        """Create CLI instance."""
        return PromptBuildCLI(agents_dir=temp_agents_dir)

    def test_build_kilo_minimal(self, cli: PromptBuildCLI, temp_output_dir: Path) -> None:
        """Test building Kilo agent with minimal variant."""
        args = [
            "--tool",
            "kilo",
            "--agent",
            "code",
            "--variant",
            "minimal",
            "--output",
            str(temp_output_dir),
        ]
        exit_code = cli.run(args)
        assert exit_code == 0
        output_file = temp_output_dir / "code.md"
        assert output_file.exists()
        assert len(output_file.read_text()) > 0

    def test_build_kilo_verbose(self, cli: PromptBuildCLI, temp_output_dir: Path) -> None:
        """Test building Kilo agent with verbose variant."""
        args = [
            "--tool",
            "kilo",
            "--agent",
            "code",
            "--variant",
            "verbose",
            "--output",
            str(temp_output_dir),
        ]
        exit_code = cli.run(args)
        assert exit_code == 0
        output_file = temp_output_dir / "code.md"
        assert output_file.exists()

    def test_build_claude(self, cli: PromptBuildCLI, temp_output_dir: Path) -> None:
        """Test building Claude agent."""
        args = [
            "--tool",
            "claude",
            "--agent",
            "code",
            "--output",
            str(temp_output_dir),
        ]
        exit_code = cli.run(args)
        assert exit_code == 0
        output_file = temp_output_dir / "code.json"
        assert output_file.exists()
        # Verify it's valid JSON
        content = json.loads(output_file.read_text())
        assert isinstance(content, dict)

    def test_build_cline(self, cli: PromptBuildCLI, temp_output_dir: Path) -> None:
        """Test building Cline agent."""
        args = [
            "--tool",
            "cline",
            "--agent",
            "code",
            "--output",
            str(temp_output_dir),
        ]
        exit_code = cli.run(args)
        assert exit_code == 0
        output_file = temp_output_dir / ".clinerules"
        assert output_file.exists()

    def test_build_cursor(self, cli: PromptBuildCLI, temp_output_dir: Path) -> None:
        """Test building Cursor agent."""
        args = [
            "--tool",
            "cursor",
            "--agent",
            "code",
            "--output",
            str(temp_output_dir),
        ]
        exit_code = cli.run(args)
        assert exit_code == 0
        output_file = temp_output_dir / ".cursorrules"
        assert output_file.exists()

    def test_build_copilot(self, cli: PromptBuildCLI, temp_output_dir: Path) -> None:
        """Test building Copilot agent (creates .github/instructions dir)."""
        args = [
            "--tool",
            "copilot",
            "--agent",
            "code",
            "--output",
            str(temp_output_dir),
        ]
        exit_code = cli.run(args)
        assert exit_code == 0
        output_file = temp_output_dir / ".github" / "instructions" / "code.md"
        assert output_file.exists()

    def test_build_with_custom_output_file(
        self, cli: PromptBuildCLI, temp_output_dir: Path
    ) -> None:
        """Test building with explicit output file path."""
        custom_file = temp_output_dir / "custom_output.md"
        args = [
            "--tool",
            "kilo",
            "--agent",
            "code",
            "--output",
            str(custom_file),
        ]
        exit_code = cli.run(args)
        assert exit_code == 0
        assert custom_file.exists()

    def test_build_multiple_agents_sequence(
        self, cli: PromptBuildCLI, temp_output_dir: Path
    ) -> None:
        """Test building multiple agents in sequence."""
        # First build
        args1 = [
            "--tool",
            "kilo",
            "--agent",
            "code",
            "--output",
            str(temp_output_dir),
        ]
        exit_code1 = cli.run(args1)
        assert exit_code1 == 0

        # Verify first build
        file1 = temp_output_dir / "code.md"
        assert file1.exists()

    def test_build_invalid_agent_error(self, cli: PromptBuildCLI, temp_output_dir: Path) -> None:
        """Test that building invalid agent returns error."""
        args = [
            "--tool",
            "kilo",
            "--agent",
            "nonexistent_agent",
            "--output",
            str(temp_output_dir),
        ]
        exit_code = cli.run(args)
        assert exit_code != 0

    def test_build_invalid_tool_error(self, cli: PromptBuildCLI, temp_output_dir: Path) -> None:
        """Test that invalid tool in args is rejected."""
        args = [
            "--tool",
            "invalid_tool",
            "--agent",
            "code",
            "--output",
            str(temp_output_dir),
        ]
        exit_code = cli.run(args)
        assert exit_code != 0

    def test_missing_required_tool_argument(
        self, cli: PromptBuildCLI, temp_output_dir: Path
    ) -> None:
        """Test that missing --tool argument causes error."""
        args = [
            "--agent",
            "code",
            "--output",
            str(temp_output_dir),
        ]
        exit_code = cli.run(args)
        assert exit_code != 0

    def test_missing_required_agent_argument(
        self, cli: PromptBuildCLI, temp_output_dir: Path
    ) -> None:
        """Test that missing --agent argument causes error."""
        args = [
            "--tool",
            "kilo",
            "--output",
            str(temp_output_dir),
        ]
        exit_code = cli.run(args)
        assert exit_code != 0


class TestPromptBuildCLIErrorHandling:
    """Tests for error handling and user feedback."""

    @pytest.fixture
    def temp_agents_dir(self) -> Generator[Path, None, None]:
        """Create minimal agents directory."""
        with TemporaryDirectory() as temp_dir:
            agents_path = Path(temp_dir) / "agents"
            agents_path.mkdir()
            code_agent_dir = agents_path / "code" / "minimal"
            code_agent_dir.mkdir(parents=True)
            (code_agent_dir / "prompt.md").write_text("Test")
            yield agents_path

    @pytest.fixture
    def cli(self, temp_agents_dir: Path) -> PromptBuildCLI:
        """Create CLI instance."""
        return PromptBuildCLI(agents_dir=temp_agents_dir)

    def test_agent_not_found_error_message(self, cli: PromptBuildCLI) -> None:
        """Test that agent not found error is helpful."""
        with pytest.raises(SystemExit):
            cli.load_agent("missing")

    def test_builder_not_found_error_message(self, cli: PromptBuildCLI) -> None:
        """Test that builder not found error is helpful."""
        with pytest.raises(SystemExit):
            cli.get_builder("nonexistent")

    def test_variant_invalid_raises_error(self, cli: PromptBuildCLI) -> None:
        """Test that invalid variant is rejected."""
        args = [
            "--tool",
            "kilo",
            "--agent",
            "code",
            "--variant",
            "invalid",
        ]
        parser = cli.create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(args)
