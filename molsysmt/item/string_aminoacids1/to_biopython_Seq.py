from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='string:aminoacids1')
def to_biopython_Seq(item, group_indices='all'):


    try:
        from Bio.Seq import Seq as bio_Seq
        #from Bio.Alphabet.IUPAC import ExtendedIUPACProtein
    except:
        raise LibraryNotFoundError('biopython')

    #tmp_item = bio_Seq(item, ExtendedIUPACProtein())
    tmp_item = bio_Seq(item)

    return tmp_item

