def is_form(item):
    """
    Checking whether an item is an instance of form string:amino_acids_1.

    Parameters
    ----------
    item : string:amino_acids_1
        Source item in string:amino_acids_1 form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    output = False

    if type(item) is str:

        if item.startswith('amino_acids_1:'):

            output = True

        else:

            from ..string_amino_acids_3.is_form import is_form as is_string_amino_acids_3

            if not is_string_amino_acids_3(item):

                from Bio.SeqUtils.ProtParam import ProteinAnalysis
                analysed_seq = ProteinAnalysis(item)
                output = (sum(analysed_seq.amino_acids_percent.values()) > 99.0)

    return output

