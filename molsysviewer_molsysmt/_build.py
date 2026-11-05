"""Native build diagnostics and detached preparation without scene adoption."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


def _independent_build_documentation(name, *, local_skip=False):
    def decorate(function):
        function = _native_documentation(name, module="build")(function)
        if local_skip:
            function.__doc__ = function.__doc__.replace(
                "\nReturns\n-------",
                "\nskip_digestion : bool, default=False\n"
                "    Keyword-only addon validation control, not forwarded to "
                "the native function. Native validation always applies.\n\n"
                "Returns\n-------",
                1,
            )
        result_description = (
            "returns an independent native MolSysBuilder; "
            if name == "editable"
            else "returns a new system when molecules are removed, otherwise the current primary; "
            if name == "remove_overlapping_molecules"
            else "returns a dictionary containing a separate molecular system and its report; "
            if name == "add_terminal_atoms"
            else "returns a separate molecular system; "
            if name
            in {
                "make_bioassembly",
                "add_missing_heavy_atoms",
                "add_missing_terminal_cappings",
                "mutate",
                "build_peptide",
            }
            else "returns a separate molecular system, optionally with its report; "
        )
        function.__doc__ += (
            "\nView integration\n----------------\n"
            "Reads the current view.molsys through the serialized molecular "
            "reader, including completed pending edits. The native function "
            + result_description
            + "it does not replace view.molsys or publish scene/history changes. "
            "There is no update_view control or implicit adoption. Native "
            "chemical-state, structure, method, prerequisite, provenance, unit "
            "and validation contracts remain unchanged. No chemistry, model "
            "or optional engine is selected or prepared by the addon. An open "
            "loaded owner is required.\n"
        )
        if name == "project_atom_names":
            function.__doc__ += (
                "Export naming projection\n------------------------\n"
                "target_form selects the native naming constraint, not a file "
                "write or output-format conversion. All source atoms and "
                "structures remain; report index maps are identity maps with "
                "original/projected labels, not a name-based atom match. "
                "No atom types, elements, chemistry or template-sensitive "
                "assignments are inferred or recertified. Native geometry "
                "blocks stay protected and shared until a later native edit; "
                "this projection does not require a trajectory-sized geometry "
                "copy. Existing assignments retain their provenance and may "
                "fail their native export validation after renaming.\n"
            )
        else:
            function.__doc__ += (
                "Full native copying may materialize coordinates and is not "
                "an out-of-core trajectory promise.\n"
            )
        if name == "make_bioassembly":
            function.__doc__ += (
                "The explicit operation dictionary or stored assembly name "
                "is interpreted by native MolSysMT. None selects its first "
                "stored assembly; chains must have declared source indices. "
                "Structure indices retain native order/repetitions and default "
                "to structure 0, not the visible structure. Common chain sets "
                "and proper rotations are supported; heterogeneous per-operation "
                "chain sets retain native rejection. Source chain IDs are "
                "preserved once; generated collisions use native unique IDs, "
                "while author names may repeat. No assembly inference, atom-map "
                "report, scene source block, periodic repair or physical-validity "
                "certificate is added. Native form/domain/composition limits "
                "remain unchanged.\n"
            )
        elif name == "merge_nonpolar_hydrogens":
            function.__doc__ += (
                "typing_scheme='autodock4' is explicit. Stored H labels merge "
                "into their retained single-bonded heavy parents; HD labels "
                "remain. Names do not choose the reduction. Complete single-state "
                "chemistry, known hydrogen inventory, finite stored charges and "
                "typing are prerequisites; the addon calculates none of them. "
                "The native atom_projection@1 report distinguishes direct "
                "correspondence, omitted atoms and merged H/parent pairs, with "
                "charge transfers/totals declared in elementary_charge. The "
                "result retains derived assignment provenance and clears reduced "
                "interaction analyses; the source is preserved. This does not "
                "derive a general united-atom force field or persist mechanics "
                "in H5MSM 0.5. Optional attribution and native validation remain "
                "with MolSysMT.\n"
            )
        elif name == "add_terminal_atoms":
            function.__doc__ += (
                "Each declared atom has one existing parent and supplied finite "
                "length coordinates covering every source structure. Native "
                "attachment appends atoms without moving or reordering old atoms, "
                "inherits parent membership and normalizes IDs to strings. No "
                "coordinates, chemistry, hydrogen inventory or force-field "
                "parameters are inferred. The terminal_attachment@1 report "
                "declares old/new identity, parent pairs, original source axes, "
                "canonical nm coordinate units and supplied-coordinate evidence. "
                "An independent record is retained in output preparation history. "
                "Nonempty expansion invalidates output analysis coverage and "
                "preserves the source; strict attribute policy rejects unsupported "
                "new values, while intersection reports discarded attributes. "
                "An empty addition preserves coverage and attributes. Native "
                "single-state, mapping and persistence limits remain explicit.\n"
            )
        elif name == "add_missing_heavy_atoms":
            function.__doc__ += (
                "Native bounded template placement estimates supported missing "
                "non-H atoms across all source structures. Standard and curated "
                "modified-residue support, observed-geometry checks and unassessed "
                "warnings remain native; no clash, stereochemistry, rotamer or "
                "energy-minimum guarantee is added. Native expansion can reorder "
                "atom indices while preserving old IDs and observed coordinates. "
                "Output analyses retain remapped provenance but lose occurrences "
                "and evaluated coverage. Existing chemistry/state metadata is "
                "retained; new chemical values remain unknown. Attribute policy "
                "controls native drops of unsupported structural/mechanical data. "
                "PDBFixer is an explicit optional engine with its own limits, not "
                "an automatic fallback. No hydrogen preparation or per-frame "
                "selection is invented.\n"
            )
        elif name == "add_missing_hydrogens":
            function.__doc__ += (
                "Legacy pH mode and fixed_chemical_state mode retain their "
                "different native contracts. Fixed-state geometry requires "
                "pH=None, explicit RDKit, one prepared component/state/structure "
                "and a complete declared hydrogen inventory. Old coordinates "
                "and indices remain; appended H carry parent maps and stored "
                "generation/attachment history, also preserved by H5MSM. No "
                "protonation choice, heavy conformer, minimization, periodic "
                "reconstruction or fallback engine is introduced. Legacy pH "
                "preparation uses approximate residue rules and does not remove "
                "already present hydrogens. Optional engines retain their own "
                "structure/form/metadata limits. No implicit visible-structure "
                "selection or additional synchronization is added.\n"
            )
        elif name == "add_missing_terminal_cappings":
            function.__doc__ += (
                "The native engine can complete terminal atoms or insert explicit "
                "ACE/NME groups and complete the opposite uncapped terminus, "
                "retaining bounded heavy-atom preflight and "
                "unassessed warnings. Native atom expansion preserves observed "
                "coordinates and IDs but can reorder indices; output analyses "
                "are remapped and invalidated while the source is preserved. "
                "New chemical assignments remain unknown and native attribute "
                "loss diagnostics remain visible. Geometry does not certify "
                "terminal chemistry or physical refinement. PDBFixer and keep_ids "
                "retain their native limitations; no report, attribute policy "
                "or hidden preparation control is invented.\n"
            )
        elif name == "editable":
            function.__doc__ += (
                "The builder copies native topology, chemical states, structures "
                "and state associations. Native builder conversion does not carry "
                "molecular mechanics or named interaction analyses. Its edits and "
                "build() outputs remain independent, also after owner replacement "
                "or closure; they are not managed edits of view.molsys. Native "
                "builder validation, coordinate-growth restrictions and domain "
                "limits remain unchanged. A loaded owner is required; use "
                "molsysmt.build.editable() directly to start an empty builder.\n"
            )
        elif name == "remove_overlapping_molecules":
            function.__doc__ += (
                "selection identifies candidate atoms whose entire declared "
                "molecules can be removed; selection_2 supplies reference atoms, "
                "or its default uses the atom complement, including unselected "
                "atoms of partially selected candidate molecules. There is no "
                "implicit exclusion of contacts within one molecule. Contacts are evaluated only "
                "at structure_index, default 0 rather than the visible structure. "
                "Removal applies to every retained structure with native remapping. "
                "Native pbc=True falls back to nonperiodic contacts without a box. "
                "There is no alignment, chemistry repair or repeated trajectory "
                "calculation. A no-contact result aliases view.molsys, so subsequent "
                "raw edits to that result are ordinary external system edits, not "
                "automatically observed scene changes.\n"
            )
        elif name == "mutate":
            function.__doc__ += (
                "Mutations use native group_index/group_id/group_name keys or "
                "source-ID mutation strings, with explicit selection and engine. "
                "The native route retains observed backbone coordinates and can "
                "leave unsupported side chains incomplete with unassessed "
                "warnings. Native hydrogen rebuilding when H are present, "
                "attribute loss, index remapping and analysis invalidation remain "
                "visible. PDBFixer is optional and explicit; no fallback, rotamer, "
                "clash, protonation or energy-minimum certificate is introduced. "
                "The addon selects no visible frame or implicit subsystem.\n"
            )
        elif name == "build_peptide":
            function.__doc__ += (
                "Builds a new peptide from the sequence converted from the "
                "current system. This is fresh native construction, not a "
                "coordinate repair or trajectory reconstruction. Output pose, "
                "atom identity, chemistry and mechanics follow native template "
                "construction; source geometry, named analyses and arbitrary "
                "metadata are not transferred. Native sequence, chain, naming "
                "and output-form limits remain. LEaP is an explicit optional "
                "engine; the addon adds no engine fallback, solvent, alignment "
                "or physical refinement. Use ordinary molsysmt.build.build_peptide "
                "with an explicit sequence to construct without a loaded view.\n"
            )
        return function

    return decorate


class _BuildTools:
    _NAMES = (
        "infer_covalent_bonds",
        "assign_autodock_atom_types",
        "assign_partial_charges",
        "project_atom_names",
        "make_bioassembly",
        "merge_nonpolar_hydrogens",
        "add_terminal_atoms",
        "add_missing_heavy_atoms",
        "add_missing_hydrogens",
        "add_missing_terminal_cappings",
        "editable",
        "remove_overlapping_molecules",
        "mutate",
        "build_peptide",
        "get_residue_chemical_coverage",
        "get_covalent_bond_candidates",
        "get_peptide_bond_candidates",
        "get_missing_heavy_atoms",
        "get_missing_bonds",
        "get_missing_residues",
        "get_missing_terminal_cappings",
        "get_non_standard_residues",
        "get_disulfide_bonds",
        "has_hydrogens",
        "is_solvated",
    )

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call(self, name, parameters):
        from molsysmt import build

        return self._owner._read(getattr(build, name), parameters)

    @_native_documentation("get_residue_chemical_coverage", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_residue_chemical_coverage(
        self,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_residue_chemical_coverage",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_covalent_bond_candidates", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_covalent_bond_candidates(
        self,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        method="exact_heavy_group_templates",
    ):
        return self._call(
            "get_covalent_bond_candidates",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "method": method,
            },
        )

    @_native_documentation("get_peptide_bond_candidates", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_peptide_bond_candidates(
        self,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        max_bond_length="2 angstroms",
        pbc=False,
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        method="adjacent_backbone_distance",
    ):
        return self._call(
            "get_peptide_bond_candidates",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "max_bond_length": max_bond_length,
                "pbc": pbc,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "method": method,
            },
        )

    @_native_documentation("get_missing_heavy_atoms", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_missing_heavy_atoms(
        self,
        selection="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_missing_heavy_atoms",
            {
                "selection": selection,
                "syntax": syntax,
                "engine": engine,
            },
        )

    @_native_documentation("get_missing_bonds", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_missing_bonds(
        self,
        selection="all",
        structure_index=0,
        max_bond_length="2 angstroms",
        disulfide_bonds=False,
        disulfide_group_names=None,
        pbc=True,
        syntax="MolSysMT",
        engine="MolSysMT",
        sorted=True,
        skip_digestion=False,
        *,
        chemical_state="reference",
        with_templates=True,
        with_distances=True,
    ):
        return self._call(
            "get_missing_bonds",
            {
                "selection": selection,
                "structure_index": structure_index,
                "max_bond_length": max_bond_length,
                "disulfide_bonds": disulfide_bonds,
                "disulfide_group_names": disulfide_group_names,
                "pbc": pbc,
                "syntax": syntax,
                "engine": engine,
                "sorted": sorted,
                "skip_digestion": skip_digestion,
                "chemical_state": chemical_state,
                "with_templates": with_templates,
                "with_distances": with_distances,
            },
        )

    @_native_documentation("get_missing_residues", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_missing_residues(
        self,
        sequence=None,
        selection="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_missing_residues",
            {
                "sequence": sequence,
                "selection": selection,
                "syntax": syntax,
                "engine": engine,
            },
        )

    @_native_documentation("get_missing_terminal_cappings", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_missing_terminal_cappings(
        self,
        selection="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_missing_terminal_cappings",
            {
                "selection": selection,
                "syntax": syntax,
                "engine": engine,
            },
        )

    @_native_documentation("get_non_standard_residues", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_non_standard_residues(
        self,
        selection="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_non_standard_residues",
            {
                "selection": selection,
                "syntax": syntax,
                "engine": engine,
            },
        )

    @_native_documentation("get_disulfide_bonds", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_disulfide_bonds(
        self,
        selection="all",
        structure_index=0,
        max_bond_length=None,
        group_names=None,
        pbc=True,
        syntax="MolSysMT",
        engine="MolSysMT",
        sorted=True,
        skip_digestion=False,
    ):
        return self._call(
            "get_disulfide_bonds",
            {
                "selection": selection,
                "structure_index": structure_index,
                "max_bond_length": max_bond_length,
                "group_names": group_names,
                "pbc": pbc,
                "syntax": syntax,
                "engine": engine,
                "sorted": sorted,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("has_hydrogens", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def has_hydrogens(
        self,
        selection="all",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "has_hydrogens",
            {
                "selection": selection,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("is_solvated", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_solvated(
        self,
        skip_digestion=False,
    ):
        return self._call(
            "is_solvated",
            {
                "skip_digestion": skip_digestion,
            },
        )

    @_independent_build_documentation("infer_covalent_bonds")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def infer_covalent_bonds(
        self,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        method="supported_group_templates",
        return_report=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "infer_covalent_bonds",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "return_report": return_report,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_independent_build_documentation("assign_autodock_atom_types")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def assign_autodock_atom_types(
        self,
        typing_scheme,
        structure_indices="all",
        chemical_state="reference",
        method="chemical_environment",
        return_report=False,
        skip_digestion=False,
    ):
        return self._call(
            "assign_autodock_atom_types",
            {
                "typing_scheme": typing_scheme,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "return_report": return_report,
                "skip_digestion": skip_digestion,
            },
        )

    @_independent_build_documentation("assign_partial_charges")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def assign_partial_charges(
        self,
        method,
        structure_indices="all",
        chemical_state="reference",
        forcefield=None,
        water_model=None,
        expected_total_charge=None,
        return_report=False,
        skip_digestion=False,
    ):
        return self._call(
            "assign_partial_charges",
            {
                "method": method,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "forcefield": forcefield,
                "water_model": water_model,
                "expected_total_charge": expected_total_charge,
                "return_report": return_report,
                "skip_digestion": skip_digestion,
            },
        )

    @_independent_build_documentation("project_atom_names")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def project_atom_names(
        self,
        target_form,
        selection="all",
        return_report=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "project_atom_names",
            {
                "target_form": target_form,
                "selection": selection,
                "return_report": return_report,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_independent_build_documentation("make_bioassembly")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def make_bioassembly(
        self,
        bioassembly=None,
        structure_indices=0,
        to_form=None,
        skip_digestion=False,
    ):
        return self._call(
            "make_bioassembly",
            {
                "bioassembly": bioassembly,
                "structure_indices": structure_indices,
                "to_form": to_form,
                "skip_digestion": skip_digestion,
            },
        )

    @_independent_build_documentation("merge_nonpolar_hydrogens")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def merge_nonpolar_hydrogens(
        self,
        typing_scheme,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        return_report=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "merge_nonpolar_hydrogens",
            {
                "typing_scheme": typing_scheme,
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "return_report": return_report,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_independent_build_documentation("add_terminal_atoms")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def add_terminal_atoms(
        self,
        new_atoms,
        coordinates,
        attribute_policy="intersection",
        skip_digestion=False,
    ):
        return self._call(
            "add_terminal_atoms",
            {
                "new_atoms": new_atoms,
                "coordinates": coordinates,
                "attribute_policy": attribute_policy,
                "skip_digestion": skip_digestion,
            },
        )

    @_independent_build_documentation("add_missing_heavy_atoms")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def add_missing_heavy_atoms(
        self,
        selection="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        skip_digestion=False,
        *,
        attribute_policy="intersection",
    ):
        return self._call(
            "add_missing_heavy_atoms",
            {
                "selection": selection,
                "syntax": syntax,
                "engine": engine,
                "skip_digestion": skip_digestion,
                "attribute_policy": attribute_policy,
            },
        )

    @_independent_build_documentation("add_missing_hydrogens")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def add_missing_hydrogens(
        self,
        pH=7.4,
        engine="OpenMM",
        skip_digestion=False,
        *,
        mode="pH",
        chemical_state="reference",
        structure_indices="all",
        return_report=False,
        attribute_policy="intersection",
    ):
        return self._call(
            "add_missing_hydrogens",
            {
                "pH": pH,
                "engine": engine,
                "skip_digestion": skip_digestion,
                "mode": mode,
                "chemical_state": chemical_state,
                "structure_indices": structure_indices,
                "return_report": return_report,
                "attribute_policy": attribute_policy,
            },
        )

    @_independent_build_documentation("add_missing_terminal_cappings")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def add_missing_terminal_cappings(
        self,
        N_terminal=None,
        C_terminal=None,
        pH=7.4,
        keep_ids=False,
        selection="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "add_missing_terminal_cappings",
            {
                "N_terminal": N_terminal,
                "C_terminal": C_terminal,
                "pH": pH,
                "keep_ids": keep_ids,
                "selection": selection,
                "syntax": syntax,
                "engine": engine,
                "skip_digestion": skip_digestion,
            },
        )

    @_independent_build_documentation("editable")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def editable(self, skip_digestion=False):
        return self._call("editable", {"skip_digestion": skip_digestion})

    @_independent_build_documentation("remove_overlapping_molecules", local_skip=True)
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def remove_overlapping_molecules(
        self,
        selection,
        selection_2=None,
        structure_index=0,
        threshold="3 angstroms",
        pbc=True,
        syntax="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "remove_overlapping_molecules",
            {
                "selection": selection,
                "selection_2": selection_2,
                "structure_index": structure_index,
                "threshold": threshold,
                "pbc": pbc,
                "syntax": syntax,
            },
        )

    @_independent_build_documentation("mutate", local_skip=True)
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def mutate(
        self,
        mutations=None,
        keys="group_index",
        selection="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "mutate",
            {
                "mutations": mutations,
                "keys": keys,
                "selection": selection,
                "syntax": syntax,
                "engine": engine,
            },
        )

    @_independent_build_documentation("build_peptide", local_skip=True)
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def build_peptide(
        self, to_form="molsysmt.MolSys", engine="MolSysMT", *, skip_digestion=False
    ):
        return self._call("build_peptide", {"to_form": to_form, "engine": engine})
