_multiple_conversion_shortcuts = {}


from .to_molsysmt_MolSys import molsysmt_Topology_and_molsysmt_Structures_to_molsysmt_MolSys
from .to_molsysmt_MolSys import file_prmtop_and_file_inpcrd_to_molsysmt_MolSys
from .to_molsysmt_MolSys import file_psf_and_file_dcd_to_molsysmt_MolSys
from .to_molsysmt_MolSys import file_gro_and_file_xtc_to_molsysmt_MolSys

_multiple_conversion_shortcuts[tuple(sorted(('molsysmt.Topology','molsysmt.Structures')))]={
        'molsysmt.MolSys': molsysmt_Topology_and_molsysmt_Structures_to_molsysmt_MolSys
        }

_multiple_conversion_shortcuts[tuple(sorted(('file:prmtop','file:inpcrd')))]={
        'molsysmt.MolSys': file_prmtop_and_file_inpcrd_to_molsysmt_MolSys
        }

_multiple_conversion_shortcuts[tuple(sorted(('file:psf','file:dcd')))]={
        'molsysmt.MolSys': file_psf_and_file_dcd_to_molsysmt_MolSys
        }

_multiple_conversion_shortcuts[tuple(sorted(('file:gro','file:xtc')))]={
        'molsysmt.MolSys': file_gro_and_file_xtc_to_molsysmt_MolSys
        }
