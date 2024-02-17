from molsysmt._private.digestion import digest

@digest(form='file:msmpk')
def to_molsysmt_MolSysOld(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from ..molsysmt_MolSysOld import extract as extract_molsysmt_MolSysOld
    from molsysmt import pyunitwizard as puw
    import pickle
    import bz2

    fff = bz2.BZ2File(item,'rb')
    aux_item = pickle.load(fff)
    fff.close()

    # lengths with nm values and time in ps

    if aux_item.structures.coordinates is not None:
        value = aux_item.structures.coordinates
        quantity = puw.quantity(value, 'nm')
        aux_item.structures.coordinates = puw.standardize(quantity)

    if aux_item.structures.box is not None:
        value = aux_item.structures.box
        quantity = puw.quantity(value, 'nm')
        aux_item.structures.box = puw.standardize(quantity)

    if aux_item.structures.time is not None:
        value = aux_item.structures.time
        quantity = puw.quantity(value, 'ps')
        aux_item.structures.time = puw.standardize(quantity)

    from molsysmt.native import MolSysOld
    from copy import deepcopy

    tmp_item = MolSysOld()

    tmp_item.topology.atoms_dataframe = deepcopy(aux_item.topology.atoms_dataframe)
    tmp_item.topology.bonds_dataframe = deepcopy(aux_item.topology.bonds_dataframe)

    tmp_item.structures.n_atoms = aux_item.structures.n_atoms
    tmp_item.structures.n_structures = aux_item.structures.n_structures

    tmp_item.structures.coordinates = deepcopy(aux_item.structures.coordinates)
    tmp_item.structures.box = deepcopy(aux_item.structures.box)
    tmp_item.structures.time = deepcopy(aux_item.structures.time)

    del aux_item

    tmp_item = extract_molsysmt_MolSysOld(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item

