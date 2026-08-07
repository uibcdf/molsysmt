from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='biopython.Seq')
@dep_digest('Bio')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices):

        if copy_if_all:
            tmp_item = item.copy()
        else:
            tmp_item = item
    else:
        from Bio.Seq import Seq

        tmp_item = Seq(''.join(str(item[index]) for index in atom_indices))

    return tmp_item
