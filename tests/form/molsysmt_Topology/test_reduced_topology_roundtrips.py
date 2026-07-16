"""Testing the exact chemical subset shared with compact topology targets."""

import pytest

import molsysmt as msm


def _representable_topology(alanine_molsys):
    topology = alanine_molsys.topology.copy()
    msm.set(
        topology,
        element='atom',
        formal_charge=[1] + [0] * (topology.n_atoms - 1),
    )
    msm.set(topology, element='bond', selection=[0], bond_evidence='explicit')
    msm.set(topology, element='bond', selection=[0], bond_order=2)
    msm.set(topology, element='bond', selection=[0], bond_is_aromatic=True)
    return topology


@pytest.mark.parametrize('target', ['mdtraj.Topology', 'openmm.Topology'])
def test_compact_topology_roundtrip_preserves_formal_charge_order_and_aromaticity(
    alanine_molsys, target
):
    pytest.importorskip(target.split('.')[0])
    source = _representable_topology(alanine_molsys)

    reduced = msm.convert(source, to_form=target)
    observed = msm.convert(reduced, to_form='molsysmt.Topology')

    assert msm.get(observed, element='atom', formal_charge=True)[0] == 1
    assert msm.get(observed, element='bond', selection=[0], bond_order=True) == [2]
    assert msm.get(
        observed, element='bond', selection=[0], bond_is_aromatic=True
    ) == [True]


def test_compact_target_reports_and_strictly_rejects_unsupported_evidence(
    alanine_molsys
):
    pytest.importorskip('mdtraj')
    source = _representable_topology(alanine_molsys)

    output, report = msm.convert(
        source, to_form='mdtraj.Topology', return_report=True
    )

    assert msm.get_form(output) == 'mdtraj.Topology'
    assert report.outcome == 'lossy'
    assert 'bond_evidence' in {issue.attribute for issue in report.issues}
    with pytest.raises(msm.NotCompatibleConversionError, match='Strict conversion'):
        msm.convert(source, to_form='mdtraj.Topology', strict=True)
