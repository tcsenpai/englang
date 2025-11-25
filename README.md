# englang

A deterministic natural language programming DSL that uses Claude as its runtime interpreter.

englang lets you write executable programs in structured English. Instead of traditional code, you write markdown files with clear sections, constraints, and directives that Claude executes predictably.

## Quick Start

```bash
# Run a script
./runtime/englang examples/hello.md --var name=World

# Create a new script
./runtime/englang init my-script

# Validate syntax
./runtime/englang lint my-script.md

# Interactive mode
./runtime/englang repl
```

## Installation

1. Clone the repository
2. Ensure `claude` CLI is available in PATH
3. Make the runtime executable: `chmod +x runtime/englang`
4. (Optional) Add to PATH for shebang support: `export PATH="$PATH:/path/to/englang/runtime"`

## Writing Scripts

englang scripts are markdown files with optional YAML frontmatter:

```markdown
---
name: greet
version: 1.0
mode: strict
expects: name (string)
returns: greeting (string)
---

# CONSTRAINTS

- MUST output only the greeting
- MUST NOT add explanations

# TASK

Output: "Hello, @VAR:name!"
```

Run it:

```bash
./runtime/englang greet.md --var name=World
# Output: Hello, World!
```

## Script Structure

### Frontmatter (Optional)

```yaml
---
name: script-name
version: 1.0
mode: strict | normal | creative
expects: description of input
returns: description of output
---
```

### Sections

| Section | Purpose |
|---------|---------|
| `# CONTEXT` | Background information (not instructions) |
| `# CONSTRAINTS` | Behavioral rules (MUST, MUST NOT, SHOULD, MAY) |
| `# TASK` | The actual program to execute |
| `# INPUT` | Data to process |
| `# OUTPUT` | Format specification |

## Execution Modes

| Mode | Behavior |
|------|----------|
| `strict` | Output only what's specified, error on ambiguity |
| `normal` | Follow instructions precisely, minimal clarification allowed |
| `creative` | Interpretation latitude, explanations welcome |

## Directives

### Output Format

```markdown
@FORMAT:json      # Valid JSON only
@FORMAT:text      # Plain text
@FORMAT:markdown  # Markdown formatted
@FORMAT:code:python  # Code block
@PRETTY           # Indented/formatted
@MINIFY           # Compressed
```

### Determinism

```markdown
@DETERMINISTIC    # Maximum reproducibility mode
@CHOICE[a|b|c]    # Output must be one of these
@LITERAL          # Take following text literally
@TEMPLATE:{var}   # Fill placeholders only
```

The `@DETERMINISTIC` directive enforces:
- No creative variations or conversational filler
- No timestamps or random values
- Canonical ordering (alphabetical/numerical)
- Consistent formatting across runs
- Minimal interpretation of instructions

### Tool Control

```markdown
@TOOLS:only[read,grep]     # Use ONLY these tools
@TOOLS:deny[write,edit]    # Do NOT use these tools
@TOOLS:prefer[bash]        # Prefer these when possible
```

Available tools: bash, read, write, edit, multiedit, glob, grep, task

### Patterns

```markdown
@PATTERN:transform  # 1:1 conversion
@PATTERN:filter     # Select matching items
@PATTERN:map        # Apply to each item
@PATTERN:classify   # Categorize input
@PATTERN:extract    # Pull structured data
```

## Variables

### CLI Variables

```bash
./runtime/englang script.md --var name=John --var count=5
```

Use in scripts:

```markdown
Hello, @VAR:name! Count: @VAR:count
```

### Environment Variables

```markdown
Current user: @ENV:USER
```

### Stdin

```bash
echo '{"data": 1}' | ./runtime/englang script.md
```

Use in scripts:

```markdown
# INPUT
@STDIN
```

## Includes

### Local Files

```markdown
@libs/helpers.md
@shared/constraints.md
```

### Remote URLs

```markdown
@https://raw.githubusercontent.com/user/repo/main/lib.md
```

## Security Modes

### Dangerous Mode

Skip all permission prompts for unattended/batch execution:

