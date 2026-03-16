# devtools/tests toolbox

Definitive local toolbox for test execution, coverage analysis, thresholds, history, and module/test association analysis in MolSysMT.

## Main commands

```bash
cd devtools/tests
make help
make coverage
make coverage-open
make coverage-hotspots
make coverage-packages
make coverage-top
make coverage-map
make coverage-markdown
make coverage-check
make coverage-history
make module-test-map
make module-test-gaps
```

## Notes

- No package paths are excluded by default.
- Coverage summaries include global metrics, top-level package tables, package tables, and hotspot tables.
- Module/test association uses heuristic matching based on paths and names. It is designed to detect likely gaps quickly, not to prove test absence with certainty.
