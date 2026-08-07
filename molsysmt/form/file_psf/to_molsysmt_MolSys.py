from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:psf')
@dep_digest('openmm')
def to_molsysmt_MolSys(
    item,
    atom_indices='all',
    structure_indices='all',
    coordinates=None,
    structure_id=None,
    box=None,
    time=None,
    skip_digestion=False,
):
    """Converting a CHARMM PSF file to a native molecular system."""

    import numpy as np
    from openmm.app import CharmmPsfFile

    from molsysmt._private.variables import is_all
    from molsysmt.form.openmm_Topology.to_molsysmt_Topology import (
        to_molsysmt_Topology,
    )
    from molsysmt.native import MolSys, MolecularMechanics, Structures

    source = CharmmPsfFile(str(item))
    output = MolSys()
    output.topology = to_molsysmt_Topology(
        source.topology,
        get_missing_bonds=False,
        skip_digestion=True,
    )
    output.molecular_mechanics = MolecularMechanics(
        partial_charge=np.asarray(
            [atom.charge for atom in source.atom_list], dtype=np.float64
        ),
        atom_ff_type=np.asarray(
            [str(atom.attype) for atom in source.atom_list], dtype=object
        ),
    )
    output.structures = Structures()
    if any(value is not None for value in (coordinates, structure_id, box, time)):
        output.structures.append(
            coordinates=coordinates,
            structure_id=structure_id,
            box=box,
            time=time,
            skip_digestion=True,
        )

    if not is_all(atom_indices) or not is_all(structure_indices):
        from molsysmt.form.molsysmt_MolSys.extract import extract

        output = extract(
            output,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )

    return output
