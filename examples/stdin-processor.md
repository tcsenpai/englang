---
name: stdin-processor
version: 1.0
mode: strict
expects: JSON via stdin
returns: processed JSON
---

# CONTEXT

We receive JSON data via stdin pipe and process it.

# CONSTRAINTS

- MUST output valid JSON only
- MUST NOT include any markdown or explanation
- MUST preserve all original fields
- MUST add "processed": true to the output

# TASK

@PATTERN:transform

Take the input JSON and add a "processed" field set to true.

# INPUT

@STDIN

# OUTPUT

@FORMAT:json
@PRETTY
