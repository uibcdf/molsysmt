"""Sharing source-axis normalization between supported build reports."""

from molsysmt._private.variables import is_all


def prepare_source(
    molecular_system, selection, structure_indices, chemical_state, syntax, caller
):
    """Normalize adapters once without reader inference or full 0.5 coordinates."""
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt.basic import convert, get_form, select

    source_forms = get_form(molecular_system)
    source = molecular_system
    if source_forms not in (
        "molsysmt.MolSys",
        "molsysmt.Topology",
        "file:h5msm",
        "molsysmt.H5MSMFileHandler",
    ):
        source = convert(source, to_form="molsysmt.MolSys", get_missing_bonds=False)
    selection_source = source
    if modular_h5msm_dimensions(source) is not None and (
        not isinstance(selection, str) or is_all(selection)
    ):
        from molsysmt._private.smonitor import NotWithThisFormError
        from molsysmt.h5msm import read_layers

        selection_source = read_layers(source, layers=["topology"])["topology"]
        if selection_source is None:
            raise NotWithThisFormError(
                caller=caller, form=source_forms, requested_attribute="group_index"
            )
    atoms = select(
        selection_source,
        selection=selection,
        syntax=syntax,
        chemical_state=chemical_state
        if isinstance(selection, str) and not is_all(selection)
        else "reference",
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    return source_forms, source, selection_source, atoms


def read_geometry(source, atoms, structure_index):
    """Read one coordinate structure plus its box and alternate-site evidence."""
    from molsysmt.basic import get_form
    from molsysmt.form import _dict_modules

    # Keep coordinate rows and sparse alternate-site atom indices on the same
    # source axes using the established adapter iterator for every native form.
    with _dict_modules[get_form(source)].StructuresIterator(
        source,
        atom_indices=atoms,
        structure_indices=[structure_index],
        coordinates=True,
        box=True,
        alternate_location=True,
        output_type="dictionary",
        skip_digestion=True,
    ) as iterator:
        return next(iterator)
