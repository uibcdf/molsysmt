from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:sdf")
def to_molsysmt_MolSys(
    item,
    atom_indices="all",
    structure_indices="all",
    discard_properties=False,
    skip_digestion=False,
    *,
    stereo_engine=None,
):
    """Converting a single explicit SDF record into native molecular domains.

    Parameters
    ----------
    item : str or pathlib.Path
        Single-record SDF file, with V2000 or V3000 connectivity.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include; source serials remain string IDs.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include. The input has one structure.
    discard_properties : bool, default=False
        Explicitly authorize discarding SD property blocks without native storage.
        Strict conversion still reports and rejects their loss.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    stereo_engine : str or None, default=None
        Keyword-only optional 'rdkit' provider for explicit tetrahedral and
        double-bond interpretation. None retains dependency-free native parsing
        and rejects stereo flags. Query and enhanced stereo remain unsupported.

    Returns
    -------
    molsysmt.MolSys
        Explicit chemistry and all source hydrogens, with angstrom coordinates
        converted through PyUnitWizard to native nanometers.

    Raises
    ------
    FormatError
        For malformed, multiple-record, query, stereo or unsupported data.

    Notes
    -----
    The default needs no RDKit installation and performs no sanitization,
    hydrogen removal, implicit-hydrogen assignment, CIP assignment or Kekule
    aromaticity perception. Explicit stereo_engine='rdkit' invokes the public
    CIP tool before atom extraction, retaining every source hydrogen atom.
    V3000 coordination type 9 becomes a dative relationship. The first source
    endpoint is the donor and the second is the acceptor, following the adapter's
    direction convention; electronic donor suitability is not inferred. These
    bonds do not join native covalent components. CTAB drawing styles are not
    retained in native domains and conversion reports identify their loss.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'], to_form='molsysmt.MolSys')
    >>> molsys.topology.n_atoms
    24

    .. admonition:: Tutorial with more examples

       See :ref:`cookbook-native-sdf` for the supported chemistry, source
       properties, selections and serialization limits.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.ctfile import read_sdf
    from molsysmt._private.variables import is_all
    from molsysmt.basic._index_validation import (
        validate_element_indices,
        validate_structure_indices,
    )
    from molsysmt.form.molsysmt_MolSys.extract import extract

    from ._native import to_native

    output = to_native(
        read_sdf(item, allow_stereo=stereo_engine == "rdkit"),
        discard_properties=discard_properties,
    )
    if stereo_engine is not None:
        from molsysmt.physchem import get_cip_stereochemistry

        report = get_cip_stereochemistry(item, engine=stereo_engine)
        from ._native import store_stereochemistry

        store_stereochemistry(output, report)
    if not is_all(atom_indices):
        atom_indices = validate_element_indices(
            output, atom_indices, "atom", "atom_indices", "file:sdf"
        )
    structure_indices = validate_structure_indices(
        output, structure_indices, "file:sdf"
    )
    if not is_all(atom_indices) or not is_all(structure_indices):
        output = extract(
            output,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )
    return output
