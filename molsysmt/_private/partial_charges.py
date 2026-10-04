"""Implementing bounded named charge models and native assignment bookkeeping."""

import hashlib
import json
from copy import deepcopy

import numpy as np
import pandas as pd
from depdigest import dep_digest

from molsysmt._private.scientific_citations import ARTICLES
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

_CALLER = "molsysmt.physchem.get_partial_charges"
_TOLERANCE = 1e-6
_ELEMENTS = {"H", "C", "N", "O", "F", "P", "S", "Cl", "Br", "I"}
_REFERENCE = dict(
    id="doi:" + ARTICLES["gasteiger_marsili"]["doi"],
    type="article",
    **ARTICLES["gasteiger_marsili"],
)


def _fail(reason):
    raise StructuralInconsistencyError(reason=reason, caller=_CALLER)


def _charge_value(value):
    """Normalize a declared scalar charge, never an unlabelled floating value."""
    from molsysmt import pyunitwizard as puw

    if value is None:
        return None
    if isinstance(value, (int, np.integer)) and not isinstance(value, (bool, np.bool_)):
        return float(value)
    try:
        if not puw.is_quantity(value):
            raise ValueError("A charge quantity or an integer is required.")
        number = np.asarray(puw.get_value(value, to_unit="elementary_charge"))
        if number.shape != () or not np.isfinite(number):
            raise ValueError("A finite scalar charge is required.")
        return float(number)
    except Exception as error:
        raise ArgumentError(
            "expected_total_charge",
            value=value,
            caller=_CALLER,
            message="Supply a finite scalar charge quantity or an integer in elementary-charge units.",
        ) from error


def _total(state, n_atoms, expected):
    formal = state.atom_attributes.get("formal_charge")
    known = formal is not None and len(formal) == n_atoms and formal.notna().all()
    formal_total = float(formal.sum()) if known else None
    declared = _charge_value(expected)
    if declared is not None and known and abs(declared - formal_total) > _TOLERANCE:
        _fail(
            "Declared total charge conflicts with the complete formal-charge inventory."
        )
    if declared is None and not known:
        _fail(
            "Total charge is unknown: provide expected_total_charge or complete formal charges."
        )
    return (
        formal_total if declared is None else declared,
        "formal_charge_inventory" if declared is None else "caller_declaration",
    )


def _state_view(source, states, state_index):
    """Detach chemical tables without copying or materializing coordinates."""
    from molsysmt.basic import convert
    from molsysmt.native import MolSys, Topology

    topology = (
        source.topology
        if isinstance(source, MolSys)
        else source
        if isinstance(source, Topology)
        else convert(source, to_form="molsysmt.Topology")
    )
    if topology is None:
        _fail("Charge calculation requires a chemical element inventory.")
    topology = topology.copy()
    chemistry = states.copy()
    chemistry._reference_index = state_index
    topology._chemical_states_domain = chemistry
    return MolSys._from_partial_domains(topology=topology, chemical_states=chemistry)


