"""Bind geometry-independent decisions to source axes and stage atomic subsets."""

import weakref
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from uuid import uuid4

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import (
    ArgumentConflictError,
    NotImplementedMethodError,
    NotWithThisFormError,
    StructuralInconsistencyError,
)

CALLER = "molsysmt.build.assess_protonation"


@dataclass
class _Context:
    native: object
    n_structures: int
    structure_states: object


@dataclass
class _Decision:
    report: dict
    signature: str
    binding: tuple
    references: tuple


@dataclass
class _Execution:
    output: object
    publish: object
    report: dict


def _context(source):
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt.basic import convert, get_form, has_attribute
    from molsysmt.native import MolSys

    dimensions = modular_h5msm_dimensions(source)
    if dimensions is not None:
        import h5py

        from molsysmt.form._h5msm05_modular import (
            _link_key,
            _read_calculation_chemistry,
            read_modular_file,
        )

        with h5py.File(source, "r") as file:
            if "topology" not in file or "chemical_states" not in file:
                raise NotWithThisFormError(
                    form="file:h5msm",
                    requested_attribute="topology and chemical_states",
                    caller=CALLER,
                )
        native, _ = _read_calculation_chemistry(
            source, chemical_state="reference", structure_indices=None
        )
        n_structures = dimensions[1]
        links = read_modular_file(source, layers={"associations"})["associations"] or []
        link = next(
            (
                link
                for link in links
                if _link_key(link)
                == ("structure_state", "structures", None, "chemical_states", None)
            ),
            None,
        )
        if link is None:
            structure_states = np.full(
                n_structures,
                0 if native.chemical_states.n_chemical_states == 1 else -1,
                dtype=np.int64,
            )
        else:
            structure_states = (
                np.arange(n_structures, dtype=np.int64)
                if isinstance(link["indices"], str)
                else np.asarray(link["indices"], dtype=np.int64)
            )
    else:
        if not isinstance(source, MolSys) and not has_attribute(source, "n_bonds"):
            raise NotWithThisFormError(
                form=get_form(source),
                requested_attribute="stored chemical connectivity",
                caller=CALLER,
            )
        native = (
            source
            if isinstance(source, MolSys)
            else convert(source, to_form="molsysmt.MolSys")
        )
        n_structures = (
            0 if native.structures is None else native.structures.n_structures
        )
        structure_states = (
            np.empty(0, dtype=np.int64)
            if native.structures is None
            else native._get_structure_chemical_state_indices().to_numpy(
                dtype=np.int64, na_value=-1
            )
        )
    if native.topology is None or native.chemical_states is None:
        raise NotWithThisFormError(
            form="molsysmt.MolSys",
            requested_attribute="topology and chemical_states",
            caller=CALLER,
        )
    if native.topology.n_atoms != native.chemical_states.n_atoms:
        raise StructuralInconsistencyError(
            reason="Stable and chemical atom axes must agree.", caller=CALLER
        )
    return _Context(native, n_structures, structure_states)


def _binding(source):
    from molsysmt.native import MolSys

    references = []

    def identity(value):
        if isinstance(value, (str, Path)):
            return ("value", str(value))
        if isinstance(value, (list, tuple)):
            return ("composite", id(value), tuple(identity(part) for part in value))
        try:
            references.append(weakref.ref(value))
        except TypeError:
            pass
        if isinstance(value, MolSys):
            return (
                "native",
                id(value),
                tuple(
                    identity(domain)
                    for domain in (
                        value.topology,
                        value.chemical_states,
                        value.structures,
                    )
                ),
            )
        return (type(value).__module__, type(value).__qualname__, id(value))

    return identity(source), tuple(references)


