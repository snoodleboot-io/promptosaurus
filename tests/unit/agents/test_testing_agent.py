"""Unit tests for Testing Agent."""

import pytest


@pytest.mark.unit
class TestTestingAgent:
    """Test suite for testing agent."""

    @pytest.fixture
    def agent_file(self, agents_dir):
        """Get testing agent file."""
        return agents_dir / "testing" / "prompt.md"

    def test_agent_exists(self, agent_file):
        """Test that agent file exists."""
        assert agent_file.exists(), "testing/prompt.md not found"


@pytest.mark.unit
class TestTestingAgentSubagents:
    """Test suite for testing agent subagents."""

    @pytest.fixture
    def subagents_dir(self, agents_dir):
        """Get testing subagents directory."""
        return agents_dir / "testing" / "subagents"

    @pytest.mark.parametrize(
        "subagent_name", ["unit-testing", "integration-testing", "e2e-testing", "load-testing"]
    )
    def test_subagent_exists(self, subagents_dir, subagent_name):
        """Test that subagent exists."""
        subagent_dir = subagents_dir / subagent_name
        assert subagent_dir.exists(), f"Subagent dir not found: {subagent_name}"