@dep_digest("rdkit")
def _gasteiger(view, state_index):
    from rdkit import rdBase
    from rdkit.Chem import rdPartialCharges

    from molsysmt.basic import convert
    from molsysmt.physchem import get_chemical_readiness

    readiness = get_chemical_readiness(view, chemical_state=state_index)
    for name in (
        "atom_type",
        "formal_charge",
        "n_unpaired_electrons",
    ):
        if readiness["fields"][name]["status"] != "present":
            _fail(
                f"Gasteiger-Marsili requires explicit supported {name} on every atom."
            )
    if not view.topology.atoms["atom_type"].isin(_ELEMENTS).all():
        _fail(
            "Gasteiger-Marsili supports closed-shell organic elements H/C/N/O/F/P/S/Cl/Br/I; no metals or element substitutions."
        )
    state = view.chemical_states._states[state_index]
    if state.atom_attributes["n_unpaired_electrons"].ne(0).any():
        _fail(
            "Gasteiger-Marsili does not support radical states in this bounded route."
        )
    if len(state.bonds) and (
        not state.bonds["bond_type"].eq("covalent").all()
        or not (
            state.bonds["bond_order"].isin([1, 2, 3])
            | state.bonds.get(
                "is_aromatic", pd.Series(False, index=state.bonds.index)
            ).fillna(False)
        ).all()
    ):
        _fail("Gasteiger-Marsili requires supported explicit covalent bond orders.")
    for name in ("n_implicit_hydrogens", "n_explicit_hydrogens"):
        counts = state.atom_attributes.get(name)
        if counts is not None and counts.fillna(0).ne(0).any():
            _fail(
                "Gasteiger-Marsili requires all declared hydrogens as indexed atoms; add fixed-state hydrogens explicitly first."
            )
    try:
        molecule = convert(view, to_form="rdkit.Mol")
        if any(
            atom.GetNumImplicitHs() or atom.GetNumExplicitHs()
            for atom in molecule.GetAtoms()
        ):
            _fail(
                "Gasteiger-Marsili requires explicit indexed hydrogens; provider valence perception found virtual hydrogens."
            )
        if any(atom.GetNumRadicalElectrons() for atom in molecule.GetAtoms()):
            _fail(
                "Provider valence perception found radical chemistry outside this bounded route."
            )
        known_aromatic = state.atom_attributes.get("is_aromatic")
        if known_aromatic is not None and any(
            pd.notna(value) and bool(value) != atom.GetIsAromatic()
            for value, atom in zip(known_aromatic, molecule.GetAtoms())
        ):
            _fail(
                "Provider aromaticity perception conflicts with declared atom aromaticity."
            )
        rdPartialCharges.ComputeGasteigerCharges(
            molecule, nIter=12, throwOnParamFailure=True
        )
        values = []
        for atom in molecule.GetAtoms():
            if not atom.HasProp("_GasteigerCharge") or not atom.HasProp(
                "_GasteigerHCharge"
            ):
                _fail(
                    "Gasteiger-Marsili did not provide complete atom charge coverage."
                )
            if (
                not np.isfinite(atom.GetDoubleProp("_GasteigerHCharge"))
                or abs(atom.GetDoubleProp("_GasteigerHCharge")) > _TOLERANCE
            ):
                _fail(
                    "Unmapped virtual hydrogen charges cannot be silently assigned to heavy atoms."
                )
            values.append(atom.GetDoubleProp("_GasteigerCharge"))
    except StructuralInconsistencyError:
        raise
    except Exception as error:
        _fail(f"Gasteiger-Marsili charge assignment failed: {error}")
    return (
        np.asarray(values, dtype=float),
        {"rdkit": rdBase.rdkitVersion},
        dict(
            iterations=12,
            throw_on_parameter_failure=True,
            chemical_perception="rdkit_sanitization",
            hydrogen_policy="indexed_atoms_only",
        ),
        [deepcopy(_REFERENCE)],
    )


@dep_digest("openmm")
def _forcefield(view, forcefield, water_model):
    import openmm
    from openmm import app, unit

    from molsysmt.basic import convert
    from molsysmt.molecular_mechanics import get_engine_forcefield

    try:
        files = get_engine_forcefield(
            forcefield, water_model=water_model, engine="OpenMM"
        )
        topology = convert(view.topology, to_form="openmm.Topology")
        if any(atom.element is None for atom in topology.atoms()):
            _fail(
                "Force-field assignment requires explicit elements on every source atom."
            )
        provider = app.ForceField(*files)
        templates = [
            template.name for template in provider.getMatchingTemplates(topology)
        ]
        system = provider.createSystem(
            topology, nonbondedMethod=app.NoCutoff, constraints=None
        )
        n_atoms = view.get_n_atoms()
        forces = [
            force
            for force in system.getForces()
            if isinstance(force, openmm.NonbondedForce)
        ]
        if (
            system.getNumParticles() != n_atoms
            or len(forces) != 1
            or any(system.isVirtualSite(i) for i in range(n_atoms))
        ):
            _fail(
                "Force-field charges require exactly the source particles and one NonbondedForce; extra particles or virtual sites are unsupported."
            )
        values = np.asarray(
            [
                forces[0]
                .getParticleParameters(i)[0]
                .value_in_unit(unit.elementary_charge)
                for i in range(n_atoms)
            ],
            dtype=float,
        )
    except StructuralInconsistencyError:
        raise
    except Exception as error:
        _fail(
            f"Force-field template charge assignment failed without repairing the source: {error}"
        )
    references = []
    if forcefield == "AMBER14" and any(
        (name[1:] if len(name) == 4 and name[0] in {"N", "C"} else name)
        in {
            "ALA",
            "ARG",
            "ASN",
            "ASP",
            "CYS",
            "CYX",
            "GLN",
            "GLU",
            "GLY",
            "HID",
            "HIE",
            "HIP",
            "ILE",
            "LEU",
            "LYS",
            "MET",
            "PHE",
            "PRO",
            "SER",
            "THR",
            "TRP",
            "TYR",
            "VAL",
        }
        for name in templates
    ):
        references.append(
            dict(
                id="doi:" + ARTICLES["ff14sb"]["doi"],
                type="article",
                **deepcopy(ARTICLES["ff14sb"]),
                roles=["parameter_set"],
            )
        )
    return (
        values,
        {"openmm": openmm.__version__},
        dict(
            forcefield=forcefield,
            water_model=water_model,
            forcefield_files=list(files),
            matched_residue_templates=templates,
        ),
        references,
    )


