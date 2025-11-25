---
name: deterministic-classification
version: 1.0
mode: strict
expects: none
returns: classification results
dangerous: true
---

@DETERMINISTIC

# CONSTRAINTS

- MUST classify each item consistently
- MUST output identical JSON structure every run
- MUST NOT add explanations

# TASK

Classify these items into categories (fruit, vegetable, protein, grain):
- Apple
- Carrot
- Chicken
- Rice
- Banana
- Broccoli
- Salmon
- Wheat

# OUTPUT

@FORMAT:json
@PRETTY
