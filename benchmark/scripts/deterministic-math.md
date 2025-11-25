---
name: deterministic-math
version: 1.0
mode: strict
expects: none
returns: mathematical calculations
dangerous: true
---

@DETERMINISTIC

# CONSTRAINTS

- MUST output exact same values every run
- MUST NOT include timestamps or random values
- MUST use consistent formatting

# TASK

Calculate and output the following:
1. The first 10 prime numbers
2. Fibonacci sequence up to 10 terms
3. Factorials from 1! to 7!

# OUTPUT

@FORMAT:json
@PRETTY
