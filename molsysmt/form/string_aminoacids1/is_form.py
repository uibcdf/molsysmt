def is_form(item):

    output = False

    if type(item) is str:

        if item.startswith('aminoacids1:'):

            output = True

        else:

            from ..string_aminoacids3 import is_form as is_string_aminoacids3

            if not is_string_aminoacids3(item):

                from Bio.SeqUtils.ProtParam import ProteinAnalysis
                analysed_seq = ProteinAnalysis(item)
                output = (sum(analysed_seq.get_amino_acids_percent().values()) > 0.99)

    return output

