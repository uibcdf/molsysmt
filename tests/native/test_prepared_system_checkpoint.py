"""Receive existing trusted native checkpoints, without adding a file format."""

import hashlib
import importlib
import json
import os
import pickle
import subprocess
import sys
from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import Structures

puw = msm.pyunitwizard
POLICIES = [("nm", "ps", "elementary_charge"), ("pm", "fs", "coulomb")]


def _plain(value):
    """Observe public data independently; this oracle never restores a system."""
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if value is pd.NA:
        return {"missing": True}
    if isinstance(value, np.generic):
        return {"scalar_dtype": str(value.dtype), "value": _plain(value.item())}
    if isinstance(value, np.ndarray):
        return {
            "dtype": str(value.dtype),
            "shape": list(value.shape),
            "values": _plain(value.tolist()),
        }
    if isinstance(value, pd.DataFrame):
        return {
            "table": _plain(value.to_dict(orient="split")),
            "dtypes": list(map(str, value.dtypes)),
        }
    if isinstance(value, dict):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return {"sequence": type(value).__name__, "values": [_plain(x) for x in value]}
    if puw.is_quantity(value):
        return {
            "unit": str(puw.get_unit(value)),
            "magnitude": _plain(puw.get_value(value)),
        }
    raise TypeError(f"Unobserved checkpoint field type: {type(value).__name__}")


def _snapshot(source):
    return _plain(
        {
            "topology": msm.convert(
                source.topology, to_form="molsysmt.TopologyDict"
            ).data,
            "chemical_states": msm.convert(
                source.chemical_states, to_form="molsysmt.ChemicalStatesDict"
            ).data,
            "structures": msm.convert(
                source.structures, to_form="molsysmt.StructuresDict"
            ),
            "state_associations": source.get(structure_chemical_state_index=True),
            "mechanics": source.molecular_mechanics.to_dict(),
            "mechanical_columns": source.molecular_mechanics.atoms_ff,
            "charge_assignment": source.molecular_mechanics.partial_charge_assignment,
            "type_assignment": source.molecular_mechanics.atom_type_assignment,
            "history": source.chemical_states.get_preparation_history(),
            "interactions": {
                name: result.to_dict() for name, result in source.interactions.items()
            },
        }
    )


def _prepared(scope):
    # Reuse the actual indexed-H molecule and coordinate fixture used by the
    # public charge-assignment guards. RDKit is required only by preparation.
    from tests.build.test_assign_autodock_atom_types import prepared

    source = prepared("CO")
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm")[0]
    source.structures = Structures(
        coordinates=puw.quantity(np.stack([xyz, xyz + 0.1, xyz + 0.2]), "nm"),
        box=puw.quantity(np.tile(np.eye(3) * 4.0, (3, 1, 1)), "nm"),
        time=puw.quantity([0.0, 1.0, 3.0], "ps"),
        structure_id=["pose-a", "pose-b", "pose-c"],
        potential_energy=puw.quantity([-3.0, -2.0, -1.0], "kJ/mol"),
    )
    source = msm.chemical_states.normalize_indexed_hydrogen_policy(source)[
        "molecular_system"
    ]
    source = msm.build.assign_autodock_atom_types(source, typing_scheme="autodock4")
    source = msm.build.assign_partial_charges(source, method="gasteiger_marsili")
    msm.set(source, structure_chemical_state_index=[0, 0, 0])
    if scope == "projected":
        source = msm.extract(source, selection=[5, 1, 0], structure_indices=[2, 0, 2])
    elif scope == "merged":
        source = msm.build.merge_nonpolar_hydrogens(source, typing_scheme="autodock4")
    # These are stored model requests, not a completed force-field calculation.
    source.molecular_mechanics.forcefield = "AMBER14"
    source.molecular_mechanics.implicit_solvent = "OBC2"
    source.molecular_mechanics.cutoff_distance = puw.quantity(12.0, "angstrom")
    source.molecular_mechanics.hydrogen_mass = puw.quantity(2.0, "dalton")
    source.molecular_mechanics.salt_concentration = puw.quantity(0.15, "mole/liter")
    source.interactions = {
        "synthetic": msm.Interactions.from_records(
            [
                {
                    "structure_index": 2,
                    "interaction_type": "synthetic_pair",
                    "participants": [
                        {"role": "first", "atom_indices": [0]},
                        {"role": "second", "atom_indices": [1]},
                    ],
                    "measurements": {"distance": distance},
                }
                for distance in [1.5, 2.0]
            ],
            n_atoms=source.get_n_atoms(),
            n_structures=3,
            evaluated_structure_indices=[0, 2],
            method="checkpoint_fixture",
            measure_units={"distance": "angstrom"},
            software={"fixture": "1"},
        )
    }
    assert source.chemical_states.get_preparation_history()
    return source


