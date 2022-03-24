from .is_string_pdb_text import is_string_pdb_text
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.structure_indices import digest_structure_indices

def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_string_pdb_text(item)
        except:
            raise WrongFormError('string:pdb_text')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    try:
        from mdtraj import load_topology as mdtraj_load_topology
    except:
        raise LibraryNotFoundError('MDTraj')

    from io import StringIO
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    tmp_io = StringIO()
    tmp_io.write(tmp_item)
    tmp_io.close()

    tmp_item = mdtraj_load_topology(tmp_io)

    return tmp_item

