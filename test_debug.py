from pathlib import Path
from promptosaurus.prompt_builder import PromptBuilder

builder = PromptBuilder("kilo-ide")
all_agents = builder.registry.get_all_agents()

# Find maintenance agent
maint = all_agents.get("orchestrator/maintenance")
if maint:
    print(f"✓ Found orchestrator/maintenance")
    print(f"  - Name: {maint.name}")
    print(f"  - Workflows: {maint.workflows}")
    print(f"  - Type of workflows: {type(maint.workflows)}")
else:
    print("✗ orchestrator/maintenance not found")

# Show all agents with orchestrator/
print("\nAll orchestrator agents:")
for name, agent in all_agents.items():
    if "orchestrator" in name:
        print(f"  {name}: {len(agent.workflows)} workflows")
