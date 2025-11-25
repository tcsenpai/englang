#!/bin/bash
# englang Determinism Benchmark Runner
# Runs scripts multiple times and measures output consistency

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENGLANG="$SCRIPT_DIR/../runtime/englang"
SCRIPTS_DIR="$SCRIPT_DIR/scripts"
RESULTS_DIR="$SCRIPT_DIR/results"
ITERATIONS=${1:-5}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RUN_DIR="$RESULTS_DIR/run_$TIMESTAMP"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================"
echo "englang Determinism Benchmark"
echo "========================================"
echo "Iterations per script: $ITERATIONS"
echo "Results directory: $RUN_DIR"
echo ""

mkdir -p "$RUN_DIR"

# Initialize results JSON
RESULTS_JSON="$RUN_DIR/results.json"
echo '{"benchmark_info": {"timestamp": "'$TIMESTAMP'", "iterations": '$ITERATIONS'}, "scripts": {}}' > "$RESULTS_JSON"

# Track overall stats
TOTAL_SCRIPTS=0
TOTAL_DETERMINISTIC=0

for script in "$SCRIPTS_DIR"/*.md; do
    [ -f "$script" ] || continue

    SCRIPT_NAME=$(basename "$script" .md)
    SCRIPT_RESULTS_DIR="$RUN_DIR/$SCRIPT_NAME"
    mkdir -p "$SCRIPT_RESULTS_DIR"

    echo -e "${YELLOW}Testing: $SCRIPT_NAME${NC}"

    TOTAL_SCRIPTS=$((TOTAL_SCRIPTS + 1))
    SUCCESS_COUNT=0
    FIRST_OUTPUT=""
    MATCH_COUNT=0
    OUTPUTS=()
    HASHES=()
    TIMES=()

    for i in $(seq 1 $ITERATIONS); do
        OUTPUT_FILE="$SCRIPT_RESULTS_DIR/output_$i.txt"

        # Capture start time
        START_TIME=$(date +%s.%N)

        # Run script and capture output
        if "$ENGLANG" "$script" > "$OUTPUT_FILE" 2>&1; then
            SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        fi

        # Capture end time
        END_TIME=$(date +%s.%N)
        ELAPSED=$(echo "$END_TIME - $START_TIME" | bc)
        TIMES+=("$ELAPSED")

        # Calculate hash
        HASH=$(sha256sum "$OUTPUT_FILE" | cut -d' ' -f1)
        HASHES+=("$HASH")

        # Store first output for comparison (reference)
        if [ $i -eq 1 ]; then
            FIRST_HASH="$HASH"
            echo "  Run $i: REFERENCE (${ELAPSED}s)"
        else
            # Only count matches for runs 2+
            echo -n "  Run $i: "
            if [ "$HASH" == "$FIRST_HASH" ]; then
                MATCH_COUNT=$((MATCH_COUNT + 1))
                echo -e "${GREEN}MATCH${NC} (${ELAPSED}s)"
            else
                echo -e "${RED}DIFFER${NC} (${ELAPSED}s)"
            fi
        fi
    done

    # Calculate determinism score (matches out of runs 2-N, i.e., ITERATIONS-1)
    if [ $ITERATIONS -gt 1 ]; then
        DETERMINISM_SCORE=$(echo "scale=2; $MATCH_COUNT / ($ITERATIONS - 1) * 100" | bc)
    else
        DETERMINISM_SCORE=100
    fi

    # Calculate average time
    TOTAL_TIME=0
    for t in "${TIMES[@]}"; do
        TOTAL_TIME=$(echo "$TOTAL_TIME + $t" | bc)
    done
    AVG_TIME=$(echo "scale=3; $TOTAL_TIME / $ITERATIONS" | bc)

    # Count unique outputs
    UNIQUE_HASHES=$(printf '%s\n' "${HASHES[@]}" | sort -u | wc -l)

    # Determine status (all runs 2-N must match run 1)
    EXPECTED_MATCHES=$((ITERATIONS - 1))
    if [ "$MATCH_COUNT" -eq "$EXPECTED_MATCHES" ]; then
        STATUS="DETERMINISTIC"
        TOTAL_DETERMINISTIC=$((TOTAL_DETERMINISTIC + 1))
        echo -e "  Result: ${GREEN}100% DETERMINISTIC${NC} ($MATCH_COUNT/$EXPECTED_MATCHES matches)"
    else
        STATUS="NON-DETERMINISTIC"
        echo -e "  Result: ${RED}${DETERMINISM_SCORE}% consistent${NC} ($MATCH_COUNT/$EXPECTED_MATCHES matches, $UNIQUE_HASHES unique outputs)"
    fi

    echo "  Avg time: ${AVG_TIME}s"
    echo ""

    # Convert bash array to JSON array string
    HASHES_JSON=$(printf '"%s",' "${HASHES[@]}" | sed 's/,$//')

    # Save script results to JSON (using Python for proper JSON handling)
    python3 << PYTHON
import json

with open("$RESULTS_JSON", "r") as f:
    data = json.load(f)

data["scripts"]["$SCRIPT_NAME"] = {
    "iterations": $ITERATIONS,
    "success_count": $SUCCESS_COUNT,
    "match_count": $MATCH_COUNT,
    "unique_outputs": $UNIQUE_HASHES,
    "determinism_score": $DETERMINISM_SCORE,
    "avg_time_seconds": $AVG_TIME,
    "status": "$STATUS",
    "hashes": [$HASHES_JSON]
}

with open("$RESULTS_JSON", "w") as f:
    json.dump(data, f, indent=2)
PYTHON

done

# Calculate overall stats
OVERALL_SCORE=$(echo "scale=2; $TOTAL_DETERMINISTIC / $TOTAL_SCRIPTS * 100" | bc)

echo "========================================"
echo "OVERALL RESULTS"
echo "========================================"
echo "Scripts tested: $TOTAL_SCRIPTS"
echo "Fully deterministic: $TOTAL_DETERMINISTIC"
echo -e "Overall score: ${GREEN}${OVERALL_SCORE}%${NC}"
echo ""
echo "Results saved to: $RUN_DIR"

# Update results JSON with overall stats
python3 << PYTHON
import json

with open("$RESULTS_JSON", "r") as f:
    data = json.load(f)

data["overall"] = {
    "total_scripts": $TOTAL_SCRIPTS,
    "deterministic_scripts": $TOTAL_DETERMINISTIC,
    "overall_score": $OVERALL_SCORE
}

with open("$RESULTS_JSON", "w") as f:
    json.dump(data, f, indent=2)
PYTHON

echo ""

# Copy to latest folder for easy access
LATEST_DIR="$RESULTS_DIR/latest"
rm -rf "$LATEST_DIR"
cp -r "$RUN_DIR" "$LATEST_DIR"
echo "Latest results copied to: $LATEST_DIR"

echo ""
echo "Generating report and plot..."
"$SCRIPT_DIR/generate-report.py" "$LATEST_DIR"
