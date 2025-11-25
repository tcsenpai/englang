# ENGLANG Language Specification v2.2

## Overview

**englang** is a deterministic natural language programming DSL that uses Claude as its runtime interpreter. It bridges the gap between human-readable instructions and machine-executable programs.

## Design Philosophy

1. **Structured Natural Language**: Readable like English, executable like code
2. **Contract-Based Execution**: Clear inputs, outputs, and constraints
3. **Determinism by Default**: Same input → same output
4. **Fail-Fast on Ambiguity**: Errors, not guesses

## File Format

englang scripts are Markdown files (`.md`) with optional YAML frontmatter.

```markdown
---
name: script-name
version: 1.0
mode: strict
expects: description of expected input
returns: description of expected output
---

# CONTEXT
Background information.

# CONSTRAINTS
- MUST: required behavior
- MUST NOT: forbidden behavior

# TASK
The actual instructions to execute.

# INPUT
Data to process.

# OUTPUT
@FORMAT:json
```

## Sections

### MANIFEST (Frontmatter)

YAML metadata between `---` delimiters:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Script identifier |
| `version` | string | No | Semantic version |
| `mode` | enum | No | `strict`, `normal`, `creative` |
| `expects` | string | No | Input description |
| `returns` | string | No | Output description |
| `dangerous` | bool | No | Enable `--dangerously-skip-permissions` |
| `autosecured` | bool | No | Enable security audit mode |

### CONTEXT

Background knowledge needed for execution. NOT instructions.

```markdown
# CONTEXT
We are processing financial data for Q4 2024.
Currency amounts are in USD unless specified.
```

### CONSTRAINTS

Behavioral rules using RFC 2119 keywords:

| Keyword | Meaning | On Violation |
|---------|---------|--------------|
| MUST | Required | Error |
| MUST NOT | Forbidden | Error |
| SHOULD | Recommended | Warning |
| SHOULD NOT | Discouraged | Warning |
| MAY | Optional | - |

### TASK

The main program. What to do.

### INPUT

Data provided for processing. Can use directives:
- `@VAR:name` - Variable from `--var name=value`
- `@ENV:NAME` - Environment variable
- `@FILE:path` - File contents (future)

### OUTPUT

Format specification for results.

## Directives

### Output Format

| Directive | Description |
|-----------|-------------|
| `@FORMAT:json` | Valid JSON, no fences |
| `@FORMAT:text` | Plain text |
| `@FORMAT:markdown` | Markdown formatted |
| `@FORMAT:code:<lang>` | Code in specified language |
| `@FORMAT:raw` | Exactly as specified |

### Output Modifiers

| Directive | Description |
|-----------|-------------|
| `@PRETTY` | Formatted/indented |
| `@MINIFY` | Compressed/minimal |
| `@TRUNCATE:<n>` | Max n characters |

### Determinism

| Directive | Description |
|-----------|-------------|
| `@DETERMINISTIC` | Maximum reproducibility mode |
| `@LITERAL` | Take following text literally |
| `@VERBATIM:<text>` | Output exact text |
| `@TEMPLATE:<pattern>` | Fill placeholders only |
| `@CHOICE[a\|b\|c]` | Output must be one of these |
| `@REGEX:<pattern>` | Output must match pattern |

The `@DETERMINISTIC` directive enforces:
- No creative variations or conversational filler
- No timestamps or random values unless requested
- Canonical ordering (alphabetical/numerical) when order not specified
- Consistent formatting across runs
- Minimal interpretation of instructions
- No hedging language

### Tool Control

| Directive | Description |
|-----------|-------------|
| `@TOOLS:only[tools]` | Use ONLY listed tools |
| `@TOOLS:deny[tools]` | Do NOT use listed tools |
| `@TOOLS:prefer[tools]` | Prefer listed tools when possible |

Available tool names: bash, read, write, edit, multiedit, glob, grep, task, todowrite

### Control Flow

| Directive | Description |
|-----------|-------------|
| `@IF:<condition>` | Conditional start |
| `@ELSE` | Alternative branch |
| `@ENDIF` | Conditional end |
| `@FOREACH:<items>` | Iteration start |
| `@ENDFOR` | Iteration end |

### Error Handling

| Directive | Description |
|-----------|-------------|
| `@ON_AMBIGUITY:fail` | Error if unclear |
| `@ON_AMBIGUITY:ask` | Request clarification |
| `@ON_AMBIGUITY:best_effort` | Make assumption |
| `@ON_ERROR:stop` | Halt on error |
| `@ON_ERROR:continue` | Skip and continue |

### Patterns

| Pattern | Description |
|---------|-------------|
| `@PATTERN:transform` | 1:1 conversion |
| `@PATTERN:filter` | Select matching items |
| `@PATTERN:map` | Apply to each item |
| `@PATTERN:reduce` | Aggregate to single value |
| `@PATTERN:generate` | Create from spec |
| `@PATTERN:classify` | Categorize input |
| `@PATTERN:extract` | Pull structured data |
| `@PATTERN:validate` | Check against rules |

## Execution Modes

### strict

- Output ONLY what's specified
- NO preamble, explanation, or commentary
- Ambiguity → Error
- Maximum determinism

### normal

- Follow instructions precisely
- Minimal explanatory text allowed
- Reasonable assumptions for minor ambiguity

### creative

