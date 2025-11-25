---
name: sentiment-classifier
version: 1.0
mode: strict
expects: text to classify
returns: sentiment category
---

# CONSTRAINTS

- MUST output exactly one of the allowed choices
- MUST NOT add explanation
- MUST NOT hedge or qualify

# TASK

@PATTERN:classify

Classify the sentiment of the following text.

# INPUT

"I absolutely love this product! It exceeded all my expectations and I would recommend it to everyone."

# OUTPUT

@CHOICE[positive|negative|neutral]
