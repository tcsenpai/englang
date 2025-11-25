---
name: entity-extractor
version: 1.0
mode: strict
expects: unstructured text
returns: structured JSON with extracted entities
---

# CONTEXT

Named Entity Recognition (NER) for business documents.

# CONSTRAINTS

- MUST output valid JSON only
- MUST NOT include markdown fences
- MUST use null for fields not found in text
- MUST NOT hallucinate entities not present

# TASK

@PATTERN:extract

Extract the following entities from the text:
- `people`: array of person names
- `organizations`: array of company/org names
- `locations`: array of place names
- `dates`: array of dates mentioned
- `money`: array of monetary amounts

# INPUT

"On January 15, 2024, Acme Corporation announced that CEO John Smith
would be opening a new facility in Austin, Texas. The $50 million
investment was praised by Mayor Jane Doe and representatives from
the Austin Chamber of Commerce."

# OUTPUT

@FORMAT:json
@PRETTY
