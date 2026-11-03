"""Resolve supplied classic donor roles through the public covalent-path tool."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def supplied_donor_pairs(molecular_system, donors, selection, syntax, argument, caller):
    """Validate declared roles before filtering anchors, preserving every D-H row."""
    from molsysmt.basic import get, select
    from molsysmt.chemical_states import get_covalent_paths
    from molsysmt.physchem.atoms.mass import physical as elements

    symbols = np.asarray(get(molecular_system, element="atom", atom_type=True))
    if np.any(donors >= len(symbols)):
        raise ArgumentError(argument, value=donors, caller=caller)
    donor_symbols = symbols[donors if donors.ndim == 1 else donors[:, 0]]
    chemical_elements = [symbol for symbol, mass in elements.items() if mass > 0]
    if np.any(~np.isin(donor_symbols, chemical_elements)) or np.any(
        donor_symbols == "H"
    ):
        raise ArgumentError(
            argument,
            value=donors,
            caller=caller,
            message="Donor anchors require declared non-hydrogen chemical elements.",
        )
    if donors.ndim == 1:
        pairs = get_covalent_paths(
            molecular_system, path=[np.unique(donors), 'atom_type=="H"']
        )
    else:
        if np.any(symbols[donors[:, 1]] != "H"):
            raise ArgumentError(
                argument,
                value=donors,
                caller=caller,
                message="Pair columns must contain a non-hydrogen donor and its hydrogen.",
            )
        paths = get_covalent_paths(
            molecular_system, path=[np.unique(donors[:, 0]), np.unique(donors[:, 1])]
        )
        rows = np.dtype([("donor", np.int64), ("hydrogen", np.int64)])
        valid = np.isin(
            np.ascontiguousarray(donors).view(rows).ravel(),
            np.ascontiguousarray(paths).view(rows).ravel(),
        )
        if not valid.all():
            raise ArgumentError(
                argument,
                value=donors,
                caller=caller,
                message="Every supplied donor-H pair must be covalently bonded.",
            )
        pairs = donors
    anchors = select(molecular_system, selection=selection, syntax=syntax)
    return np.unique(pairs[np.isin(pairs[:, 0], anchors)], axis=0)
