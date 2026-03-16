.PHONY: help test coverage coverage-html coverage-open coverage-json _coverage-source-check coverage-hotspots coverage-packages coverage-top coverage-map coverage-markdown slowest coverage-diff coverage-check coverage-history coverage-history-report module-test-map module-test-gaps ci clean

TEST_DIR ?= ../../tests
PACKAGE ?= molsysmt
NPROC ?= 14
DIST_MODE ?= loadfile
QUIET ?= -q
PYTEST_FLAGS = -n $(NPROC) --dist $(DIST_MODE) $(QUIET)
BASELINE_FILE ?= coverage_baseline.json
HISTORY_FILE ?= coverage_history.json
SUMMARY_MD ?= coverage_summary.md
SUMMARY_JSON ?= coverage_summary.json
MODULE_TEST_MAP_JSON ?= module_test_map.json
PACKAGE_DEPTH ?= 1
MAP_DEPTH ?= 2
HOTSPOT_TOP ?= 15
THRESHOLDS_FILE ?= coverage_thresholds.json
COV_TERM_MODE ?= term-missing:skip-covered
BROWSER_OPEN ?= xdg-open
COVERAGE_FAIL_UNDER ?=
SUBPACKAGE ?=
SORT ?= coverage

help:
	@echo ""
	@echo "MolSysMT devtools/tests toolbox - definitive edition"
	@echo "===================================================="
	@echo ""
	@echo "This toolbox is designed for:"
	@echo "  - running local tests"
	@echo "  - exploring coverage visually and textually"
	@echo "  - generating Markdown and JSON summaries"
	@echo "  - checking thresholds globally and by subpackage"
	@echo "  - tracking temporal coverage history"
	@echo "  - comparing coverage reports against a baseline"
	@echo "  - mapping modules to tests and detecting modules without associated tests"
	@echo ""
	@echo "USAGE"
	@echo "-----"
	@echo "  Run from: devtools/tests"
	@echo "  General form:"
	@echo "    make <target> [VARIABLE=value ...]"
	@echo ""
	@echo "PRIMARY TARGETS"
	@echo "---------------"
	@echo "  make test"
	@echo "      Run the test suite without coverage."
	@echo "      Variables:"
	@echo "        TEST_DIR=$(TEST_DIR)"
	@echo "        NPROC=$(NPROC)"
	@echo "        DIST_MODE=$(DIST_MODE)"
	@echo "        QUIET=$(QUIET)"
	@echo ""
	@echo "  make coverage"
	@echo "      Run tests with coverage and print a compact terminal report."
	@echo "      Uses --cov-report=$(COV_TERM_MODE)"
	@echo "      Variables:"
	@echo "        PACKAGE=$(PACKAGE)"
	@echo "        COV_TERM_MODE=$(COV_TERM_MODE)"
	@echo "        COVERAGE_FAIL_UNDER=$(COVERAGE_FAIL_UNDER)"
	@echo ""
	@echo "  make coverage-html"
	@echo "      Run tests with coverage and generate htmlcov/index.html."
	@echo ""
	@echo "  make coverage-open"
	@echo "      Generate the HTML report and open it locally."
	@echo "      Variables:"
	@echo "        BROWSER_OPEN=$(BROWSER_OPEN)"
	@echo ""
	@echo "  make coverage-json"
	@echo "      Force a fresh test run: deletes coverage.json and regenerates it."
	@echo "  make coverage.json"
	@echo "      Internal file target: runs pytest only if coverage.json is absent."
	@echo "      Used automatically as a dependency by all analysis targets."
	@echo ""
	@echo "COVERAGE ANALYSIS TARGETS"
	@echo "-------------------------"
	@echo "  make coverage-hotspots"
	@echo "      Show the lowest-coverage files."
	@echo "      Variables:"
	@echo "        HOTSPOT_TOP=$(HOTSPOT_TOP)"
	@echo "        SUBPACKAGE=$(SUBPACKAGE)      e.g. molsysmt.form or molsysmt.structure"
	@echo ""
	@echo "  make coverage-packages"
	@echo "      Aggregate coverage by package / subpackage."
	@echo "      Variables:"
	@echo "        PACKAGE_DEPTH=$(PACKAGE_DEPTH)  1 => molsysmt.basic"
	@echo "        SUBPACKAGE=$(SUBPACKAGE)"
	@echo ""
	@echo "  make coverage-top"
	@echo "      Aggregate coverage at top-level package depth only."
	@echo "      Equivalent to PACKAGE_DEPTH=1 for MolSysMT top functional areas."
	@echo ""
	@echo "  make coverage-map"
	@echo "      Print a hierarchical textual map of package coverage."
	@echo "      Variables:"
	@echo "        MAP_DEPTH=$(MAP_DEPTH)"
	@echo "        SORT=$(SORT)                  coverage | name"
	@echo "        SUBPACKAGE=$(SUBPACKAGE)"
	@echo ""
	@echo "  make coverage-markdown"
	@echo "      Generate:"
	@echo "        $(SUMMARY_MD)"
	@echo "        $(SUMMARY_JSON)"
	@echo "      Includes:"
	@echo "        - global coverage summary"
	@echo "        - top-level package table"
	@echo "        - package/subpackage table"
	@echo "        - low-coverage hotspot table"
	@echo "      Variables:"
	@echo "        PACKAGE_DEPTH=$(PACKAGE_DEPTH)"
	@echo "        HOTSPOT_TOP=$(HOTSPOT_TOP)"
	@echo "        SUBPACKAGE=$(SUBPACKAGE)"
	@echo "        SUMMARY_MD=$(SUMMARY_MD)"
	@echo "        SUMMARY_JSON=$(SUMMARY_JSON)"
	@echo ""
	@echo "SLOW TEST ANALYSIS"
	@echo "------------------"
	@echo "  make slowest"
	@echo "      Show slowest pytest items."
	@echo "      Variables:"
	@echo "        DURATIONS=25"
	@echo ""
	@echo "BASELINE COMPARISON AND THRESHOLDS"
	@echo "----------------------------------"
	@echo "  make coverage-diff"
	@echo "      Compare current coverage.json against $(BASELINE_FILE)."
	@echo "      Variables:"
	@echo "        BASELINE_FILE=$(BASELINE_FILE)"
	@echo ""
	@echo "  make coverage-check"
	@echo "      Validate coverage against thresholds declared in $(THRESHOLDS_FILE)."
	@echo "      Thresholds supported:"
	@echo "        - overall_min_percent"
	@echo "        - package-specific minimum percentages"
	@echo "      Variables:"
	@echo "        THRESHOLDS_FILE=$(THRESHOLDS_FILE)"
	@echo ""
	@echo "TEMPORAL HISTORY"
	@echo "----------------"
	@echo "  make coverage-history"
	@echo "      Append the current summarized coverage to $(HISTORY_FILE)."
	@echo ""
	@echo "  make coverage-history-report"
	@echo "      Print recent history rows from $(HISTORY_FILE)."
	@echo "      Variables:"
	@echo "        HISTORY_FILE=$(HISTORY_FILE)"
	@echo "        LAST=10"
	@echo ""
	@echo "MODULE / TEST ASSOCIATION ANALYSIS"
	@echo "----------------------------------"
	@echo "  make module-test-map"
	@echo "      Generate a JSON map between Python modules in $(PACKAGE) and associated test directories/files."
	@echo "      Writes:"
	@echo "        $(MODULE_TEST_MAP_JSON)"
	@echo ""
	@echo "  make module-test-gaps"
	@echo "      Print modules that do not appear to have associated tests."
	@echo "      Association rules are heuristic and based on path/name similarity."
	@echo "      Variables:"
	@echo "        MODULE_TEST_MAP_JSON=$(MODULE_TEST_MAP_JSON)"
	@echo ""
	@echo "CI"
	@echo "--"
	@echo "  make ci"
	@echo "      Opinionated pipeline:"
	@echo "        1) coverage.json (file target)"
	@echo "        2) coverage-markdown"
	@echo "        3) coverage-check"
	@echo "        4) coverage-history"
	@echo "        5) module-test-map"
	@echo ""
	@echo "CLEANUP"
	@echo "-------"
	@echo "  make clean"
	@echo "      Remove generated coverage and summary artifacts."
	@echo ""
	@echo "KEY VARIABLES"
	@echo "-------------"
	@echo "  TEST_DIR=$(TEST_DIR)"
	@echo "  PACKAGE=$(PACKAGE)"
	@echo "  NPROC=$(NPROC)"
	@echo "  DIST_MODE=$(DIST_MODE)"
	@echo "  QUIET=$(QUIET)"
	@echo "  BASELINE_FILE=$(BASELINE_FILE)"
	@echo "  HISTORY_FILE=$(HISTORY_FILE)"
	@echo "  SUMMARY_MD=$(SUMMARY_MD)"
	@echo "  SUMMARY_JSON=$(SUMMARY_JSON)"
	@echo "  MODULE_TEST_MAP_JSON=$(MODULE_TEST_MAP_JSON)"
	@echo "  PACKAGE_DEPTH=$(PACKAGE_DEPTH)"
	@echo "  MAP_DEPTH=$(MAP_DEPTH)"
	@echo "  HOTSPOT_TOP=$(HOTSPOT_TOP)"
	@echo "  THRESHOLDS_FILE=$(THRESHOLDS_FILE)"
	@echo "  COV_TERM_MODE=$(COV_TERM_MODE)"
	@echo "  BROWSER_OPEN=$(BROWSER_OPEN)"
	@echo "  SUBPACKAGE=$(SUBPACKAGE)"
	@echo "  SORT=$(SORT)"
	@echo ""
	@echo "COMMON EXAMPLES"
	@echo "---------------"
	@echo "  make coverage"
	@echo "  make coverage NPROC=8"
	@echo "  make coverage-open"
	@echo "  make coverage-hotspots HOTSPOT_TOP=25"
	@echo "  make coverage-hotspots SUBPACKAGE=molsysmt.form"
	@echo "  make coverage-packages PACKAGE_DEPTH=2"
	@echo "  make coverage-top"
	@echo "  make coverage-map MAP_DEPTH=3 SORT=name"
	@echo "  make coverage-markdown PACKAGE_DEPTH=2 HOTSPOT_TOP=20"
	@echo "  make coverage-diff BASELINE_FILE=coverage_baseline_main.json"
	@echo "  make coverage-check THRESHOLDS_FILE=coverage_thresholds.json"
	@echo "  make coverage-history"
	@echo "  make coverage-history-report LAST=20"
	@echo "  make module-test-map"
	@echo "  make module-test-gaps"
	@echo "  make ci NPROC=12"
	@echo ""

