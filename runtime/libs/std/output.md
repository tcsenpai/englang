# ENGLANG OUTPUT FORMATTING

## Format Directives

### @FORMAT:json
Output valid JSON only. No markdown fences, no explanation.

```markdown
@FORMAT:json
# Correct output:
{"name": "John", "age": 30}

# WRONG output:
```json
{"name": "John", "age": 30}
```
Here is the JSON...
```

### @FORMAT:text
Plain text, no formatting.

### @FORMAT:markdown
Markdown formatted output. Fences allowed.

### @FORMAT:code:<language>
Single code block in specified language.

```markdown
@FORMAT:code:python
# Output:
def hello():
    print("Hello, World!")
```

### @FORMAT:raw
Exactly as specified. Whitespace preserved. No interpretation.

---

## Output Modifiers

### @MINIFY
Remove unnecessary whitespace (for JSON).

```markdown
@FORMAT:json
@MINIFY
# Output: {"name":"John","age":30}
```

### @PRETTY
Indent and format for readability.

```markdown
@FORMAT:json
@PRETTY
# Output:
{
  "name": "John",
  "age": 30
}
```

### @WRAP:<width>
Wrap text at specified character width.

### @TRUNCATE:<length>
Limit output to N characters, add "..." if truncated.

---

## Output Composition

### Single Value
```markdown
# OUTPUT
@FORMAT:text
The result is a single value.
```

### Multiple Sections
```markdown
# OUTPUT
@SECTION:summary
Brief summary here.

@SECTION:details
Detailed content here.

@SECTION:metadata
@FORMAT:json
{"timestamp": "..."}
```

### Streaming (for long outputs)
```markdown
# OUTPUT
@STREAM
Output can be delivered incrementally.
```

---

## Null/Empty Handling

### Empty Result
```markdown
@ON_EMPTY:null     # Output: null
@ON_EMPTY:[]       # Output: []
@ON_EMPTY:""       # Output: (empty string)
@ON_EMPTY:error    # Output: @ERROR: empty result
```

### Missing Fields
```markdown
@ON_MISSING:null      # Include field with null
@ON_MISSING:omit      # Exclude field entirely
@ON_MISSING:error     # Fail if field cannot be determined
```

---

## Output Examples

### API Response Style
```markdown
# OUTPUT
@FORMAT:json
@PRETTY
{
  "success": true,
  "data": <result>,
  "error": null
}
```

### CLI Style
```markdown
# OUTPUT
@FORMAT:text
<result>
@EXIT:0
```

### Report Style
```markdown
# OUTPUT
@FORMAT:markdown

# Report Title

## Summary
<summary>

## Details
<details>

## Conclusion
<conclusion>
```
