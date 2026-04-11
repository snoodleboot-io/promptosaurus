"""Unit tests for Data Agent."""

import pytest
from pathlib import Path


@pytest.mark.unit
class TestDataAgent:
    """Test suite for data agent."""
    
    @pytest.fixture
    def agent_file(self, agents_dir):
        """Get data agent file."""
        return agents_dir / "data" / "prompt.md"
    
    @pytest.fixture
    def agent_content(self, agent_file, read_file):
        """Read agent file content."""
        assert agent_file.exists(), f"Agent file not found: {agent_file}"
        return read_file(agent_file)
    
    def test_agent_exists(self, agent_file):
        """Test that agent file exists."""
        assert agent_file.exists(), "data/prompt.md not found"
    
    def test_agent_has_purpose(self, agent_content):
        """Test that agent has purpose section."""
        assert "Purpose" in agent_content or "purpose" in agent_content.lower(), \
            "Agent missing purpose section"
    
    def test_agent_has_responsibilities(self, agent_content):
        """Test that agent has responsibilities section."""
        assert "Responsibilit" in agent_content, \
            "Agent missing responsibilities section"
    
    def test_agent_has_capabilities(self, agent_content):
        """Test that agent has capabilities section."""
        assert "Capabilit" in agent_content, \
            "Agent missing capabilities section"
    
    def test_agent_min_length(self, agent_content):
        """Test that agent has minimum content."""
        lines = len(agent_content.strip().split('\n'))
        assert lines > 20, f"Agent too short: {lines} lines (min 20)"
    
    def test_agent_has_subagents(self, agent_content):
        """Test that agent references subagents."""
        assert "subagent" in agent_content.lower(), \
            "Agent doesn't reference subagents"
    
    def test_agent_references_key_subagents(self, agent_content):
        """Test agent references all expected subagents."""
        expected = ["pipeline", "warehouse", "quality", "governance", "streaming"]
        for subagent in expected:
            assert subagent.lower() in agent_content.lower(), \
                f"Agent missing reference to {subagent} subagent"


@pytest.mark.unit
class TestDataAgentSubagents:
    """Test suite for data agent subagents."""
    
    @pytest.fixture
    def subagents_dir(self, agents_dir):
        """Get data subagents directory."""
        return agents_dir / "data" / "subagents"
    
    @pytest.mark.parametrize("subagent_name", [
        "pipeline", "warehouse", "quality", "governance", "streaming"
    ])
    def test_subagent_exists(self, subagents_dir, subagent_name):
        """Test that subagent exists."""
        subagent_dir = subagents_dir / subagent_name
        assert subagent_dir.exists(), f"Subagent dir not found: {subagent_name}"
    
    @pytest.mark.parametrize("variant", ["minimal", "verbose"])
    @pytest.mark.parametrize("subagent_name", [
        "pipeline", "warehouse", "quality", "governance", "streaming"
    ])
    def test_subagent_variant_exists(self, subagents_dir, subagent_name, variant, read_file):
        """Test that subagent variants exist."""
        file_path = subagents_dir / subagent_name / variant / "prompt.md"
        assert file_path.exists(), f"Missing {variant} variant for {subagent_name}"
        
        # Verify minimum content
        content = read_file(file_path)
        lines = len(content.strip().split('\n'))
        min_lines = 40 if variant == "minimal" else 200
        assert lines > min_lines, \
            f"{subagent_name}/{variant} too short: {lines} lines (min {min_lines})"


