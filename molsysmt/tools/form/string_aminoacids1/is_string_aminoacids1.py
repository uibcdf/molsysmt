
def is_string_aminoacids1(item):

    output = False

    if type(item) is str:

        from Bio.SeqUtils.ProtParam import ProteinAnalysis
        analysed_seq = ProteinAnalysis(item)
        output = (sum(analysed_seq.get_amino_acids_percent().values()) > 0.95)

    return output

