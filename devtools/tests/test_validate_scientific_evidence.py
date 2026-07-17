import json

from devtools.scripts import validate_scientific_evidence as validator


def _fixture(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    scientific_truth = tests / "scientific_truth"
    scientific_truth.mkdir()
    test_file = scientific_truth / "test_quantity.py"
    test_file.write_text(
        "def test_matches_closed_form():\n    assert 2 + 2 == 4\n",
        encoding="utf-8",
    )
    registry = {
        "schema_version": "molsysmt.scientific-evidence@1",
        "stable_api_scopes": ["molsysmt.domain"],
        "status_definitions": {
            "validated": "Independent evidence exists.",
            "partial": "Incomplete evidence exists.",
            "gap": "Independent evidence is absent.",
        },
        "tolerances": {
            "exact": {
                "atol": 1.0e-12,
                "rtol": 0.0,
                "applies_to": "Exact fixture.",
                "rationale": "Float64 propagation.",
            }
        },
        "capabilities": {
            "molsysmt.domain.quantity": {
                "domain": "domain",
                "status": "validated",
                "claim": "Computing one exact quantity.",
                "units": ["nm"],
                "periodic_behavior": "Not periodic.",
                "contract_test_area": "tests",
                "scientific_evidence": [
                    {
                        "class": "analytic",
                        "test": "tests/scientific_truth/test_quantity.py::test_matches_closed_form",
                        "oracle": "Closed-form value.",
                        "tolerance": "exact",
                    }
                ],
                "gap": None,
            }
        },
    }
    api_registry = {
        "symbols": {
            "molsysmt.domain.quantity": {"stability": "stable"},
        }
    }
    return registry, api_registry


def test_registry_accepts_exact_stable_inventory_and_independent_evidence(tmp_path):
    registry, api_registry = _fixture(tmp_path)

    assert validator.validate_registry(registry, api_registry, tmp_path) == []


def test_registry_rejects_unclassified_stable_scientific_api(tmp_path):
    registry, api_registry = _fixture(tmp_path)
    api_registry["symbols"]["molsysmt.domain.missing"] = {"stability": "stable"}

    assert (
        "Stable scientific API is missing evidence classification: molsysmt.domain.missing"
        in validator.validate_registry(registry, api_registry, tmp_path)
    )


def test_validated_status_rejects_parity_as_sole_evidence(tmp_path):
    registry, api_registry = _fixture(tmp_path)
    registry["capabilities"]["molsysmt.domain.quantity"]["scientific_evidence"][0][
        "class"
    ] = "parity"

    assert (
        "molsysmt.domain.quantity: validated status requires independent evidence."
        in validator.validate_registry(registry, api_registry, tmp_path)
    )


def test_scientific_evidence_must_live_in_the_governed_suite(tmp_path):
    registry, api_registry = _fixture(tmp_path)
    evidence = registry["capabilities"]["molsysmt.domain.quantity"][
        "scientific_evidence"
    ][0]
    evidence["test"] = "tests/test_quantity.py::test_matches_closed_form"

    assert any(
        "must reference the governed Scientific Truth suite" in error
        for error in validator.validate_registry(registry, api_registry, tmp_path)
    )


def test_registry_rejects_stale_test_nodes_and_unknown_tolerances(tmp_path):
    registry, api_registry = _fixture(tmp_path)
    evidence = registry["capabilities"]["molsysmt.domain.quantity"][
        "scientific_evidence"
    ][0]
    evidence["test"] = "tests/scientific_truth/test_quantity.py::test_missing"
    evidence["tolerance"] = "unregistered"

    errors = validator.validate_registry(registry, api_registry, tmp_path)

    assert any("test function does not exist" in error for error in errors)
    assert any("references unknown tolerance 'unregistered'" in error for error in errors)


def test_exact_categorical_evidence_does_not_require_a_tolerance(tmp_path):
    registry, api_registry = _fixture(tmp_path)
    evidence = registry["capabilities"]["molsysmt.domain.quantity"][
        "scientific_evidence"
    ][0]
    evidence["comparison"] = "exact"
    evidence["tolerance"] = None

    assert validator.validate_registry(registry, api_registry, tmp_path) == []


def test_gap_status_requires_no_evidence_and_an_explanation(tmp_path):
    registry, api_registry = _fixture(tmp_path)
    capability = registry["capabilities"]["molsysmt.domain.quantity"]
    capability["status"] = "gap"
    capability["gap"] = ""

    errors = validator.validate_registry(registry, api_registry, tmp_path)

    assert "molsysmt.domain.quantity: gap status cannot register scientific evidence." in errors
    assert "molsysmt.domain.quantity: gap status requires an actionable explanation." in errors


def test_repository_scientific_evidence_registry_is_valid():
    registry, load_errors = validator.read_evidence_registry()
    with validator.API_REGISTRY_PATH.open(encoding="utf-8") as file:
        api_registry = json.load(file)

    assert load_errors == []
    assert validator.validate_registry(registry, api_registry) == []


def test_split_registry_rejects_duplicate_capabilities(tmp_path):
    evidence_root = tmp_path / "evidence"
    capabilities = evidence_root / "capabilities"
    capabilities.mkdir(parents=True)
    (evidence_root / "registry.json").write_text(
        json.dumps(
            {
                "schema_version": "molsysmt.scientific-evidence@1",
                "stable_api_scopes": ["molsysmt.domain"],
                "status_definitions": {},
            }
        ),
        encoding="utf-8",
    )
    (evidence_root / "tolerances.json").write_text("{}", encoding="utf-8")
    entry = {"molsysmt.domain.quantity": {"domain": "first"}}
    (capabilities / "first.json").write_text(json.dumps(entry), encoding="utf-8")
    (capabilities / "second.json").write_text(json.dumps(entry), encoding="utf-8")

    _, errors = validator.read_evidence_registry(evidence_root)

    assert errors == [
        "Duplicate scientific capability across domain files: "
        "molsysmt.domain.quantity"
    ]
