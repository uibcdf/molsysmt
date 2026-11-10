"""Private independent construction tasks delegated to public native science."""

from math import isfinite

from ._task_panel import _structures

CONSTRUCTION_TASKS = {"peptide", "water_cell", "bioassembly", "solvate", "ions"}
FRESH_TASKS = {"peptide", "water_cell"}
CONSTRUCTION_DEFAULTS = {
    "sequence": "",
    "sequence_format": "amino_acids_3",
    "naming_scheme": "sequence",
    "cell_a": "2",
    "cell_b": "2",
    "cell_c": "2",
    "cell_alpha": "90",
    "cell_beta": "90",
    "cell_gamma": "90",
    "cell_length_unit": "nm",
    "cell_angle_unit": "degrees",
    "construction_structures": "current",
    "construction_indices": "",
    "assembly_name": "",
    "construction_engine": "OpenMM",
    "box_shape": "cubic",
    "clearance": "0.5 nm",
    "solvent_model": "TIP3P",
    "construction_forcefield": "",
    "anion": "Cl-",
    "cation": "Na+",
    "n_anions": "0",
    "n_cations": "0",
    "ionic_strength": "0 molar",
    "charge_source": "formal_charge",
    "ion_expected_charge": "",
    "min_solute_distance": "0.5 nm",
    "min_ion_distance": "0.5 nm",
    "random_seed": "0",
    "max_attempts": "10",
}


def validate_construction_parameters(p):
    for key in CONSTRUCTION_DEFAULTS:
        if not isinstance(p[key], str) or len(p[key]) > (
            4096 if key in {"sequence", "construction_indices"} else 200
        ):
            raise ValueError(
                "Enter bounded construction text and explicit quantities with units."
            )
    for key, choices in {
        "sequence_format": {"amino_acids_1", "amino_acids_3"},
        "naming_scheme": {"sequence", "amber", "ccd", "legacy"},
        "cell_length_unit": {"nm", "angstrom", "pm"},
        "cell_angle_unit": {"degrees", "radians"},
        "construction_structures": {"current", "all", "indices"},
        "construction_engine": {"OpenMM", "MolSysMT", "PDBFixer"},
        "box_shape": {
            "cubic",
            "truncated octahedral",
            "rhombic dodecahedral",
            "rectangular",
        },
        "charge_source": {"formal_charge", "partial_charge"},
        "anion": {"Cl-", "Br-", "F-", "I-"},
        "cation": {"Na+", "K+", "Li+", "Rb+", "Cs+"},
    }.items():
        if p[key] not in choices:
            raise ValueError("Choose a supported explicit construction option.")


def _integer(text, name, *, optional=False, signed=False):
    text = text.strip()
    if optional and not text:
        return None
    try:
        value = int(text)
    except ValueError as exc:
        raise ValueError(f"Enter an integer for {name}.") from exc
    if not signed and value < 0:
        raise ValueError(f"Use a nonnegative integer for {name}.")
    return value


def _ion_arguments(p):
    return {
        key: p[key] if p[key] == "neutralize" else _integer(p[key], key)
        for key in ("n_anions", "n_cations")
    } | {
        "anion": p["anion"],
        "cation": p["cation"],
        "ionic_strength": p["ionic_strength"],
        "random_seed": _integer(p["random_seed"], "random seed", optional=True),
    }


