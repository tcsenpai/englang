# englang Determinism Benchmark

This benchmark suite measures how deterministic englang scripts are across multiple executions.

## Quick Start

```bash
# Run benchmark with 5 iterations (default)
./run-benchmark.sh

# Run with custom iteration count
./run-benchmark.sh 10

# Generate report and plots
./generate-report.py
```

## Structure

```
benchmark/
├── scripts/           # Test scripts to benchmark
│   ├── deterministic-math.md
│   ├── deterministic-text.md
│   ├── deterministic-classification.md
│   └── deterministic-transform.md
├── results/           # Benchmark results (timestamped)
│   └── run_YYYYMMDD_HHMMSS/
│       ├── results.json
│       ├── REPORT.md
│       ├── benchmark_plot.png
│       └── <script_name>/
│           ├── output_1.txt
│           ├── output_2.txt
│           └── ...
├── run-benchmark.sh   # Main benchmark runner
├── generate-report.py # Report/plot generator
└── README.md
```

## What It Measures

- **Determinism Score**: Percentage of runs producing identical output
- **Unique Outputs**: Number of distinct outputs across runs
- **Execution Time**: Average time per script execution
- **Consistency**: SHA-256 hash comparison of outputs

## Test Scripts

| Script | Purpose |
|--------|---------|
| deterministic-math | Pure computation (primes, fibonacci, factorials) |
| deterministic-text | Creative text generation (haiku) |
| deterministic-classification | Category assignment |
| deterministic-transform | Data transformation |

## Interpreting Results

- **100% Score**: Script is fully deterministic
- **< 100% Score**: Some variation in outputs (may be acceptable for creative tasks)
- **Unique Outputs = 1**: All runs identical
- **Unique Outputs > 1**: Variation detected

## Requirements

- bash, bc, python3
- Optional: matplotlib (`pip install matplotlib`) for graphical plots

## Adding New Benchmark Scripts

1. Create a new `.md` file in `scripts/`
2. Use `@DETERMINISTIC` directive for maximum reproducibility
3. Use `mode: strict` in frontmatter
4. Add `dangerous: true` for unattended execution
