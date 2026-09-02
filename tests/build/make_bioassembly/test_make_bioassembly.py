"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time


def test_make_bioassembly_molsysmt_MolSys_1():
    molsys = msm.convert('3U71')
    n_atoms = msm.get(molsys, element='system', n_atoms=True)
    molsys_2 = msm.build.make_bioassembly(molsys)
    molsys_3 = msm.build.make_bioassembly(molsys, bioassembly='1')
    n_atoms_2 = msm.get(molsys_2, element='system', n_atoms=True)
    n_atoms_3 = msm.get(molsys_3, element='system', n_atoms=True)
    assert n_atoms==755
    assert n_atoms_2==1510
    assert n_atoms_3==1510


def test_generated_copies_receive_unique_chain_ids_and_keep_author_names():
    molsys = msm.convert(systems['Barnase-Barstar']['1brs.bcif.gz'])
    bioassembly = msm.get(molsys, bioassembly=True)['1']
    all_chain_indices = np.arange(msm.get(molsys, element='system', n_chains=True))

    bioassembly = {
        'rotations': [bioassembly['rotations'][0]] * 3,
        'translations': [bioassembly['translations'][0]] * 3,
        'chain_indices': [all_chain_indices] * 3,
    }

    source_chain_ids, source_chain_names = msm.get(
        molsys,
        element='chain',
        chain_id=True,
        chain_name=True,
    )
    assembled = msm.build.make_bioassembly(
        molsys,
        bioassembly=bioassembly,
        skip_digestion=True,
    )
    chain_ids, chain_names = msm.get(
        assembled,
        element='chain',
        chain_id=True,
        chain_name=True,
    )

    assert source_chain_ids == list('ABCDEFGHIJKL')
    expected_chain_ids = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    expected_chain_ids.extend(['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ'])

    assert chain_ids == expected_chain_ids
    assert len(set(chain_ids)) == len(chain_ids)
    assert chain_names == source_chain_names * 3
    assert len(msm.select(assembled, selection="chain_id == 'A'")) == len(
        msm.select(molsys, selection="chain_id == 'A'")
    )
