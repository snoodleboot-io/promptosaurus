---
name: strategy-workflow
description: Step-by-step process for strategy
steps:
- Read the source file(s) under test first — do not assume their shape.
- Read Core Conventions for the test framework and mock library.
- 'Identify the public interface: what inputs go in, what outputs or'
- If the code is untestable as written, say so and suggest the minimal
- HAPPY PATH — the expected inputs produce the expected output
- BOUNDARY VALUES — min, max, exactly at limit, one over limit
- EMPTY / NULL / ZERO — each nullable input absent or zeroed
- ERROR CASES — dependency throws, network fails, DB is unavailable
- CONCURRENT / ORDERING — if the function has state, test ordering
- AUTHORIZATION BOUNDARIES — does it enforce who can call it?
- ADVERSARIAL INPUTS — SQL fragments, script tags, path traversal,
- '**Check for session file:**'
- '**If no session exists:**'
- '**If session exists:**'
- '**During work:**'
- '**On mode switch:**'
---

## Steps

### Step 1: Read the source file(s) under test first — do not assume their shape.

Detailed instructions for this step.

### Step 2: Read Core Conventions for the test framework and mock library.

Detailed instructions for this step.

### Step 3: Identify the public interface: what inputs go in, what outputs or

Detailed instructions for this step.

### Step 4: If the code is untestable as written, say so and suggest the minimal

Detailed instructions for this step.

### Step 5: HAPPY PATH — the expected inputs produce the expected output

Detailed instructions for this step.

### Step 6: BOUNDARY VALUES — min, max, exactly at limit, one over limit

Detailed instructions for this step.

### Step 7: EMPTY / NULL / ZERO — each nullable input absent or zeroed

Detailed instructions for this step.

### Step 8: ERROR CASES — dependency throws, network fails, DB is unavailable

Detailed instructions for this step.

### Step 9: CONCURRENT / ORDERING — if the function has state, test ordering

Detailed instructions for this step.

### Step 10: AUTHORIZATION BOUNDARIES — does it enforce who can call it?

Detailed instructions for this step.

### Step 11: ADVERSARIAL INPUTS — SQL fragments, script tags, path traversal,

Detailed instructions for this step.

### Step 12: **Check for session file:**

Detailed instructions for this step.

### Step 13: **If no session exists:**

Detailed instructions for this step.

### Step 14: **If session exists:**

Detailed instructions for this step.

### Step 15: **During work:**

Detailed instructions for this step.

### Step 16: **On mode switch:**

Detailed instructions for this step.

