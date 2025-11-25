---
name: json-transform
version: 1.0
mode: strict
expects: JSON array of user objects
returns: JSON array with transformed fields
---

# CONTEXT

We are processing user data for an API response.

# CONSTRAINTS

- MUST output valid JSON only
- MUST NOT include markdown fences
- MUST NOT add any explanatory text
- MUST preserve array order

# TASK

@PATTERN:map

Transform the following user array:
- Rename `firstName` to `name`
- Remove `password` field
- Add `processed: true` to each object

# INPUT

```json
[
  {"firstName": "John", "email": "john@example.com", "password": "secret123"},
  {"firstName": "Jane", "email": "jane@example.com", "password": "hunter2"}
]
```

# OUTPUT

@FORMAT:json
@PRETTY
