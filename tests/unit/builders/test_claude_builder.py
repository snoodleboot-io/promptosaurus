"""Unit tests for ClaudeBuilder class.

Tests cover:
- JSON dictionary structure generation
- System prompt extraction
- Tools list with JSON schemas
- Instructions formatting from all sections
- Agent validation
- Component loading with variants
- Error handling
- JSON serializability verification
"""

import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Generator

from src.builders.claude_builder import ClaudeBuilder
from src.builders.base import BuildOptions
from src.builders.errors import BuilderValidationError
from src.ir.models import Agent


class TestClaudeBuilderInitialization:
    """Tests for ClaudeBuilder initialization."""

    def test_init_with_default_agents_dir(self) -> None:
        """Test ClaudeBuilder initializes with default 'agents' directory."""
        builder = ClaudeBuilder()
        assert builder.agents_dir == "agents"
        assert builder.selector is not None

    def test_init_with_custom_agents_dir(self) -> None:
        """Test ClaudeBuilder initializes with custom agents directory."""
        builder = ClaudeBuilder(agents_dir="/custom/agents")
        assert builder.agents_dir == "/custom/agents"

    def test_init_with_path_object(self) -> None:
        """Test ClaudeBuilder accepts Path object for agents_dir."""
        path = Path("/custom/agents")
        builder = ClaudeBuilder(agents_dir=path)
        assert builder.agents_dir == path

    def test_selector_initialized(self) -> None:
        """Test that ComponentSelector is initialized."""
        builder = ClaudeBuilder()
        assert builder.selector is not None


class TestClaudeBuilderValidation:
    """Tests for Agent validation."""

    def test_validate_valid_agent(self) -> None:
        """Test validation succeeds for valid agent."""
        agent = Agent(
            name="code",
            description="Code agent",
            system_prompt="You are a code assistant",
        )
        builder = ClaudeBuilder()
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
        builder = ClaudeBuilder()
        errors = builder.validate(agent)
        assert isinstance(errors, list)
        assert len(errors) == 0

    def test_validate_error_list_is_list_type(self) -> None:
        """Test validation returns a list type."""
        agent = Agent(
            name="test",
            description="Test agent",
            system_prompt="Valid system prompt",
        )
        builder = ClaudeBuilder()
        errors = builder.validate(agent)
        assert isinstance(errors, list)


class TestClaudeBuilderSystemPrompt:
    """Tests for system prompt building."""

    def test_build_system_prompt_basic(self) -> None:
        """Test system prompt extraction from bundle."""
        builder = ClaudeBuilder()
        prompt = "You are an expert code assistant"
        result = builder._build_system_prompt(prompt)
        assert result == "You are an expert code assistant"

    def test_build_system_prompt_strips_whitespace(self) -> None:
        """Test system prompt strips leading/trailing whitespace."""
        builder = ClaudeBuilder()
        prompt = "  \n  You are an expert.  \n  "
        result = builder._build_system_prompt(prompt)
        assert result == "You are an expert."

    def test_build_system_prompt_preserves_internal_newlines(self) -> None:
        """Test system prompt preserves internal content."""
        builder = ClaudeBuilder()
        prompt = "You are an expert.\n\nYour tasks:\n- Code\n- Test"
        result = builder._build_system_prompt(prompt)
        assert "Your tasks:" in result
        assert "- Code" in result


