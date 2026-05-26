#!/bin/bash
# Run FTRS service automation tests and generate Allure report
#
# Usage:
#   ./run_pytest_with_html_report.sh
#       → runs all CRUD markers: crud-org-api crud-healthcare-service-api crud-location-api
#
#   ./run_pytest_with_html_report.sh "crud-org-api"
#       → runs a single marker
#
#   ./run_pytest_with_html_report.sh "crud-org-api crud-location-api"
#       → runs multiple markers (space-separated, quoted)
#
# The script:
#   1. Cleans previous allure-results and allure-reports
#   2. Runs tests via make test MARKERS="..."
#   3. Generates a self-contained allure-reports/index.html
#   4. Opens the report in your browser automatically

set -uo pipefail

# ============================================================
# Configuration
# ============================================================
SERVICE_AUTOMATION_DIR="/Users/sylwia.luczak-jagiela/WORK/NHSDigital/ftrs-directory-of-services/tests/service_automation"
ALLURE_RESULTS="allure-results"
ALLURE_REPORTS="allure-reports"
DEFAULT_MARKERS="crud-org-api crud-healthcare-service-api crud-location-api"

# Ensure Java (OpenJDK via Homebrew) is in PATH for allure generate
export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"

MARKERS="${1:-$DEFAULT_MARKERS}"

# ============================================================
echo ""
echo "=================================================="
echo "  FTRS Service Automation Tests + Allure Report"
echo "  Markers : $MARKERS"
echo "=================================================="
echo ""

cd "$SERVICE_AUTOMATION_DIR"

# 1. Clean previous results for a fresh run
echo "[1/3] Cleaning previous results..."
rm -rf "$ALLURE_RESULTS" "$ALLURE_REPORTS"
echo "      Done."
echo ""

# 2. Run tests (capture exit code without stopping the script)
echo "[2/3] Running tests..."
echo ""
set +e
make test MARKERS="$MARKERS"
TEST_EXIT_CODE=$?
set -e
echo ""

# 3. Generate Allure report
echo "[3/3] Generating Allure report..."
allure generate --single-file -c -o "$ALLURE_REPORTS" "$ALLURE_RESULTS"

REPORT_FILE="$SERVICE_AUTOMATION_DIR/$ALLURE_REPORTS/index.html"

echo ""
echo "=================================================="
if [ "$TEST_EXIT_CODE" -eq 0 ]; then
    echo "  RESULT  : ALL TESTS PASSED"
else
    echo "  RESULT  : SOME TESTS FAILED (exit code: $TEST_EXIT_CODE)"
fi
echo "  Report  : $REPORT_FILE"
echo "=================================================="
echo ""
echo "Opening report in browser..."
open "$REPORT_FILE"

exit "$TEST_EXIT_CODE"
