"""Exercise a private development root without changing public 0.5 defaults."""

import json
import os
import subprocess
import sys

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.h5msm_storage import modular
from molsysmt.form._h5msm05_associations import normalize_associations
from molsysmt.native import MolecularMechanics, MolSys, Structures
from tests.form.file_h5msm.test_mechanics_presence import _system


@pytest.mark.parametrize(
    "domain",
    ["complete", "topology_free", "no_chemistry", "no_structures", "interactions"],
)
def test_partial_native_domains_and_mechanics_roundtrip_without_synthetic_domains(
    tmp_path, domain
):
    source = _system(domain)
    source.molecular_mechanics.forcefield = "model_request_only"
    source.molecular_mechanics.partial_charge = np.array([0.25, -0.25])
    path = tmp_path / "development.h5msm"
    modular.write_molsys_file(path, source)
    restored = modular.read_molsys_file(path)
    assert (restored.topology is None) == (source.topology is None)
    assert (restored.chemical_states is None) == (source.chemical_states is None)
    assert (restored.structures is None) == (source.structures is None)
    assert restored.get_n_atoms() == source.get_n_atoms()
    assert restored._get_n_structures() == source._get_n_structures()
    assert restored.molecular_mechanics.forcefield == "model_request_only"
    np.testing.assert_array_equal(
        restored.molecular_mechanics.partial_charge, [0.25, -0.25]
    )
    assert set(restored.interactions) == set(source.interactions)
    if source.interactions:
        assert restored.interactions["empty"].evaluated_structure_indices.tolist() == [
            0
        ]
    with h5py.File(path, "r") as file:
        assert file.attrs["version"] == "0.6"
        assert file.attrs["creator_version"] == msm.__version__
        assert "created_at" in file.attrs
    axes = modular.read_axis_sizes(path)
    assert axes[("molecular_mechanics", None, "atom")] == 2


def _link(
    source,
    target,
    *,
    indices="identity",
    axis="atom",
    source_name=None,
    target_name=None,
):
    return dict(
        axis=axis,
        source=source,
        target=target,
        source_name=source_name,
        target_name=target_name,
        indices=indices,
    )


def test_equal_counts_without_declared_identity_do_not_assemble_a_molsys(tmp_path):
    source = _system("complete")
    path = tmp_path / "independent.h5msm"
    modular.write_modular_file(
        path,
        topology=source.topology,
        structures=source.structures,
        molecular_mechanics=MolecularMechanics(forcefield="request"),
        mechanics_n_atoms=2,
    )
    layers = modular.read_modular_file(path)
    assert layers["topology"].n_atoms == 2
    assert layers["molecular_mechanics"].forcefield == "request"
    assert layers["associations"] is None
    with pytest.raises(ValueError, match="identity associations"):
        modular.read_molsys_file(path)


def test_transitive_identity_links_are_sufficient(tmp_path):
    source = _system("complete")
    path = tmp_path / "chain.h5msm"
    links = [
        _link("chemical_states", "topology"),
        _link("structures", "chemical_states"),
        _link("molecular_mechanics", "structures"),
    ]
    modular.write_modular_file(
        path,
        topology=source.topology,
        chemical_states=source.chemical_states,
        structures=source.structures,
        molecular_mechanics=MolecularMechanics(forcefield="request"),
        mechanics_n_atoms=2,
        associations=links,
    )
    restored = modular.read_molsys_file(path)
    assert restored.get_n_atoms() == 2
    assert restored.chemical_states._molsys_owner_ref() is restored
    assert restored.molecular_mechanics.forcefield == "request"


def test_explicit_atom_permutation_remains_independent_and_is_not_silently_attached(
    tmp_path,
):
    source = _system("complete")
    path = tmp_path / "permutation.h5msm"
    modular.write_modular_file(
        path,
        topology=source.topology,
        molecular_mechanics=MolecularMechanics(partial_charge=[0.25, -0.25]),
        mechanics_n_atoms=2,
        associations=[_link("molecular_mechanics", "topology", indices=[1, 0])],
    )
    layers = modular.read_modular_file(path)
    np.testing.assert_array_equal(layers["associations"][0]["indices"], [1, 0])
    np.testing.assert_array_equal(
        layers["molecular_mechanics"].partial_charge, [0.25, -0.25]
    )
    with pytest.raises(ValueError, match="identity associations"):
        modular.read_molsys_file(path)


