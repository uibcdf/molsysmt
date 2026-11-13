"""Keep selected Modeller topology and coordinates on the same atom axis."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
@pytest.mark.parametrize("operation", ["extract", "convert"])
def test_modeller_subset_matches_source_sorted_unique_inventory(
    openmm_pdb_ensemble, length, time, operation
):
    from openmm import unit
    from openmm.app import Modeller

    source = Modeller(openmm_pdb_ensemble.topology, openmm_pdb_ensemble.positions)
    xyz = source.positions.value_in_unit(unit.nanometer)
    names = [a.name for a in source.topology.atoms()]
    with puw.context(standard_units=[length, time, "radians"]):
        arguments = dict(selection=[3, 1, 1], structure_indices=[0])
        result = (
            msm.extract(source, **arguments)
            if operation == "extract"
            else msm.convert(source, to_form="openmm.Modeller", **arguments)
        )
        assert result is not source
        assert [a.name for a in result.topology.atoms()] == [names[1], names[3]]
        np.testing.assert_allclose(
            puw.get_value(result.positions, to_unit="nm"),
            np.asarray(xyz)[[1, 3]],
            rtol=0,
            atol=1e-12,
        )
        assert len(result.positions) == result.topology.getNumAtoms()
    assert source.topology.getNumAtoms() == 4


def test_modeller_copy_is_independent_and_full_extract_can_reuse(openmm_pdb_ensemble):
    from openmm.app import Modeller

    source = Modeller(openmm_pdb_ensemble.topology, openmm_pdb_ensemble.positions)
    independent = msm.copy(source)
    assert independent is not source
    assert independent.topology is not source.topology
    independent.topology.addChain("new")
    assert source.topology.getNumChains() == 1
    assert msm.extract(source, copy_if_all=False) is source