def _pdbqt_texts(source):
    return [
        msm.convert(
            source,
            to_form="string:pdbqt_text",
            typing_scheme="autodock4",
            structure_indices=[index],
        )
        for index in [2, 0, 2]
    ]


def _policy():
    report = puw.configure.report()
    return {
        key: deepcopy(report[key])
        for key in ["default_form", "default_parser", "standard_units", "provenance"]
    }


def read_checkpoint(directory):
    """Exercise public reads and continuation in a fresh, backend-blocked process."""

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "Checkpoint restoration must not recalculate an assignment"
        )

    for name in [
        "molsysmt.build.assign_partial_charges",
        "molsysmt.build.assign_autodock_atom_types",
        "molsysmt.physchem.get_partial_charges",
        "molsysmt.physchem.get_autodock_atom_types",
    ]:
        module = importlib.import_module(name)
        setattr(module, name.rsplit(".", 1)[1], forbidden)
    before = _policy()
    current_version = msm.__version__
    try:
        # A reader label must not replace the stored producer, even when the
        # same compatible source is used for this controlled restoration test.
        msm.__version__ = "999.0.0+reader.probe"
        with (directory / "prepared.pkl").open("rb") as stream:
            restored = pickle.load(stream)
    finally:
        msm.__version__ = current_version
    expected = json.loads((directory / "expected.json").read_text())
    assert _snapshot(restored) == expected
    assert _policy() == before
    if (directory / "expect_stale").exists():
        with pytest.raises(StructuralInconsistencyError):
            msm.convert(
                restored,
                to_form="string:pdbqt_text",
                typing_scheme="autodock4",
                structure_indices=[1],
            )
        assert _snapshot(restored) == expected
        assert _policy() == before
        assert not any(
            name.split(".")[0] in {"rdkit", "openmm", "ackredit"}
            for name in sys.modules
        )
        print(
            json.dumps(
                {
                    "restored": True,
                    "stale_assignment_refused": True,
                    "original_producer_retained": True,
                    "assignment_recalculation": False,
                    "policy_preserved": True,
                }
            )
        )
        return
    # Re-export checks the restored named assignments against actual chemistry,
    # values and structure associations through the public writer.
    assert _pdbqt_texts(restored) == json.loads(
        (directory / "expected_pdbqt.json").read_text()
    )
    assert _policy() == before
    assert not any(
        name.split(".")[0] in {"rdkit", "openmm", "ackredit"} for name in sys.modules
    )
    # Restored ownership must work, not merely retain a plausible weak reference.
    before_geometry = puw.get_value(
        restored.structures.coordinates, to_unit="nm"
    ).copy()
    msm.structure.translate(
        restored,
        translation=puw.quantity([1, 0, 0], "nm"),
        structure_indices=[2],
        in_place=True,
    )
    xyz = puw.get_value(restored.structures.coordinates, to_unit="nm")
    np.testing.assert_allclose(
        xyz[2], before_geometry[2] + [1, 0, 0], rtol=0, atol=1e-15
    )
    np.testing.assert_array_equal(xyz[:2], before_geometry[:2])
    assert restored.interactions["synthetic"].n_interactions == 0
    assert restored.interactions["synthetic"].evaluated_structure_indices.tolist() == [
        0
    ]
    assert restored.get(structure_chemical_state_index=True) == [0, 0, 0]
    assert all(_pdbqt_texts(restored))
    print(
        json.dumps(
            {
                "restored": True,
                "assignment_recalculation": False,
                "public_reexport_identical": True,
                "original_producer_retained": True,
                "coordinate_edit_and_invalidation": True,
                "policy_preserved": True,
            }
        )
    )


