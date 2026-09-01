import numpy as np
from molsysmt import pyunitwizard as puw
from smonitor import signal
from molsysmt._private.argdigest import arg_digest
from molsysmt.basic import get
from molsysmt._private import rust_backend as _kernels
from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit

@signal(tags=['api', 'structure'])
@arg_digest()
def get_dihedral_angles(molecular_system, selection='all', dihedral_quartets=None,
                        structure_indices='all', syntax='MolSysMT', pbc=False,
                        use_gpu=None, **kwargs):
    """
    Compute dihedral angles for a set of atom quartets over one or more structures.

    Two usage modes are available:

    * **Explicit quartets** — provide ``dihedral_quartets`` as an array of shape
      ``(n_quartets, 4)`` containing the atom indices that define each dihedral.
    * **Named backbone/side-chain dihedrals** — omit ``dihedral_quartets`` and pass
      keyword arguments such as ``phi=True``, ``psi=True``, ``omega=True``,
      ``chi1=True``, etc.  The required quartets are then obtained from
      ``molsysmt.topology.get_dihedral_quartets`` for the atoms in ``selection``.
      When more than one named type is requested the function returns a list of
      arrays, one per type.

    Angles are computed in the minimum-image convention when ``pbc=True`` and the
    system has a periodic box.  Results are always returned in the MolSysMT standard
    angle unit (degrees).


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    dihedral_quartets : object, default=None
        Argument dihedral_quartets.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    pbc : bool, default=False
        Whether to take periodic boundary conditions into account.
    use_gpu : bool, default=None
        Whether to perform computation using GPU acceleration.

    Returns
    -------
    quantity or list of quantity
        PyUnitWizard angle quantity of shape ``(n_structures, n_quartets)`` in the
        standard angle unit (degrees).  When more than one named dihedral type is
        requested, a list of such quantities is returned — one per type, in the
        order the kwargs were provided.


    .. versionadded:: 1.0.0
    """

    # phi, psi, omega, chi1, chi2, chi3, chi4, chi5

    angles_split=None

    if dihedral_quartets is None:

        from molsysmt.topology import get_dihedral_quartets

        dihedral_quartets = []
        angles_split=[]
        for key in kwargs.keys():
            if kwargs[key]:
                aux_dihedral_quartets = get_dihedral_quartets(molecular_system, selection=selection,
                                                     syntax=syntax, **{key:True})
                dihedral_quartets.append(aux_dihedral_quartets)
                angles_split.append(len(aux_dihedral_quartets))
        dihedral_quartets = np.concatenate(dihedral_quartets)

    atom_indices=[]
    n_quartets=dihedral_quartets.shape[0]
    aux_dihedral_quartets=np.zeros((n_quartets,4), dtype=np.int64)
    aux_dict={}
    mm=0
    for ii in range(n_quartets):
        for jj in range(4):
            kk = dihedral_quartets[ii,jj]
            if kk in aux_dict:
                aux_dihedral_quartets[ii,jj]=aux_dict[kk]
            else:
                aux_dict[kk]=mm
                atom_indices.append(kk)
                aux_dihedral_quartets[ii,jj]=mm
                mm+=1
    dihedral_quartets=aux_dihedral_quartets
    del(aux_dict, aux_dihedral_quartets)

    coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                      coordinates=True)

    coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)

    if pbc:

        box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

        if box is not None:
            if box[0] is not None:
                box = np.asarray(puw.get_value(box, to_unit=length_unit), dtype=np.float64)
                angles = _kernels.get_mic_dihedral_angles(coordinates, box, dihedral_quartets)
                del(coordinates, box, dihedral_quartets)
            else:
                pbc = False
        else:
            pbc = False

    if not pbc:

        from molsysmt._private.gpu import resolve_use_gpu
        payload = coordinates.shape[0] * dihedral_quartets.shape[0]
        if resolve_use_gpu(use_gpu, payload):
            from molsysmt.lib.structure.get_dihedral_angles_cuda import (
                get_dihedral_angles as _gpu_dihedral,
            )
            angles = _gpu_dihedral(coordinates, dihedral_quartets)
        else:
            angles = _kernels.get_dihedral_angles(coordinates, dihedral_quartets)
        del(coordinates, dihedral_quartets)


    angles = puw.quantity(angles, 'radians')
    angles = puw.standardize(angles)

    if angles_split is None:
        output=angles
    elif len(angles_split)==1:
        output=angles
    else:
        output = []
        ii=0
        for jj in angles_split:
            output.append(angles[:,ii:ii+jj])
            ii+=jj

    del(angles)

    return output
