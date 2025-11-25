---
name: deterministic-counter
version: 1.0
mode: strict
expects: count (number)
returns: numbered list
---

@DETERMINISTIC
@TOOLS:deny[write,edit,bash]

# CONSTRAINTS

- MUST output exactly the specified count of items
- MUST NOT add any commentary
- MUST use consistent formatting

# TASK

Generate a numbered list from 1 to @VAR:count.
Each line format: "N. Item N"

# OUTPUT

@FORMAT:text
