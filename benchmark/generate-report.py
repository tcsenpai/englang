#!/usr/bin/env python3
"""
englang Benchmark Report Generator
Generates plots and markdown report from benchmark results
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def load_results(results_dir):
    """Load benchmark results from JSON file"""
    results_file = Path(results_dir) / "results.json"
    if not results_file.exists():
        print(f"Error: {results_file} not found")
        sys.exit(1)

    with open(results_file) as f:
        return json.load(f)

def generate_ascii_bar(value, max_value=100, width=30):
    """Generate ASCII bar chart"""
    filled = int((value / max_value) * width)
    empty = width - filled
    return f"[{'#' * filled}{'-' * empty}] {value:.1f}%"

def generate_report(results_dir, results):
    """Generate markdown report"""
    report_lines = []

    # Header
    report_lines.append("# englang Determinism Benchmark Report")
    report_lines.append("")
    report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"**Benchmark Run:** {results['benchmark_info']['timestamp']}")
    report_lines.append(f"**Iterations per script:** {results['benchmark_info']['iterations']}")
    report_lines.append("")

    # Overall Summary
    overall = results.get("overall", {})
    report_lines.append("## Overall Summary")
    report_lines.append("")
    report_lines.append(f"| Metric | Value |")
    report_lines.append(f"|--------|-------|")
    report_lines.append(f"| Scripts Tested | {overall.get('total_scripts', 0)} |")
    report_lines.append(f"| Fully Deterministic | {overall.get('deterministic_scripts', 0)} |")
    report_lines.append(f"| Overall Score | {overall.get('overall_score', 0):.1f}% |")
    report_lines.append("")

    # Visual Summary (ASCII)
    report_lines.append("## Determinism Score by Script")
    report_lines.append("")
    report_lines.append("```")
    for script_name, script_data in results.get("scripts", {}).items():
        score = script_data.get("determinism_score", 0)
        bar = generate_ascii_bar(score)
        report_lines.append(f"{script_name:30} {bar}")
    report_lines.append("```")
    report_lines.append("")

    # Detailed Results
    report_lines.append("## Detailed Results")
    report_lines.append("")

    for script_name, script_data in results.get("scripts", {}).items():
        status_emoji = "PASS" if script_data.get("status") == "DETERMINISTIC" else "FAIL"
        report_lines.append(f"### {script_name} [{status_emoji}]")
        report_lines.append("")
        report_lines.append(f"| Metric | Value |")
        report_lines.append(f"|--------|-------|")
        report_lines.append(f"| Status | {script_data.get('status', 'N/A')} |")
        report_lines.append(f"| Determinism Score | {script_data.get('determinism_score', 0):.1f}% |")
        report_lines.append(f"| Iterations | {script_data.get('iterations', 0)} |")
        report_lines.append(f"| Matching Outputs | {script_data.get('match_count', 0)} |")
        report_lines.append(f"| Unique Outputs | {script_data.get('unique_outputs', 0)} |")
        report_lines.append(f"| Avg Execution Time | {script_data.get('avg_time_seconds', 0):.3f}s |")
        report_lines.append("")

    # Performance Summary
    report_lines.append("## Performance Summary")
    report_lines.append("")
    report_lines.append("```")
    report_lines.append(f"{'Script':<30} {'Avg Time':>12} {'Status':>15}")
    report_lines.append("-" * 60)
    for script_name, script_data in results.get("scripts", {}).items():
        avg_time = f"{script_data.get('avg_time_seconds', 0):.3f}s"
        status = script_data.get("status", "N/A")
        report_lines.append(f"{script_name:<30} {avg_time:>12} {status:>15}")
    report_lines.append("```")
    report_lines.append("")

    # Methodology
    report_lines.append("## Methodology")
    report_lines.append("")
    report_lines.append("Each script was executed multiple times with identical inputs.")
    report_lines.append("Outputs were hashed (SHA-256) and compared to measure consistency.")
    report_lines.append("")
    report_lines.append("- **Determinism Score**: Percentage of runs matching the first run")
    report_lines.append("- **Unique Outputs**: Number of distinct outputs across all runs")
    report_lines.append("- **DETERMINISTIC**: 100% of runs produced identical output")
    report_lines.append("")

    return "\n".join(report_lines)

def generate_plot(results_dir, results):
    """Generate ASCII plot and optionally matplotlib plot"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np

        scripts = list(results.get("scripts", {}).keys())
        scores = [results["scripts"][s].get("determinism_score", 0) for s in scripts]
        times = [results["scripts"][s].get("avg_time_seconds", 0) for s in scripts]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Determinism Score Bar Chart
        colors = ['#2ecc71' if s == 100 else '#e74c3c' for s in scores]
        bars = ax1.barh(scripts, scores, color=colors)
        ax1.set_xlabel('Determinism Score (%)')
        ax1.set_title('Determinism Score by Script')
        ax1.set_xlim(0, 105)
        ax1.axvline(x=100, color='green', linestyle='--', alpha=0.5, label='Target (100%)')

        # Add value labels
        for bar, score in zip(bars, scores):
            ax1.text(score + 1, bar.get_y() + bar.get_height()/2,
                    f'{score:.0f}%', va='center', fontsize=9)

        # Execution Time Bar Chart
        ax2.barh(scripts, times, color='#3498db')
        ax2.set_xlabel('Average Execution Time (seconds)')
        ax2.set_title('Execution Time by Script')

        # Add value labels
        for i, (script, time) in enumerate(zip(scripts, times)):
            ax2.text(time + 0.1, i, f'{time:.2f}s', va='center', fontsize=9)

        plt.tight_layout()

        plot_path = Path(results_dir) / "benchmark_plot.png"
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to: {plot_path}")

        return str(plot_path)

    except ImportError:
        print("matplotlib not available, skipping graphical plot")
        print("Install with: pip install matplotlib")
        return None

def main():
    if len(sys.argv) < 2:
        # Default to latest results
        results_dir = Path(__file__).parent / "results" / "latest"
        if not results_dir.exists():
            print("Usage: generate-report.py <results_dir>")
            print("No benchmark results found. Run ./run-benchmark.sh first.")
            sys.exit(1)
    else:
        results_dir = sys.argv[1]

    print(f"Loading results from: {results_dir}")
    results = load_results(results_dir)

    # Generate report
    report = generate_report(results_dir, results)
    report_path = Path(results_dir) / "REPORT.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Report saved to: {report_path}")

    # Generate plot
    plot_path = generate_plot(results_dir, results)

    # Print summary
    print("")
    print("=" * 50)
    print("BENCHMARK SUMMARY")
    print("=" * 50)
    overall = results.get("overall", {})
    print(f"Total scripts: {overall.get('total_scripts', 0)}")
    print(f"Deterministic: {overall.get('deterministic_scripts', 0)}")
    print(f"Overall score: {overall.get('overall_score', 0):.1f}%")

    if plot_path:
        # Add plot reference to report
        with open(report_path, "a") as f:
            f.write("\n## Visualization\n\n")
            f.write(f"![Benchmark Results](benchmark_plot.png)\n")

if __name__ == "__main__":
    main()
