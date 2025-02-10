def is_form(item):

    output = False

    if type(item) is str:

        if item.startswith('amino_acids_1:'):

            output = True

        else:

            from ..string_amino_acids_3 import is_form as is_string_amino_acids_3

            if not is_string_amino_acids_3(item):

                from Bio.SeqUtils.ProtParam import ProteinAnalysis
                analysed_seq = ProteinAnalysis(item)
                output = (sum(analysed_seq.amino_acids_percent.values()) > 99.0)

    return output