def _signature(context):
    native = context.native
    topology, states = native.topology, native.chemical_states
    digest = sha256()

    def table(value):
        digest.update(
            repr((list(value.columns), [str(dtype) for dtype in value.dtypes])).encode()
        )
        digest.update(
            pd.util.hash_pandas_object(value, index=True).to_numpy().tobytes()
        )

    digest.update(
        repr(
            (
                topology.n_atoms,
                topology.n_groups,
                context.n_structures,
                states.n_chemical_states,
                states.reference_chemical_state_index,
            )
        ).encode()
    )
    for name in ("atoms", "groups", "chains", "molecules", "entities"):
        table(getattr(topology, name))
    digest.update(repr(tuple(topology.group_naming_schemes)).encode())
    digest.update(context.structure_states.tobytes())
    for state in states._states:
        digest.update(
            repr(
                (
                    state.state_id,
                    state.connectivity_completeness,
                    state.component_completeness,
                    state.component_evidence,
                    state.provenance_index,
                )
            ).encode()
        )
        table(state.atom_attributes)
        table(state.bonds)
        table(state.components)
        digest.update(
            pd.util.hash_pandas_object(state.component_indices, index=True)
            .to_numpy()
            .tobytes()
        )
    return digest.hexdigest()


def prepare(source, pH, engine):
    from molsysmt import _ackredit
    from molsysmt._private.scientific_attribution import executed_software_reference
    from molsysmt.build._protonation import assess

    if engine != "MolSysMT":
        raise NotImplementedMethodError(
            method="assess_protonation",
            arguments=engine,
            caller=CALLER,
            message="Only the MolSysMT fixed-pKa reference method is implemented.",
        )
    binding, references = _binding(source)
    context = _context(source)
    signature = _signature(context)
    report = assess(context.native, pH, n_structures=context.n_structures)
    if signature != _signature(_context(source)):
        raise ArgumentConflictError(
            "molecular_system",
            "assessment",
            reason="Source chemistry changed during assessment.",
            caller=CALLER,
        )
    report["operation_id"] = uuid4().hex
    report["attribution"]["items"].insert(
        0, executed_software_reference("molsysmt", report["software"]["molsysmt"])
    )
    report["source"]["fingerprint"] = signature
    report["source"]["structure_chemical_state_indices"] = (
        context.structure_states.copy()
    )
    report["assumptions"] = [
        "Same input object or resource; positional maps are not atom-ID matching.",
        "Callers serialize source access through preparation and publication.",
        "Coordinates may change on unchanged atom and structure axes.",
        "Execution projects all states and stored domains; it does not choose or repair chemistry.",
    ]
    with _ackredit.scope(CALLER) as provider:
        _ackredit.credit(
            provider,
            report["attribution"]["items"],
            CALLER,
            contextual=True,
            context=report["parameters"],
        )
    return _Decision(report, signature, binding, references)


def _validate_source(decision, source):
    binding, _ = _binding(source)
    if binding != decision.binding or any(
        reference() is None for reference in decision.references
    ):
        raise ArgumentConflictError(
            "molecular_system",
            "assessment",
            reason="The assessment belongs to a different or replaced source object/domain.",
            caller=CALLER,
        )
    if _signature(_context(source)) != decision.signature:
        raise ArgumentConflictError(
            "molecular_system",
            "assessment",
            reason="The source inventory, chemistry, naming or structure axis has changed; assess it again.",
            caller=CALLER,
        )


def stage(decision, source, in_place):
    from molsysmt.basic import remove
    from molsysmt.native import MolSys
    from molsysmt.native._subset import publish_subset, validate_removal_target

    if in_place:
        validate_removal_target(source, None)
        if not isinstance(source, MolSys):
            raise NotWithThisFormError(
                form=type(source).__name__,
                requested_attribute="native MolSys publication",
                caller=CALLER,
            )
    _validate_source(decision, source)
    removed = decision.report["removed_atom_indices"]
    execution = dict(
        status="no_op" if not len(removed) else "applied", in_place=in_place
    )
    if in_place and not len(removed):
        return _Execution(None, None, execution)
    candidate = remove(
        source, selection=removed, to_form="molsysmt.MolSys", in_place=False
    )
    if candidate.get(n_atoms=True) != len(
        decision.report["atom_map"]["output_to_source_atom_indices"]
    ):
        raise StructuralInconsistencyError(
            reason="Prepared subset does not match the retained atom map.",
            caller=CALLER,
        )
    n_structures = (
        0 if candidate.structures is None else candidate.structures.n_structures
    )
    if n_structures != decision.report["source"]["n_structures"]:
        raise StructuralInconsistencyError(
            reason="Prepared subset changed the structure axis.", caller=CALLER
        )
    _validate_source(decision, source)
    if in_place:
        return _Execution(None, lambda: publish_subset(source, candidate), execution)
    return _Execution(candidate, None, execution)
