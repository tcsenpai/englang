---
name: deterministic-transform
version: 1.0
mode: strict
expects: none
returns: transformed data
dangerous: true
---

@DETERMINISTIC
@PATTERN:transform

# CONSTRAINTS

- MUST apply exact same transformation every run
- MUST preserve order
- MUST output valid JSON

# TASK

Transform this data by:
1. Converting names to uppercase
2. Doubling the age
3. Adding "processed": true to each object

Input data:
[
  {"name": "alice", "age": 25},
  {"name": "bob", "age": 30},
  {"name": "charlie", "age": 35}
]

# OUTPUT

@FORMAT:json
@PRETTY
