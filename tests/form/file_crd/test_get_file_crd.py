"""Testing direct metadata access for CHARMM CRD files."""

import molsysmt as msm


def test_get_n_atoms_reads_the_crd_header():
    crd = msm.systems['POPC']['popc.crd']

    assert msm.get(crd, element='system', n_atoms=True) == 134