test:
	pytest $(PYTEST_FLAGS) $(TEST_DIR)

coverage:
	pytest $(PYTEST_FLAGS) \
	       --cov=$(PACKAGE) \
	       --cov-report=$(COV_TERM_MODE) \
	       $(if $(COVERAGE_FAIL_UNDER),--cov-fail-under=$(COVERAGE_FAIL_UNDER),) \
	       $(TEST_DIR)

coverage-html:
	pytest $(PYTEST_FLAGS) \
	       --cov=$(PACKAGE) \
	       --cov-report=html \
	       $(if $(COVERAGE_FAIL_UNDER),--cov-fail-under=$(COVERAGE_FAIL_UNDER),) \
	       $(TEST_DIR)

coverage-open: coverage-html
	$(BROWSER_OPEN) htmlcov/index.html

# coverage.json is a real file target: Make checks whether it exists and skips
# pytest if it does.  Use 'make coverage-run' to force a fresh test run.
coverage.json:
	pytest $(PYTEST_FLAGS) \
	       --cov=$(PACKAGE) \
	       --cov-report= \
	       $(if $(COVERAGE_FAIL_UNDER),--cov-fail-under=$(COVERAGE_FAIL_UNDER),) \
	       $(TEST_DIR)
	coverage json -o coverage.json