def test_mechanics_only_context_remains_an_independent_layer(tmp_path):
    path = tmp_path / "mechanics_only.h5msm"
    modular.write_modular_file(
        path,
        molecular_mechanics=MolecularMechanics(forcefield="request"),
        mechanics_n_atoms=7,
    )
    assert (
        modular.read_modular_file(path)["molecular_mechanics"].forcefield == "request"
    )
    assert modular.read_axis_sizes(path) == {("molecular_mechanics", None, "atom"): 7}
    with pytest.raises(ValueError, match="mechanics-only"):
        modular.read_molsys_file(path)


def test_explicitly_empty_mechanics_keeps_its_independent_presence(tmp_path):
    source = _system("complete")
    path = tmp_path / "empty_mechanics.h5msm"
    modular.write_modular_file(
        path,
        topology=source.topology,
        molecular_mechanics=MolecularMechanics(),
        mechanics_n_atoms=2,
        associations=[_link("molecular_mechanics", "topology")],
    )
    assert modular.read_modular_file(path)["molecular_mechanics"] is not None
    with pytest.raises(ValueError, match="empty mechanics layer.*presence marker"):
        modular.read_molsys_file(path)


@pytest.mark.parametrize(
    "report", ["partial_charge_assignment", "atom_type_assignment"]
)
def test_present_empty_reports_survive_native_composition(tmp_path, report):
    source = _system("complete")
    setattr(source.molecular_mechanics, report, {})
    path = tmp_path / "empty_report.h5msm"
    modular.write_molsys_file(path, source)
    restored = modular.read_molsys_file(path)
    assert getattr(restored.molecular_mechanics, report) == {}
    rewritten = tmp_path / "rewritten.h5msm"
    modular.write_molsys_file(rewritten, restored)
    assert (
        getattr(modular.read_molsys_file(rewritten).molecular_mechanics, report) == {}
    )


@pytest.mark.parametrize("damage", ["type", "version", "root_field", "root_attribute"])
def test_unsupported_root_metadata_is_not_silently_ignored(tmp_path, damage):
    path = tmp_path / "unsupported.h5msm"
    modular.write_molsys_file(path, _system("complete"))
    with h5py.File(path, "a") as file:
        if damage == "root_field":
            file.create_group("unrepresented")
        elif damage == "root_attribute":
            file.attrs["unrepresented"] = "not in this schema"
        else:
            file.attrs[damage] = "unsupported"
    with pytest.raises(ValueError, match="Unsupported"):
        modular.read_modular_file(path)


def test_time_only_structures_do_not_provide_a_mechanical_atom_axis(tmp_path):
    structures = Structures(time=msm.pyunitwizard.quantity([0.0, 1.0], "ps"))
    source = MolSys._from_partial_domains(structures=structures)
    path = tmp_path / "time_only.h5msm"
    modular.write_molsys_file(path, source)
    restored = modular.read_molsys_file(path)
    assert restored.get_n_atoms() is None and restored.structures.n_structures == 2
    source.molecular_mechanics.forcefield = "request"
    with pytest.raises(ValueError, match="atom count"):
        modular.write_molsys_file(tmp_path / "unsupported.h5msm", source)
    assert not (tmp_path / "unsupported.h5msm").exists()
    independent = tmp_path / "independent.h5msm"
    modular.write_modular_file(
        independent,
        structures=structures,
        molecular_mechanics=source.molecular_mechanics,
        mechanics_n_atoms=7,
    )
    with pytest.raises(ValueError, match="compatible native atom domain"):
        modular.read_molsys_file(independent)


