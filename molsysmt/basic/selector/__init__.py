from . import molsysmt
from . import molsysmt_new
from . import mdtraj
from . import amber
from . import nglview
from . import mdanalysis

## Selection Syntaxes
_dict_select = {
        'MolSysMT': molsysmt.select,
        'MolSysMT_NEW': molsysmt_new.select,
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

