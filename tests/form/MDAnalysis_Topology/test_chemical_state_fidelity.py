"""Testing MDAnalysis chemical-state conversion fidelity."""

import pytest

import molsysmt as msm


def _chemical_universe():
    mda = pytest.importorskip('MDAnalysis')
    from MDAnalysis.core.topologyattrs import Bonds, FormalCharges

    universe = mda.Universe.empty(
        4,
        n_residues=1,
        atom_resindex=[0, 0, 0, 0],
        trajectory=True,
    )
    for attribute, values in (
        ('names', ['C1', 'C2', 'N', 'O']),
        ('types', ['C', 'C', 'N', 'O']),
        ('ids', [1, 2, 3, 4]),
        ('resnames', ['LIG']),
        ('resids', [7]),
        ('segids', ['A']),
    ):
        universe.add_TopologyAttr(attribute, values)
    universe.add_TopologyAttr(FormalCharges([0, 0, 1, -1]))
    universe.add_TopologyAttr(
        Bonds(
            [(0, 1), (1, 2), (2, 3)],
            types=['aromatic', 'opaque-class', 'dative'],
            guessed=[False, True, False],
            order=[1.5, 2, None],
        )
    )
    return universe


@pytest.mark.parametrize('source_kind', ['topology', 'universe'])
def test_mdanalysis_preserves_independent_chemistry(source_kind):
    universe = _chemical_universe()
    source = universe._topology if source_kind == 'topology' else universe

    topology = msm.convert(source, to_form='molsysmt.Topology')

    assert msm.get(topology, element='atom', formal_charge=True) == [0, 0, 1, -1]
    assert msm.get(topology, element='bond', fractional_bond_order=True)[0] == 1.5
    assert msm.get(topology, element='bond', bond_order=True)[1] == 2
    assert msm.get(topology, element='bond', bond_is_aromatic=True)[0] is True
    assert msm.get(topology, element='bond', bond_type=True)[2] == 'dative'
    assert msm.get(topology, element='bond', bond_evidence=True) == [
        'explicit', 'inferred', 'explicit'
    ]
    assert msm.get(topology, element='system', n_components=True) == 2


def test_mdanalysis_opaque_type_is_reported_and_strictly_rejected():
    source = _chemical_universe()._topology

    _, report = msm.convert(
        source,
        to_form='molsysmt.Topology',
        return_report=True,
    )

    assert report.outcome == 'lossy'
    assert {issue.attribute for issue in report.issues} == {'bond_source_type'}
    with pytest.raises(msm.NotCompatibleConversionError, match='Strict conversion'):
        msm.convert(source, to_form='molsysmt.Topology', strict=True)


def test_mdanalysis_universe_writes_selected_atoms_to_pdb(tmp_path):
    universe = _chemical_universe()
    output_filename = tmp_path / 'selected.pdb'

    msm.convert(universe, to_form=str(output_filename), selection=[0, 2])

    topology = msm.convert(str(output_filename), to_form='molsysmt.Topology')
    assert topology.n_atoms == 2