def calculate(
    molecular_system,
    method,
    selection,
    frames,
    chemical_state,
    forcefield,
    water_model,
    expected,
    syntax,
):
    from molsysmt import __version__, _ackredit
    from molsysmt import pyunitwizard as puw
    from molsysmt._private.scientific_citations import SOFTWARE
    from molsysmt.basic import get_form
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        select_chemical_atoms,
    )

    if method not in {"gasteiger_marsili", "forcefield"}:
        raise ArgumentError("method", value=method, caller=_CALLER)
    if (method == "forcefield" and forcefield is None) or (
        method == "gasteiger_marsili"
        and (forcefield is not None or water_model is not None)
    ):
        raise ArgumentError(
            "forcefield",
            value=forcefield,
            caller=_CALLER,
            message="Specify a named force field only for method='forcefield'.",
        )
    if get_form(molecular_system) == "rdkit.Mol":
        from rdkit import Chem

        molecular_system = Chem.Mol(molecular_system)
    source, states, state, state_index, _, _, selection_frames = chemical_graph_context(
        molecular_system, chemical_state, frames, method == "forcefield", _CALLER
    )
    from molsysmt._private.variables import is_all
    from molsysmt.basic._index_validation import _get_count, validate_structure_indices

    frame_source = source
    if not is_all(selection_frames) and selection_frames is not None:
        if _get_count(source, "structure") is None:
            from molsysmt.basic import convert

            frame_source = convert(source, to_form="molsysmt.MolSys")
        if _get_count(frame_source, "structure") is None:
            raise ArgumentError(
                "structure_indices",
                value=frames,
                caller=_CALLER,
                message="Explicit structure_indices require a known source structure axis.",
            )
    selection_frames = validate_structure_indices(
        frame_source, selection_frames, _CALLER
    )
    if not states.n_atoms:
        _fail("Charge assignment requires at least one source atom.")
    total, total_source = _total(state, states.n_atoms, expected)
    view = _state_view(source, states, state_index)
    # Atom types are chemical element symbols in MolSysMT, not docking labels.
    from molsysmt._private.atom_types import CHEMICAL_ATOM_TYPES

    if not view.topology.atoms["atom_type"].isin(CHEMICAL_ATOM_TYPES).all():
        _fail(
            "Charge assignment requires explicit chemical element symbols, not guessed atom names or force-field types."
        )
    values, software, parameters, references = (
        _gasteiger(view, state_index)
        if method == "gasteiger_marsili"
        else _forcefield(view, forcefield, water_model)
    )
    if values.shape != (states.n_atoms,) or not np.isfinite(values).all():
        _fail("The charge model did not provide finite complete atom-aligned coverage.")
    observed = float(np.sum(values, dtype=np.float64))
    if abs(observed - total) > _TOLERANCE:
        _fail(
            f"Partial charges sum to {observed:.12g} e; expected {total:.12g} e (tolerance {_TOLERANCE:g} e). No renormalization was applied."
        )
    # Rich selections need the original structural domain. In particular the
    # H5MSM chemistry-only context deliberately did not load coordinates.
    rich_selection = isinstance(selection, str) and not is_all(selection)
    indices = select_chemical_atoms(
        molecular_system if rich_selection else source,
        states,
        state_index,
        selection,
        frames if rich_selection else selection_frames,
        syntax,
    )
    software = {"molsysmt": __version__, **software}
    items = [
        dict(reference, roles=reference.get("roles", ["scientific_criterion"]))
        for reference in references
    ]
    items.extend(
        dict(
            id=f"software:{name}:{version}",
            type="software",
            **deepcopy(SOFTWARE.get(name, dict(title=name))),
            version=version,
            roles=["executed_software"],
        )
        for name, version in software.items()
    )
    report = dict(
        schema="molsysmt.partial_charge_assignment@1",
        method=method,
        engine="RDKit" if method == "gasteiger_marsili" else "OpenMM",
        chemical_state_index=state_index,
        chemical_state_id=state.state_id,
        n_atoms=states.n_atoms,
        atom_indices=indices.copy(),
        coverage="complete",
        evaluated_atom_indices=np.arange(states.n_atoms, dtype=np.int64),
        evidence="calculated_from_declared_graph"
        if method == "gasteiger_marsili"
        else "matched_forcefield_templates",
        parameters=parameters,
        software=software,
        references=references,
        charge_unit="elementary_charge",
        expected_total_charge=total,
        total_charge_source=total_source,
        total_charge=observed,
        total_charge_tolerance=_TOLERANCE,
        attribution=dict(
            schema="molsysmt.scientific_attribution@1", target=_CALLER, items=items
        ),
    )
    with _ackredit.scope(_CALLER) as provider:
        _ackredit.credit(provider, items, _CALLER)
    return {
        "partial_charge": puw.quantity(
            values[indices], "elementary_charge", standardized=True
        ),
        "report": report,
    }


