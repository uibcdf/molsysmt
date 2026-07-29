"""Public contracts for assigning molecular-system attributes."""

import molsysmt as msm


def test_set_broadcasts_scalar_chain_id_to_selected_chain(t4_h5msm_molsys):
    molecular_system = t4_h5msm_molsys

    msm.set(
        molecular_system,
        element='chain',
        selection='chain_index==0',
        chain_id='PROTEIN',
    )

    assert msm.get(
        molecular_system,
        element='chain',
        selection='chain_index==0',
        chain_id=True,
    ) == ['PROTEIN']
