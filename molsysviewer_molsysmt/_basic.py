"""Thin explicit scientific wrappers; no unknown mutating exports are proxied."""

import inspect
import re

from argdigest import arg_digest
from smonitor import signal


def _native_documentation(name, module="basic", *, bind_primary=True):
    def decorate(function):
        import molsysmt

        native = getattr(getattr(molsysmt, module), name)
        doc = inspect.getdoc(native) or ""
        doc = re.sub(
            r"(?m)^molecular_system :[^\n]*\n(?:[ \t]+[^\n]*\n|\n)*",
            "",
            doc,
            count=1,
        )
        # Keep the provider's parameter/result definitions as the help source.
        # Examples are explicitly native calls, not invented addon signatures.
        first, _, rest = doc.partition("\n")
        binding = (
            "This utility keeps its explicit molecular_systems collection; "
            "no current view.molsys is inserted. "
            if name == "are_multiple_molecular_systems"
            else (
                "The primary molecular system is the current view.molsys. "
                if bind_primary
                else "This utility keeps its explicit scientific inputs; "
                "no current view.molsys or implicit box is inserted. "
            )
        )
        function.__doc__ = (
            first
            + "\n\n"
            + binding
            + "The remaining parameters and returns follow the native function below. "
            "Its examples show ordinary MolSysMT calls.\n" + rest
        )
        if module == "pbc" and name not in {"wrap_to_pbc", "wrap_to_mic", "unwrap"}:
            function.__doc__ += (
                "\n\nView integration\n----------------\n"
                "The native scientific value is returned without a scene object, "
                "molecular edit, box assignment, result adoption or scene update. "
                "Box vectors are rows. Native unit policy, numerical rounding and "
                "angle-based shape classification are preserved. Shape labels "
                "summarize the native mean-angle criterion, not edge equality.\n"
            )
            if bind_primary:
                function.__doc__ += (
                    "has_pbc reads the current primary through the managed reader, "
                    "including pending scientific edits. Its native criterion uses "
                    "the first structure, not an all-structures aggregation.\n"
                )
            else:
                function.__doc__ += (
                    "This explicit-input utility works before a system is loaded, "
                    "while its owning view remains open. Inputs stay caller-owned "
                    "and must remain stable during the call; no managed molecular "
                    "edit lock is acquired for them. Obtain selected boxes explicitly "
                    "with basic.get(box=True, structure_indices=...).\n"
                )
            if "skip_digestion" not in inspect.signature(native).parameters:
                function.__doc__ += (
                    "skip_digestion : bool, keyword-only, default=False\n"
                    "    Control addon digestion only. The native callable has no "
                    "declared skip_digestion parameter and retains ordinary validation.\n"
                )
            if name == "get_box_from_lengths_and_angles":
                function.__doc__ += (
                    "Omitted or None angles delegate to the native orthogonal "
                    "box default. The addon does not synthesize angles. Native output "
                    "has shape (n_structures, 3, 3).\n"
                )
        if name in {
            "get_form",
            "is_a_molecular_system",
            "are_multiple_molecular_systems",
        }:
            function.__doc__ += (
                "\n\nView integration\n----------------\n"
                "skip_digestion : bool, keyword-only, default=False\n"
                "    Control addon argument digestion only. The native helper deliberately "
                "has no digestion escape hatch and receives no such argument. View lifetime "
                "checks remain active.\n"
            )
        if name == "are_multiple_molecular_systems":
            function.__doc__ += (
                "The explicit collection may be checked before this view loads a system. "
                "Inputs are caller-owned and must remain stable during the native call; "
                "the utility acquires no managed-edit locks for them. It neither combines "
                "systems nor loads or adopts a result into the view.\n"
            )
        if name == "where_is_attribute":
            function.__doc__ += (
                "\n\nView integration\n----------------\n"
                "The native item/form pair is returned without copying. Its item may be "
                "the actual current view.molsys; later external edits retain explicit "
                "reconciliation responsibilities.\n"
            )
        if module == "physchem":
            function.__doc__ += (
                "\n\nView integration\n----------------\n"
                "The native scientific value is returned, not a scene object. "
                "No assignment, implicit preparation, result adoption or scene update "
                "is introduced. Native derived/cache behavior, definitions, units, "
                "container types and supported element scopes remain unchanged. "
                "Group scales require names present in their native table; missing "
                "chemical groups are not silently assigned neutral values. "
                "OpenMM definitions retain their native form/parameterization limits; "
                "a table charge is not an assigned partial charge or a protonation model.\n"
                "Selection syntax and element scopes follow the repaired native "
                "contract under uibcdf/molsysmt#470 and uibcdf/molsysmt#471. "
                "Unsupported levels reject explicitly; no aggregation is invented. "
                "OpenMM charge conversion of a multi-frame periodic box is rejected; "
                "the addon never selects a frame implicitly.\n"
            )
        if (
            module == "physchem"
            and "skip_digestion" not in inspect.signature(native).parameters
        ):
            function.__doc__ += (
                "skip_digestion : bool, keyword-only, default=False\n"
                "    Control addon digestion only; this native callable has no "
                "declared skip_digestion parameter and retains ordinary validation.\n"
            )
        if module == "physchem" and name.startswith("get_protor"):
            function.__doc__ += (
                "ProtOr returns native atom types/provenance or radii in nm. "
                "It does not add hydrogens, store chemical assignments or prepare "
                "the primary. Native heavy-atom rules, ignored hydrogen typing "
                "and radius fallbacks remain distinct.\n"
            )
        if module == "physchem" and name in {
            "get_surface_area",
            "get_volume",
            "get_area_buried",
            "get_buried_fraction",
        }:
            function.__doc__ += (
                "These are reference-table values per group, not geometry calculated "
                "from the visible structure. Native raw list/array values are preserved; "
                "the addon adds no quantity units, conversion or normalization. "
                "Use get_sasa for an explicit conformational "
                "surface calculation, with its separate native engine limitations. "
                "get_area_buried has no native syntax argument. Other native syntax "
                "and supported-level choices retain ordinary public validation.\n"
            )
        if module == "physchem" and name in {
            "get_hydrogen_inventory",
            "get_chemical_readiness",
        }:
            function.__doc__ += (
                "This is a detached stored-chemistry report, not a preparation "
                "operation or chemical-validity certificate. Select one distinct "
                "structure when coordinates exist; the addon does not substitute "
                "the visible structure for the native default. Native chemical "
                "state/reference resolution, sorted unique source indices, empty "
                "arrays and issue/coverage semantics are retained. Missing data "
                "remain unknown; no valence, protonation or missing atoms are inferred. "
                "No hydrogen placement dependency is added. Returned report edits "
                "do not update the primary or scene.\n"
            )
        if module == "physchem" and name == "get_hydrogen_inventory":
            function.__doc__ += (
                "Indexed H neighbors and stored virtual H annotations are separate. "
                "Counts are dimensionless int64; -1 is unknown, not zero. The full "
                "graph is audited before filtering selected parents, whose H pairs "
                "may include H atoms outside the output atom selection.\n"
            )
        if module == "physchem" and name == "get_chemical_readiness":
            function.__doc__ += (
                "Incident/crossing bonds retain source indices, including external "
                "endpoints. Coordinate values are finite-position booleans, not "
                "coordinate arrays. Stored-field availability and declared evidence "
                "do not establish a universal ready flag or downstream suitability. "
                "Default-reference external syntax follows the native #480 repair. "
                "Explicit/associated states retain the public selector's restrictions; "
                "no selector translation or implicit state choice is added.\n"
            )
        if module == "physchem" and name == "get_sasa":
            function.__doc__ += (
                "This is a conformational surface calculation. All primary atoms "
                "remain occluders; selection filters the reported elements. Native "
                "structure ordering, probe units, sampling and execution options "
                "are forwarded without hidden preparation or engine overrides. "
                "Periodic control pbc is forwarded explicitly: native MIC screening "
                "uses other atom indices and excludes self-images; MDTraj requires "
                "pbc=False for boxed input. Area units follow the squared configured "
                "standard length unit. Native corrections are guarded under "
                "uibcdf/molsysmt#478 and uibcdf/molsysmt#479. "
                "CPU receiving uses explicit use_gpu=False; GPU support requires "
                "its own native qualification. No color or representation is added.\n"
            )
        if module == "physchem" and name == "get_surface_area":
            function.__doc__ += (
                "The Collantes unit label requires verification under "
                "uibcdf/molsysmt#473. Raw output is not received as a verified "
                "nm-squared quantity or calculated conformational SASA.\n"
            )
        if module in {"topology", "structure"} and name not in {
            "translate",
            "rotate",
            "flip",
            "least_rmsd_fit",
            "least_rmsd_align",
            "center",
            "move_away",
            "align_principal_axes",
            "set_dihedral_angles",
            "shift_dihedral_angles",
        }:
            function.__doc__ += (
                "\n\nView integration\n----------------\n"
                "The result is a native scientific value, not a scene object. "
                "No molecular edit, implicit preparation, adoption or scene update "
                "is introduced. Native derived/cache behavior is unchanged.\n"
            )
            if "skip_digestion" not in inspect.signature(native).parameters:
                function.__doc__ += (
                    "skip_digestion : bool, keyword-only, default=False\n"
                    "    Control addon digestion only; the native callable has no "
                    "declared skip_digestion parameter and is invoked with its ordinary "
                    "public validation. The flag is not added to scientific **kwargs.\n"
                )
        if module == "structure" and name in {
            "translate",
            "rotate",
            "flip",
            "least_rmsd_fit",
            "least_rmsd_align",
            "center",
            "move_away",
            "align_principal_axes",
            "set_dihedral_angles",
            "shift_dihedral_angles",
        }:
            function.__doc__ += (
                "\n\nView integration\n----------------\n"
                "update_view : bool, keyword-only, default=True\n"
                "    Synchronize an admitted in-place coordinate edit immediately. "
                "False defers projection only; sync_view() finishes pending work. "
                "The native in_place=False default returns an independent native result "
                "without adoption or scene update. Native quantities, broadcasting "
                "and returns remain unchanged. Source identities and axes are retained; "
                "named interactions follow native edited-structure invalidation. "
                "A synchronization failure exposes science_completed=True and the "
                "native scientific_result; retry synchronization, not the scientific operation. "
                "Potential partial scientific writes require explicit recovery.\n"
            )
        if module == "pbc" and name in {"wrap_to_pbc", "wrap_to_mic", "unwrap"}:
            function.__doc__ += (
                "\n\nView integration\n----------------\n"
                "update_view : bool, keyword-only, default=True\n"
                "    Synchronize an admitted in-place coordinate edit immediately. "
                "False defers projection only; sync_view() finishes pending work. "
                "The native in_place=False default returns an independent native result "
                "without adoption or scene update. Native row-vector boxes, units, "
                "ordered structure indices and results remain scientific-owner behavior. "
                "Named interactions follow native edited-structure invalidation. "
                "A synchronization failure exposes science_completed=True and the "
                "scientific_result; retry synchronization, not scientific work. "
                "The addon adds no minimum-image algorithm, reconstruction or "
                "implicit periodic preparation.\n"
            )
            if name == "unwrap":
                function.__doc__ += (
                    "Unwrapping follows the supplied structure order and restores "
                    "per-atom temporal continuity; it is not covalent reconstruction "
                    "inside one structure. No unsupplied trajectory history is inferred.\n"
                )
            else:
                function.__doc__ += (
                    "compact='component' keeps covalent blocks whole; False wraps "
                    "atoms independently. Origins and centers remain explicit native "
                    "parameters. Centered in-place wrapping publishes to the original "
                    "primary through the native repair under uibcdf/molsysmt#467. "
                    "The centering reference must be contained in the moved selection. "
                    "Independent centered outputs remain separate.\n"
                )
        if module == "structure" and name == "flip":
            function.__doc__ += (
                "skip_digestion : bool, keyword-only, default=False\n"
                "    Control addon digestion only; the native flip callable has no "
                "declared escape hatch and always receives ordinary validation.\n"
                "Reflection can invert chirality; it is not a proper rotation or "
                "an automatic change to topology or chemical-state assignments.\n"
                "The native None default uses the z normal. Finite nonzero normals "
                "are normalized by native validation; their scale or sign does not "
                "change the plane. Undefined normals and invalid plane points reject "
                "before coordinate writes (uibcdf/molsysmt#460). The addon forwards "
                "these inputs unchanged and supplies no reflection algorithm.\n"
            )
        if module == "structure" and name in {
            "set_dihedral_angles",
            "shift_dihedral_angles",
        }:
            function.__doc__ += (
                "Native quartets, angular units, ordered structure axes and "
                "moving covalent blocks determine the edit. The addon adds no "
                "torsion formula, graph cut, block correction or periodic preparation. "
                "Native editors reject nonfinite edit requests before coordinate "
                "publication and preserve explicit block pools, including shifting "
                "(uibcdf/molsysmt#461 and #462, source repair 6f6ed6bf1). "
                "Only bounded finite scientific routes are received; this is not "
                "unconditional scientific or installed-package qualification.\n"
            )
            if name == "set_dihedral_angles":
                function.__doc__ += (
                    "skip_digestion : bool, keyword-only, default=False\n"
                    "    Control addon digestion only. Native set_dihedral_angles "
                    "has no skip_digestion parameter and retains ordinary validation.\n"
                )
        if module == "structure" and name == "align_principal_axes":
            function.__doc__ += (
                "skip_digestion : bool, keyword-only, default=False\n"
                "    Control addon digestion only. The native callable has no "
                "skip_digestion argument and always receives ordinary validation. "
                "Native principal_axes_of_selection defines the fitting population "
                "independently of the atoms moved by selection. Target axes are rows "
                "of a right-handed orthonormal basis; degenerate moments reject. "
                "The center flag controls translation relative to the initial "
                "weighted fitting center. The addon adds no eigensolver, sign choice, "
                "periodic reconstruction, box rotation or scientific preparation.\n"
            )
        if module == "structure" and name == "move_away":
            function.__doc__ += (
                "Only single-structure nondegenerate displacement is qualified at the "
                "reviewed source. Auto direction adds distance to the existing separation; "
                "explicit direction places the source center at the initial reference "
                "center plus distance along the normalized direction. The reference "
                "remains caller-owned and is not locked or synchronized by this call. "
                "Undefined, zero or nonfinite directions and multiple structures "
                "are rejected by the native tool before coordinate writes "
                "(uibcdf/molsysmt#456 and #457). Rejection preserves coordinates "
                "and interaction coverage. "
                "The addon supplies no substitute geometry or periodic preparation.\n"
            )
        if module == "structure" and name == "center":
            function.__doc__ += (
                "All three atom populations address the current view.molsys. "
                "Native centering owns source containment, destination snapshots, "
                "weights, units and refinement. The addon introduces no center "
                "calculation, legacy keyword alias or automatic periodic preparation.\n"
            )
        if module == "structure" and name in {"least_rmsd_fit", "least_rmsd_align"}:
            function.__doc__ += (
                "An external reference remains caller-owned; keep it stable for "
                "the call. Only the bound primary view is serialized, with no automatic "
                "locking or synchronization of another reference view. No periodic "
                "reimaging, molecular preparation or scientific fitting is added here.\n"
            )
        if module == "structure" and name == "least_rmsd_fit":
            function.__doc__ += (
                "selection_fit and reference_selection_fit define the ordered native "
                "fit anchors; selection defines the atoms moved. to_form affects the "
                "native independent output only, without adopting that result.\n"
            )
        if module == "structure" and name == "least_rmsd_align":
            function.__doc__ += (
                "selection and reference_selection define sequence-derived anchors; "
                "the native operation moves complete selected components, not only "
                "those anchor atoms. Native omitted/None self-reference uses the "
                "original reference_structure_index, including in-place edits. "
                "Native atom indices and full-axis Boolean masks are resolved before "
                "sequence-group projection; selected names stay paired within each "
                "identically aligned group. These repairs are tracked under "
                "uibcdf/molsysmt#452 and uibcdf/molsysmt#453. The addon forwards "
                "arguments without replacing references or calculating correspondences.\n"
            )
        if name in {"copy", "convert", "get_conversion_report"}:
            function.__doc__ += (
                "\n\nView integration\n----------------\n"
                "The result is not adopted and no scene update is requested. "
                "Explicit filenames address the Python host filesystem, not a browser download. "
                "Conversion ownership and optional converter dependencies remain native; "
                "copy_if_all=False may expose shared/live data. Reports describe only their "
                "declared audited scopes and are not a guarantee of complete format fidelity.\n"
            )
        if name in {"contains", "is_composed_of", "compare"}:
            function.__doc__ += (
                "\n\nView integration\n----------------\n"
                "The current view is the primary system. Native queries return their "
                "ordinary results without adopting data, attaching analyses or requesting "
                "a scene update. Native derived/cache behavior is unchanged.\n"
            )
        if name == "compare":
            function.__doc__ += (
                "The second molecular_system_2 input remains explicit. The initial "
                "receiver admits redefine_indices=False only. True rebuilds topology "
                "in both native inputs and raises NotImplementedError before edits, "
                "also with skip_digestion=True. This mutating route needs separate "
                "receiving and reconciliation.\n"
            )
        if name == "remove":
            function.__doc__ += (
                "\n\nView integration\n----------------\n"
                "update_view : bool, keyword-only, default=True\n"
                "    Reconcile an in-place edit immediately. False defers only the scene update; "
                "call tools.sync_view() to apply pending edits. Independent outputs are never adopted. "
                "The initial retained-axis receiver rejects removal of every atom or structure "
                "before executing in-place science. Use in_place=False for those outputs.\n"
                "A scene update failure raises SystemEditSyncError with science_completed=True, "
                "operation_id and scientific_result; retry synchronization, not removal.\n"
            )
        if name == "set":
            function.__doc__ += (
                "\n\nView integration\n----------------\n"
                "update_view : bool, keyword-only, default=True\n"
                "    Reconcile the bound edit immediately; False defers projection only. "
                "The initial receiver admits coordinates and box with retained atom/structure "
                "axes, native units/selection/order and native None return. Other attributes "
                "are rejected before scientific execution. Native setters invalidate only "
                "affected structures; no detector runs. Use sync_view() to retry projection, "
                "not set() again. Potentially partial writes require explicit recovery.\n"
            )
        return function

    return decorate