def _digest(source, state_index, method):
    """Bind stored provenance to ordered chemical data, not coordinates or IDs."""
    state = source.chemical_states._states[state_index]

    def table(frame):
        return frame.astype(object).where(frame.notna(), None).to_dict(orient="list")

    data = dict(
        elements=source.topology.atoms["atom_type"].tolist(),
        isotope=table(source.topology.atoms[["isotope"]]),
        atoms=table(state.atom_attributes),
        bonds=table(state.bonds.drop(columns=["bond_id"], errors="ignore")),
        completeness=state.connectivity_completeness,
    )
    if method == "forcefield":
        data["atom_template_inputs"] = table(
            source.topology.atoms[["atom_name", "group_index", "chain_index"]]
        )
        data["residue_names"] = table(source.topology.groups[["group_name"]])
    payload = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        default=lambda value: (
            value.item() if isinstance(value, np.generic) else str(value)
        ),
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def _values_digest(values):
    return hashlib.sha256(np.asarray(values, dtype="<f8").tobytes()).hexdigest()


def bind_assignment(source, report):
    result = deepcopy(report)
    result.update(
        status="assigned",
        atom_source_indices=np.arange(source.get_n_atoms(), dtype=np.int64),
        chemical_digest=_digest(
            source, report["chemical_state_index"], report["method"]
        ),
        values_digest=_values_digest(source.molecular_mechanics.partial_charge),
    )
    return result


def validate_assignment(source):
    """Reject stale provenance while retaining legacy explicitly provided charges."""
    report = getattr(source.molecular_mechanics, "partial_charge_assignment", None)
    if report is None:
        return
    index = report["chemical_state_index"]
    if (
        source.topology is None
        or source.chemical_states is None
        or index >= source.chemical_states.n_chemical_states
        or report.get("status") == "stale"
        or _digest(source, index, report["method"]) != report["chemical_digest"]
        or _values_digest(source.molecular_mechanics.partial_charge)
        != report["values_digest"]
    ):
        _fail(
            "Stored partial charges no longer match their bound chemistry or values; explicitly recalculate or replace the assignment."
        )
    if source.structures is not None and source.structures.n_structures:
        associated = source._get_structure_chemical_state_indices(resolved=True)
        if np.any(pd.isna(associated)) or np.any(
            np.asarray(associated, dtype=int) != index
        ):
            _fail(
                "Stored partial charges do not match the chemical state associated with the output structures."
            )


def project_assignment(source, output, indices):
    """Keep original provenance and atom correspondence through native extraction."""
    report = getattr(source.molecular_mechanics, "partial_charge_assignment", None)
    if report is None:
        return
    from molsysmt._private.variables import is_all

    if is_all(indices):
        return
    projected = deepcopy(report)
    indices = np.asarray(indices, dtype=np.int64)
    try:
        validate_assignment(source)
    except StructuralInconsistencyError:
        projected["status"] = "stale"
    else:
        projected.update(
            status="projected",
            chemical_digest=_digest(
                output, projected["chemical_state_index"], projected["method"]
            ),
            values_digest=_values_digest(output.molecular_mechanics.partial_charge),
        )
    projected["atom_source_indices"] = report["atom_source_indices"][indices].copy()
    # Original full-system totals/coverage stay in the original report. These
    # fields explicitly describe the retained projection, without renormalization.
    projected["retained_total_charge"] = float(
        np.sum(np.asarray(output.molecular_mechanics.partial_charge, dtype=float))
    )
    output.molecular_mechanics.partial_charge_assignment = projected
