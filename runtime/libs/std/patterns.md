# ENGLANG EXECUTION PATTERNS

## Pattern: Transform

Convert input from one form to another.

```markdown
@PATTERN:transform

# INPUT
<source data>

# TASK
Transform the input by <transformation rules>.

# OUTPUT
<transformed data>
```

**Characteristics:**
- 1:1 mapping (one input → one output)
- Deterministic (same input → same output)
- No side effects

---

## Pattern: Filter

Select items matching criteria.

```markdown
@PATTERN:filter

# INPUT
<collection>

# TASK
Select items where <condition>.

# OUTPUT
<filtered collection>
```

**Characteristics:**
- Many:fewer mapping
- Preserves item structure
- Order preserved unless specified

---

## Pattern: Map

Apply operation to each item.

```markdown
@PATTERN:map

# INPUT
<collection>

# TASK
For each item, <operation>.

# OUTPUT
<mapped collection>
```

**Characteristics:**
- Many:many mapping (same count)
- Each item transformed independently
- Order preserved

---

## Pattern: Reduce

Aggregate collection to single value.

```markdown
@PATTERN:reduce

# INPUT
<collection>

# TASK
Combine all items by <aggregation rule>.
Starting value: <initial>

# OUTPUT
<single value>
```

**Characteristics:**
- Many:1 mapping
- Sequential processing
- Accumulator pattern

---

## Pattern: Generate

Create output from specification.

```markdown
@PATTERN:generate

# CONTEXT
<background knowledge>

# TASK
Generate <thing> with these characteristics:
- <requirement 1>
- <requirement 2>

# OUTPUT
<generated content>
```

**Characteristics:**
- 0/spec:1 mapping
- Creative latitude (unless strict mode)
- May vary between runs

---

## Pattern: Classify

Categorize input into predefined classes.

```markdown
@PATTERN:classify

# INPUT
<item to classify>

# TASK
Classify into one of: @CHOICE[category1|category2|category3]

# OUTPUT
<category>
```

**Characteristics:**
- 1:1 mapping to category
- Deterministic with same criteria
- Output constrained to choices

---

## Pattern: Extract

Pull specific information from unstructured input.

```markdown
@PATTERN:extract

# INPUT
<unstructured content>

# TASK
Extract:
- field1: <what to extract>
- field2: <what to extract>

# OUTPUT
@FORMAT:json
```

**Characteristics:**
- Unstructured → Structured
- Field-based output
- Null for missing fields

---

## Pattern: Validate

Check input against rules.

```markdown
@PATTERN:validate

# INPUT
<data to validate>

# TASK
Validate against:
- Rule 1: <condition>
- Rule 2: <condition>

# OUTPUT
@FORMAT:json
{
  "valid": boolean,
  "errors": array<string>
}
```

**Characteristics:**
- 1:1 mapping to validation result
- All rules checked
- Errors collected

---

## Pattern: Branch

Conditional execution paths.

```markdown
@PATTERN:branch

# INPUT
<data>

# TASK
@IF:<condition1>
  <action1>
@ELSE
  @IF:<condition2>
    <action2>
  @ELSE
    <default action>
  @ENDIF
@ENDIF
```

**Characteristics:**
- Multiple execution paths
- Only one path executed
- Deterministic given same input
