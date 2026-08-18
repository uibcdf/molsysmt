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
    """
    Converting from file:psf to molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    coordinates : object, default=None
        Argument coordinates.
    structure_id : object, default=None
        Argument structure_id.
    box : object, default=None
        Argument box.
    time : object, default=None
        Argument time.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.


    .. versionadded:: 1.0.0
    """

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
