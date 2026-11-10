"""Read-only native property, sequence and connectivity report orchestration."""

from secrets import token_urlsafe
from weakref import ref

import numpy as np

from ._figure_observation import capture_call
from ._task_panel import _structures

PROPERTY_METHODS = {
    "secondary_structure": "molsysmt.structure.get_secondary_structure",
    "mass": "molsysmt.physchem.get_mass",
    "reference_charge": "molsysmt.physchem.get_charge",
    "hydrophobicity": "molsysmt.physchem.get_hydrophobicity",
    "polarity": "molsysmt.physchem.get_polarity",
    "sasa": "molsysmt.physchem.get_sasa",
    "sequence": "molsysmt.form.molsysmt_Topology.to_string_amino_acids_1",
    "bonds": "molsysmt.chemical_states.get_bondgraph",
    "blocks": "molsysmt.chemical_states.get_covalent_blocks",
    "rings": "molsysmt.chemical_states.get_rings",
}
HYDROPHOBICITY_SCALES = (
    "eisenberg",
    "rao",
    "sweet",
    "kyte",
    "abraham",
    "bull",
    "guy",
    "miyazawa",
    "roseman",
    "wolfenden",
    "chothia",
    "hopp",
    "manavalan",
    "black",
    "fauchere",
)
PROPERTY_DEFAULTS = {
    "property_element": "atom",
    "secondary_mode": "simplified",
    "property_scale": "eisenberg",
    "polarity_scale": "grantham",
    "sasa_engine": "MolSysMT",
    "probe_radius": "1.4",
    "probe_unit": "angstrom",
    "sphere_points": "240",
    "sequence_scheme": "stored",
    "graph_state": "reference",
    "graph_state_index": "0",
    "assume_complete": False,
}


def validate_property_parameters(p):
    for key, choices in {
        "property_element": {"atom", "group"},
        "secondary_mode": {"simplified", "full"},
        "property_scale": set(HYDROPHOBICITY_SCALES),
        "polarity_scale": {"grantham", "zimmerman"},
        "sasa_engine": {"MolSysMT", "MDTraj"},
        "probe_unit": {"nm", "angstrom", "pm"},
        "sequence_scheme": {"stored", "sequence", "amber", "ccd", "legacy"},
        "graph_state": {"reference", "structure", "index"},
    }.items():
        if not isinstance(p[key], str) or p[key] not in choices:
            raise ValueError("Choose supported property and chemical-state options.")
    for key in ("probe_radius", "sphere_points", "graph_state_index"):
        if not isinstance(p[key], str) or len(p[key]) > 64:
            raise ValueError("Enter bounded property calculation parameters.")
    if not isinstance(p["assume_complete"], bool):
        raise ValueError("Connectivity completeness must be an explicit choice.")


def _groups(target, atoms):
    import molsysmt as msm

    # A GUI atom population includes complete groups for group-level reports.
    # Numeric atom positions must never be passed on the native group axis.
    indices = msm.get(
        target, element="atom", selection=atoms.tolist(), group_index=True
    )
    groups = np.asarray(list(dict.fromkeys(map(int, indices))), dtype=np.int64)
    names = msm.get(target, element="group", selection=groups.tolist(), group_name=True)
    members = msm.get(
        target, element="group", selection=groups.tolist(), atom_index=True
    )
    return (
        groups,
        [str(name) for name in names],
        [list(map(int, row)) for row in members],
    )


