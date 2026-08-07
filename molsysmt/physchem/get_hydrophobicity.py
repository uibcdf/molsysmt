from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt.physchem.groups._lookup import group_table_value
from molsysmt._private.smonitor import InternalAlgorithmError
import numpy as np

@arg_digest()
def get_hydrophobicity(molecular_system, element='group', selection='all', definition='eisenberg', syntax='MolSysMT',
                      skip_digestion=False):
    """
    Hydrophobicity index per residue group from a reference scale.

    Returns a dimensionless hydrophobicity value for each selected residue
    group, looked up from one of several published hydrophobicity scales.
    Values are normalized or consensus-derived depending on the chosen scale.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    element : {'group'}, default 'group'
        Hierarchical element for which hydrophobicity is returned.  Only
        ``'group'`` (residue level) is currently supported.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of groups to include in the output.
    definition : {'eisenberg', 'rao', 'sweet', 'kyte', 'abraham', 'bull', \
'guy', 'miyazawa', 'roseman', 'wolfenden', 'chothia', 'hopp', \
'manavalan', 'black', 'fauchere'}, default 'eisenberg'
        Hydrophobicity scale to use.  All scales are taken from the ExPASy
        ProtScale resource.  The default ``'eisenberg'`` is the normalized
        consensus scale (Eisenberg et al., 1984).
    syntax : str, default 'MolSysMT'
        Selection syntax.
    skip_digestion : bool, default False
        If ``True``, bypass argument validation (for internal use only).

    Returns
    -------
    numpy.ndarray
        1-D array of shape ``(n_groups,)`` with dimensionless hydrophobicity
        values for the selected residues.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported ``definition`` is requested.

    Notes
    -----
    Supported scales and their primary references:

    * ``'eisenberg'``: Eisenberg D. et al. *J. Mol. Biol.* 179:125–142 (1984).
    * ``'rao'``: Rao M.J.K., Argos P. *Biochim. Biophys. Acta* 869:197–214 (1986).
    * ``'kyte'``: Kyte J., Doolittle R.F. *J. Mol. Biol.* 157:105–132 (1982).
    * ``'hopp'``: Hopp T.P., Woods K.R. *Proc. Natl. Acad. Sci.* 78:3824–3828 (1981).
    * ``'chothia'``: Chothia C. *J. Mol. Biol.* 105:1–14 (1976).
    * ``'wolfenden'``: Wolfenden R. et al. *Science* 206:575–577 (1979).
    * Other scales follow their respective original publications as indexed in ExPASy ProtScale.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if element != 'group':
        raise InternalAlgorithmError("Unexpected empty state", caller="molsysmt.physchem.get_hydrophobicity")
    if definition == 'eisenberg':
        from .groups.hydrophobicity import eisenberg as values
    elif definition == 'rao':
        from .groups.hydrophobicity import rao as values
    elif definition == 'sweet':
        from .groups.hydrophobicity import sweet as values
    elif definition == 'kyte':
        from .groups.hydrophobicity import kyte as values
    elif definition == 'abraham':
        from .groups.hydrophobicity import abraham as values
    elif definition == 'bull':
        from .groups.hydrophobicity import bull as values
    elif definition == 'guy':
        from .groups.hydrophobicity import guy as values
    elif definition == 'miyazawa':
        from .groups.hydrophobicity import miyazawa as values
    elif definition == 'roseman':
        from .groups.hydrophobicity import roseman as values
    elif definition == 'wolfenden':
        from .groups.hydrophobicity import wolfenden as values
    elif definition == 'chothia':
        from .groups.hydrophobicity import chothia as values
    elif definition == 'hopp':
        from .groups.hydrophobicity import hopp as values
    elif definition == 'manavalan':
        from .groups.hydrophobicity import manavalan as values
    elif definition == 'black':
        from .groups.hydrophobicity import black as values
    elif definition == 'fauchere':
        from .groups.hydrophobicity import fauchere as values
    else:
        print(definition)
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element='group', selection=selection, name=True)

    output = []

    for ii in group_types:
        output.append(group_table_value(values, ii))

    output = np.array(output)

    return output