# Phony: always deletes coverage.json and regenerates it.
# Use this when you want an explicit fresh run.  Analysis targets use the
# coverage.json file target instead and skip pytest if the file exists.
coverage-json:
	rm -f coverage.json
	$(MAKE) coverage.json

# Phony guard: always evaluated before any analysis target.  Prints a notice
# when coverage.json already exists so the user knows tests were not re-run.
# When coverage.json is absent this target does nothing; coverage.json recipe
# will run immediately after and generate the file.
_coverage-source-check:
	@if [ -f coverage.json ]; then \
		printf 'Note: reusing existing coverage.json (generated: %s). Run "make coverage-json" to refresh.\n' \
		    "$$(stat -c '%y' coverage.json | cut -d. -f1)"; \
	fi

coverage-hotspots: _coverage-source-check coverage.json
	python coverage_hotspots.py --top $(HOTSPOT_TOP) $(if $(SUBPACKAGE),--subpackage $(SUBPACKAGE),) --package $(PACKAGE)

coverage-packages: _coverage-source-check coverage.json
	python coverage_by_package.py --root $(PACKAGE) --depth $(PACKAGE_DEPTH) $(if $(SUBPACKAGE),--subpackage $(SUBPACKAGE),)

coverage-top: _coverage-source-check coverage.json
	python coverage_by_package.py --root $(PACKAGE) --depth 1 $(if $(SUBPACKAGE),--subpackage $(SUBPACKAGE),)

