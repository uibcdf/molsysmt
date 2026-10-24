from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "copy"])
@arg_digest()
def copy(molecular_system, output_filename=None, skip_digestion=False):
    """
    Creating an independent copy of a molecular system.

    Resident objects use their independent-copy protocol. Without a destination,
    supported file forms create a private temporary copy owned by the current
    Python process. An explicit output filename instead creates a persistent
    caller-owned copy. Raw copying preserves file bytes and format version
    without loading the molecular system into memory.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    output_filename : str or pathlib.Path, default=None
        None creates session-owned temporary copies of file members. An explicit
        destination addresses one file and is never automatically deleted.
        Existing distinct files may be overwritten; directories and source
        aliases are rejected. One filename cannot address a composite source.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
     molecular system or list of molecular systems
        A new molecular system (or list of systems if the input is a sequence), independent
        of the original and in the same form as the input.
        When `output_filename` is given for a file-based form, the returned object follows
        the form-specific handler’s semantics (typically the path or a file-form handle).


    Raises
    ------
    NotSupportedFormError
        If the input molecular system has an unsupported form.
    ArgumentError
        If an explicit file destination aliases its source, names a directory,
        or a single destination is supplied for a composite source.


    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Automatic paths remain valid until normal interpreter shutdown, independently
      of path-string references or garbage collection. MolSysMT attempts to remove
      only its owned files at shutdown; abrupt termination or locked files can
      leave leftovers. Use an explicit destination for data that must outlive
      the process. Temporary copies retain their suffix and private read/write
      permissions, including when the source is read-only.
    - Composite inputs without a destination retain their member forms: resident
      members detach and file members receive individual temporary paths.
    - Copying retains a legacy file version; it does not migrate H5MSM. Copying
      does not add a format's missing write capabilities; use a native MolSys
      when a subsequent transformation requires one.


    See Also
    --------
    :func:`molsysmt.basic.convert`
        Convert a molecular system into another form.


    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys_A = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'])
    >>> molsys_B = msm.copy(molsys_A)
    >>> msm.compare(molsys_A, molsys_B, rule='equal')
    True
    >>> id(molsys_A) == id(molsys_B)
    False
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as directory:
    ...     source = msm.convert(molsys_A, to_form=Path(directory) / 'source.h5msm')
    ...     destination = msm.copy(source,
    ...         output_filename=Path(directory) / 'snapshot.h5msm')
    ...     temporary = msm.copy(source)
    ...     copied_form = msm.get_form(destination)
    >>> copied_form
    'file:h5msm'
    >>> Path(temporary).is_file()
    True


    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Copy`.

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.files_and_directories import validate_copy_destination
    from molsysmt._private.smonitor import ArgumentError
    from molsysmt.form import _dict_modules

    from . import get_form

    form_in = get_form(molecular_system)

    composite = isinstance(form_in, (list, tuple))
    if composite and output_filename is not None:
        raise ArgumentError(
            "output_filename",
            caller="molsysmt.basic.copy",
            message="One output_filename cannot address a composite source; copy its files individually or convert to molsysmt.MolSys.",
        )
    items = (
        zip(form_in, molecular_system) if composite else [(form_in, molecular_system)]
    )
    for item_form, item in items:
        if output_filename is not None and _dict_modules[item_form].form_type == "file":
            validate_copy_destination(
                item, output_filename, caller="molsysmt.basic.copy"
            )

    if output_filename is None:
        if not isinstance(form_in, (list, tuple)):
            form_in = [form_in]
            molecular_system = [molecular_system]

        output = []

        try:
            for item_form, item in zip(form_in, molecular_system):
                output_item = _dict_modules[item_form].copy(item)
                output.append(output_item)
        except BaseException:
            from molsysmt._private.session_files import discard_copy

            for copied_form, copied_item in zip(form_in, output):
                if _dict_modules[copied_form].form_type == "file":
                    discard_copy(copied_item)
            raise

        if len(output) == 1:
            output = output[0]

    else:
        output = _dict_modules[form_in].copy(
            molecular_system, output_filename=output_filename
        )

    return output
