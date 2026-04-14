#!/usr/bin/env bash
set -euo pipefail

# ── Ghost Tequila 360 Report — Containerized Run ──
#
# Usage:
#   ./run_ghost_tequila.sh
#
# Prerequisites:
#   - Docker installed
#   - OPENAI_API_KEY set in your environment or in .env file at repo root

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IMAGE_NAME="ghost-tequila-360"
OUTPUT_DIR="$SCRIPT_DIR/ghost_tequila"

# Load .env if it exists
if [ -f "$SCRIPT_DIR/.env" ]; then
    echo "Loading .env file..."
    set -a
    source "$SCRIPT_DIR/.env"
    set +a
fi

# Validate API key
if [ -z "${OPENAI_API_KEY:-}" ]; then
    echo "ERROR: OPENAI_API_KEY is not set."
    echo "Either export it or create a .env file with:"
    echo "  OPENAI_API_KEY=sk-..."
    exit 1
fi

echo "Building container..."
docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"

echo "Running Ghost Tequila 360 pipeline..."
echo "This will take a while (deep research can run 10-30 minutes)."
echo ""

# Run the container:
#   - Pass OPENAI_API_KEY
#   - Mount ghost_tequila/ so outputs persist on host
#   - Mount generated_sections/ and report_txt_sections/ for intermediate files
#   - Mount report_output/ for final TS bundle
docker run --rm \
    -e OPENAI_API_KEY="$OPENAI_API_KEY" \
    -v "$OUTPUT_DIR:/app/ghost_tequila" \
    -v "$SCRIPT_DIR/generated_sections:/app/generated_sections" \
    -v "$SCRIPT_DIR/report_txt_sections:/app/report_txt_sections" \
    -v "$SCRIPT_DIR/report_output:/app/report_output" \
    "$IMAGE_NAME"

echo ""
echo "Done. Outputs:"
echo "  Research report:  ghost_tequila/report.txt"
echo "  Split sections:   report_txt_sections/"
echo "  Extracted JSON:   generated_sections/"
echo "  TypeScript bundle: report_output/reportData.ts"
