from molsysmt._private.argdigest import arg_digest


@arg_digest(form='molsysmt.StructuresDict')
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
    """Appending one structural block to a native structures dictionary."""

    from molsysmt.native import Structures
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures.to_molsysmt_StructuresDict import (
        to_molsysmt_StructuresDict,
    )

    target = to_molsysmt_Structures(to_item, skip_digestion=True)
    if item is None:
        item = Structures(
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
            skip_digestion=True,
        )
    target.append_structures(
        item,
        attribute_policy=attribute_policy,
        skip_digestion=True,
    )
    output = to_molsysmt_StructuresDict(target, skip_digestion=True)
    to_item.clear()
    to_item.update(output)
