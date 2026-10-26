import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError, NotImplementedMethodError
from molsysmt.physchem.groups._lookup import group_table_value


@arg_digest()
def get_hydrophobicity(
    molecular_system,
    element="group",
    selection="all",
    definition="eisenberg",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Getting hydrophobicity scores for selected amino-acid groups.

    Returns a dimensionless hydrophobicity value for each selected residue
    group, looked up from one of several published hydrophobicity scales.
    Values are normalized or consensus-derived depending on the chosen scale.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='group'
        Only 'group' is supported. Other levels raise ArgumentChoiceError
        before resolving selection; no aggregate is inferred.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    definition : object, default='eisenberg'
        Published scale used for the selected population.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    numpy.ndarray
        1-D array of shape ``(n_groups,)`` with dimensionless hydrophobicity
        values for the selected residues.


    Raises
    ------
    ArgumentChoiceError
        If element requests an unsupported population level.
    NotImplementedMethodError
        If an unsupported ``definition`` is requested.


    Notes
    -----
    Selection strings are resolved with the requested syntax on the supported
    atom/group axis. Explicit numeric indices retain order and repetitions;
    an empty supported population returns an empty result of the same type.
    A table lookup does not assign a chemical state or validate a molecule's
    chemistry. Unknown non-placeholder amino-acid groups retain their table
    diagnostics; no missing property is silently invented.

    Supported scales and their primary references:

    * ``'eisenberg'``: Eisenberg D. et al. *J. Mol. Biol.* 179:125–142 (1984).
    * ``'rao'``: Rao M.J.K., Argos P. *Biochim. Biophys. Acta* 869:197–214 (1986).
    * ``'kyte'``: Kyte J., Doolittle R.F. *J. Mol. Biol.* 157:105–132 (1982).
    * ``'hopp'``: Hopp T.P., Woods K.R. *Proc. Natl. Acad. Sci.* 78:3824–3828 (1981).
    * ``'chothia'``: Chothia C. *J. Mol. Biol.* 105:1–14 (1976).
    * ``'wolfenden'``: Wolfenden R. et al. *Science* 206:575–577 (1979).
    * Other scales follow their respective original publications as indexed in ExPASy ProtScale.


    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0])
    >>> result = msm.physchem.get_hydrophobicity(molsys, element='group', selection=[3, 1, 3])
    >>> len(result)
    3

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_hydrophobicity` for selection, supported scope and reference definitions.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if element != "group":
        raise ArgumentChoiceError(
            argument="element",
            value=element,
            choices=["group"],
            caller="molsysmt.physchem.get_hydrophobicity",
        )

    if definition == "eisenberg":
        from .groups.hydrophobicity import eisenberg as values
    elif definition == "rao":
        from .groups.hydrophobicity import rao as values
    elif definition == "sweet":
        from .groups.hydrophobicity import sweet as values
    elif definition == "kyte":
        from .groups.hydrophobicity import kyte as values
    elif definition == "abraham":
        from .groups.hydrophobicity import abraham as values
    elif definition == "bull":
        from .groups.hydrophobicity import bull as values
    elif definition == "guy":
        from .groups.hydrophobicity import guy as values
    elif definition == "miyazawa":
        from .groups.hydrophobicity import miyazawa as values
    elif definition == "roseman":
        from .groups.hydrophobicity import roseman as values
    elif definition == "wolfenden":
        from .groups.hydrophobicity import wolfenden as values
    elif definition == "chothia":
        from .groups.hydrophobicity import chothia as values
    elif definition == "hopp":
        from .groups.hydrophobicity import hopp as values
    elif definition == "manavalan":
        from .groups.hydrophobicity import manavalan as values
    elif definition == "black":
        from .groups.hydrophobicity import black as values
    elif definition == "fauchere":
        from .groups.hydrophobicity import fauchere as values
    else:
        print(definition)
        raise NotImplementedMethodError()

    group_types = get(
        molecular_system, element="group", selection=selection, name=True, syntax=syntax
    )

    output = []

    for ii in group_types:
        output.append(
            group_table_value(
                values,
                ii,
                table="hydrophobicity",
                caller="molsysmt.physchem.get_hydrophobicity",
            )
        )

    output = np.array(output)

    return output
