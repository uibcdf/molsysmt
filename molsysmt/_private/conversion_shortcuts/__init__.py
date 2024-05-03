_multiple_conversion_shortcuts = {}


from .to_molsysmt_MolSys import molsysmt_Topology_and_molsysmt_Structures_to_molsysmt_MolSys
from .to_molsysmt_MolSys import file_prmtop_and_file_inpcrd_to_molsysmt_MolSys
from .to_molsysmt_MolSys import file_psf_and_file_dcd_to_molsysmt_MolSys
from .to_molsysmt_MolSys import file_psf_and_file_crd_to_molsysmt_MolSys
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

_multiple_conversion_shortcuts[tuple(sorted(('file:psf','file:crd')))]={
        'molsysmt.MolSys': file_psf_and_file_crd_to_molsysmt_MolSys
        }

_multiple_conversion_shortcuts[tuple(sorted(('file:gro','file:xtc')))]={
        'molsysmt.MolSys': file_gro_and_file_xtc_to_molsysmt_MolSys
        }

from .to_molsysmt_Topology import molsysmt_Topology_and_molsysmt_Structures_to_molsysmt_Topology
from .to_molsysmt_Topology import file_prmtop_and_file_inpcrd_to_molsysmt_Topology
from .to_molsysmt_Topology import file_psf_and_file_dcd_to_molsysmt_Topology
from .to_molsysmt_Topology import file_psf_and_file_crd_to_molsysmt_Topology
from .to_molsysmt_Topology import file_gro_and_file_xtc_to_molsysmt_Topology

_multiple_conversion_shortcuts[tuple(sorted(('molsysmt.Topology','molsysmt.Structures')))]={
        'molsysmt.Topology': molsysmt_Topology_and_molsysmt_Structures_to_molsysmt_Topology
        }

_multiple_conversion_shortcuts[tuple(sorted(('file:prmtop','file:inpcrd')))]={
        'molsysmt.Topology': file_prmtop_and_file_inpcrd_to_molsysmt_Topology
        }

_multiple_conversion_shortcuts[tuple(sorted(('file:psf','file:dcd')))]={
        'molsysmt.Topology': file_psf_and_file_dcd_to_molsysmt_Topology
        }

_multiple_conversion_shortcuts[tuple(sorted(('file:psf','file:crd')))]={
        'molsysmt.Topology': file_psf_and_file_crd_to_molsysmt_Topology
        }

_multiple_conversion_shortcuts[tuple(sorted(('file:gro','file:xtc')))]={
        'molsysmt.Topology': file_gro_and_file_xtc_to_molsysmt_Topology
        }

