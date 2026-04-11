"""Unit tests for Incident Agent."""

import pytest


@pytest.mark.unit
class TestIncidentAgent:
    """Test suite for incident agent."""
    
    @pytest.fixture
    def agent_file(self, agents_dir):
        """Get incident agent file."""
        return agents_dir / "incident" / "prompt.md"
    
    @pytest.fixture
    def agent_content(self, agent_file, read_file):
        """Read agent file content."""
        assert agent_file.exists(), f"Agent file not found: {agent_file}"
        return read_file(agent_file)
    
    def test_agent_exists(self, agent_file):
        """Test that agent file exists."""
        assert agent_file.exists(), "incident/prompt.md not found"
    
    def test_agent_has_purpose(self, agent_content):
        """Test that agent has purpose section."""
        assert "Purpose" in agent_content or "purpose" in agent_content.lower()
    
    def test_agent_has_all_subagents(self, agent_content):
        """Test that agent references all subagents."""
        expected = ["triage", "postmortem", "runbook", "oncall"]
        for subagent in expected:
            assert subagent.lower() in agent_content.lower(), \
                f"Agent missing reference to {subagent} subagent"


