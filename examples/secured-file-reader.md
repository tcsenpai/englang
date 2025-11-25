---
name: secured-file-reader
version: 1.0
mode: normal
autosecured: true
expects: filename via --var
returns: file contents with security audit
---

# CONTEXT

This script runs with security audit mode enabled.
All file operations will be analyzed for security implications.

# CONSTRAINTS

- MUST perform security audit before reading files
- MUST refuse to read sensitive system files
- SHOULD explain security decisions

# TASK

Read the contents of the file specified by the filename variable.
Show the security audit before displaying contents.

# INPUT

Filename: @VAR:filename

# OUTPUT

@FORMAT:text
