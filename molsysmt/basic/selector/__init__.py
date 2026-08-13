from . import molsysmt
from . import mdtraj
from . import nglview
from . import mdanalysis

## Selection Syntaxes
_dict_select = {
        'MolSysMT': molsysmt.select,
        'MDTraj': mdtraj.select,
        'MDAnalysis': mdanalysis.select,
        }

_dict_indices_to_selection = {
        'MDTraj': mdtraj.indices_to_selection,
        'NGLView': nglview.indices_to_selection,
        }
