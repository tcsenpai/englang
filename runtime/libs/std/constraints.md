# ENGLANG CONSTRAINT SYSTEM

## Constraint Keywords

Constraints define behavioral rules using RFC 2119 keywords:

| Keyword | Meaning | Violation |
|---------|---------|-----------|
| **MUST** | Absolute requirement | @ERROR |
| **MUST NOT** | Absolute prohibition | @ERROR |
| **SHOULD** | Recommended | Warning, continue |
| **SHOULD NOT** | Discouraged | Warning, continue |
| **MAY** | Optional | No effect if omitted |

---

## Constraint Categories

### Content Constraints
Control WHAT is produced.

```markdown
# CONSTRAINTS
- MUST include all required fields
- MUST NOT include sensitive data (passwords, keys)
- SHOULD use consistent naming conventions
- MAY include optional metadata
```

### Format Constraints
Control HOW output is structured.

```markdown
# CONSTRAINTS
- MUST be valid JSON
- MUST NOT exceed 1000 characters
- SHOULD be minified
- MAY include comments (if format allows)
```

### Behavioral Constraints
Control execution behavior.

```markdown
# CONSTRAINTS
- MUST complete in single pass
- MUST NOT make assumptions about missing data
- SHOULD prefer explicit over implicit
- MAY cache intermediate results
```

### Safety Constraints
Prevent harmful outputs.

```markdown
# CONSTRAINTS
- MUST NOT generate executable code without @ALLOW:code
- MUST NOT include PII unless explicitly provided
- MUST NOT make external requests
- SHOULD sanitize all outputs
```

---

## Predefined Constraint Sets

### @CONSTRAINTS:strict
```markdown
- MUST produce exact output format
- MUST NOT add explanatory text
- MUST NOT interpret ambiguously
- MUST fail on unclear input
```

### @CONSTRAINTS:safe
```markdown
- MUST NOT generate harmful content
- MUST NOT include credentials
- MUST NOT produce executable exploits
- SHOULD sanitize inputs
```

### @CONSTRAINTS:deterministic
```markdown
- MUST produce identical output for identical input
- MUST NOT use random/time-based values
- MUST NOT reference external state
- SHOULD be reproducible
```

### @CONSTRAINTS:minimal
```markdown
- MUST use minimum necessary output
- MUST NOT add unnecessary fields
- SHOULD omit null/empty values
- SHOULD prefer brevity
```

---

## Constraint Composition

Combine multiple constraint sets:

```markdown
# CONSTRAINTS
@CONSTRAINTS:strict
@CONSTRAINTS:safe

# Additional constraints:
- MUST include timestamp field
- MUST NOT exceed 500 tokens
```

---

## Constraint Validation

### Pre-execution Validation
Check constraints BEFORE executing:

```markdown
@VALIDATE:pre
- Input must contain 'data' field
- Input must be valid JSON
```

### Post-execution Validation
Check constraints AFTER executing:

```markdown
@VALIDATE:post
- Output must match schema
- Output must contain required fields
```

---

## Constraint Errors

When MUST/MUST NOT violated:

```
@ERROR: constraint_violation
Constraint: MUST include 'id' field
Actual: 'id' field missing from output
```

When SHOULD/SHOULD NOT violated:

```
@WARNING: constraint_advisory
Constraint: SHOULD use camelCase
Actual: snake_case used for 'user_name'
(execution continued)
```

---

## Dynamic Constraints

Constraints based on input:

```markdown
# CONSTRAINTS
@IF:input.strict == true
  - MUST follow strict formatting
@ELSE
  - MAY use flexible formatting
@ENDIF
```

---

## Constraint Inheritance

Child scripts inherit parent constraints:

```markdown
# In parent.md
# CONSTRAINTS
- MUST be valid JSON

# In child.md
@USE:parent.md
# CONSTRAINTS (additional)
- MUST include 'version' field

# Effective constraints:
# - MUST be valid JSON (inherited)
# - MUST include 'version' field (local)
```
