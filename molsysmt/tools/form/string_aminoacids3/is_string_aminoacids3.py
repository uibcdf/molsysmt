
def is_string_aminoacids3(item):

    output = False

    if type(item) is str:

        from Bio.SeqUtils.ProtParam import ProteinAnalysis
        from Bio.SeqUtils import seq1

        analysed_seq = ProteinAnalysis(seq1(item))
        output = (sum(analysed_seq.get_amino_acids_percent().values()) > 0.95)

    return output

