from molsysmt._private.digestion import digest
from io import StringIO

@digest(form='string:pdb_text')
def to_molsysmt_PDBFileHandler(item, skip_digestion=False):

    from molsysmt.native import PDBFileHandler

    tmp_item = StringIO(item)

    return PDBFileHandler(tmp_item, io_mode='r')