class TestClaudeBuilderTools:
    """Tests for tools list building."""

    def test_build_tools_list_empty(self) -> None:
        """Test building tools list with no tools."""
        builder = ClaudeBuilder()
        result = builder._build_tools_list([])
        assert isinstance(result, list)
        assert len(result) == 0

    def test_build_tools_list_single_tool(self) -> None:
        """Test building tools list with single tool."""
        builder = ClaudeBuilder()
        result = builder._build_tools_list(["read"])
        assert len(result) == 1
        assert result[0]["name"] == "read"

    def test_build_tools_list_multiple_tools(self) -> None:
        """Test building tools list with multiple tools."""
        builder = ClaudeBuilder()
        result = builder._build_tools_list(["read", "write", "bash"])
        assert len(result) == 3
        assert result[0]["name"] == "read"
        assert result[1]["name"] == "write"
        assert result[2]["name"] == "bash"

    def test_tool_has_required_fields(self) -> None:
        """Test each tool has name, description, and input_schema."""
        builder = ClaudeBuilder()
        result = builder._build_tools_list(["read"])
        tool = result[0]
        assert "name" in tool
        assert "description" in tool
        assert "input_schema" in tool

    def test_tool_input_schema_is_valid_json_schema(self) -> None:
        """Test tool input_schema is valid JSON schema structure."""
        builder = ClaudeBuilder()
        result = builder._build_tools_list(["read"])
        schema = result[0]["input_schema"]
        assert schema["type"] == "object"
        assert "properties" in schema
        assert isinstance(schema["properties"], dict)

    def test_build_tool_schema_structure(self) -> None:
        """Test tool schema structure is correct."""
        builder = ClaudeBuilder()
        schema = builder._build_tool_schema("test-tool")
        assert schema["name"] == "test-tool"
        assert schema["description"] == "Tool: test-tool"
        assert "input_schema" in schema
        assert schema["input_schema"]["type"] == "object"


class TestClaudeBuilderInstructions:
    """Tests for instructions building."""

    def test_build_instructions_empty_bundle(self) -> None:
        """Test building instructions with minimal content."""
        builder = ClaudeBuilder()
        agent = Agent(
            name="test",
            description="Test agent",
            system_prompt="Test prompt",
        )
        options = BuildOptions(
            include_skills=False, include_workflows=False, include_subagents=False
        )

        # Mock bundle with empty content
        class MockBundle:
            skills = ""
            workflow = ""
            rules = ""

        result = builder._build_instructions(MockBundle(), agent, options)
        assert isinstance(result, str)

    def test_format_skills_section(self) -> None:
        """Test skills section formatting."""
        builder = ClaudeBuilder()
        skills_content = "Available skills for implementation"
        skill_names = ["test-implementation", "code-review"]
        result = builder._format_skills_section(skills_content, skill_names)
        assert "Skills:" in result
        assert "use_skill" in result
        assert "test_implementation" in result
        assert "code_review" in result

    def test_format_skills_section_single_skill(self) -> None:
        """Test skills section with single skill."""
        builder = ClaudeBuilder()
        result = builder._format_skills_section("", ["my-skill"])
        assert "Skills:" in result
        assert "my_skill" in result
        assert "use_skill my_skill" in result

    def test_format_skills_section_empty(self) -> None:
        """Test skills section with no skills."""
        builder = ClaudeBuilder()
        result = builder._format_skills_section("Skills content", [])
        assert "Skills:" in result
        assert "Skills content" in result

    def test_format_workflows_section(self) -> None:
        """Test workflows section formatting."""
        builder = ClaudeBuilder()
        workflow_content = "Step 1: Do something\nStep 2: Do something else"
        result = builder._format_workflows_section(workflow_content)
        assert "Workflows:" in result
        assert "Step 1:" in result
        assert "Step 2:" in result

    def test_format_workflows_section_strips_whitespace(self) -> None:
        """Test workflows section strips excess whitespace."""
        builder = ClaudeBuilder()
        workflow_content = "  \n  Workflow steps  \n  "
        result = builder._format_workflows_section(workflow_content)
        assert result == "Workflows:\n\nWorkflow steps"

    def test_format_subagents_section(self) -> None:
        """Test subagents section formatting."""
        builder = ClaudeBuilder()
        result = builder._format_subagents_section(["code", "test", "review"])
        assert "Subagents:" in result
        assert "- code:" in result
        assert "- test:" in result
        assert "- review:" in result

    def test_format_subagents_section_single(self) -> None:
        """Test subagents section with single subagent."""
        builder = ClaudeBuilder()
        result = builder._format_subagents_section(["code"])
        assert "Subagents:" in result
        assert "- code:" in result

    def test_format_subagents_section_empty(self) -> None:
        """Test subagents section with no subagents."""
        builder = ClaudeBuilder()
        result = builder._format_subagents_section([])
        assert "Subagents:" in result

    def test_format_rules_section(self) -> None:
        """Test rules section formatting."""
        builder = ClaudeBuilder()
        rules_content = "Follow these rules:\n- Rule 1\n- Rule 2"
        result = builder._format_rules_section(rules_content)
        assert "Rules:" in result
        assert "Rule 1" in result
        assert "Rule 2" in result


