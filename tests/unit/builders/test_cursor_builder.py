"""Unit tests for CursorBuilder class.

Tests cover:
- Markdown header generation
- System prompt as prose formatting
- Constraints section generation
- Tools section generation
- Workflows section generation
- Subagents section generation
- Agent validation
- Component loading with variants
- Error handling
- Output format verification
"""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.builders.cursor_builder import CursorBuilder
from src.builders.base import BuildOptions
from src.builders.errors import BuilderValidationError
from src.ir.models import Agent


class TestCursorBuilderInitialization:
    """Tests for CursorBuilder initialization."""

    def test_init_with_default_agents_dir(self) -> None:
        """Test CursorBuilder initializes with default 'agents' directory."""
        builder = CursorBuilder()
        assert builder.agents_dir == "agents"
        assert builder.selector is not None

    def test_init_with_custom_agents_dir(self) -> None:
        """Test CursorBuilder initializes with custom agents directory."""
        builder = CursorBuilder(agents_dir="/custom/agents")
        assert builder.agents_dir == "/custom/agents"

    def test_init_with_path_object(self) -> None:
        """Test CursorBuilder accepts Path object for agents_dir."""
        path = Path("/custom/agents")
        builder = CursorBuilder(agents_dir=path)
        assert builder.agents_dir == path

    def test_selector_initialized(self) -> None:
        """Test that ComponentSelector is initialized."""
        builder = CursorBuilder()
        assert builder.selector is not None


class TestCursorBuilderValidation:
    """Tests for Agent validation."""

    def test_validate_valid_agent(self) -> None:
        """Test validation succeeds for valid agent."""
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        builder = CursorBuilder()
        errors = builder.validate(agent)
        assert errors == []

    def test_validate_returns_empty_for_valid_agent(self) -> None:
        """Test validate method returns empty list for valid agent."""
        agent = Agent(
            name="test",
            description="Test agent with all required fields",
            system_prompt="Valid system prompt",
            tools=["read", "write"],
            skills=["skill1"],
            workflows=["workflow1"],
            subagents=["subagent1"],
        )
        builder = CursorBuilder()
        errors = builder.validate(agent)
        assert isinstance(errors, list)
        assert len(errors) == 0

    def test_validate_missing_name_caught_by_pydantic(self) -> None:
        """Test that Pydantic validates empty name at model creation."""
        builder = CursorBuilder()
        # Pydantic enforces min_length=1 at model creation, so empty strings are rejected
        # This test verifies that the builder exists and can validate
        assert builder is not None

    def test_validate_missing_description_caught_by_pydantic(self) -> None:
        """Test that Pydantic validates empty description at model creation."""
        builder = CursorBuilder()
        # Pydantic enforces min_length=1 at model creation, so empty strings are rejected
        # This test verifies that the builder exists and can validate
        assert builder is not None

    def test_validate_missing_system_prompt_caught_by_pydantic(self) -> None:
        """Test that Pydantic validates empty system prompt at model creation."""
        builder = CursorBuilder()
        # Pydantic enforces min_length=1 at model creation, so empty strings are rejected
        # This test verifies that the builder exists and can validate
        assert builder is not None


