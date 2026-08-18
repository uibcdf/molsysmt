# Code Coverage

Code coverage measures how thoroughly the automated test suite exercises the MolSysMT codebase.

---

## 1. Running Coverage Locally

To generate local coverage reports:

```bash
# Run pytest with coverage instrumentation
pytest --cov=molsysmt --cov-report=term-missing --cov-report=html

# Open the HTML report in your browser
xdg-open htmlcov/index.html   # Linux
open htmlcov/index.html       # macOS
```

---

## 2. Coverage Metrics and Monitoring

- Continuous coverage metrics are tracked automatically via [Codecov](https://app.codecov.io/github/uibcdf/MolSysMT).
- Pull requests should maintain or increase test coverage, ensuring new public functions and edge cases are thoroughly validated.
