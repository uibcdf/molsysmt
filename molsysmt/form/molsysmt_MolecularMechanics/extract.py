from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
from molsysmt._private.variables import is_all


@arg_digest(form='molsysmt.MolecularMechanics')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True,
            skip_digestion=False):
    """
    Extracting a subset of elements or structures from form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolecularMechanics
        Resulting object in molsysmt.MolecularMechanics form.

    .. versionadded:: 1.0.0
    """

    form = 'molsysmt.MolecularMechanics'

    if not is_all(structure_indices):
        raise NotWithThisFormError(
            caller='molsysmt.extract',
            form=form,
            requested_attribute='structure_indices',
            message=f"Form {form!r} does not contain structures to extract.",
        )

    if is_all(atom_indices):
        return item.copy() if copy_if_all else item

    if item.atoms_ff is None:
        raise NotWithThisFormError(
            caller='molsysmt.extract',
            form=form,
            requested_attribute='atom_indices',
            message=f"Form {form!r} has no per-atom parameters to extract.",
        )

    output = item.copy()
    output.atoms_ff = output.atoms_ff.iloc[atom_indices].reset_index(drop=True)
    return output