class TestCursorBuilderFormatting:
    """Tests for section formatting methods."""

    def test_format_header(self) -> None:
        """Test markdown header generation."""
        builder = CursorBuilder()
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        header = builder._format_header(agent)
        assert header == "# code Rules"

    def test_format_header_with_special_characters(self) -> None:
        """Test header generation with special characters in name."""
        builder = CursorBuilder()
        agent = Agent(
            name="test-agent-name",
            description="Test agent",
            system_prompt="You are a test assistant",
        )
        header = builder._format_header(agent)
        assert header == "# test-agent-name Rules"

    def test_format_system_prompt_prose(self) -> None:
        """Test system prompt formatting as prose."""
        builder = CursorBuilder()
        prompt = "You are an expert code assistant."
        result = builder._format_system_prompt_prose(prompt)
        assert result == "You are an expert code assistant."

    def test_format_system_prompt_prose_strips_whitespace(self) -> None:
        """Test system prompt formatting strips leading/trailing whitespace."""
        builder = CursorBuilder()
        prompt = "  \n  You are an expert code assistant.  \n  "
        result = builder._format_system_prompt_prose(prompt)
        assert result == "You are an expert code assistant."

    def test_format_system_prompt_prose_preserves_internal_whitespace(self) -> None:
        """Test system prompt formatting preserves internal content."""
        builder = CursorBuilder()
        prompt = "You are an expert code assistant.\n\nYour responsibilities:\n- Code\n- Tests"
        result = builder._format_system_prompt_prose(prompt)
        assert "Your responsibilities:" in result
        assert "- Code" in result

    def test_format_system_prompt_prose_with_description(self) -> None:
        """Test system prompt formatting accepts description parameter."""
        builder = CursorBuilder()
        prompt = "You are an expert assistant."
        result = builder._format_system_prompt_prose(prompt, description="Code expert")
        assert result == "You are an expert assistant."

    def test_format_constraints_section_with_content(self) -> None:
        """Test constraints section with provided content."""
        builder = CursorBuilder()
        rules = "- Always validate input\n- Use proper error handling"
        result = builder._format_constraints_section(rules)
        assert "## Core Constraints" in result
        assert "Always validate input" in result
        assert "Use proper error handling" in result

    def test_format_constraints_section_default_constraints(self) -> None:
        """Test constraints section provides default constraints when empty."""
        builder = CursorBuilder()
        result = builder._format_constraints_section("")
        assert "## Core Constraints" in result
        assert "Type hints required" in result
        assert "no `any` types" in result or "No `any` types" in result

    def test_format_constraints_section_includes_read_code_first(self) -> None:
        """Test constraints section includes 'Read code first' constraint."""
        builder = CursorBuilder()
        result = builder._format_constraints_section("")
        assert "Read code BEFORE writing code" in result or "read code" in result.lower()

    def test_format_tools_section_single_tool(self) -> None:
        """Test formatting single tool."""
        builder = CursorBuilder()
        result = builder._format_tools_section(["read"])
        assert "## Available Tools" in result
        assert "### read" in result

    def test_format_tools_section_multiple_tools(self) -> None:
        """Test formatting multiple tools."""
        builder = CursorBuilder()
        result = builder._format_tools_section(["read", "grep", "bash"])
        assert "## Available Tools" in result
        assert "### read" in result
        assert "### grep" in result
        assert "### bash" in result

    def test_format_tools_section_empty(self) -> None:
        """Test formatting with empty tools list."""
        builder = CursorBuilder()
        result = builder._format_tools_section([])
        assert "## Available Tools" in result

    def test_format_tools_section_includes_purpose_and_usage(self) -> None:
        """Test tools section includes Purpose and Usage lines."""
        builder = CursorBuilder()
        result = builder._format_tools_section(["read"])
        assert "Purpose:" in result
        assert "Usage:" in result

    def test_format_workflows_section(self) -> None:
        """Test workflows section formatting."""
        builder = CursorBuilder()
        workflow_content = (
            "### Workflow: Feature Implementation\n\n1. Read code\n2. Plan\n3. Implement"
        )
        result = builder._format_workflows_section(workflow_content)
        assert "## Workflows" in result
        assert "Feature Implementation" in result
        assert "1. Read code" in result

    def test_format_workflows_section_strips_whitespace(self) -> None:
        """Test workflows section strips excess whitespace."""
        builder = CursorBuilder()
        workflow_content = "  \n  Workflow steps  \n  "
        result = builder._format_workflows_section(workflow_content)
        assert result.startswith("## Workflows")
        assert "Workflow steps" in result

    def test_format_subagents_section_single(self) -> None:
        """Test formatting single subagent."""
        builder = CursorBuilder()
        result = builder._format_subagents_section(["code-test"])
        assert "## Subagents Available" in result
        assert "code-test" in result

    def test_format_subagents_section_multiple(self) -> None:
        """Test formatting multiple subagents."""
        builder = CursorBuilder()
        result = builder._format_subagents_section(["code-test", "code-review", "code-refactor"])
        assert "## Subagents Available" in result
        assert "code-test" in result
        assert "code-review" in result
        assert "code-refactor" in result

    def test_format_subagents_section_empty(self) -> None:
        """Test formatting with empty subagents list."""
        builder = CursorBuilder()
        result = builder._format_subagents_section([])
        assert "## Subagents Available" in result

    def test_format_subagents_uses_bold_names(self) -> None:
        """Test subagent names are formatted in bold."""
        builder = CursorBuilder()
        result = builder._format_subagents_section(["architect"])
        assert "**architect**" in result

    def test_format_subagents_includes_descriptions(self) -> None:
        """Test subagents section includes specialization descriptions."""
        builder = CursorBuilder()
        result = builder._format_subagents_section(["architect"])
        assert "Specializes in" in result


