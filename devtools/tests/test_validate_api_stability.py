import json

from devtools.scripts import validate_api_stability as validator


def _fixture(tmp_path):
    package = tmp_path / "example"
    package.mkdir()
    (package / "__init__.py").write_text(
        "_LAZY_ATTRIBUTES = {'run': ('.run', 'run')}\n",
        encoding="utf-8",
    )
    (tmp_path / "docs.md").write_text("# Contract\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    registry = {
        "schema_version": "molsysmt.api-stability@1",
        "release_line": "1.x",
        "tracked_scopes": {
            "example": {
                "source": "example/__init__.py",
                "discovery": "lazy-root",
            }
        },
        "symbols": {
            "example.run": {
                "stability": "experimental",
                "introduced": "1.0.0",
                "owner": "example",
                "documentation": "docs.md",
                "contract_tests": "tests",
            }
        },
    }
    return registry


def test_registry_accepts_an_exact_ast_inventory(tmp_path):
    registry = _fixture(tmp_path)

    assert validator.validate_registry(registry, tmp_path) == []


def test_registry_rejects_new_unclassified_exports(tmp_path):
    registry = _fixture(tmp_path)
    source = tmp_path / "example/__init__.py"
    source.write_text(
        "_LAZY_ATTRIBUTES = {'run': ('.run', 'run'), 'new': '.new'}\n",
        encoding="utf-8",
    )

    assert "Unclassified public export: example.new" in validator.validate_registry(
        registry, tmp_path
    )


def test_untracked_public_namespace_requires_an_inherited_policy(tmp_path):
    registry = _fixture(tmp_path)
    source = tmp_path / "example/__init__.py"
    source.write_text("_LAZY_ATTRIBUTES = {'tools': '.tools'}\n", encoding="utf-8")
    registry["symbols"] = {
        "example.tools": {
            **registry["symbols"]["example.run"],
            "stability": "experimental",
        }
    }

    assert (
        "Untracked public namespace requires subtree_stability: example.tools"
        in validator.validate_registry(registry, tmp_path)
    )

def test_registry_rejects_removed_exports_and_private_entries(tmp_path):
    registry = _fixture(tmp_path)
    registry["symbols"]["example._private.helper"] = {
        **registry["symbols"]["example.run"],
        "stability": "outside-contract",
    }

    errors = validator.validate_registry(registry, tmp_path)

    assert "Stale or nonexistent registry symbol: example._private.helper" in errors
    assert "Internal symbol cannot be registered: example._private.helper" in errors


def test_deprecated_symbol_requires_a_registered_replacement_and_timeline(tmp_path):
    registry = _fixture(tmp_path)
    registry["symbols"]["example.run"].update(
        lifecycle="deprecated",
        deprecated_since="1.0.0",
        replacement="example.missing",
    )

    errors = validator.validate_registry(registry, tmp_path)

    assert "example.run: deprecated symbols require removal_not_before." in errors
    assert "example.run: replacement is not registered: example.missing" in errors


def test_registry_file_is_valid_json():
    with validator.REGISTRY_PATH.open(encoding="utf-8") as file:
        registry = json.load(file)

    assert registry["schema_version"] == "molsysmt.api-stability@1"


def test_transition_rejects_stable_demotion_and_removal(tmp_path):
    previous = _fixture(tmp_path)
    previous["symbols"]["example.run"]["stability"] = "stable"
    demoted = json.loads(json.dumps(previous))
    demoted["symbols"]["example.run"]["stability"] = "experimental"

    assert validator.validate_transition(previous, demoted) == [
        "Stable symbol cannot be demoted to experimental: example.run"
    ]
    assert validator.validate_transition(previous, {"symbols": {}}) == [
        "Stable symbol removed from registry: example.run"
    ]
