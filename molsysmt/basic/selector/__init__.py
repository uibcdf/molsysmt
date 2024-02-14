from . import molsysmt
from . import molsysmt_old
from . import mdtraj
from . import amber
from . import nglview
from . import mdanalysis

## Selection Syntaxes
_dict_select = {
        'MolSysMT_OLD': molsysmt_old.select,
        'MolSysMT': molsysmt.select,
        'MDTraj': mdtraj.select,
        'Amber': amber.select,
        'NGLView': nglview.select,
        'MDAnalysis': mdanalysis.select,
        }

_dict_indices_to_selection = {
        'MDTraj': mdtraj.indices_to_selection,
        'Amber': amber.indices_to_selection,
        'NGLView': nglview.indices_to_selection,
        'MDAnalysis': mdanalysis.indices_to_selection,
        }