@pytest.mark.parametrize("scope", ["complete", "projected", "merged"])
@pytest.mark.parametrize("policy", POLICIES)
def test_prepared_checkpoint_retains_full_public_state_in_a_fresh_reader(
    tmp_path, scope, policy
):
    with puw.context(
        standard_units=[*policy, "K", "mole", "dalton", "kJ/mol", "radians"]
    ):
        source = _prepared(scope)
        expected = _snapshot(source)
        texts = _pdbqt_texts(source)
        (tmp_path / "expected.json").write_text(json.dumps(expected))
        (tmp_path / "expected_pdbqt.json").write_text(json.dumps(texts))
        with (tmp_path / "prepared.pkl").open("wb") as stream:
            pickle.dump(source, stream, protocol=pickle.HIGHEST_PROTOCOL)
        assert _snapshot(source) == expected
    _run_reader(tmp_path)
    assert _snapshot(source) == expected


def _run_reader(tmp_path):
    script = """
import builtins, json, sys
from pathlib import Path
original_import = builtins.__import__
def guarded(name, *args, **kwargs):
    if name.split('.')[0] in {'rdkit', 'openmm', 'ackredit'}:
        raise ImportError('Scientific backend deliberately unavailable: ' + name)
    return original_import(name, *args, **kwargs)
builtins.__import__ = guarded
import pyunitwizard as puw
with puw.context(standard_units=['angstrom', 'fs', 'coulomb', 'K', 'mole', 'dalton', 'kJ/mol', 'radians']):
    fields = ['default_form', 'default_parser', 'standard_units', 'provenance']
    chosen = {key: puw.configure.report()[key] for key in fields}
    from tests.native.test_prepared_system_checkpoint import read_checkpoint
    assert {key: puw.configure.report()[key] for key in fields} == chosen
    read_checkpoint(Path(sys.argv[1]))
    assert {key: puw.configure.report()[key] for key in fields} == chosen
"""
    result = subprocess.run(
        [sys.executable, "-c", script, str(tmp_path)],
        capture_output=True,
        text=True,
        timeout=40,
        env=os.environ.copy(),
    )
    (tmp_path / "reader_result.json").write_text(
        json.dumps(
            {
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "pickle_protocol": pickle.HIGHEST_PROTOCOL,
                "checkpoint_sha256": hashlib.sha256(
                    (tmp_path / "prepared.pkl").read_bytes()
                ).hexdigest(),
                "checkpoint_bytes": (tmp_path / "prepared.pkl").stat().st_size,
            },
            indent=2,
        )
    )
    assert result.returncode == 0, result.stdout + result.stderr
    observed = json.loads(result.stdout)
    assert observed["restored"] and observed["policy_preserved"]
    assert observed["original_producer_retained"]
    assert not observed["assignment_recalculation"]
    assert observed.get(
        "stale_assignment_refused", observed.get("public_reexport_identical")
    )


@pytest.mark.parametrize("mutation", ["charges", "types", "chemistry", "association"])
def test_checkpoint_does_not_rebind_stale_assignments(tmp_path, mutation):
    source = _prepared("complete")
    if mutation == "charges":
        source.molecular_mechanics.atoms_ff.loc[0, "partial_charge"] += 0.1
    elif mutation == "types":
        source.molecular_mechanics.atoms_ff.loc[0, "atom_ff_type"] = "OA"
    elif mutation == "chemistry":
        msm.set(source, element="atom", selection=[0], formal_charge=[1])
    else:
        msm.set(source, structure_chemical_state_index=[0, None, 0])
    with pytest.raises(StructuralInconsistencyError):
        msm.convert(
            source,
            to_form="string:pdbqt_text",
            typing_scheme="autodock4",
            structure_indices=[1],
        )
    expected = _snapshot(source)
    (tmp_path / "expected.json").write_text(json.dumps(expected))
    (tmp_path / "expect_stale").touch()
    with (tmp_path / "prepared.pkl").open("wb") as stream:
        pickle.dump(source, stream, protocol=pickle.HIGHEST_PROTOCOL)
    _run_reader(tmp_path)
    assert _snapshot(source) == expected
