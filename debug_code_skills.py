#!/usr/bin/env python3
"""Debug script to investigate skills filtering for the 'code' agent.

This script:
1. Loads the "code" agent from the bundled IR
2. Runs _filter_agent_for_language on it with language=None
3. Prints out agent.skills before and after filtering
4. Compares with what agent_skill_mapping.yaml says should be there
"""

from promptosaurus.prompt_builder import PromptBuilder


def main():
    print("=" * 80)
    print("DEBUG: Code Agent Skills Filtering")
    print("=" * 80)
    print()

    # Initialize PromptBuilder (tool_name doesn't matter for this test)
    builder = PromptBuilder(tool_name="kilo")

    # Load the "code" agent from registry
    print("1. Loading 'code' agent from bundled IR...")
    code_agent = builder.registry.get_agent("code")
    print(f"   Agent name: {code_agent.name}")
    print(f"   Agent description: {code_agent.description}")
    print()

    # Print original skills
    print("2. BEFORE filtering - Original agent.skills:")
    print(f"   Count: {len(code_agent.skills)}")
    for skill in code_agent.skills:
        print(f"   - {skill}")
    print()

    # Check what agent_skill_mapping.yaml says
    print("3. What agent_skill_mapping.yaml says for 'code' agent:")
    expected_skills = []
    expected_workflows = []
    if builder.agent_skill_loader:
        expected_skills = builder.agent_skill_loader.get_skills_for_agent("code")
        expected_workflows = builder.agent_skill_loader.get_workflows_for_agent("code")
        print(f"   Skills count: {len(expected_skills)}")
        for skill in expected_skills:
            print(f"   - {skill}")
        print()
        print(f"   Workflows count: {len(expected_workflows)}")
        for workflow in expected_workflows:
            print(f"   - {workflow}")
    else:
        print("   ERROR: agent_skill_loader not initialized!")
    print()

    # Filter with language=None
    print("4. Running _filter_agent_for_language(agent, language=None)...")
    filtered_agent = builder._filter_agent_for_language(code_agent, language=None)
    print()

    # Print filtered skills
    print("5. AFTER filtering - Filtered agent.skills:")
    print(f"   Count: {len(filtered_agent.skills)}")
    for skill in filtered_agent.skills:
        print(f"   - {skill}")
    print()

    # Print filtered workflows
    print("6. AFTER filtering - Filtered agent.workflows:")
    print(f"   Count: {len(filtered_agent.workflows)}")
    for workflow in filtered_agent.workflows:
        print(f"   - {workflow}")
    print()

    # Compare original vs filtered
    print("7. Comparison:")
    original_skills_set = set(code_agent.skills)
    filtered_skills_set = set(filtered_agent.skills)
    expected_skills_set = set(expected_skills)

    print(f"   Original skills: {len(original_skills_set)}")
    print(f"   Filtered skills: {len(filtered_skills_set)}")
    print(f"   Expected skills (from YAML): {len(expected_skills_set)}")
    print()

    # Skills only in original
    only_in_original = original_skills_set - filtered_skills_set
    if only_in_original:
        print("   Skills REMOVED by filtering:")
        for skill in sorted(only_in_original):
            print(f"   - {skill}")
        print()

    # Skills only in filtered
    only_in_filtered = filtered_skills_set - original_skills_set
    if only_in_filtered:
        print("   Skills ADDED by filtering:")
        for skill in sorted(only_in_filtered):
            print(f"   - {skill}")
        print()

    # Skills in filtered but not in expected YAML
    unexpected_skills = filtered_skills_set - expected_skills_set
    if unexpected_skills:
        print("   Skills in filtered but NOT in agent_skill_mapping.yaml:")
        for skill in sorted(unexpected_skills):
            print(f"   - {skill}")
        print()

    # Check for ML-related skills
    print("8. ML-related skills analysis:")
    ml_keywords = [
        "ml",
        "machine",
        "learning",
        "model",
        "feature-store",
        "data-versioning",
        "hyperparameter",
        "ensemble",
    ]

    print("   In ORIGINAL agent:")
    ml_in_original = [s for s in code_agent.skills if any(kw in s.lower() for kw in ml_keywords)]
    if ml_in_original:
        for skill in ml_in_original:
            print(f"   - {skill}")
    else:
        print("   - None found")
    print()

    print("   In FILTERED agent:")
    ml_in_filtered = [
        s for s in filtered_agent.skills if any(kw in s.lower() for kw in ml_keywords)
    ]
    if ml_in_filtered:
        for skill in ml_in_filtered:
            print(f"   - {skill}")
    else:
        print("   - None found")
    print()

    print("   In YAML specification:")
    ml_in_yaml = [s for s in expected_skills if any(kw in s.lower() for kw in ml_keywords)]
    if ml_in_yaml:
        for skill in ml_in_yaml:
            print(f"   - {skill}")
    else:
        print("   - None found")
    print()

    print("=" * 80)
    print("DEBUG COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