def test_write_failure_after_partial_staging_publishes_nothing(tmp_path, monkeypatch):
    source = _system("complete")

    def fail(root, *args, **kwargs):
        root.create_dataset("partial", data=np.arange(3))
        raise RuntimeError("simulated late encoder failure")

    monkeypatch.setattr(modular, "write_independent_structures", fail)
    with pytest.raises(RuntimeError, match="late encoder"):
        modular.write_molsys_file(tmp_path / "failed.h5msm", source)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize(
    "extension", ["molsys", "topology", "structures", "state", "table"]
)
def test_unrepresented_native_extensions_are_refused_before_publication(
    tmp_path, extension
):
    source = _system("complete")
    if extension == "table":
        source.topology.atoms.attrs["unrepresented"] = 1
    else:
        target = {
            "molsys": source,
            "topology": source.topology,
            "structures": source.structures,
            "state": source.chemical_states._states[0],
        }[extension]
        target.unrepresented = None
    with pytest.raises(ValueError, match="[Uu]ntyped|[Uu]nrepresented|[Uu]nsupported"):
        modular.write_molsys_file(tmp_path / "refused.h5msm", source)
    assert not list(tmp_path.iterdir())


def test_current_public_05_defaults_and_refusals_are_unchanged(tmp_path):
    source = _system("complete")
    old = tmp_path / "public05.h5msm"
    msm.h5msm.write(source, old)
    assert modular.read_molsys_file(old).get_n_atoms() == 2
    assert modular.read_modular_file(old, layers="molecular_mechanics") == {
        "molecular_mechanics": None
    }
    with h5py.File(old, "r") as file:
        assert file.attrs["version"] == "0.5"
    source.molecular_mechanics.forcefield = "request"
    with pytest.raises(ValueError, match="molecular mechanics"):
        msm.h5msm.write(source, tmp_path / "public_refused.h5msm")
    development = tmp_path / "private06.h5msm"
    modular.write_molsys_file(development, source)
    assert msm.h5msm.read(development).molecular_mechanics.forcefield == "request"


def test_default_association_vocabulary_does_not_expand_05():
    sizes = {("molecular_mechanics", None, "atom"): 2, ("topology", None, "atom"): 2}
    with pytest.raises(ValueError, match="unsupported axis or layer"):
        normalize_associations([_link("molecular_mechanics", "topology")], sizes)


def test_identity_metadata_does_not_materialize_the_atom_population(monkeypatch):
    sizes = {
        ("molecular_mechanics", None, "atom"): 10**9,
        ("topology", None, "atom"): 10**9,
        ("structures", None, "structure"): 1,
        ("chemical_states", None, "state"): 2,
    }

    def no_population(*args, **kwargs):
        raise AssertionError(
            "Identity metadata must not allocate an atom-index vector."
        )

    monkeypatch.setattr(np, "arange", no_population)
    links = [
        _link("molecular_mechanics", "topology"),
        _link("structures", "chemical_states", axis="structure_state", indices=[0]),
    ]
    normalized = normalize_associations(
        links,
        sizes,
        layers={"topology", "molecular_mechanics", "structures", "chemical_states"},
    )
    assert normalized[0]["indices"] == "identity"
    np.testing.assert_array_equal(normalized[1]["indices"], [0])


def _hdf_snapshot(source):
    """Observe values under the two documented HDF transport normalizations.

    Structural schema 1 restores textual labels as object arrays. QuantityRecord
    restores scalar quantities as zero-dimensional arrays while retaining their
    numeric dtype and unit. Everything else keeps the strict checkpoint oracle.
    """
    from tests.native.test_prepared_system_checkpoint import _snapshot

    result = _snapshot(source)
    labels = result["structures"]["structure_id"]
    if labels is not None and all(isinstance(value, str) for value in labels["values"]):
        labels["dtype"] = "object"
    for name in (
        "cutoff_distance",
        "switch_distance",
        "hydrogen_mass",
        "salt_concentration",
        "kappa",
    ):
        value = result["mechanics"][name]
        if value is not None and not isinstance(value["magnitude"], dict):
            magnitude = np.asarray(value["magnitude"])
            value["magnitude"] = {
                "dtype": str(magnitude.dtype),
                "shape": [],
                "values": magnitude.item(),
            }
    return result


