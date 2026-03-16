# devtools/tests toolbox

Definitive local toolbox for test execution, coverage analysis, thresholds, history, and module/test association analysis in MolSysMT.

## Main commands

```bash
cd devtools/tests
make help
make coverage          # compact terminal report
make coverage-open     # HTML report opened in browser
make coverage-json     # force fresh run: deletes coverage.json and regenerates it
make coverage-hotspots
make coverage-packages
make coverage-top
make coverage-map
make coverage-markdown
make coverage-check
make coverage-history
make module-test-map
make module-test-gaps
make clean             # remove all generated artifacts (keeps coverage_history.json)
```

## Notes

- No package paths are excluded by default.
- Coverage summaries include global metrics, top-level package tables, package tables, and hotspot tables.
- Module/test association uses heuristic matching based on paths and names. It is designed to detect likely gaps quickly, not to prove test absence with certainty.