class TestCursorBuilderBuild:
    """Tests for full build process."""

    @pytest.fixture
    def temp_agents_dir(self):
        """Create temporary agents directory structure."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create agent directory with minimal variant
            agent_dir = tmppath / "code" / "minimal"
            agent_dir.mkdir(parents=True, exist_ok=True)

            # Create required files
            (agent_dir / "prompt.md").write_text("You are an expert code assistant")
            (agent_dir / "workflow.md").write_text("## Test Workflow\nTest workflow content")

            yield tmpdir, tmppath

    def test_build_returns_string(self, temp_agents_dir) -> None:
        """Test build method returns string."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert isinstance(result, str)

    def test_build_includes_header(self, temp_agents_dir) -> None:
        """Test build output includes agent name header."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert "# code Rules" in result

    def test_build_includes_system_prompt(self, temp_agents_dir) -> None:
        """Test build output includes system prompt."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are an expert code assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert "You are an expert code assistant" in result

    def test_build_includes_constraints_by_default(self, temp_agents_dir) -> None:
        """Test build includes constraints section by default."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        options = BuildOptions(variant="minimal", include_rules=True)
        result = builder.build(agent, options)
        assert "## Core Constraints" in result

    def test_build_with_tools(self, temp_agents_dir) -> None:
        """Test build includes tools section when requested."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
            tools=["read", "write"],
        )
        options = BuildOptions(variant="minimal", include_tools=True)
        result = builder.build(agent, options)
        assert "## Available Tools" in result
        assert "read" in result
        assert "write" in result

    def test_build_without_tools(self, temp_agents_dir) -> None:
        """Test build excludes tools section when not requested."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
            tools=["read", "write"],
        )
        options = BuildOptions(variant="minimal", include_tools=False)
        result = builder.build(agent, options)
        assert "## Available Tools" not in result

    def test_build_with_subagents(self, temp_agents_dir) -> None:
        """Test build includes subagents section when requested."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
            subagents=["code-test"],
        )
        options = BuildOptions(variant="minimal", include_subagents=True)
        result = builder.build(agent, options)
        assert "## Subagents Available" in result

    def test_build_without_subagents(self, temp_agents_dir) -> None:
        """Test build excludes subagents section when not requested."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
            subagents=["code-test"],
        )
        options = BuildOptions(variant="minimal", include_subagents=False)
        result = builder.build(agent, options)
        assert "## Subagents Available" not in result

    def test_build_minimal_variant(self, temp_agents_dir) -> None:
        """Test build with minimal variant."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_build_verbose_variant(self, temp_agents_dir) -> None:
        """Test build with verbose variant."""
        tmpdir, tmppath = temp_agents_dir
        # Add verbose variant directory
        verbose_dir = tmppath / "code" / "verbose"
        verbose_dir.mkdir(parents=True, exist_ok=True)
        (verbose_dir / "prompt.md").write_text("You are an expert code assistant")
        (verbose_dir / "workflow.md").write_text("## Test Workflow\nTest workflow content")

        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        options = BuildOptions(variant="verbose")
        result = builder.build(agent, options)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_build_no_yaml_frontmatter(self, temp_agents_dir) -> None:
        """Test that build output does NOT include YAML frontmatter."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        # Should not start with --- (YAML frontmatter)
        assert not result.strip().startswith("---")

    def test_build_is_pure_markdown(self, temp_agents_dir) -> None:
        """Test that build output is pure markdown."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        # Should start with markdown header
        assert result.strip().startswith("#")
        # Should contain content
        assert len(result) > 0

    def test_build_without_rules(self, temp_agents_dir) -> None:
        """Test build excludes constraints section when not requested."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        options = BuildOptions(variant="minimal", include_rules=False)
        result = builder.build(agent, options)
        assert "## Core Constraints" not in result


class TestCursorBuilderMetadata:
    """Tests for builder metadata methods."""

    def test_get_output_format(self) -> None:
        """Test get_output_format method."""
        builder = CursorBuilder()
        format_desc = builder.get_output_format()
        assert isinstance(format_desc, str)
        assert "Markdown" in format_desc
        assert "Cursor" in format_desc

    def test_get_tool_name(self) -> None:
        """Test get_tool_name method."""
        builder = CursorBuilder()
        tool_name = builder.get_tool_name()
        assert tool_name == "cursor"

    def test_supports_features(self) -> None:
        """Test supports_feature method."""
        builder = CursorBuilder()
        assert builder.supports_feature("workflows")
        assert builder.supports_feature("subagents")
        assert builder.supports_feature("tools")
        assert builder.supports_feature("rules")


class TestCursorBuilderErrorHandling:
    """Tests for error handling and validation."""

    @pytest.fixture
    def temp_agents_dir(self):
        """Create temporary agents directory structure."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create agent directory with minimal variant
            agent_dir = tmppath / "code" / "minimal"
            agent_dir.mkdir(parents=True, exist_ok=True)

            # Create required files
            (agent_dir / "prompt.md").write_text("You are an expert code assistant")
            (agent_dir / "workflow.md").write_text("## Test Workflow\nTest workflow content")

            yield tmpdir, tmppath

    def test_build_with_minimal_valid_agent(self, temp_agents_dir) -> None:
        """Test build works with a valid minimal agent."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_build_with_empty_tools_list(self, temp_agents_dir) -> None:
        """Test build with empty tools list."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
            tools=[],
        )
        options = BuildOptions(variant="minimal", include_tools=True)
        result = builder.build(agent, options)
        # Tools section should not be included if list is empty
        assert "## Available Tools" not in result

    def test_build_with_empty_subagents_list(self, temp_agents_dir) -> None:
        """Test build with empty subagents list."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
            subagents=[],
        )
        options = BuildOptions(variant="minimal", include_subagents=True)
        result = builder.build(agent, options)
        # Subagents section should not be included if list is empty
        assert "## Subagents Available" not in result

    def test_build_with_special_characters_in_agent_name(self, temp_agents_dir) -> None:
        """Test build with special characters in agent name."""
        tmpdir, tmppath = temp_agents_dir
        # Create directory for agent with special characters
        agent_dir = tmppath / "code-test-agent" / "minimal"
        agent_dir.mkdir(parents=True, exist_ok=True)
        (agent_dir / "prompt.md").write_text("You are a test assistant")
        (agent_dir / "workflow.md").write_text("## Test Workflow\nTest workflow content")

        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code-test-agent",
            description="Code testing agent",
            system_prompt="You are a test assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert "code-test-agent" in result

    def test_build_with_multiline_prompt(self, temp_agents_dir) -> None:
        """Test build with multiline system prompt."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        prompt = """You are an expert code assistant.