coverage-map: _coverage-source-check coverage.json
	python coverage_map.py --root $(PACKAGE) --max-depth $(MAP_DEPTH) --sort $(SORT) $(if $(SUBPACKAGE),--subpackage $(SUBPACKAGE),)

coverage-markdown: _coverage-source-check coverage.json
	python coverage_markdown.py --root $(PACKAGE) --package-depth $(PACKAGE_DEPTH) --top $(HOTSPOT_TOP) --output $(SUMMARY_MD) --json-output $(SUMMARY_JSON) $(if $(SUBPACKAGE),--subpackage $(SUBPACKAGE),)

slowest:
	pytest $(PYTEST_FLAGS) --durations=$${DURATIONS:-25} $(TEST_DIR)

coverage-diff: _coverage-source-check coverage.json
	python coverage_diff.py --baseline $(BASELINE_FILE) --current coverage.json

coverage-check: coverage-markdown
	python coverage_check.py --summary-json $(SUMMARY_JSON) --thresholds $(THRESHOLDS_FILE)

coverage-history: coverage-markdown
	python coverage_history.py append --summary-json $(SUMMARY_JSON) --history $(HISTORY_FILE)

coverage-history-report:
	python coverage_history.py report --history $(HISTORY_FILE) --last $${LAST:-10}

module-test-map:
	python module_test_map.py --package-root ../../$(PACKAGE) --tests-root $(TEST_DIR) --output $(MODULE_TEST_MAP_JSON)

module-test-gaps: module-test-map
	python module_test_map.py report-gaps --input $(MODULE_TEST_MAP_JSON)

ci: coverage.json coverage-markdown
	python coverage_check.py --summary-json $(SUMMARY_JSON) --thresholds $(THRESHOLDS_FILE)
	python coverage_history.py append --summary-json $(SUMMARY_JSON) --history $(HISTORY_FILE)
	python module_test_map.py --package-root ../../$(PACKAGE) --tests-root $(TEST_DIR) --output $(MODULE_TEST_MAP_JSON)
	@echo "Toolbox CI pipeline completed."

# Removes all generated artifacts.  coverage_history.json is intentionally kept
# (it is a persistent record, not a build artifact).
clean:
	rm -rf htmlcov .pytest_cache
	rm -f .coverage coverage.json $(SUMMARY_MD) $(SUMMARY_JSON) $(MODULE_TEST_MAP_JSON)
