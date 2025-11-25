---
name: deterministic-text
version: 1.0
mode: strict
expects: none
returns: formatted text
dangerous: true
---

@DETERMINISTIC

# CONSTRAINTS

- MUST output exact same text every run
- MUST NOT add any creative variations
- MUST NOT include greetings or filler

# TASK

Generate a haiku about programming with exactly this structure:
- Line 1: 5 syllables about code
- Line 2: 7 syllables about debugging
- Line 3: 5 syllables about success

Output the haiku as plain text with each line on its own line.

# OUTPUT

@FORMAT:text
