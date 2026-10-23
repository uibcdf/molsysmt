from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="openmm.Modeller")
@dep_digest("openmm")
def to_file_pdb(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    skip_digestion=False,
):
    """
    Converting from openmm.Modeller to file:pdb.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:pdb
        Resulting object in file:pdb form.


    Notes
    -----
    The source adapter builds a native MolSys and reuses its PDB writer.
    Atom selection is applied jointly to topology and positions in source
    order; the source Modeller is not modified. PDB lengths use angstroms.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from tempfile import TemporaryDirectory
    >>> source = msm.systems["T4 lysozyme L99A"]["181l.pdb"]
    >>> modeller = msm.convert(source, to_form='openmm.Modeller')
    >>> with TemporaryDirectory() as directory:
    ...     output = to_file_pdb(modeller, output_filename=f"{directory}/export.pdb")
    ...     assert msm.get_form(output) == 'file:pdb'

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_MolSys.to_file_pdb import (
        to_file_pdb as native_to_file_pdb,
    )

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    return native_to_file_pdb(
        tmp_item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        output_filename=output_filename,
        skip_digestion=True,
    )
