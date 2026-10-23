# Unit Tests

MolSysMT uses `pytest` for automated test execution across all modules, forms, and calculation engines.

---

## 1. Running Tests

Run the test suite from the repository root:

```bash
# Run the complete test suite
pytest

# Run tests in a specific module
python -m pytest tests/structure/get_distances --receptor=llm

# Run tests matching an expression
pytest -k "test_convert"

# Run tests in parallel across multiple CPU cores
python -m pytest --receptor=llm -n 12

# Stop immediately upon the first failure
pytest -x
```

---

## 2. Test Organization and Conventions

- **Mirrored Paths**: Tests live in `tests/` mirroring the package structure (e.g. tests for `molsysmt/structure/get_distances.py` reside in `tests/structure/get_distances/`).
- **File Naming**: All test files must be prefixed with `test_*.py`.
- **Parametrization**: Use `@pytest.mark.parametrize` to test operations across multiple supported forms and syntaxes.
- **Bundled Demo Systems**: Rely on demo datasets from `molsysmt.systems` for deterministic, lightweight, and fast testing rather than generating heavy synthetic systems.
- **Doctest Validation**: Doctests in docstrings are verified automatically via `pytest --doctest-modules molsysmt`.


## 3. Scientific Evidence

A passing regression test does not necessarily establish scientific accuracy.
The evidence registry distinguishes independent analytic/external oracles from
cross-form or wrapper-engine parity. API stability and scientific evidence are
separate classifications: an Experimental operation may have a tested oracle,
and a scientific gap does not mean its ordinary tests fail.

The registry covers Stable scientific APIs and an explicit Claimed review scope
of additional public operations. Claimed is a selection for evidence review,
not approved manuscript wording. The generated matrix reports the two scopes
separately and identifies other experimental symbols as unreviewed.

```bash
# Validate metadata, cited test nodes and the generated matrix without running tests
python devtools/scripts/validate_scientific_evidence.py

# Execute every cited node; skips and failures prevent a passing certificate
python devtools/scripts/execute_scientific_evidence.py --receptor=llm
```

Read the [scientific validation contract](https://github.com/uibcdf/molsysmt/blob/main/devguide/scientific_validation.md)
and [generated evidence matrix](https://github.com/uibcdf/molsysmt/blob/main/devguide/scientific_evidence_matrix.md)
for declared claims, conventions, tolerances and remaining gaps. A local run in
a development checkout does not qualify a different installed release artifact.


## 4. Conversion Execution

The resident/native-engine/H5MSM/PDB profile discovers declared direct routes between its covered
forms and executes each adapter and its public conversion route on fresh inputs.
It checks execution and output form; fidelity remains a separate test obligation.

```bash
# Inventory planned and deferred routes without executing them
python devtools/scripts/audit_conversion_execution.py --json

# Run the actual direct/public conversion cases
python -m pytest tests/conversion_truth/test_declared_native_edges.py tests/conversion_truth/test_declared_h5msm_edges.py tests/conversion_truth/test_declared_pdb_edges.py --receptor=llm -n 12
```

The [conversion execution guide](https://github.com/uibcdf/molsysmt/blob/main/devguide/conversion_execution.md)
explains fixture coverage, explicit debt and how to extend the profile. A passing
bounded profile does not certify every MolSysMT conversion.

H5MSM cases state their schema scope explicitly. Raw legacy adapters exercise
0.4, while the public conversion route writes 0.5. Separate 0.5 controls verify
partial domains, named interactions and atom/structure remapping. A legacy
`H5MSMFileHandler` is not a modular 0.5 reader. The profile's versioned fixtures
and resource cleanup are described in the conversion execution guide.

PDB cases use a literal local two-structure file/text fixture and fresh handler
resources. Each selected edge runs directly and publicly. Separate regressions
check destination bytes, source ownership, selected positions, equivalent length
units, multiple structures and scratch cleanup after reader errors/interruption.
