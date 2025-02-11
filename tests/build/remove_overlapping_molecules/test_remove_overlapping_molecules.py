"""
Unit and regression test for the is solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import pytest
import molsysmt as msm
import numpy as np
import sys

def test_remove_overlapping_molecules_MolSys_1():

    box = np.zeros((3,3))
    box[0,0] = 3.0
    box[1,1] = 3.0
    box[2,2] = 3.0
    box = msm.pyunitwizard.quantity(box, 'nm')
    
    water_box = msm.build.make_water_box(box)
    
    peptide = msm.build.build_peptide('ACEALAALANME')
    peptide = msm.structure.center(peptide, center_coordinates=0.5*box.diagonal())
    
    molsys = msm.merge([water_box, peptide])
    
    n_waters_before = msm.get(molsys, n_waters=True)
    
    new_molsys = msm.build.remove_overlapping_molecules(molsys, selection='atom_type!="H" and molecule_type=="water"',
                                                        selection_2='atom_type!="H" and molecule_type=="peptide"',
                                                        threshold='3 angstroms')
    
    n_waters_after = msm.get(new_molsys, n_waters=True)
    
    contact_map = msm.structure.get_contacts(new_molsys, selection='atom_type!="H" and molecule_type=="water"',
                                             selection_2='atom_type!="H" and molecule_type=="peptide"',
                                             threshold='3 angstroms', pbc=True)
    
    assert n_waters_before == 899
    assert n_waters_after == 881
    assert np.any(contact_map) == False

