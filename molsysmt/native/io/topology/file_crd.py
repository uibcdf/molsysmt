from molsysmt._private_tools.exceptions import *

def from_file_crd(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_file_crd import to_mdanalysis_Universe as file_crd_to_mdanalysis_Universe
    from molsysmt.forms.api_mdanalysis_Universe import to_molsysmt_Topology as mdanalysis_Universe_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = file_crd_to_mdanalysis_Universe(item,
            molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = mdanalysis_Universe_to_molsysmt_Topology(tmp_item,
            molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_file_crd(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError()

