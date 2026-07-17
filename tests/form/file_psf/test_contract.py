"""Testing the contractual CHARMM PSF read path."""

import numpy as np
import pytest

import molsysmt as msm


PSF_TEXT = """PSF EXT XPLOR

         1 !NTITLE
 REMARKS generated for adapter contract testing

         3 !NATOM
         1 SEG      4        LIG      C1       CT1      0.250000       12.0110
         2 SEG      4        LIG      O1       OT      -0.500000       15.9990
         3 SEG      4        LIG      H1       HT       0.250000        1.0080

         2 !NBOND: bonds
         1         2         2         3

         0 !NTHETA: angles

         0 !NPHI: dihedrals

         0 !NIMPHI: impropers

         0 !NDON: donors

         0 !NACC: acceptors

         0 !NNB

         0         0         0         0

         1         0 !NGRP NST2
         0         0         0
"""


@pytest.fixture
def psf_file(tmp_path):
    """Creating a small PSF with nonzero partial charges."""

    path = tmp_path / 'contract.psf'
    path.write_text(PSF_TEXT)
    return str(path)


def test_psf_to_native_preserves_identity_connectivity_and_mechanics(psf_file):
    molecular_system = msm.convert(psf_file, to_form='molsysmt.MolSys')

    assert molecular_system.topology.atoms['atom_id'].tolist() == ['1', '2', '3']
    assert molecular_system.topology.atoms['atom_type'].tolist() == ['C', 'O', 'H']
    assert molecular_system.molecular_mechanics.atom_ff_type.tolist() == [
        'CT1', 'OT', 'HT'
    ]
    assert np.allclose(
        molecular_system.molecular_mechanics.partial_charge.astype(float),
        [0.25, -0.5, 0.25],
    )
    assert molecular_system.topology.n_bonds == 2
    assert molecular_system.topology.bonds['bond_type'].tolist() == [
        'covalent', 'covalent'
    ]
    assert molecular_system.topology.bonds['evidence'].tolist() == [
        'explicit', 'explicit'
    ]
    assert 'bond_order' not in molecular_system.topology.bonds
    assert molecular_system.structures.n_structures == 0


def test_psf_public_get_delivers_aligned_force_field_attributes(psf_file):
    partial_charge, atom_ff_type = msm.get(
        psf_file,
        element='atom',
        selection=[2, 0],
        partial_charge=True,
        atom_ff_type=True,
    )

    assert np.allclose(msm.pyunitwizard.get_value(partial_charge), [0.25, 0.25])
    assert atom_ff_type.tolist() == ['HT', 'CT1']
    assert msm.has_attribute(psf_file, 'partial_charge')
    assert msm.has_attribute(psf_file, 'atom_ff_type')
    assert not msm.has_attribute(psf_file, 'bond_order')


def test_psf_native_subset_keeps_topology_and_mechanics_aligned(psf_file):
    molecular_system = msm.convert(
        psf_file,
        to_form='molsysmt.MolSys',
        selection=[2, 0],
    )

    assert molecular_system.topology.atoms['atom_id'].tolist() == ['1', '3']
    assert molecular_system.molecular_mechanics.atom_ff_type.tolist() == [
        'CT1', 'HT'
    ]
    assert np.allclose(
        molecular_system.molecular_mechanics.partial_charge.astype(float),
        [0.25, 0.25],
    )
    assert molecular_system.topology.n_bonds == 0


def test_psf_openmm_topology_materializes_the_requested_subset(psf_file):
    topology = msm.convert(
        psf_file,
        to_form='openmm.Topology',
        selection=[0, 1],
    )

    assert [atom.id for atom in topology.atoms()] == ['1', '2']
    assert topology.getNumBonds() == 1


def test_psf_self_copy_uses_the_requested_output_name(psf_file, tmp_path):
    output = tmp_path / 'copy.psf'

    observed = msm.convert(psf_file, to_form=str(output))

    assert observed == str(output)
    assert output.read_text() == PSF_TEXT