@pytest.mark.parametrize("scope", ["complete", "projected", "merged"])
@pytest.mark.parametrize("route", ["private", "public"])
def test_prepared_whole_file_in_a_fresh_reader_retains_provenance_and_edit_ownership(
    tmp_path, scope, route
):
    from tests.native.test_prepared_system_checkpoint import (
        _pdbqt_texts,
        _prepared,
        _snapshot,
    )

    (tmp_path / "case.json").write_text(json.dumps({"scope": scope, "route": route}))
    source = _prepared(scope)
    path = tmp_path / "prepared06.h5msm"
    unchanged = _snapshot(source)
    expected = _hdf_snapshot(source)
    exports = _pdbqt_texts(source)
    if route == "public":
        msm.h5msm.write(source, path, format_version="0.6")
    else:
        modular.write_molsys_file(path, source)
    assert _snapshot(source) == unchanged
    (tmp_path / "expected.json").write_text(json.dumps(expected))
    (tmp_path / "exports.json").write_text(json.dumps(exports))
    script = """
import builtins,json,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
original_import=builtins.__import__
def guarded(name,*args,**kwargs):
    if name.split('.')[0] in {'rdkit','openmm','ackredit'}:raise ImportError('Backend deliberately unavailable: '+name)
    return original_import(name,*args,**kwargs)
builtins.__import__=guarded
import pyunitwizard as puw
with puw.context(standard_units=['angstrom','fs','coulomb','K','mole','dalton','kJ/mol','radians']):
    keys=['default_form','default_parser','standard_units','provenance']
    policy={key:puw.configure.report()[key] for key in keys}
    import molsysmt as msm
    import numpy as np
    from molsysmt._private.h5msm_storage.modular import read_molsys_file
    from tests.native.test_prepared_system_checkpoint import _pdbqt_texts
    from tests.form.file_h5msm.test_modular_mechanics import _hdf_snapshot
    current=msm.__version__
    try:
        msm.__version__='999.0.0+reader.probe'
        restored=msm.h5msm.read(sys.argv[1]) if sys.argv[4]=="public" else read_molsys_file(sys.argv[1])
    finally:msm.__version__=current
    actual=_hdf_snapshot(restored)
    Path(sys.argv[2]).with_name("actual.json").write_text(json.dumps(actual))
    assert actual==json.loads(Path(sys.argv[2]).read_text())
    if sys.argv[4]=="public":
        assert _hdf_snapshot(msm.convert(sys.argv[1]))==actual
    assert _pdbqt_texts(restored)==json.loads(Path(sys.argv[3]).read_text())
    xyz=puw.get_value(restored.structures.coordinates,to_unit='nm').copy()
    msm.structure.translate(restored,translation=puw.quantity([1,0,0],'nm'),structure_indices=[2],in_place=True)
    np.testing.assert_allclose(puw.get_value(restored.structures.coordinates,to_unit='nm')[2],xyz[2]+[1,0,0])
    assert restored.interactions['synthetic'].n_interactions==0
    assert restored.interactions['synthetic'].evaluated_structure_indices.tolist()==[0]
    assert all(_pdbqt_texts(restored))
    assert {key:puw.configure.report()[key] for key in keys}==policy
    assert not any(name.split('.')[0] in {'rdkit','openmm','ackredit'} for name in sys.modules)
    print(json.dumps({'restored':True,'reexport_identical':True,'edit_invalidates_analysis':True,'no_engines':True,'policy_preserved':True}))
"""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            str(path),
            str(tmp_path / "expected.json"),
            str(tmp_path / "exports.json"),
            route,
        ],
        env=os.environ.copy(),
        text=True,
        capture_output=True,
        timeout=60,
    )
    (tmp_path / "reader_result.json").write_text(
        json.dumps(
            {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["edit_invalidates_analysis"]
