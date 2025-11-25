# ENGLANG TYPE SYSTEM

## Primitive Types

| Type | Description | Examples |
|------|-------------|----------|
| `string` | Text value | `"hello"`, `'world'` |
| `number` | Numeric value | `42`, `3.14`, `-1` |
| `boolean` | True/false | `true`, `false` |
| `null` | Absence of value | `null` |

## Composite Types

| Type | Description | Examples |
|------|-------------|----------|
| `array<T>` | List of type T | `[1, 2, 3]`, `["a", "b"]` |
| `object` | Key-value map | `{"key": "value"}` |
| `tuple<T1, T2, ...>` | Fixed-length typed array | `[string, number]` |

## Type Annotations

Use in EXPECTS/RETURNS:

```markdown
@EXPECTS: name (string), age (number)
@RETURNS: user (object)
```

## Type Validation

When `@FORMAT:json` is used, output MUST be valid JSON matching declared types.

```markdown
@RETURNS: result (array<string>)
@FORMAT:json

# Valid output:
["apple", "banana", "cherry"]

# Invalid output:
[1, 2, 3]  # wrong type
"apple"    # not an array
```

## Custom Type Definitions

Define with `@TYPE`:

```markdown
@TYPE:User = {
  "name": string,
  "email": string,
  "age": number,
  "active": boolean
}

@RETURNS: users (array<User>)
```

## Optional Fields

Use `?` suffix:

```markdown
@TYPE:Config = {
  "required_field": string,
  "optional_field?": number
}
```

## Union Types

Use `|` separator:

```markdown
@RETURNS: result (string | null)
@RETURNS: value (number | "error")
```
