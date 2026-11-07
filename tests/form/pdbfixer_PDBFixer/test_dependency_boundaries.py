"""Checking optional-provider diagnostics at PDBFixer construction boundaries."""

import builtins
from importlib import import_module
from importlib.machinery import ModuleSpec
from pathlib import Path

import pytest
from depdigest import is_installed
from depdigest.core import checker

import molsysmt as msm
from molsysmt._private.smonitor import LibraryNotFoundError


@pytest.fixture(params=["file_pdb", "string_pdb_text"])
def pdb_input(request):
    path = Path(msm.__file__).parent / "data" / "pdb" / "1l2y.pdb"
    item = str(path) if request.param == "file_pdb" else path.read_text()
    return request.param, item


@pytest.fixture
def provider_boundary(monkeypatch):
    """Model discovery separately from an actual provider import failure."""
    original_find_spec = checker.find_spec
    original_import = builtins.__import__
    attempts = []

    with monkeypatch.context() as patch:

        def configure(*, available, error):
            def find_spec(name, *args, **kwargs):
                if name == "pdbfixer" or name.startswith("pdbfixer."):
                    return ModuleSpec(name, loader=None) if available else None
                return original_find_spec(name, *args, **kwargs)

            def import_provider(name, *args, **kwargs):
                if name == "pdbfixer" or name.startswith("pdbfixer."):
                    attempts.append(name)
                    raise error
                return original_import(name, *args, **kwargs)

            patch.setattr(checker, "find_spec", find_spec)
            patch.setattr(builtins, "__import__", import_provider)
            is_installed.cache_clear()
            return attempts

        try:
            yield configure
        finally:
            is_installed.cache_clear()


def _construct(pdb_input, boundary, skip_digestion):
    source, item = pdb_input
    if boundary == "public":
        return msm.convert(
            item, to_form="pdbfixer.PDBFixer", skip_digestion=skip_digestion
        )
    converter = import_module(
        f"molsysmt.form.{source}.to_pdbfixer_PDBFixer"
    ).to_pdbfixer_PDBFixer
    return converter(item, skip_digestion=skip_digestion)


@pytest.mark.parametrize("boundary", ["public", "direct"])
@pytest.mark.parametrize("skip_digestion", [False, True])
def test_missing_provider_is_diagnosed_before_import(
    pdb_input, provider_boundary, boundary, skip_digestion
):
    attempts = provider_boundary(
        available=False,
        error=ModuleNotFoundError("PDBFixer is unavailable", name="pdbfixer"),
    )
    assert not is_installed("pdbfixer")

    with pytest.raises(LibraryNotFoundError, match="pdbfixer"):
        _construct(pdb_input, boundary, skip_digestion)

    assert attempts == []


def test_native_conversion_does_not_require_pdbfixer(pdb_input, provider_boundary):
    attempts = provider_boundary(
        available=False,
        error=ModuleNotFoundError("PDBFixer is unavailable", name="pdbfixer"),
    )
    _, item = pdb_input

    molsys = msm.convert(item, to_form="molsysmt.MolSys")

    assert molsys.topology.n_atoms == 304
    assert molsys.topology.n_groups == 20
    assert molsys.structures.coordinates.shape == (38, 304, 3)
    assert attempts == []


@pytest.mark.parametrize("boundary", ["public", "direct"])
@pytest.mark.parametrize("skip_digestion", [False, True])
@pytest.mark.parametrize("error_type", [ImportError, ModuleNotFoundError])
def test_provider_import_failures_keep_their_original_error(
    pdb_input, provider_boundary, boundary, skip_digestion, error_type
):
    error = error_type("PDBFixer's transitive dependency failed to import")
    if isinstance(error, ModuleNotFoundError):
        error.name = "pdbfixer_missing_transitive_dependency"
    attempts = provider_boundary(available=True, error=error)
    assert is_installed("pdbfixer")

    with pytest.raises(error_type) as caught:
        _construct(pdb_input, boundary, skip_digestion)

    assert caught.value is error
    assert not isinstance(caught.value, LibraryNotFoundError)
    assert attempts == ["pdbfixer.pdbfixer"]