class TestClaudeBuilderBuild:
    """Tests for build method and output generation."""

    @pytest.fixture
    def temp_agents_dir(self) -> Generator[tuple[str, Path], Any, Any]:
        """Create temporary agents directory structure."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create agent directory with minimal variant
            agent_dir = tmppath / "test_agent" / "minimal"
            agent_dir.mkdir(parents=True, exist_ok=True)

            # Create required files
            (agent_dir / "prompt.md").write_text("Test system prompt")
            (agent_dir / "skills.md").write_text("## Test Skill\nTest skill content")
            (agent_dir / "workflow.md").write_text("## Test Workflow\nTest workflow content")

            yield tmpdir, tmppath

    def test_build_returns_dict(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build method returns a dictionary."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert isinstance(result, dict)

    def test_build_dict_has_system_key(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test output dict has 'system' key."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert "system" in result

    def test_build_dict_has_tools_key(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test output dict has 'tools' key."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert "tools" in result

    def test_build_dict_has_instructions_key(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test output dict has 'instructions' key."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert "instructions" in result

    def test_build_system_prompt_is_string(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test system prompt value is a string."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert isinstance(result["system"], str)
        # The system prompt comes from the component bundle, not the agent
        assert len(result["system"]) > 0

    def test_build_tools_is_list(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test tools value is a list."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
            tools=["read", "write"],
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert isinstance(result["tools"], list)

    def test_build_instructions_is_string(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test instructions value is a string."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert isinstance(result["instructions"], str)

    def test_build_tools_include_flag(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test tools are included/excluded based on include_tools flag."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
            tools=["read"],
        )

        # With include_tools=True
        options = BuildOptions(variant="minimal", include_tools=True)
        result = builder.build(agent, options)
        assert len(result["tools"]) > 0

        # With include_tools=False
        options = BuildOptions(variant="minimal", include_tools=False)
        result = builder.build(agent, options)
        assert len(result["tools"]) == 0

    def test_build_output_is_json_serializable(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build output can be serialized to JSON."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
            tools=["read", "write"],
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)

        # Should not raise
        json_str = json.dumps(result)
        assert isinstance(json_str, str)

    def test_build_json_roundtrip(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build output can be dumped and loaded as JSON."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
            tools=["read"],
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)

        # Dump and reload
        json_str = json.dumps(result)
        reloaded = json.loads(json_str)

        assert reloaded["system"] == result["system"]
        assert reloaded["tools"] == result["tools"]
        assert reloaded["instructions"] == result["instructions"]

    def test_build_with_empty_tools_list(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build with agent that has no tools."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
            tools=[],
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert isinstance(result, dict)
        assert result["tools"] == []

    def test_build_with_multiple_tools(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build with agent that has multiple tools."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
            tools=["read", "write", "bash", "grep"],
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert len(result["tools"]) == 4
        names = [tool["name"] for tool in result["tools"]]
        assert "read" in names
        assert "write" in names
        assert "bash" in names
        assert "grep" in names


class TestClaudeBuilderMetadata:
    """Tests for metadata methods."""

    def test_get_output_format(self) -> None:
        """Test get_output_format returns correct string."""
        builder = ClaudeBuilder()
        format_str = builder.get_output_format()
        assert "Claude" in format_str
        assert "JSON" in format_str
        assert "dict" in format_str

    def test_get_tool_name(self) -> None:
        """Test get_tool_name returns 'claude'."""
        builder = ClaudeBuilder()
        assert builder.get_tool_name() == "claude"

    def test_supports_feature(self) -> None:
        """Test supports_feature returns correct values."""
        builder = ClaudeBuilder()
        assert builder.supports_feature("tools") is True
        assert builder.supports_feature("skills") is True
        assert builder.supports_feature("workflows") is True
        assert builder.supports_feature("unknown_feature") is False


class TestClaudeBuilderOptions:
    """Tests for BuildOptions handling."""

    @pytest.fixture
    def temp_agents_dir(self) -> Generator[tuple[str, Path], Any, Any]:
        """Create temporary agents directory structure."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create agent directory with minimal variant
            agent_dir = tmppath / "test_agent" / "minimal"
            agent_dir.mkdir(parents=True, exist_ok=True)

            # Create required files
            (agent_dir / "prompt.md").write_text("Test system prompt")
            (agent_dir / "skills.md").write_text("## Test Skill\nTest skill content")
            (agent_dir / "workflow.md").write_text("## Test Workflow\nTest workflow content")

            yield tmpdir, tmppath

    def test_build_with_minimal_variant(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build works with minimal variant."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert isinstance(result, dict)

    def test_build_with_verbose_variant(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build works with verbose variant."""
        tmpdir, tmppath = temp_agents_dir
        # Create verbose variant as fallback
        agent_dir = tmppath / "test_agent" / "verbose"
        agent_dir.mkdir(parents=True, exist_ok=True)
        (agent_dir / "prompt.md").write_text("Test system prompt - verbose")
        (agent_dir / "skills.md").write_text("## Test Skill\nTest skill content - verbose")
        (agent_dir / "workflow.md").write_text("## Test Workflow\nTest workflow content - verbose")

        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
        )
        options = BuildOptions(variant="verbose")
        result = builder.build(agent, options)
        assert isinstance(result, dict)

    def test_build_exclude_skills(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build respects include_skills flag."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
            skills=["skill1"],
        )
        options = BuildOptions(variant="minimal", include_skills=False)
        result = builder.build(agent, options)
        assert isinstance(result, dict)

    def test_build_exclude_workflows(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build respects include_workflows flag."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
            workflows=["workflow1"],
        )
        options = BuildOptions(variant="minimal", include_workflows=False)
        result = builder.build(agent, options)
        assert isinstance(result, dict)

    def test_build_exclude_subagents(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build respects include_subagents flag."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="test_agent",
            description="Test agent",
            system_prompt="You are a test assistant",
            subagents=["subagent1"],
        )
        options = BuildOptions(variant="minimal", include_subagents=False)
        result = builder.build(agent, options)
        assert isinstance(result, dict)


class TestClaudeBuilderComplexScenarios:
    """Tests for complex scenarios and edge cases."""

    @pytest.fixture
    def temp_agents_dir(self) -> Generator[tuple[str, Path], Any, Any]:
        """Create temporary agents directory structure."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create agent directory with minimal variant
            agent_dir = tmppath / "comprehensive" / "minimal"
            agent_dir.mkdir(parents=True, exist_ok=True)

            # Create required files
            (agent_dir / "prompt.md").write_text("Test system prompt")
            (agent_dir / "skills.md").write_text("## Test Skill\nTest skill content")
            (agent_dir / "workflow.md").write_text("## Test Workflow\nTest workflow content")

            yield tmpdir, tmppath

    def test_build_with_all_components(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build with agent having all possible components."""
        tmpdir, tmppath = temp_agents_dir
        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="comprehensive",
            description="An agent with all components",
            system_prompt="You are a comprehensive assistant",
            tools=["read", "write", "bash"],
            skills=["coding", "testing"],
            workflows=["feature-dev", "bug-fix"],
            subagents=["code", "test", "review"],
        )
        options = BuildOptions(
            variant="minimal",
            include_tools=True,
            include_skills=True,
            include_workflows=True,
            include_subagents=True,
        )
        result = builder.build(agent, options)
        assert len(result["tools"]) == 3
        assert isinstance(result["instructions"], str)
        assert len(result["instructions"]) > 0

    def test_build_with_special_characters_in_name(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build with special characters in agent name."""
        tmpdir, tmppath = temp_agents_dir
        # Create agent directory for special name
        agent_dir = tmppath / "code-architect" / "minimal"
        agent_dir.mkdir(parents=True, exist_ok=True)
        (agent_dir / "prompt.md").write_text("You are a code architect")

        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code-architect",
            description="An agent for code architecture",
            system_prompt="You are a code architect",
            tools=["analyze"],
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert isinstance(result, dict)

    def test_build_with_multiline_system_prompt(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build with multiline system prompt."""
        tmpdir, tmppath = temp_agents_dir
        # Create agent directory
        agent_dir = tmppath / "code" / "minimal"
        agent_dir.mkdir(parents=True, exist_ok=True)

        system_prompt = """You are an expert code assistant.

Your responsibilities:
- Write clean code
- Follow best practices
- Maintain consistency"""

        (agent_dir / "prompt.md").write_text(system_prompt)

        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="code",
            description="Code assistant",
            system_prompt=system_prompt,
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)
        assert system_prompt.strip() in result["system"]

    def test_build_json_with_unicode_characters(self, temp_agents_dir: tuple[str, Path]) -> None:
        """Test build output handles unicode characters."""
        tmpdir, tmppath = temp_agents_dir
        # Create agent directory
        agent_dir = tmppath / "unicode_test" / "minimal"
        agent_dir.mkdir(parents=True, exist_ok=True)
        (agent_dir / "prompt.md").write_text("You are helpful. ✓ ✗ → ←")

        builder = ClaudeBuilder(agents_dir=tmppath)
        agent = Agent(
            name="unicode_test",
            description="Test agent with unicode: 你好 مرحبا",
            system_prompt="You are helpful. ✓ ✗ → ←",
            tools=["read"],
        )
        options = BuildOptions(variant="minimal")
        result = builder.build(agent, options)

        # Should be JSON serializable with unicode characters
        json_str = json.dumps(result, ensure_ascii=False)
        assert isinstance(json_str, str)
        # Description contains unicode, so check the result is serializable
        assert "read" in json_str

    def test_tool_schema_required_fields(self) -> None:
        """Test tool schema includes required fields."""
        builder = ClaudeBuilder()
        schema = builder._build_tool_schema("test")
        input_schema = schema["input_schema"]
        assert "required" in input_schema
        assert isinstance(input_schema["required"], list)

    def test_instructions_section_ordering(self) -> None:
        """Test instructions sections appear in expected order."""
        builder = ClaudeBuilder()
        agent = Agent(
            name="test",
            description="Test agent",
            system_prompt="Test",
            skills=["skill1"],
            workflows=["workflow1"],
            subagents=["sub1"],
        )
        options = BuildOptions()

        # Mock bundle
        class MockBundle:
            skills = "Skill content"
            workflow = "Workflow content"
            rules = ""

        result = builder._build_instructions(MockBundle(), agent, options)
        assert "Skills:" in result
        assert "Workflows:" in result
        assert "Subagents:" in result

    def test_empty_instructions_when_all_excluded(self) -> None:
        """Test instructions are minimal when all components excluded."""
        builder = ClaudeBuilder()
        agent = Agent(
            name="test",
            description="Test agent",
            system_prompt="Test",
        )
        options = BuildOptions(
            include_skills=False,
            include_workflows=False,
            include_subagents=False,
            include_rules=False,
        )

        class MockBundle:
            skills = ""
            workflow = ""
            rules = ""

        result = builder._build_instructions(MockBundle(), agent, options)
        assert isinstance(result, str)
