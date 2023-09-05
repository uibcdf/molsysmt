from . import native
from . import mdtraj
from . import amber
from . import nglview
from . import mdanalysis


_dict_select = {
        'MolSysMT': native.select,
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

