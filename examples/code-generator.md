---
name: code-generator
version: 1.0
mode: strict
expects: function description
returns: Python code
---

# CONSTRAINTS

- MUST output only Python code
- MUST NOT include markdown fences
- MUST NOT include explanations
- MUST include type hints
- MUST include docstring
- SHOULD follow PEP 8

# TASK

@PATTERN:generate

Generate a Python function that:
- Name: `calculate_fibonacci`
- Takes parameter `n` (int) - the position in sequence
- Returns the nth Fibonacci number
- Use iterative approach (not recursive)
- Handle edge cases (n < 0, n = 0, n = 1)

# OUTPUT

@FORMAT:code:python