def construct(panel, target):
    """Return a native independent result and bounded operation provenance."""
    import molsysmt as msm

    p, task = panel._parameters, panel._parameters["task"]
    name = {
        "peptide": "build_peptide",
        "water_cell": "make_water_box",
        "bioassembly": "make_bioassembly",
        "solvate": "solvate",
        "ions": "add_ions",
    }[task]
    title = {
        "peptide": "Constructed peptide",
        "water_cell": "Constructed water cell",
        "bioassembly": "Biological assembly",
        "solvate": "Solvated system",
        "ions": "Ion placement",
    }[task]
    science = {
        "task": task,
        "engine": "MolSysMT",
        "scope": "independent_input" if task in FRESH_TASKS else "whole_system",
    }
    frames = []
    if task == "peptide":
        sequence = p["sequence"].strip()
        if not sequence:
            raise ValueError("Enter the explicit peptide sequence first.")
        # Prefix declares the input form. Native naming owns all label semantics.
        candidate = msm.build.build_peptide(
            p["sequence_format"] + ":" + sequence, from_naming_scheme=p["naming_scheme"]
        )
        science.update(
            sequence=sequence,
            sequence_format=p["sequence_format"],
            from_naming_scheme=p["naming_scheme"],
        )
    elif task == "water_cell":
        from ._geometry_panel import _cell_box

        for key in (
            "cell_a",
            "cell_b",
            "cell_c",
            "cell_alpha",
            "cell_beta",
            "cell_gamma",
        ):
            try:
                finite = isfinite(float(p[key]))
            except ValueError as exc:
                raise ValueError("Enter finite cell lengths and angles.") from exc
            if not finite:
                raise ValueError("Enter finite cell lengths and angles.")
        box = _cell_box(p)
        candidate = panel._owner.build.make_water_box(box)
        science.update(
            box_vectors=msm.pyunitwizard.get_value(box, to_unit="nm")[0].tolist(),
            box_unit="nm",
            reference="bundled SPC-MODEL at 300 K; no parameter assignment or equilibration",
        )
    else:
        frames = _structures(
            p["construction_structures"],
            p["construction_indices"],
            int(target.structures.n_structures),
            int(panel._view.player.index),
            allow_repeated=task == "bioassembly",
        )
        if task == "bioassembly":
            assembly = p["assembly_name"].strip()
            if not assembly:
                raise ValueError("Name the stored biological assembly explicitly.")
            available = msm.get(target, bioassembly=True)
            if not isinstance(available, dict) or assembly not in available:
                raise ValueError(
                    "That stored assembly is unavailable; inspect the deposited assembly names in Python."
                )
            candidate = panel._owner.build.make_bioassembly(
                bioassembly=assembly,
                structure_indices=frames,
                to_form="molsysmt.MolSys",
            )
            science.update(bioassembly=assembly)
        else:
            if len(frames) != 1:
                raise ValueError(
                    "Choose exactly one construction structure; no trajectory loop is performed."
                )
            # Explicit whole-system projection, shown by the panel before execution.
            independent = msm.extract(target, structure_indices=frames)
            arguments = _ion_arguments(p)
            if task == "solvate":
                # These are user-declared requests on the result input, never on source.
                requests = {"water_model": p["solvent_model"]}
                if p["construction_forcefield"].strip():
                    requests["forcefield"] = p["construction_forcefield"].strip()
                msm.set(independent, **requests)
                arguments.update(
                    box_shape=p["box_shape"],
                    clearance=p["clearance"],
                    water_model=p["solvent_model"],
                    engine=p["construction_engine"],
                    to_form="molsysmt.MolSys",
                )
                candidate = msm.build.solvate(independent, **arguments)
                science.update(declared_requests=requests)
            else:
                arguments.update(
                    expected_total_charge=_integer(
                        p["ion_expected_charge"],
                        "expected whole-system charge",
                        optional=True,
                        signed=True,
                    ),
                    charge_source=p["charge_source"],
                    min_solute_distance=p["min_solute_distance"],
                    min_ion_distance=p["min_ion_distance"],
                    max_attempts=_integer(p["max_attempts"], "placement attempts"),
                    return_report=True,
                )
                output = msm.build.add_ions(independent, **arguments)
                candidate = output["molecular_system"]
                science.update(report_schema=str(output["report"]["schema"])[:200])
            science.update(
                {
                    key: value
                    for key, value in arguments.items()
                    if key not in {"return_report", "to_form"}
                }
            )
        science.update(
            source_structure_indices=frames[:200],
            structures_truncated=len(frames) > 200,
        )
    return candidate, "molsysmt.build." + name, science, title, frames