```bash
# Via CLI flag
./runtime/englang script.md --dangerous

# Via frontmatter
---
name: batch-job
dangerous: true
---
```

Warning: This runs Claude with `--dangerously-skip-permissions`. Use only for trusted scripts in controlled environments.

### Autosecured Mode

Enable security audit mode that analyzes operations before execution:

```bash
# Via CLI flag
./runtime/englang script.md --autosecured

# Via frontmatter
---
name: secure-script
autosecured: true
---
```

In this mode, Claude will:
- Analyze each file/command operation for security implications
- Report risk levels (LOW/MEDIUM/HIGH/CRITICAL)
- Refuse operations that appear malicious
- Warn about sensitive file access
- Block data exfiltration attempts

Example audit output:
```
[SECURITY AUDIT]
Operation: Read file /etc/passwd
Risk Level: HIGH
Assessment: System file containing user account information
Decision: BLOCK - Sensitive system file
```

Note: `--dangerous` and `--autosecured` are mutually exclusive.

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
    --dry-run       Parse and validate without executing
    --verbose       Show execution details
    --var KEY=VAL   Set variable (can be repeated)
    -o, --output    Write output to file
    --dangerous     Skip permission prompts (use with caution!)
    --autosecured   Enable security audit mode
    --version       Show version
    --help          Show help
```

## Examples

### JSON Transformation

```markdown
---
name: transform
mode: strict
---

# CONSTRAINTS
- MUST output valid JSON only
- MUST NOT include markdown fences

# TASK
@PATTERN:map
Add "processed": true to each object.

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
"I love this product!"

# OUTPUT
@CHOICE[positive|negative|neutral]
```

### Code Generation

```markdown
---
name: codegen
mode: strict
---

# CONSTRAINTS
- MUST output only Python code
- MUST include type hints
- MUST include docstring

# TASK
@PATTERN:generate
Generate a function that calculates factorial.

# OUTPUT
@FORMAT:code:python
```

## Shebang Support

Make scripts directly executable:

```markdown
#!/usr/bin/env englang-run
---
name: my-script
mode: strict
---

# TASK
Output: "Hello from executable script!"
```

```bash
chmod +x my-script.md
./my-script.md
```

## Benchmarks

We include a determinism benchmark suite to measure output consistency across multiple runs.

```bash
./benchmark/run-benchmark.sh 5    # Run each script 5 times
```

### Results (5 iterations)

![Benchmark Results](benchmark/results/latest/benchmark_plot.png)

| Script | Score | Unique Outputs | Notes |
|--------|-------|----------------|-------|
| deterministic-math | 100% | 1 | Pure computation is fully deterministic |
| deterministic-classification | 25% | 2 | Category assignment shows variance |
| deterministic-transform | 0% | 2 | Data transformation inconsistent |
| deterministic-text | 0% | 5 | Creative text (haiku) never repeats |

**Key insight**: LLMs are inherently non-deterministic. The `@DETERMINISTIC` directive helps with structured/computational tasks (math achieved 100%) but cannot guarantee consistency for creative or interpretive outputs. For maximum reliability, prefer constrained outputs (`@CHOICE`, `@FORMAT:json`) over open-ended generation.

See [benchmark/README.md](benchmark/README.md) for details.

## Project Structure

```
englang/
├── runtime/
│   ├── englang           # Main CLI
│   ├── englang-run       # Shebang wrapper
│   └── libs/
│       ├── MAIN.md       # Runtime core
│       └── std/          # Standard library
│           ├── types.md
│           ├── patterns.md
│           ├── output.md
│           └── constraints.md
├── examples/             # Example scripts
├── benchmark/            # Determinism benchmarks
└── docs/
    └── SPECIFICATION.md  # Full language spec
```

## How It Works

1. **Preprocessing** (bash): Resolves includes, injects variables, captures stdin
2. **Assembly**: Combines runtime core + stdlib + user script into single prompt
3. **Execution**: Sends assembled prompt to Claude with "execute" command
4. **Cleanup**: Removes temporary files

The key insight is separating concerns: bash handles file I/O and preprocessing, Claude handles natural language understanding and execution.

## License

MIT
