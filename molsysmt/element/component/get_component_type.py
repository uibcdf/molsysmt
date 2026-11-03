import pandas as pd

from molsysmt._private.argdigest import arg_digest


@arg_digest()
def get_component_type(
    molecular_system,
    element="component",
    selection="all",
    redefine_indices=False,
    redefine_types=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Getting component types from a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='component'
        Structural element level to query ('atom', 'group', 'component', 'molecule', 'chain', 'entity').
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    redefine_indices : bool, default=False
        Whether to reassign contiguous 0-based indices.
    redefine_types : object, default=False
        Argument redefine_types.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of str
        List of component type classifications ('protein', 'peptide', 'dna', 'water', etc.).


    .. versionadded:: 1.0.0
    """

    from molsysmt.native._component_projection import prepare

    source = prepare(molecular_system, indices=redefine_indices, types=redefine_types)
    return source.get(
        element=element,
        selection=selection,
        syntax=syntax,
        component_type=True,
        skip_digestion=True,
    )


def _get_component_type_from_group_names_and_types(group_names, group_types):

    from molsysmt.configure import min_length_protein

    from ..group.nucleotide import dna_names, rna_names

    n_groups = len(group_types)
    first_group_type = group_types[0]
    last_group_type = group_types[-1]
    first_group_name = group_names[0]

    if first_group_type in ["water", "ion", "small molecule", "lipid"]:
        tmp_type = first_group_type
    elif (first_group_type == "amino acid") or (first_group_type == "terminal capping"):
        if first_group_type == "terminal capping":
            n_groups -= 1
        if last_group_type == "terminal capping":
            n_groups -= 1
        if n_groups >= min_length_protein:
            tmp_type = "protein"
        else:
            tmp_type = "peptide"
    elif first_group_type == "nucleotide":
        tmp_type = "unknown"
        if pd.notna(first_group_name):
            if first_group_name in rna_names:
                tmp_type = "rna"
            elif first_group_name in dna_names:
                tmp_type = "dna"
    elif first_group_type == "saccharide":
        tmp_type = "polysaccharide"
    else:
        tmp_type = "unknown"

    return tmp_type
