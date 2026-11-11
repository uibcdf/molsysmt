"""Record exact reconstruction axes without matching atoms or copying coordinates."""

from copy import deepcopy
from hashlib import sha256
from importlib.resources import files

import numpy as np


def template_evidence(name, template):
    """Identify the actual bundled placement data independently of its label."""
    payload = (
        files("molsysmt.data.databases.residue_templates")
        .joinpath(name + ".json")
        .read_bytes()
    )
    return dict(
        name=name,
        resource="molsysmt.data.databases.residue_templates/" + name + ".json",
        sha256=sha256(payload).hexdigest(),
        source=deepcopy(template.get("source")),
    )


def expansion(source, output, old_to_new, introduced_bonds):
    """Expose the insertion algorithm's map and actual losses on its local axes."""
    from molsysmt.native.structures import (
        _ATOM_ALIGNED_ATTRIBUTES,
        _SYSTEM_LEVEL_OBSERVABLES,
    )

    n_source, n_output = source.get_n_atoms(), output.get_n_atoms()
    forward = np.asarray([old_to_new[i] for i in range(n_source)], dtype=np.int64)
    inverse = np.full(n_output, -1, dtype=np.int64)
    inverse[forward] = np.arange(n_source)
    dropped = [
        name
        for name in _ATOM_ALIGNED_ATTRIBUTES + _SYSTEM_LEVEL_OBSERVABLES
        if getattr(source.structures, name) is not None
        and getattr(output.structures, name) is None
    ]
    if source.molecular_mechanics is not None:
        for name in ("atoms_ff", "partial_charge_assignment", "atom_type_assignment"):
            if getattr(source.molecular_mechanics, name) is not None and (
                output.molecular_mechanics is None
                or getattr(output.molecular_mechanics, name) is None
            ):
                dropped.append(name)
    return dict(
        schema="molsysmt.atom_map@1",
        n_source_atoms=n_source,
        n_output_atoms=n_output,
        source_to_output_atom_indices=forward,
        output_to_source_atom_indices=inverse,
        introduced_bond_atom_pairs=np.asarray(introduced_bonds, dtype=np.int64).reshape(
            -1, 2
        ),
        bond_index_scope="output",
        dropped_attributes=dropped,
        invalidated_interactions=list(output.interactions)
        if n_output != n_source
        else [],
    )


class Reconstruction:
    """Compose real stage maps and retain operation-scoped generation evidence."""

    def __init__(self, source):
        self.source = source
        self.forward = np.arange(source.get_n_atoms(), dtype=np.int64)
        self.steps = []
        self.bonds = np.empty((0, 2), dtype=np.int64)
        self.unassessed = []

    def add(self, report, method, *, evidence=None):
        step = deepcopy(report)
        step["method"] = method
        if evidence is not None:
            step["coordinate_evidence"] = deepcopy(evidence)
        mapping = step["source_to_output_atom_indices"]
        self.forward = mapping[self.forward]
        self.bonds = np.concatenate(
            (mapping[self.bonds], step["introduced_bond_atom_pairs"]), axis=0
        )
        self.steps.append(step)

    def finish(self, output, schema, parameters, atoms, groups, *, archive=True):
        from molsysmt import __version__
        from molsysmt._private.preparation_history import append_report
        from molsysmt._private.smonitor import StructuralInconsistencyError

        states = output.chemical_states
        if states is None or states.n_chemical_states != 1:
            raise StructuralInconsistencyError(
                reason="Reconstruction evidence requires exactly one chemical state.",
                caller="molsysmt.build",
            )
        inverse = np.full(output.get_n_atoms(), -1, dtype=np.int64)
        inverse[self.forward] = np.arange(len(self.forward))
        generated = np.flatnonzero(inverse < 0)
        state = states._states[0]
        report = dict(
            schema=schema,
            method="native_terminal_completion"
            if "terminal" in schema
            else "native_heavy_atom_completion",
            engine="MolSysMT",
            status="changed" if len(generated) or len(self.bonds) else "unchanged",
            parameters=deepcopy(parameters),
            source=dict(
                n_atoms=len(self.forward),
                n_structures=self.source.structures.n_structures,
                chemical_state_index=0,
                chemical_state_id=state.state_id,
            ),
            n_source_atoms=len(self.forward),
            n_output_atoms=len(inverse),
            source_to_output_atom_indices=self.forward.copy(),
            output_to_source_atom_indices=inverse,
            generated_atom_indices=generated,
            generated_atom_ids=output.topology.atoms.iloc[generated][
                "atom_id"
            ].tolist(),
            introduced_bond_atom_pairs=self.bonds.copy(),
            bond_index_scope="output",
            selected_source_atom_indices=np.asarray(atoms, dtype=np.int64),
            selected_source_group_indices=np.asarray(groups, dtype=np.int64),
            structure_indices=np.arange(
                self.source.structures.n_structures, dtype=np.int64
            ),
            coordinate_unit="nm",
            coordinate_evidence="native_estimated_geometry"
            if len(generated)
            else "not_generated",
            dropped_attributes=sorted(
                {name for step in self.steps for name in step["dropped_attributes"]}
            ),
            invalidated_interactions=sorted(
                {
                    name
                    for step in self.steps
                    for name in step["invalidated_interactions"]
                }
            ),
            steps=deepcopy(self.steps),
            unassessed=deepcopy(self.unassessed),
            complete_chemical_state_assigned=False,
            geometry_validation="placement_checks_only; no clash, rotamer or energy-minimum assessment",
            software=dict(molsysmt=__version__),
        )
        if archive:
            from molsysmt._private.scientific_attribution import (
                attach_reconstruction_attribution,
            )

            caller = (
                "molsysmt.build.add_missing_terminal_cappings"
                if "terminal" in schema
                else "molsysmt.build.add_missing_heavy_atoms"
            )
            attach_reconstruction_attribution(report, caller)
            append_report(state, report, 0)
        return dict(molecular_system=output, report=report)
