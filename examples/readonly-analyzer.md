---
name: readonly-analyzer
version: 1.0
mode: strict
expects: filename via --var
returns: file analysis
---

@DETERMINISTIC
@TOOLS:only[read,grep,glob]

# CONTEXT

This script analyzes files using only read-only operations.
It cannot modify any files.

# CONSTRAINTS

- MUST NOT modify any files
- MUST use only read, grep, and glob tools
- MUST output structured analysis

# TASK

Analyze the file specified by filename:
1. Read the file contents
2. Count the number of lines
3. Identify the file type based on extension
4. List any TODO comments found

# INPUT

Filename: @VAR:filename

# OUTPUT

@FORMAT:json