- Interpretation latitude
- Explanations welcome
- Best for generative tasks

## Security Modes

### Dangerous Mode

Enables `--dangerously-skip-permissions` for unattended execution.

Set via frontmatter:
```yaml
---
dangerous: true
---
```

Or CLI flag: `--dangerous`

Use only for trusted scripts in controlled environments.

### Autosecured Mode

Enables security audit protocol. Claude analyzes all sensitive operations before execution.

Set via frontmatter:
```yaml
---
autosecured: true
---
```

Or CLI flag: `--autosecured`

In this mode, before each sensitive operation Claude outputs:
```
[SECURITY AUDIT]
Operation: <description>
Risk Level: LOW | MEDIUM | HIGH | CRITICAL
Assessment: <reasoning>
Decision: PROCEED | WARN | BLOCK
```

Operations that may be blocked:
- Reading sensitive system files
- Writing to system directories
- Executing obfuscated commands
- Data exfiltration attempts
- Privilege escalation

Note: `--dangerous` and `--autosecured` are mutually exclusive.

## Include System

Reference other files with `@filename.md`:

```markdown
@std/types.md        # Standard library
@libs/custom.md      # Custom library
@ENV.md              # Runtime environment
@exec/PROMPT.md      # User script
```

Resolution order:
1. Relative to current file
2. Relative to LIBS_DIR
3. Error if not found

## Variable System

### CLI Variables

Set with `--var name=value`:

```bash
englang script.md --var name=World --var count=5
```

Use in scripts with `@VAR:name`:

```markdown
Hello, @VAR:name! Count: @VAR:count
```

### Environment Variables

Access with `@ENV:NAME`:

```markdown
Running as user: @ENV:USER
```

## Output Protocol

### Success (strict mode)

```
<raw output only>
```

### Success (normal mode)

```
<output, possibly with minimal context>
```

### Error

```
@ERROR: <error_type>
<description>
```

### Ambiguity (with @ON_AMBIGUITY:fail)

```
@AMBIGUOUS: <what is unclear>
<possible interpretations>
```

## CLI Reference

```
englang v2.2.0 - Natural Language Runtime

Usage: englang <script.md> [options]
       englang <command> [options]

Commands:
    init [name]     Create a new script template
    lint <file>     Validate script syntax without executing
    repl            Interactive REPL mode

Options:
    --debug         Show assembled prompt (no API call)
    --dry-run       Parse and validate only
    --verbose       Show execution details
    --var KEY=VAL   Set variable (repeatable)
    -o, --output    Write output to file
    --dangerous     Skip permission prompts
    --autosecured   Enable security audit mode
    --version       Show version
    --help          Show help
```

## Examples

### Hello World

```markdown
---
name: hello
mode: strict
---

# TASK
Output: "Hello, World!"
```

### JSON Transform

```markdown
---
name: transform
mode: strict
---

# TASK
@PATTERN:map
Add "processed: true" to each object.

# INPUT
[{"id": 1}, {"id": 2}]

# OUTPUT
@FORMAT:json
```

### Classification

```markdown
---
name: classify
mode: strict
---

# TASK
@PATTERN:classify
Classify the sentiment.

# INPUT
"I love this!"

# OUTPUT
@CHOICE[positive|negative|neutral]
```

## Best Practices

1. **Always use frontmatter** for non-trivial scripts
2. **Prefer strict mode** for deterministic outputs
3. **Use explicit constraints** rather than implicit assumptions
4. **Keep TASK focused** - one primary operation
5. **Test with --dry-run** before execution
6. **Use --debug** to verify assembled prompt

## CLI Commands

### init

Create a new script from template:

```bash
englang init my-script
# Creates my-script.md with boilerplate
```

### lint

Validate script syntax without executing:

```bash
englang lint script.md
# Checks: frontmatter, directives, includes, structure
```

### repl

Interactive mode for experimentation:

```bash
englang repl
# Type script, then END to execute
# Commands: :quit, :mode strict, :clear, :help
```

## Pipe Support

Inject stdin data into scripts:

```bash
echo '{"name": "John"}' | englang transform.md
# Use @STDIN in script to access piped data
```

Example script:
```markdown
# TASK
Parse the JSON and extract the name.

# INPUT
@STDIN

# OUTPUT
@FORMAT:text
```

## Output to File

Save output directly to a file:

```bash
englang script.md -o result.json
englang script.md --output report.txt
```

## Remote Includes

Include files from URLs:

```markdown
# Include from GitHub raw
@https://raw.githubusercontent.com/user/repo/main/lib.md

# Include from any URL
@https://example.com/shared-constraints.md
```

Remote includes are:
- Fetched with curl (10s timeout)
- Cached per execution (not persisted)
- Recursively expanded

## Shebang Support

Make englang scripts directly executable:

```markdown
#!/usr/bin/env englang-run
---
name: my-script
mode: strict
---

# TASK
Do something.
```

Then run directly:
```bash
chmod +x my-script.md
./my-script.md
```

**Setup**: Add englang's runtime directory to PATH:
```bash
export PATH="$PATH:/path/to/englang/runtime"
```

## Future Roadmap

- [ ] `@FILE:path` directive for file loading
- [ ] `@CALL:module.function()` for reusable functions
- [ ] `@ASSERT` post-condition validation
- [ ] Output schema validation
- [ ] Streaming output support
- [ ] Watch mode for auto-reload
