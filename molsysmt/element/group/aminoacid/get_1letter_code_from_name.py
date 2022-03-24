
aa3_to_aa1 = {
        'ALA': 'A', # Alanine
        'ARG': 'R', # Arginine
        'ASN': 'N', # Asparagine
        'ASP': 'D', # Aspartic Acid
        'CYS': 'C', # Cysteine
        'GLU': 'E', # Glutamic Acid
        'GLN': 'Q', # Glutamine
        'GLY': 'G', # Glycine
        'HIS': 'H', # Histidine
        'ILE': 'I', # Isoleucine
        'LEU': 'L', # Leucine
        'LYS': 'K', # Lysine
        'MET': 'M', # Methionine
        'PHE': 'F', # Phenylalanine
        'PRO': 'P', # Proline
        'PYL': 'O', # Pyrrolysine
        'SER': 'S', # Serine
        'SEC': 'U', # Selenocysteine
        'THR': 'T', # Threonine
        'TRP': 'W', # Tryptophan
        'TYR': 'Y', # Tyrosine
        'VAL': 'V', # Valine
        'ASX': 'B', # Aspartic acid or Asparagine
        'GLX': 'Z', # Glutamic acid or Glutamine
        'XAA': 'X', # Any amino acid
        'XLE': 'J', # Leucine or Isoleucine
        }

def get_1letter_code_from_name(name):

    return aa3_to_aa1[name]

