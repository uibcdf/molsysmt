from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.atom_indices import complementary_atom_indices
from molsysmt._private.structure_indices import complementary_structure_indices
from molsysmt._private.variables import is_all


@signal(tags=["api", "structure"])
@arg_digest()
def remove(
    molecular_system,
    selection=None,
    structure_indices=None,
    to_form=None,
    syntax="MolSysMT",
    in_place=False,
    skip_digestion=False,
):
    """
    Removing atoms or structures from a molecular system.

    By default, return an independent molecular system retaining the complementary
    atom and structure indices. ``None`` removes nothing on that axis. Explicit
    in-place removal prepares the complete subset before updating a native object.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default=None
        Atom indices or selection expression identifying atoms to remove.
        ``None`` or an empty selection removes no atoms; ``'all'`` removes all atoms.
    structure_indices : int, list, tuple, or numpy.ndarray, default=None
        Positional structure indices to remove. Repetitions remove a structure
        once. ``None`` or an empty list removes nothing; ``'all'`` removes all structures.
    to_form : str, list of str, or None, default=None
        Target molecular-system form; ``None`` preserves the singular input form
        or assembles complementary inputs as MolSys. In-place removal requires None.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    in_place : bool, default=False
        False returns an independent result, including no-op removals. True updates
        a native MolSys or standalone Topology/Structures and returns None.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molecular system or None
        Independent extracted system when ``in_place=False``; None after updating
        the original native object when ``in_place=True``.


    Raises
    ------
    NotSupportedFormError
        If the molecular system is provided in an unsupported form.
    ArgumentError
        If the selection or `structure_indices` are invalid or incompatible
        with the system, or in-place mutation is unsupported for the target.
        Explicit atom and structure indices are range checked.


    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.
    - Removal delegates complementary indices to :func:`molsysmt.basic.extract`.
      Named analyses retain its projection, source maps and coverage semantics;
      no detector runs. Removed participants lose their observations. Surviving
      observations describe the original evaluated scope, not a new calculation.
    - In-place removal keeps the system object identity and replaces its native
      domains together. Old domain/result references remain historical snapshots.
      Client extension attributes are retained without remapping derived caches.
      Invalid requests or candidate-preparation failures leave the input unchanged.
      Preparing a subset can temporarily retain both source and candidate data;
      ``in_place=True`` does not promise an allocation-free edit.
    - An attached Topology or Structures domain cannot be resized in place on its
      own. Pass its owning MolSys. Other forms and complementary inputs support
      out-of-place extraction through their normal adapters.
    - A file or file-handler input requires an explicit non-file output form
      or a distinct destination path through ``to_form``, even for no-op removal.
      A path or a second handle to the source file is not an independent result.
    - Before the #406 pre-1.0 correction, ``in_place=True`` was an ignored default.
      The False default preserves existing return-new calls; callers explicitly
      passing True must now use the mutated object rather than the return value.


    See Also
    --------
    :func:`molsysmt.select`
        Select atoms or structures from a molecular system.
    :func:`molsysmt.basic.extract` :
        Extract a subset of atoms/structures into a new molecular system.


    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.native import MolSys
    >>> molsys = MolSys(n_atoms=3)
    >>> molsys_A = msm.remove(molsys, selection=[1])
    >>> (molsys.get(n_atoms=True), molsys_A.get(n_atoms=True))
    (3, 2)
    >>> msm.remove(molsys_A, selection=[0], in_place=True)
    >>> molsys_A.get(n_atoms=True)
    1


    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Remove`.

    .. versionadded:: 1.0.0
    """

    from . import extract, get, select

    if in_place:
        from molsysmt.native._subset import validate_removal_target

        validate_removal_target(molecular_system, to_form)
    else:
        _validate_file_destination(molecular_system, to_form)

    atom_indices_to_be_kept = "all"
    structure_indices_to_be_kept = "all"

    if structure_indices is not None:
        from ._index_validation import validate_structure_indices

        structure_indices = validate_structure_indices(
            molecular_system, structure_indices, "molsysmt.remove"
        )

    if selection is not None:
        from ._index_validation import validate_element_indices

        atom_indices_to_be_removed = select(
            molecular_system, selection=selection, syntax=syntax, skip_digestion=True
        )
        atom_indices_to_be_removed = validate_element_indices(
            molecular_system,
            atom_indices_to_be_removed,
            "atom",
            "selection",
            "molsysmt.remove",
        )
        if atom_indices_to_be_removed:
            atom_indices_to_be_kept = complementary_atom_indices(
                molecular_system, atom_indices_to_be_removed
            )

    if structure_indices is not None:
        if is_all(structure_indices):
            n_structures = get(
                molecular_system,
                element="system",
                n_structures=True,
                skip_digestion=True,
            )
            structure_indices = list(range(n_structures))
        if structure_indices:
            structure_indices_to_be_kept = complementary_structure_indices(
                molecular_system, structure_indices
            )

    if (
        in_place
        and is_all(atom_indices_to_be_kept)
        and is_all(structure_indices_to_be_kept)
    ):
        return None

    tmp_item = extract(
        molecular_system,
        selection=atom_indices_to_be_kept,
        structure_indices=structure_indices_to_be_kept,
        to_form=to_form,
        copy_if_all=True,
        skip_digestion=True,
    )

    if in_place:
        from molsysmt.native._subset import publish_subset

        publish_subset(molecular_system, tmp_item)
        return None

    if isinstance(tmp_item, (list, tuple)) and len(tmp_item) == 1:
        tmp_item = tmp_item[0]

    return tmp_item


def _validate_file_destination(molecular_system, to_form):
    """Require explicit independent output for disk-backed extraction."""
    from os.path import samefile
    from pathlib import Path

    from molsysmt._private.smonitor import ArgumentError
    from molsysmt.form import is_file

    from . import get_form

    form = get_form(molecular_system)
    if not isinstance(form, str) or not (
        form.startswith("file:") or form.endswith("FileHandler")
    ):
        return
    outputs = to_form if isinstance(to_form, (list, tuple)) else [to_form]
    resource = getattr(molecular_system, "file", None)
    filename = (
        molecular_system
        if form.startswith("file:")
        else getattr(resource, "filename", getattr(resource, "name", None))
    )
    for output in outputs:
        ambiguous = output is None or (
            isinstance(output, str)
            and (output.startswith("file:") or output.endswith("FileHandler"))
        )
        if not ambiguous and filename is not None and is_file(output):
            source_path, destination = Path(filename), Path(output)
            ambiguous = source_path.resolve() == destination.resolve()
            if not ambiguous:
                try:
                    ambiguous = samefile(source_path, destination)
                except FileNotFoundError:
                    pass
        if ambiguous:
            raise ArgumentError(
                "to_form",
                value=to_form,
                caller="molsysmt.basic.remove",
                message=(
                    "Removal from a file or file handler requires an explicit "
                    "in-memory to_form or a distinct output path, including "
                    "for empty removals. The source file must remain unchanged."
                ),
            )
