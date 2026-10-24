from molsysmt._private.argdigest import arg_digest
from molsysmt.element.group.amino_acid.codes import aa1_to_aa3


@arg_digest(form="string:amino_acids_1")
def to_string_amino_acids_3(item, group_indices="all", skip_digestion=False):
    """
    Converting from string:amino_acids_1 to string:amino_acids_3.


    Parameters
    ----------
    item : molecular system
        Sequence text in the declared alphabet; an explicit amino_acids prefix is supported.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Original group positions in requested order; repetitions are retained.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_3
        Resulting object in string:amino_acids_3 form.


    .. versionadded:: 1.0.0
    """

    from .extract import extract

    selected = extract(item, group_indices=group_indices, skip_digestion=True)
    sequence = selected.removeprefix("amino_acids_1:")
    output = "".join(
        ("TER" if code == "*" else aa1_to_aa3.get(code.upper(), "XAA")).title()
        for code in sequence
    )

    return output if output else "amino_acids_3:"
