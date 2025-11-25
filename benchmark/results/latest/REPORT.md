# englang Determinism Benchmark Report

**Generated:** 2025-11-25 15:53:50
**Benchmark Run:** 20251125_155022
**Iterations per script:** 3

## Overall Summary

| Metric | Value |
|--------|-------|
| Scripts Tested | 4 |
| Fully Deterministic | 1 |
| Overall Score | 25.0% |

## Determinism Score by Script

```
deterministic-classification   [###################-----------] 66.0%
deterministic-math             [##############################] 100.0%
deterministic-text             [#########---------------------] 33.0%
deterministic-transform        [###################-----------] 66.0%
```

## Detailed Results

### deterministic-classification [FAIL]

| Metric | Value |
|--------|-------|
| Status | NON-DETERMINISTIC |
| Determinism Score | 66.0% |
| Iterations | 3 |
| Matching Outputs | 2 |
| Unique Outputs | 2 |
| Avg Execution Time | 14.338s |

### deterministic-math [PASS]

| Metric | Value |
|--------|-------|
| Status | DETERMINISTIC |
| Determinism Score | 100.0% |
| Iterations | 3 |
| Matching Outputs | 3 |
| Unique Outputs | 1 |
| Avg Execution Time | 15.353s |

### deterministic-text [FAIL]

| Metric | Value |
|--------|-------|
| Status | NON-DETERMINISTIC |
| Determinism Score | 33.0% |
| Iterations | 3 |
| Matching Outputs | 1 |
| Unique Outputs | 3 |
| Avg Execution Time | 13.325s |

### deterministic-transform [FAIL]

| Metric | Value |
|--------|-------|
| Status | NON-DETERMINISTIC |
| Determinism Score | 66.0% |
| Iterations | 3 |
| Matching Outputs | 2 |
| Unique Outputs | 2 |
| Avg Execution Time | 13.379s |

## Performance Summary

```
Script                             Avg Time          Status
------------------------------------------------------------
deterministic-classification        14.338s NON-DETERMINISTIC
deterministic-math                  15.353s   DETERMINISTIC
deterministic-text                  13.325s NON-DETERMINISTIC
deterministic-transform             13.379s NON-DETERMINISTIC
```

## Methodology

Each script was executed multiple times with identical inputs.
Outputs were hashed (SHA-256) and compared to measure consistency.

- **Determinism Score**: Percentage of runs matching the first run
- **Unique Outputs**: Number of distinct outputs across all runs
- **DETERMINISTIC**: 100% of runs produced identical output

## Visualization

![Benchmark Results](benchmark_plot.png)