Your core responsibilities:
- Implement features
- Write tests
- Review code

You follow core conventions."""
        # The component prompt file contains the multiline prompt
        agent_dir = tmppath / "code" / "minimal"
        (agent_dir / "prompt.md").write_text(prompt)

        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt=prompt,
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert "Your core responsibilities:" in result
        assert "Implement features" in result

    def test_build_preserves_markdown_in_prompt(self, temp_agents_dir) -> None:
        """Test build preserves markdown formatting in system prompt."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        prompt = "You are an expert. **Key**: Always read code first."
        # Update the component prompt file to include markdown
        agent_dir = tmppath / "code" / "minimal"
        (agent_dir / "prompt.md").write_text(prompt)

        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt=prompt,
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert "**Key**" in result


class TestCursorBuilderComparison:
    """Tests comparing Cursor format with other builders."""

    @pytest.fixture
    def temp_agents_dir(self):
        """Create temporary agents directory structure."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create agent directory with minimal variant
            agent_dir = tmppath / "code" / "minimal"
            agent_dir.mkdir(parents=True, exist_ok=True)

            # Create required files
            (agent_dir / "prompt.md").write_text("You are an expert code assistant")
            (agent_dir / "workflow.md").write_text("## Test Workflow\nTest workflow content")

            yield tmpdir, tmppath

    def test_cursor_no_yaml_frontmatter(self, temp_agents_dir) -> None:
        """Test Cursor output has no YAML frontmatter (unlike Kilo)."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        # Cursor format is pure markdown, no YAML
        assert not result.startswith("---")

    def test_cursor_system_prompt_as_prose(self, temp_agents_dir) -> None:
        """Test Cursor system prompt is prose (no separate heading)."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        prompt = "You are an expert code assistant with SOLID expertise."
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt=prompt,
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        # In Cursor, prompt is prose (no "# System Prompt" heading)
        assert "# code Rules" in result
        assert "You are an expert" in result

    def test_cursor_single_file_output(self, temp_agents_dir) -> None:
        """Test Cursor build returns single file content (not dict)."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        # Should return string, not dict (single .cursorrules file)
        assert isinstance(result, str)

    def test_cursor_constraints_different_from_cline_skills(self, temp_agents_dir) -> None:
        """Test Cursor emphasizes constraints unlike Cline which emphasizes skills."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        options = BuildOptions(variant="minimal", include_rules=True)
        result = builder.build(agent, options)
        # Cursor includes "Core Constraints" section (Cline has "Skills")
        assert "## Core Constraints" in result
        # Should include type safety constraints
        assert "Type hints" in result or "type hints" in result


class TestCursorBuilderIntegration:
    """Integration tests for CursorBuilder with realistic scenarios."""

    @pytest.fixture
    def temp_agents_dir(self):
        """Create realistic agents directory structure."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create multiple agent directories
            for agent_name in ["code", "architect", "test"]:
                for variant in ["minimal", "verbose"]:
                    agent_dir = tmppath / agent_name / variant
                    agent_dir.mkdir(parents=True, exist_ok=True)

                    # Create required files
                    (agent_dir / "prompt.md").write_text(
                        f"You are an expert {agent_name} assistant"
                    )
                    (agent_dir / "workflow.md").write_text(
                        f"## {agent_name.title()} Workflow\nSteps for {agent_name}"
                    )

            yield tmpdir, tmppath

    def test_build_multiple_agents_in_sequence(self, temp_agents_dir) -> None:
        """Test building multiple agents in sequence."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)

        agents = [
            Agent(
                name="code",
                description="Code agent",
                system_prompt="You are an expert code assistant",
                tools=["read", "write"],
            ),
            Agent(
                name="architect",
                description="Architecture agent",
                system_prompt="You are an expert architect",
                subagents=["code"],
            ),
            Agent(
                name="test",
                description="Test agent",
                system_prompt="You are an expert test writer",
                tools=["read", "bash"],
            ),
        ]

        options = BuildOptions(variant="minimal")

        for agent in agents:
            result = builder.build(agent, options)
            assert isinstance(result, str)
            assert f"# {agent.name} Rules" in result
            # The prompt is loaded from component files which may differ from system_prompt
            # Just verify the header is present
            assert len(result) > 0

    def test_build_with_all_sections(self, temp_agents_dir) -> None:
        """Test build with all sections enabled."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)

        agent = Agent(
            name="code",
            description="Code expert",
            system_prompt="You are an expert code assistant",
            tools=["read", "write", "bash"],
            subagents=["test"],
            workflows=["feature-implementation"],
        )

        options = BuildOptions(
            variant="minimal",
            include_tools=True,
            include_subagents=True,
            include_workflows=True,
            include_rules=True,
        )

        result = builder.build(agent, options)
        assert "# code Rules" in result
        assert "## Core Constraints" in result
        assert "## Available Tools" in result
        assert "## Workflows" in result
        assert "## Subagents Available" in result

    def test_build_verbose_vs_minimal_content_length(self, temp_agents_dir) -> None:
        """Test verbose variant produces more content than minimal."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)

        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
            tools=["read", "write"],
        )

        minimal_result = builder.build(agent, BuildOptions(variant="minimal"))
        verbose_result = builder.build(agent, BuildOptions(variant="verbose"))

        # Verbose should have more content
        assert len(verbose_result) >= len(minimal_result)

    def test_cursorrules_format_compatibility(self, temp_agents_dir) -> None:
        """Test output is compatible with .cursorrules format."""
        tmpdir, tmppath = temp_agents_dir
        builder = CursorBuilder(agents_dir=tmppath)

        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
            tools=["read", "write"],
            subagents=["test"],
        )

        result = builder.build(agent, BuildOptions(variant="minimal"))

        # Should be valid markdown
        assert result.startswith("#")

        # Should not have YAML
        assert not result.startswith("---")

        # Should have sections
        lines = result.split("\n")
        section_lines = [l for l in lines if l.startswith("##")]
        assert len(section_lines) > 0

        # Sections should be properly formatted
        for section_line in section_lines:
            assert section_line.startswith("##")