class _BasicTools:
    _NAMES = (
        "get",
        "select",
        "info",
        "get_attributes",
        "has_attribute",
        "get_label",
        "get_form",
        "where_is_attribute",
        "is_a_molecular_system",
        "are_multiple_molecular_systems",
        "contains",
        "is_composed_of",
        "compare",
        "extract",
        "copy",
        "convert",
        "get_conversion_report",
        "remove",
        "set",
    )

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call(self, name, parameters, extra=None):
        from molsysmt import basic

        return self._owner._read(getattr(basic, name), parameters, extra)

    @_native_documentation("get")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get(
        self,
        element="system",
        selection="all",
        structure_indices="all",
        mask=None,
        syntax="MolSysMT",
        get_missing_bonds=True,
        output_type="values",
        chemical_state="reference",
        skip_digestion=False,
        **kwargs,
    ):
        return self._call(
            "get",
            {
                "element": element,
                "selection": selection,
                "structure_indices": structure_indices,
                "mask": mask,
                "syntax": syntax,
                "get_missing_bonds": get_missing_bonds,
                "output_type": output_type,
                "chemical_state": chemical_state,
                "skip_digestion": skip_digestion,
            },
            kwargs,
        )

    @_native_documentation("select")
    @signal(tags=["addon", "selection"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def select(
        self,
        selection="all",
        structure_indices="all",
        element="atom",
        mask=None,
        syntax="MolSysMT",
        to_syntax=None,
        chemical_state="reference",
        skip_digestion=False,
    ):
        return self._call(
            "select",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "element": element,
                "mask": mask,
                "syntax": syntax,
                "to_syntax": to_syntax,
                "chemical_state": chemical_state,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("info")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def info(
        self,
        element="system",
        selection="all",
        structure_indices="all",
        syntax="MolSysMT",
        output_type="styler",
        skip_digestion=False,
        *,
        mask=None,
    ):
        return self._call(
            "info",
            {
                "element": element,
                "selection": selection,
                "structure_indices": structure_indices,
                "syntax": syntax,
                "output_type": output_type,
                "skip_digestion": skip_digestion,
                "mask": mask,
            },
        )

    @_native_documentation("get_attributes")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_attributes(
        self,
        include_none=False,
        attribute_type="all",
        output_type="list",
        skip_digestion=False,
    ):
        return self._call(
            "get_attributes",
            {
                "include_none": include_none,
                "attribute_type": attribute_type,
                "output_type": output_type,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("has_attribute")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def has_attribute(
        self,
        attribute,
        include_none=False,
        structure_indices="all",
        chemical_state="reference",
        skip_digestion=False,
    ):
        return self._call(
            "has_attribute",
            {
                "attribute": attribute,
                "include_none": include_none,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_label")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_label(
        self,
        element="atom",
        selection="all",
        string="{name}-{id}@{index}",
        syntax="MolSysMT",
        skip_digestion=False,
        **kwargs,
    ):
        return self._call(
            "get_label",
            {
                "element": element,
                "selection": selection,
                "string": string,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
            kwargs,
        )

    @_native_documentation("get_form")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_form(self, *, skip_digestion=False):
        return self._call("get_form", {})

    @_native_documentation("is_a_molecular_system")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_a_molecular_system(self, *, skip_digestion=False):
        return self._call("is_a_molecular_system", {})

    @_native_documentation("are_multiple_molecular_systems")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def are_multiple_molecular_systems(
        self, molecular_systems, *, skip_digestion=False
    ):
        self._owner._view()
        from molsysmt.basic import are_multiple_molecular_systems

        # This is an explicit-input utility, not a bound-primary reader. Its
        # collection remains caller-owned, including before a view is loaded.
        return are_multiple_molecular_systems(molecular_systems)

    @_native_documentation("where_is_attribute")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def where_is_attribute(self, attribute, include_none=False, skip_digestion=False):
        return self._call(
            "where_is_attribute",
            {
                "attribute": attribute,
                "include_none": include_none,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("contains")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def contains(
        self, selection="all", syntax="MolSysMT", skip_digestion=False, **kwargs
    ):
        return self._call(
            "contains",
            {
                "selection": selection,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
            kwargs,
        )

    @_native_documentation("is_composed_of")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_composed_of(
        self, selection="all", syntax="MolSysMT", skip_digestion=False, **kwargs
    ):
        return self._call(
            "is_composed_of",
            {
                "selection": selection,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
            kwargs,
        )

    @_native_documentation("compare")
    @signal(tags=["addon", "compare"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def compare(
        self,
        molecular_system_2,
        selection="all",
        structure_indices="all",
        selection_2="all",
        structure_indices_2="all",
        syntax="MolSysMT",
        rule="equal",
        output_type="boolean",
        attribute_type=None,
        include_none=False,
        redefine_indices=False,
        skip_digestion=False,
        **kwargs,
    ):
        self._owner._target()
        from molsysmt._private.argdigest.argument.redefine_indices import (
            digest_redefine_indices,
        )

        # The forced native branch rebuilds BOTH inputs. It is an edit family,
        # not an ordinary reader, including for a trusted skip_digestion call.
        redefine_indices = digest_redefine_indices(
            redefine_indices, caller="molsysmt.basic.compare.compare"
        )
        if redefine_indices:
            raise NotImplementedError(
                "Bound compare does not yet receive redefine_indices=True, which "
                "rebuilds topology in both systems. Use native MolSysMT with explicit "
                "reconciliation of affected views for that edit."
            )
        return self._call(
            "compare",
            {
                "molecular_system_2": molecular_system_2,
                "selection": selection,
                "structure_indices": structure_indices,
                "selection_2": selection_2,
                "structure_indices_2": structure_indices_2,
                "syntax": syntax,
                "rule": rule,
                "output_type": output_type,
                "attribute_type": attribute_type,
                "include_none": include_none,
                "redefine_indices": redefine_indices,
                "skip_digestion": skip_digestion,
            },
            kwargs,
        )

    @_native_documentation("extract")
    @signal(tags=["addon", "extract"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def extract(
        self,
        selection="all",
        structure_indices="all",
        to_form=None,
        output_filename=None,
        copy_if_all=True,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "extract",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "to_form": to_form,
                "output_filename": output_filename,
                "copy_if_all": copy_if_all,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("copy")
    @signal(tags=["addon", "copy"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def copy(self, output_filename=None, skip_digestion=False):
        return self._call(
            "copy",
            {"output_filename": output_filename, "skip_digestion": skip_digestion},
        )

    @_native_documentation("convert")
    @signal(tags=["addon", "conversion"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def convert(
        self,
        to_form="molsysmt.MolSys",
        selection="all",
        structure_indices="all",
        syntax="MolSysMT",
        strict=False,
        return_report=False,
        skip_digestion=False,
        **kwargs,
    ):
        return self._call(
            "convert",
            {
                "to_form": to_form,
                "selection": selection,
                "structure_indices": structure_indices,
                "syntax": syntax,
                "strict": strict,
                "return_report": return_report,
                "skip_digestion": skip_digestion,
            },
            kwargs,
        )

    @_native_documentation("get_conversion_report")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_conversion_report(
        self,
        to_form="molsysmt.MolSys",
        selection="all",
        structure_indices="all",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_conversion_report",
            {
                "to_form": to_form,
                "selection": selection,
                "structure_indices": structure_indices,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("remove")
    @signal(tags=["addon", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def remove(
        self,
        selection=None,
        structure_indices=None,
        to_form=None,
        syntax="MolSysMT",
        in_place=False,
        skip_digestion=False,
        *,
        update_view=True,
    ):
        parameters = {
            "selection": selection,
            "structure_indices": structure_indices,
            "to_form": to_form,
            "syntax": syntax,
            "in_place": in_place,
            "skip_digestion": skip_digestion,
        }
        # This branch determines integration, so it remains validated even when
        # native argument digestion is explicitly skipped.
        from molsysmt._private.argdigest.argument.in_place import digest_in_place

        in_place = digest_in_place(
            in_place, caller="molsysviewer_molsysmt.basic.remove"
        )
        if not isinstance(update_view, bool):
            raise TypeError("update_view must be a boolean.")
        if not in_place:
            return self._call("remove", parameters)

        view = self._owner._view_ref()
        self._owner._target()  # Closed/empty rejection before host access.
        coordinator = getattr(view.addons.manager, "system_edits", None)
        if coordinator is None:
            raise RuntimeError(
                "This Viewer host lacks managed molecular-edit receiving. Update the host before in-place edits."
            )
        return coordinator.execute(
            lambda target: self._prepare_removal(target, parameters),
            name="molsysmt.basic.remove",
            update_view=update_view,
        )

    @staticmethod
    def _prepare_removal(target, parameters):
        from molsysmt import basic
        from molsysmt._private.variables import is_all
        from molsysmt.basic._index_validation import (
            validate_element_indices,
            validate_structure_indices,
        )
        from molsysmt.native._subset import validate_removal_target

        validate_removal_target(target, parameters["to_form"])
        selection = parameters["selection"]
        atoms = (
            []
            if selection is None
            else basic.select(
                target,
                selection=selection,
                syntax=parameters["syntax"],
                skip_digestion=parameters["skip_digestion"],
            )
        )
        atoms = validate_element_indices(
            target, atoms, "atom", "selection", "molsysmt.remove"
        )
        n_atoms, n_frames = (
            int(target.get_n_atoms()),
            int(target.structures.n_structures),
        )
        removed_atoms = set(range(n_atoms)) if is_all(atoms) else set(atoms)
        frames = validate_structure_indices(
            target, parameters["structure_indices"], "molsysmt.remove"
        )
        removed_frames = (
            set(range(n_frames))
            if is_all(frames)
            else set([] if frames is None else frames)
        )
        atom_map = (
            None
            if not removed_atoms
            else {
                old: new
                for new, old in enumerate(
                    i for i in range(n_atoms) if i not in removed_atoms
                )
            }
        )
        frame_map = (
            None
            if not removed_frames
            else [i for i in range(n_frames) if i not in removed_frames]
        )
        return {
            "run": lambda: basic.remove(target, **parameters),
            "changed": bool(removed_atoms or removed_frames),
            "atom_index_map": atom_map if removed_atoms else None,
            "structure_index_map": frame_map if removed_frames else None,
            "interactions_policy": "preserve",
            # Native removal prepares an extracted candidate and publishes a
            # new state dictionary once. The host also checks dictionary identity
            # before accepting this atomic-rejection declaration.
            "failure_atomic": True,
        }

    @_native_documentation("set")
    @signal(tags=["addon", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def set(
        self,
        element=None,
        selection="all",
        structure_indices="all",
        syntax="MolSysMT",
        chemical_state="reference",
        skip_digestion=False,
        *,
        update_view=True,
        **kwargs,
    ):
        if "molecular_system" in kwargs:
            raise TypeError(
                "The primary molecular_system is bound to view.molsys and cannot be overridden."
            )
        if not isinstance(update_view, bool):
            raise TypeError("update_view must be a boolean.")
        self._owner._target()
        from ._geometry import _geometry_token, _prepare_geometry_set

        view = self._owner._view_ref()
        coordinator = getattr(view.addons.manager, "system_edits", None)
        if coordinator is None:
            raise RuntimeError(
                "This Viewer host lacks managed molecular-edit receiving."
            )
        parameters = {
            "element": element,
            "selection": selection,
            "structure_indices": structure_indices,
            "syntax": syntax,
            "chemical_state": chemical_state,
            "skip_digestion": skip_digestion,
        }
        return coordinator.execute(
            lambda target: _prepare_geometry_set(target, parameters, kwargs),
            name="molsysmt.basic.set",
            update_view=update_view,
            rejection_check=_geometry_token,
        )
