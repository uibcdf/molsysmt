"""Repository-wide pytest collection safeguards."""


# These developer command-line utilities are executable scripts rather than
# import-safe doctest modules. Their dedicated tests exercise the reusable
# validators without importing argument-parsing entry points.
collect_ignore = [
    "devtools/tests/coverage_by_package.py",
    "devtools/tests/coverage_check.py",
    "devtools/tests/coverage_diff.py",
    "devtools/tests/coverage_history.py",
    "devtools/tests/coverage_hotspots.py",
    "devtools/tests/coverage_map.py",
    "devtools/tests/coverage_markdown.py",
    "devtools/tests/coverage_utils.py",
    "devtools/tests/module_test_map.py",
]
