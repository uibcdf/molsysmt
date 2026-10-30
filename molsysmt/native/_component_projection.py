"""Prepare explicit component reconstruction without a chemical Topology facade."""

from copy import deepcopy

from molsysmt._private.smonitor import StructuralInconsistencyError


def prepare(source, *, indices=False, names=False, types=False):
    from molsysmt.native import ChemicalStates, MolSys

    if not isinstance(source, (MolSys, ChemicalStates)):
        from molsysmt.basic import convert

        source = convert(source, to_form="molsysmt.MolSys")
    states = source.chemical_states if isinstance(source, MolSys) else source
    if states is None:
        raise StructuralInconsistencyError(
            reason="Component queries require an explicit ChemicalStates domain.",
            caller="molsysmt.element.component",
        )
    if not (indices or names or types):
        return source
    temporary = ChemicalStates(n_atoms=states.n_atoms, skip_digestion=True)
    temporary._append_state(
        deepcopy(states._resolve_chemical_state()), set_as_reference=True
    )
    topology = source.topology if isinstance(source, MolSys) else None
    temporary.rebuild_components(
        redefine_indices=indices,
        redefine_ids=False,
        redefine_names=names or indices,
        redefine_types=types or indices,
        topology=topology,
        skip_digestion=True,
    )
    if topology is None:
        return temporary
    return MolSys._from_partial_domains(
        topology=topology.copy(), chemical_states=temporary
    )
