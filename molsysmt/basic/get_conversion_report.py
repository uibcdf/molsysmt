"""Inspecting conversion losses without performing the requested conversion."""

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError


@arg_digest()
def get_conversion_report(
    molecular_system,
    to_form="molsysmt.MolSys",
    selection="all",
    structure_indices="all",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Getting a conversion preflight report without creating the destination.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT form, or a composition of forms.
    to_form : str, pathlib.Path or list, default='molsysmt.MolSys'
        Target form name or output filename. Default is 'molsysmt.MolSys'.
        A list returns one report per target, in the requested order.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Selection of atoms to be converted. Default is 'all'.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based) to be converted. Default is 'all'.
    syntax : str, default='MolSysMT'
        Selection syntax. Default is 'MolSysMT'.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    ConversionReport or list of ConversionReport
        Immutable reports with outcome, detected issues, audited scopes and
        is_exhaustive. Source files may be read, but the source is not mutated
        and no destination file is created or overwritten.

    Raises
    ------
    ArgumentError
        If arguments or explicit structure indices are invalid.
    FormatError
        If inspecting a source encounters an unsupported file encoding.

    Notes
    -----
    Uses the same preflight as convert(strict=True) and convert(return_report=True).
    A report without detected losses is a preservation guarantee only within
    its audited scopes. Check is_exhaustive before drawing broader conclusions.
    This is not a test of converter availability, dependency availability or
    successful writing. It does not accept converter-specific options such as
    ctfile_version or discard_properties; these remain arguments of convert.

    See Also
    --------
    convert : Convert a system, optionally rejecting detected losses.
    ConversionReport : Inspect the report contract and serialization.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.native import Structures
    >>> molsys = Structures()
    >>> report = msm.get_conversion_report(molsys, to_form='molsysmt.StructuresDict')
    >>> report.to_form, report.is_exhaustive, report.is_lossy
    ('molsysmt.StructuresDict', True, False)

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Get_Conversion_Report` for preflight limitations.

    .. versionadded:: 1.0.0
    """

    from os import PathLike

    from molsysmt._private.conversion_report import build_conversion_report
    from molsysmt._private.h5msm import maybe_read_modular_h5msm

    from ._index_validation import validate_structure_indices
    from .get_form import get_form

    targets = list(to_form) if isinstance(to_form, (list, tuple)) else [to_form]
    if any(not isinstance(target, (str, PathLike)) for target in targets):
        raise ArgumentError(
            "to_form",
            value=to_form,
            caller=__name__,
            message="Supply a target form or filename, or a flat list of targets.",
        )
    molecular_system = maybe_read_modular_h5msm(molecular_system)
    from_form = get_form(molecular_system)
    if isinstance(from_form, (list, tuple)) and len(from_form) == 1:
        molecular_system, from_form = molecular_system[0], from_form[0]
    structure_indices = validate_structure_indices(
        molecular_system, structure_indices, __name__
    )
    reports = [
        build_conversion_report(
            molecular_system,
            from_form,
            target,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
        )
        for target in targets
    ]
    return reports if isinstance(to_form, (list, tuple)) else reports[0]
