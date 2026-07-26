from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.Structures', to_form='molsysmt.Structures')
def append_structures(
    to_item,
    item=None,
    structure_id=None,
    time=None,
    coordinates=None,
    velocities=None,
    box=None,
    temperature=None,
    potential_energy=None,
    kinetic_energy=None,
    b_factor=None,
    alternate_location=None,
    occupancy=None,
    attribute_policy='intersection',
    skip_digestion=False,
):

    if item is not None:
        to_item.append_structures(
            item,
            attribute_policy=attribute_policy,
            skip_digestion=True,
        )
    else:
        to_item.append(
            structure_id=structure_id,
            time=time,
            coordinates=coordinates,
            velocities=velocities,
            box=box,
            temperature=temperature,
            potential_energy=potential_energy,
            kinetic_energy=kinetic_energy,
            b_factor=b_factor,
            alternate_location=alternate_location,
            occupancy=occupancy,
            attribute_policy=attribute_policy,
            skip_digestion=True,
        )

    pass