class _PropertyReports:
    def _calculate_property(self, target, status, atoms):
        import molsysmt as msm

        p, task = self._parameters, self._parameters["task"]
        frames = (
            _structures(
                p["structures"],
                p["indices"],
                int(target.structures.n_structures),
                int(self._view.player.index),
                allow_repeated=True,
            )
            if task in {"sasa", "bonds", "blocks", "rings", "secondary_structure"}
            else []
        )
        metadata = {
            "method": PROPERTY_METHODS[task],
            "frames": [],
            "element": "atom",
            "definition": "",
            "notice": "",
            "names": [],
            "indices": [],
            "members": [],
            "columns": [],
        }
        group_level = task in {
            "secondary_structure",
            "reference_charge",
            "hydrophobicity",
            "polarity",
            "sequence",
        } or (task in {"mass", "sasa"} and p["property_element"] == "group")
        if group_level:
            indices, names, members = _groups(target, atoms)
            element = "group"
        else:
            indices, names, members = (
                atoms,
                [""] * len(atoms),
                [[int(a)] for a in atoms],
            )
            element = "atom"
        metadata.update(element=element, indices=indices, names=names, members=members)
        native, values, unit, layout = None, None, "", "property_values"
        calculation_context = None
        selection = indices.tolist()
        if task in {"mass", "reference_charge", "hydrophobicity", "polarity"}:
            method, definition, unit = {
                "mass": ("get_mass", "physical", "dalton"),
                "reference_charge": ("get_charge", "physical_pH7", "elementary_charge"),
                "hydrophobicity": (
                    "get_hydrophobicity",
                    p["property_scale"],
                    "dimensionless",
                ),
                "polarity": ("get_polarity", p["polarity_scale"], "dimensionless"),
            }[task]
            native = getattr(self._owner.physchem, method)(
                element=element, selection=selection, definition=definition
            )
            values = np.asarray(
                msm.pyunitwizard.get_value(native, to_unit=unit)
                if task in {"mass", "reference_charge"}
                else native,
                dtype=float,
            )
            if values.shape != (len(indices),):
                raise ValueError(
                    "The native property does not match its source element axis."
                )
            metadata["definition"] = definition
            metadata["notice"] = {
                "mass": "IUPAC 2021 standard atomic masses; group values include complete groups.",
                "reference_charge": "Fixed amino-acid reference charges at pH 7; not stored formal charges, partial charges or a protonation prediction.",
                "hydrophobicity": "Named amino-acid reference scale; no chemical assignment or preparation is inferred.",
                "polarity": "Named amino-acid polarity reference scale; no chemical assignment is inferred.",
            }[task]
            metadata["columns"] = [
                element.title() + " index",
                "Name",
                "Value (" + unit + ")",
            ]
            total = len(indices)
        elif task == "sasa":
            try:
                probe, points = float(p["probe_radius"]), int(p["sphere_points"])
            except ValueError as exc:
                raise ValueError(
                    "Enter a positive finite probe radius and integer sampling count."
                ) from exc
            if not np.isfinite(probe) or probe <= 0 or points <= 0:
                raise ValueError(
                    "Enter a positive finite probe radius and integer sampling count."
                )
            arguments = dict(
                element=element,
                selection=selection,
                structure_indices=frames,
                engine=p["sasa_engine"],
                probe_radius=msm.pyunitwizard.quantity(probe, p["probe_unit"]),
                n_sphere_points=points,
                use_cell_list="auto",
                use_gpu=False,
                parallel=False,
                num_threads=1,
                pbc=p["pbc"],
            )
            arguments, calculation_context = capture_call(
                target, "molsysmt.physchem.get_sasa", arguments
            )
            native = self._owner.physchem.get_sasa(**arguments)
            values = np.asarray(
                msm.pyunitwizard.get_value(native, to_unit="nm**2"), dtype=float
            )
            if values.shape != (len(frames), len(indices)):
                raise ValueError(
                    "Native SASA does not match its structure and output-element axes."
                )
            unit, layout, total = "nm**2", "property_structures", int(values.size)
            metadata.update(
                frames=frames,
                definition="Shrake–Rupley / " + p["sasa_engine"],
                columns=["Structure index", element.title() + " index", "Area (nm²)"],
                notice="All source atoms, including solvent and atoms outside the output selection, occlude the surface. Native periodic screening excludes self-images; MDTraj periodic requests with a box are refused. No reconstruction is inferred.",
            )
        elif task == "secondary_structure":
            native = self._owner.structure.get_secondary_structure(
                selection=selection,
                structure_indices=frames,
                simplified=p["secondary_mode"] == "simplified",
                engine="MDTraj",
                heavy_mode="auto",
            )
            values = np.asarray(native, dtype="U2")
            if values.shape != (len(frames), len(indices)):
                raise ValueError(
                    "Native DSSP labels do not match the source structure/group axes."
                )
            import mdtraj as md

            layout, total = "property_categories", int(values.size)
            metadata.update(
                frames=frames,
                definition="Kabsch–Sander DSSP / MDTraj / " + p["secondary_mode"],
                software={"mdtraj": str(md.__version__)},
                columns=["Structure index", "Group index", "DSSP code (quoted)"],
                notice="Observed categorical assignments in full molecular backbone context, then selected groups. MDTraj's DSSP-2.2.0-based implementation uses stored coordinates without periodic reconstruction. NA means its required backbone quartet is unavailable; a quoted space is the full-code loop assignment. This is not sequence prediction or a reference propensity. No preparation, source edit, color or scalar plot is inferred.",
            )
        elif task == "sequence":
            from molsysmt.form.molsysmt_Topology.to_string_amino_acids_1 import (
                to_string_amino_acids_1,
            )

            scheme = None if p["sequence_scheme"] == "stored" else p["sequence_scheme"]
            # Native public per-group projection retains source correspondence
            # even when non-amino-acid groups are omitted. No trajectory copies.
            native = [
                to_string_amino_acids_1(
                    target.topology, group_indices=[int(g)], from_naming_scheme=scheme
                )
                for g in indices
            ]
            values, total = native, len(indices)
            metadata.update(
                definition="Stored naming declarations" if scheme is None else scheme,
                columns=["Group index", "Group name", "One-letter projection"],
                notice="Groups are reported separately in source population order; omitted non-amino-acid groups are explicit. No chain concatenation, name correction, chemical assignment or inferred correspondence.",
            )
        else:
            state = p["graph_state"]
            if state == "index":
                try:
                    state = int(p["graph_state_index"])
                except ValueError as exc:
                    raise ValueError(
                        "Enter a nonnegative chemical-state index."
                    ) from exc
                if state < 0:
                    raise ValueError("Enter a nonnegative chemical-state index.")
            arguments = dict(
                selection=atoms.tolist(), structure_indices=frames, chemical_state=state
            )
            if task == "bonds":
                native = self._owner.chemical_states.get_bondgraph(**arguments)
                members = [list(map(int, pair)) for pair in native.edges]
                metadata["columns"] = ["First atom index", "Second atom index"]
                metadata["notice"] = (
                    f"Stored induced graph: {native.number_of_nodes()} selected nodes, including isolated atoms. No extra relationship-type filter, bond inference, bond orders or completeness certification."
                )
            elif task == "blocks":
                native = self._owner.chemical_states.get_covalent_blocks(
                    **arguments, output_type="sets"
                )
                members = [sorted(map(int, block)) for block in native]
                metadata["columns"] = [
                    "Block index",
                    "Atom count",
                    "Source atoms (preview)",
                ]
                metadata["notice"] = (
                    "Connected blocks of the selected induced graph, without cuts. Omitted atoms cannot connect selected atoms. These are not stable molecule identities."
                )
            else:
                native = self._owner.chemical_states.get_rings(
                    **arguments,
                    assume_complete_connectivity=p["assume_complete"],
                    method="minimum_cycle_basis",
                    max_cyclic_block_size=256,
                )
                offsets, packed = native["atom_offsets"], native["atom_indices"]
                members = [
                    packed[a:b].tolist()
                    for a, b in zip(offsets[:-1], offsets[1:], strict=True)
                ]
                metadata["columns"] = [
                    "Ring index",
                    "Atom count",
                    "Source atoms (preview)",
                ]
                metadata["notice"] = (
                    "Experimental minimum cycle basis, not all cycles or aromaticity. Memberships are atom sets, not traversal order. Full source connectivity is examined before selection; partial rings and cyclic blocks above 256 atoms are refused."
                )
            total, layout = len(members), "property_members"
            metadata.update(
                members=members,
                frames=frames,
                definition=f"Chemical state: {state}; explicit completeness assumption: {p['assume_complete'] if task == 'rings' else False}",
            )
        return self._report_type(
            token=token_urlsafe(18),
            target=ref(target),
            revision=status["target_revision"],
            visible_frame=int(self._view.player.index),
            first_draft=dict(self._draft),
            second_draft=dict(self._second),
            parameters=dict(p),
            frames=frames,
            first=atoms,
            second=np.empty(0, dtype=np.int64),
            selections=(False, False),
            values=values,
            native_values=native,
            unit=unit,
            auxiliary=metadata,
            offsets=None,
            layout=layout,
            total=total,
            periodic=bool(task == "sasa" and p["pbc"] and msm.pbc.has_pbc(target)),
            software=str(msm.__version__)[:200],
            calculation_context=calculation_context,
        )

    def _property_summary(self):
        r, m = self._report, self._report.auxiliary
        return dict(
            id=r.token,
            method=m["method"],
            software={"molsysmt": r.software, **m.get("software", {})},
            rows=r.total,
            unit=r.unit,
            first_atoms=len(r.first),
            second_atoms=0,
            source_revision=r.revision,
            structure_indices=m["frames"][:200],
            structures_truncated=len(m["frames"]) > 200,
            structure_count=len(m["frames"]),
            family="property",
            result_axis=m["element"],
            definition=m["definition"],
            notice=m["notice"],
            periodic=r.periodic,
            requested_pbc=(r.parameters["task"] == "sasa" and r.parameters["pbc"]),
            disk_backed=False,
            live_distance_unavailable="This report is not a pair distance.",
            plot_unavailable="This report is not one scalar per loaded structure.",
            reference_structure_index=None,
            pca_component=None,
        )

    def _property_row(self, position):
        r = self._report
        if r.layout in {"property_structures", "property_categories"}:
            f, i = divmod(position, len(r.auxiliary["indices"]))
            return r.auxiliary["members"][i], r.frames[f]
        return r.auxiliary["members"][position], None

    def _property_page(self, offset, size):
        r, m, rows = self._report, self._report.auxiliary, []
        for position in range(offset, min(r.total, offset + size)):
            task = r.parameters["task"]
            if r.layout in {"property_structures", "property_categories"}:
                f, i = divmod(position, len(m["indices"]))
                row = [
                    r.frames[f],
                    int(m["indices"][i]),
                    repr(str(r.values[f, i]))
                    if r.layout == "property_categories"
                    else self._property_number(r.values[f, i]),
                ]
            elif r.layout == "property_members":
                members = m["members"][position]
                row = (
                    members
                    if task == "bonds"
                    else [
                        position,
                        len(members),
                        ", ".join(map(str, members[:30]))
                        + (" …" if len(members) > 30 else ""),
                    ]
                )
            else:
                value = (
                    (r.values[position] or "omitted by native projection")
                    if task == "sequence"
                    else self._property_number(r.values[position])
                )
                row = [int(m["indices"][position]), m["names"][position], value]
            rows.append(row)
        return dict(
            offset=offset,
            total=r.total,
            page_size=size,
            columns=m["columns"],
            rows=rows,
        )

    @staticmethod
    def _property_number(value):
        return format(float(value), ".9g") if np.isfinite(value) else "undefined"
