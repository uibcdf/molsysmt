from molsysmt._private.digestion import digest

form = 'molsysviewer.MolSysView'


@digest(form=form)
def append_structures(item, structure_id=None, time=None, coordinates=None, velocities=None,
                      box=None, temperature=None, potential_energy=None, kinetic_energy=None,
                      atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from ..molsysmt_MolSys.append_structures import append_structures as molsys_append_structures

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    if tmp_item is None:
        return None

    molsys_append_structures(
        tmp_item,
        structure_id=structure_id,
        time=time,
        coordinates=coordinates,
        velocities=velocities,
        box=box,
        temperature=temperature,
        potential_energy=potential_energy,
        kinetic_energy=kinetic_energy,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )

    item._molsys = tmp_item
    return None
