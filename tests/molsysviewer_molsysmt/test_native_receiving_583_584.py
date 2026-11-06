"""Receive repaired native provenance and mechanics readers through the facade."""

import warnings

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.smonitor.warnings import AckreditTrackingWarning


@pytest.mark.parametrize("policy", ["none", "hbonds", "all_bonds", "h_angles"])
def test_bound_mechanical_reads_keep_native_flags_and_do_not_edit(
    alanine_molsys, policy
):
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    msm.set(molsys, constraints=policy)
    with msv.new_view(molsys) as view:
        before = view.addons.molsysmt.get_sync_status()
        reader = view.addons.molsysmt.basic.get
        assert reader(constraints=True, forcefield=False, n_atoms=True) == [policy, 22]
        assert reader(constraints=False) == []
        assert reader(output_type="dictionary", constraints=True) == {
            "constraints": policy
        }
        with pytest.raises(ArgumentError, match="constraints"):
            reader(constraints="none")
        assert view.molsys.molecular_mechanics.constraints == policy
        assert view.addons.molsysmt.get_sync_status() == before


@pytest.mark.parametrize("order", [("implicit", "solvate"), ("solvate", "implicit")])
def test_bound_independent_model_operations_share_canonical_software(
    alanine_molsys, order
):
    ackredit = pytest.importorskip("ackredit")
    openmm = pytest.importorskip("openmm")
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    records = []
    with msv.new_view(molsys) as view:
        source = view.molsys
        before = view.addons.molsysmt.get_sync_status()
        coordinates = msm.pyunitwizard.get_value(source.structures.coordinates).copy()
        with warnings.catch_warnings(record=True) as observed:
            warnings.simplefilter("always", AckreditTrackingWarning)
            with ackredit.session("bound-native-models"):
                view.addons.molsysmt.molecular_mechanics.get_engine_forcefield(
                    "AMBER14", implicit_solvent="OBC1"
                )
                assert not ackredit.get_used_items()
                for operation in order:
                    with ackredit.capture(operation) as run:
                        if operation == "implicit":
                            result = view.addons.molsysmt.basic.convert(
                                to_form="openmm.System", implicit_solvent="OBC1"
                            )
                            assert result.getNumParticles() == 22
                            assert any(
                                isinstance(force, openmm.CustomGBForce)
                                for force in result.getForces()
                            )
                        else:
                            result = view.addons.molsysmt.build.solvate(
                                engine="OpenMM",
                                box_shape="cubic",
                                clearance="0.35 nm",
                                n_cations=0,
                                n_anions=0,
                                random_seed=1,
                            )
                            assert (
                                result is not source
                                and msm.get(result, n_waters=True) > 0
                            )
                    attribution = run.attribution.to_dict()
                    software_id = f"software:openmm:{openmm.__version__}"
                    records.append(
                        next(
                            item
                            for item in attribution["items"]
                            if item["id"] == software_id
                        )
                    )
                    assert any(
                        use["item_id"] == software_id
                        and use["roles"] == ["executed_software"]
                        for use in attribution["uses"]
                    )
        assert not [
            warning
            for warning in observed
            if issubclass(warning.category, AckreditTrackingWarning)
        ]
        assert records[0] == records[1]
        assert records[0]["title"] == "OpenMM"
        assert view.molsys is source
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(source.structures.coordinates), coordinates
        )
        assert view.addons.molsysmt.get_sync_status() == before
