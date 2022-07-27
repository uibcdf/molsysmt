from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_biopython_Seq(item, group_indices='all'):

    if check:

        digest_item(item, 'string:aminoacids1')
        group_indices = digest_group_indices(group_indices)

    try:
        from Bio.Seq import Seq as bio_Seq
        #from Bio.Alphabet.IUPAC import ExtendedIUPACProtein
    except:
        raise LibraryNotFoundError('biopython')

    #tmp_item = bio_Seq(item, ExtendedIUPACProtein())
    tmp_item = bio_Seq(item)

    return tmp_item

