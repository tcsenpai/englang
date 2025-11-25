---
name: dangerous-batch
version: 1.0
mode: strict
dangerous: true
expects: nothing
returns: file listing
---

# CONTEXT

This script runs with --dangerously-skip-permissions enabled.
It will execute without prompting for confirmation.

# CONSTRAINTS

- MUST list files in the current directory
- MUST NOT delete or modify any files
- SHOULD complete quickly

# TASK

List all files in the current working directory and show their sizes.
Output as a simple text list.

# OUTPUT

@FORMAT:text
