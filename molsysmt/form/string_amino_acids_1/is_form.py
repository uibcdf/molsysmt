_STANDARD_AMINO_ACID_CODES = frozenset("ACDEFGHIKLMNPQRSTVWY")


def is_form(item):
    """
    Checking whether an item is an instance of form string:amino_acids_1.


    Parameters
    ----------
    item : molecular system
        Argument item.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.


    .. versionadded:: 1.0.0
    """

    output = False

    if type(item) is str:
        if item.startswith("amino_acids_1:"):
            output = True

        else:
            from ..string_amino_acids_3.is_form import (
                is_form as is_string_amino_acids_3,
            )

            if not is_string_amino_acids_3(item):
                sequence = item.upper()
                if sequence:
                    standard_count = sum(
                        residue in _STANDARD_AMINO_ACID_CODES for residue in sequence
                    )
                    output = 100 * standard_count > 99 * len(sequence)

    return output
