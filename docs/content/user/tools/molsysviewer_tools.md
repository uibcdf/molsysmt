(user-tools-molsysviewer)=
# MolSysViewer tools addon

Use MolSysMT tools on the molecular system already loaded in your view. The
expert API follows MolSysMT's module/function hierarchy, with `view.molsys`
supplied as the primary input.

## Availability

The experimental source implementation provides six queries under
`view.addons.molsysmt.basic`: `get`, `select`, `info`, `get_attributes`,
`has_attribute` and `get_label`, plus independent extraction with `extract`,
managed native removal with `remove`, the coordinates/box routes of `set`,
and native `copy`, `convert` and `get_conversion_report`. Presence/composition
checks `contains`, `is_composed_of` and the read-only `compare` route are also
received; the topology-rebuilding comparison mode remains pending. Identification
helpers `get_form`, `is_a_molecular_system`, `where_is_attribute` and the explicit
collection utility `are_multiple_molecular_systems` are also available in source.
Their root aliases are also available, such as `view.addons.molsysmt.get`.

The `view.addons.molsysmt.chemical_states` namespace provides the nine native
graph tools: bond graphs, covalent blocks/paths, dihedral quartets, rings, rigid
fragments, rotatable bonds, SMARTS matches and atom correspondences. Sequence
alignment and identity remain under `view.addons.molsysmt.topology`. Both follow
the independent native domains introduced by MolSysMT #255. There are no old-path
graph aliases or invented root aliases. Native scientific prerequisites and
optional-engine limits remain applicable. Source receiving is experimental;
scene-loader migration is tracked in MolSysViewer #269 and does not follow from
an addon registration or namespace check alone.
The current `view.addons.molsysmt.structure` slice adds `get_distances`,
`get_vectors`, `get_center`, `get_radius_of_gyration`, `get_angles`,
`get_dihedral_angles`, `get_rmsd`, `get_least_rmsd`, `get_principal_axes` and
`get_least_squares_plane`, `get_maximum_distances`, `get_contacts`, `get_rmsf`,
`get_minimum_distances`, `get_neighbors`, `get_symmetry_corrected_rmsd`,
`get_secondary_structure` and `principal_component_analysis`.
Results retain native quantities, arrays and metadata. The separate
`structure.translate`, `structure.rotate`, `structure.flip`, `structure.least_rmsd_fit`,
`structure.least_rmsd_align`, `structure.center`, `structure.move_away` and
`structure.align_principal_axes`, `structure.set_dihedral_angles` and
`structure.shift_dihedral_angles` wrappers receive independent outputs and managed
in-place coordinate changes. Sequence alignment receives the native self-reference and atom-index/mask
repairs documented below. Reflection receiving includes the default z normal and finite nonzero scaled normals,
with native pre-write rejection of invalid planes. Displacement receiving covers single-structure, finite nonzero directions; undefined directions and unsupported axes reject before native coordinate writes. The reviewed structure namespace now has explicit wrappers for all 28 native function exports; finite torsion requests and explicit block pools have bounded native and addon guards. This is source exposure and bounded receiving, not unconditional scientific or package compatibility.

The explicit `view.addons.molsysmt.pbc` namespace also provides ten box queries
and factories. Only `has_pbc` binds the current system; box/length/angle inputs
remain explicit for the other nine. The same namespace adds three coordinate
editors: `wrap_to_pbc`, `wrap_to_mic` and `unwrap`, with native independent
outputs or managed in-place updates. Centered in-place wrapping is received through the native #467 repair; see
the periodic sections for units and precise limits.

The `view.addons.molsysmt.build` namespace provides eleven read-only tools.
The first three are:
`get_residue_chemical_coverage`, `get_covalent_bond_candidates` and
`get_peptide_bond_candidates`. They return diagnostics/candidates, not prepared
systems or assigned bonds. Eight further readers audit missing heavy atoms, bonds,
residues and terminal cappings, nonstandard groups, indexed hydrogens, solvation
and disulfide candidates; see the preparation-audit section below. Their native single-structure, exact-template and
source metadata requirements remain explicit. Three additional build methods return
independent prepared systems: infer_covalent_bonds, assign_autodock_atom_types
and assign_partial_charges. They do not adopt the result or update the scene;
The label-only project_atom_names route also returns an independent output;
`add_missing_bonds` also receives native independent results or managed in-place
graph publication; its default is in-place. The native
`solve_atoms_with_alternate_location` route receives selected coordinate,
B-factor and atom-label publication with managed synchronization and explicit
native limitations. Other build editing remains pending.

The explicit `view.addons.molsysmt.interactions.hbonds` namespace now provides
four recognition/characterization tools: `get_donor_atoms`, `get_acceptor_atoms`,
`get_hbond_sites` and `get_hbond_site_directions`, plus native `get_hbonds`,
`get_buch_hbonds` and `get_luzard_chandler_hbonds` detection. The separate
`interactions.disulfides` family adds `get_disulfide_candidates`. These raw
scientific values remain distinct from the core `view.interactions` scene
owner; none is attached or represented automatically.

Three further families mirror native detection: `interactions.ionic.get_ionic_interactions`,
`interactions.hydrophobic.get_hydrophobic_interactions` and
`interactions.halogen_bonds.get_halogen_bonds`. They keep required scientific
inputs, optional providers and sparse output contracts. See their examples below.

The source now also exposes `interactions.metal_coordination.get_metal_coordination`,
`interactions.pi_pi.get_pi_pi_interactions`,
`interactions.cation_pi.get_cation_pi_interactions` and
`interactions.water_bridges.get_water_bridges`. All fifteen inventoried canonical
interaction function paths have explicit expert wrappers. This counts source
exposure, not unconditional scientific accuracy, stability or installed compatibility.

The initial `view.addons.molsysmt.molecular_mechanics` slice provides explicit
`get_engine_forcefield` resource lookup and primary-bound
`get_degrees_of_freedom`, `get_potential_energy`,
`get_non_bonded_potential_energy` and `potential_energy_minimization`.
The minimizer retains independent output by default and supports managed
in-place coordinate updates. Other mechanical calculations retain their separate
receiving; see the mechanical section for model, engine and ownership limits.

Independent `build` results also include biological assemblies and an explicit
AutoDock4 nonpolar-hydrogen projection. They preserve native preparation and
mapping requirements and never replace the view automatically; see the
construction examples below.
Explicit terminal-atom attachment and bounded missing-heavy-atom repair are
also available as independent outputs. Their atom identity, attribute-loss
and saved-analysis contracts are described below.
Hydrogen generation and terminal capping also mirror their native paths;
the pH-driven and explicitly fixed-state preparation contracts remain distinct.
Native builder staging and molecule-overlap filtering are also exposed, with
explicit independent-builder and conditional-result ownership.
Peptide construction from the loaded sequence and amino-acid mutation are
available as independent native results, with reconstruction limits below.

Other scientific modules, editing families and graphical task panels
are still being implemented. This is not a complete MolSysMT mirror
or a claim that the currently published package pair contains these tools.

The received `view.addons.molsysmt.element` slice contains eight explicit-input
utilities: `is_element`, `is_composed_of`, four `atom` type/name/isotope tools,
and `group.is_group_type` / `group.get_group_type_from_group_name`. They work
with an open empty view and keep caller inputs explicit; see the element
utilities section below. Nine current-system chain/entity readers are received
separately below. Twelve more primary-bound paths cover molecules, components,
group types and a legacy name heuristic. Fourteen more explicit name/type/code
utilities and fourteen reference-template queries are received below. The reviewed
element source surface has all 57 paths; native qualification limits remain explicit.

Install compatible versions of both components. MolSysMT supplies the
integration; MolSysViewer discovers its declared entry point automatically.
Source checkouts need current generated distribution metadata as well as an
editable installation after an entry-point change. No manual registration is needed in a correctly installed compatible
environment. Ordinary MolSysMT import and the core visualization backend work
independently of this optional interface.

## Discovering capabilities before loading a system

The experimental `view.addons.molsysmt.supported` namespace mirrors
`msm.supported.forms`, `conversions`, `dependencies` and `syntaxes`. These reports
work with an open empty view; they do not read the current molecular system,
synchronize pending edits or change the scene or history.

```python
import molsysviewer as msv

with msv.new_view() as view:
    tools = view.addons.molsysmt.supported
    file_forms = tools.forms("file", output_type="list")
    routes = tools.conversions(
        from_form=["molsysmt.MolSys"],
        to_form=["molsysmt.Topology"],
        output_type="dictionary",
    )
    syntaxes = tools.syntaxes(output_type="dataframe")
    dependencies = tools.dependencies(output_type="dictionary")
    assert "molsysmt.MolSys" in tools.forms(output_type="list")
    assert routes["data"] == [[True]]
    assert view.molsys is None
```

The native default remains a pandas Styler. Request `dataframe` or `dictionary`
for programmatic use; only `forms` also supports `list`. Filters, conversion
orientation and empty axes retain native behavior. Selection-input support and
translation-output support are separate syntax columns. A listed conversion
route or installed dependency does not guarantee that every molecular input or
optional scientific engine can execute it.

Results are fresh native metadata, not a view-owned scientific registry. They
remain usable after closing the view; new calls through a retained tools object
reject a closed owner. These utilities have no `molecular_system`, selection or
`update_view` argument. Source availability does not establish that a published
package pair contains them.

## Inspecting attribute metadata before loading a system

The `view.addons.molsysmt.attribute` namespace mirrors the seven native metadata
utilities. They work on an open empty view: they inspect explicit names and
query requirements without reading or changing the primary molecular system.

```python
import molsysviewer as msv

with msv.new_view() as view:
    metadata = view.addons.molsysmt.attribute
    aliases = metadata.get_argument_aliases()
    assert aliases["element_attribute_aliases"]["group"]["name"] == "group_name"
    assert metadata.is_attribute("atom_name") is True
    assert metadata.is_attribute("atom_names") is False
    assert metadata.is_chemical_state_attribute("bond_order") is True
    assert metadata.is_topological_attribute("bond_order") is True
    assert metadata.is_structural_attribute("atom_index") is True
    assert metadata.is_mechanical_attribute("forcefield") is True
    assert metadata.bonds_are_required_to_get_attribute("molecule_index", "atom") is False
    assert metadata.bonds_are_required_to_get_attribute("atom_index", "component") is True
```

`is_attribute()` tests canonical-name membership; it does not resolve synonyms.
`get_argument_aliases()` returns an independent versioned dictionary, including
element-dependent names. Editing that dictionary does not change MolSysMT or
install alias rules on other addon methods. The four classification predicates
preserve native validation and overlap: atom inventory can be both topological
and structural, and the compatibility topology predicate includes nonstructural
chemical-state attributes. A classification does not prove that a particular
system supplies that domain or that a mechanics engine is available.

The connectivity helper distinguishes stored stable inventory from state-local
graph queries. A bond or component source axis requires its chemical graph even
when the requested value describes atoms. Its `from_element=None` default
checks the requested attribute alone; no selection or source element is inferred
from the view. Conversion-specific reconstruction of missing inventory remains a
separate native responsibility.

All seven utilities preserve pending edits without synchronization or scene,
history, storage or scientific-calculation effects. Keep the view open while
calling them; detached results remain usable after close. Native predicates
with `skip_digestion` receive its value unchanged. The native `is_attribute` and
`get_argument_aliases` utilities have no such parameter, so their keyword-only
addon control validates the integration call and is not forwarded. This source
increment receives the native metadata/bootstrap repair from #534/#535; it does
not establish a new compatible published package floor.

## Using explicit element utilities

You can check a supplied label or normalize explicit isotope aliases before
loading a system. These helpers keep their scientific inputs; they do not read
`view.molsys`, assign atom/group types or change the scene.

```python
import molsysviewer as msv

with msv.new_view() as view:
    element = view.addons.molsysmt.element
    assert element.is_element("groups") is True
    assert element.is_composed_of("group", "atom") is True
    assert element.atom.is_atom_type("Ca") is True
    assert element.atom.is_atom_type("CA") is False
    assert element.atom.get_atom_type_from_atom_name("CA") == "C"
    assert element.atom.normalize_atom_types(
        ["C", "D", "T"], isotope=[13, None, 3]
    ) == (["C", "H", "H"], [13, 2, 3])
    assert element.atom.get_atom_type_from_atom_ff_type(
        ["A", "NA", "HD", "Cl"], typing_scheme="autodock4"
    ) == ["C", "N", "H", "Cl"]
    assert element.group.is_group_type("amino acid") is True
    assert element.group.get_group_type_from_group_name("ALA") == "amino acid"
```

`Ca` is a chemical element symbol; `CA` is an atom name in the name lookup.
Force-field labels use their explicitly named typing scheme. `D` and `T`
normalize to hydrogen with isotope mass numbers 2 and 3, respectively. No
reference isotope, force-field type, chemical preparation or charge is assigned.
Array/list shapes, errors, unknown-name warnings and result ownership follow
MolSysMT; these eight tools do not acquire the primary molecular reader or
flush pending managed edits.

`element.is_composed_of` reports the native declared relation between two
**element-level names**. It does not examine the contents of your system. The
existing `basic.is_composed_of` and its root alias keep their molecular-system
query role. Group-name lookup uses the public native export, including its
`"unknown"` marker and spelling; no additional classification is invented.

All eight methods expose `skip_digestion=False`. For `is_element`,
`is_composed_of`, `atom.get_atom_type_from_atom_name` and `group.is_group_type`,
this is a keyword-only addon control because the native function has no skip
parameter. It is consumed locally, and native validation remains in force.
The other four forward their declared native skip flag unchanged.

Native references: {func}`molsysmt.element.is_element`,
{func}`molsysmt.element.is_composed_of`,
{func}`molsysmt.element.atom.is_atom_type`,
{func}`molsysmt.element.atom.normalize_atom_types`,
{func}`molsysmt.element.atom.get_atom_type_from_atom_name`,
{func}`molsysmt.element.atom.get_atom_type_from_atom_ff_type`,
{func}`molsysmt.element.group.is_group_type` and
{func}`molsysmt.element.group.get_group_type_from_group_name`.

## Recognizing explicit labels and looking up amino-acid codes

Fourteen additional utilities accept explicit names without reading your system:
`component.is_component_type`, `molecule.is_molecule_type`, ten group-family
predicates, and the two amino-acid name/code lookups. They work before a system
is loaded and do not inspect coordinates, select atoms, assign chemistry or
change the scene.

```python
import molsysviewer as msv

with msv.new_view() as view:
    element = view.addons.molsysmt.element
    assert element.component.is_component_type("peptide") is True
    assert element.molecule.is_molecule_type("waters") is True
    assert element.group.amino_acid.is_amino_acid("ALA") is True
    assert element.group.ion.is_ion("NA") is True
    assert element.group.lipid.is_lipid("POPC") is True
    assert element.group.nucleotide.is_nucleotide("DA") is True
    assert element.group.saccharide.is_saccharide("NAG") is True
    assert element.group.small_molecule.is_small_molecule("ATP") is True
    assert element.group.water.is_water("HOH") is True
    assert element.group.terminal_capping.is_terminal_capping("ACE") is True
    # Classify the protected peptide end without attaching a cap.
    n_membership = element.group.terminal_capping.is_n_terminal_capping("ACE")
    c_membership = element.group.terminal_capping.is_c_terminal_capping("NME")
    assert isinstance(n_membership, bool) and isinstance(c_membership, bool)
    assert element.group.amino_acid.get_standard_name("MSE") == "MET"
    assert element.group.amino_acid.get_standard_name("ALA") is None
    assert element.group.get_1_letter_code_from_name("SEC", naming_scheme="sequence") == "U"
    assert view.molsys is None
```

These predicates recognize native catalogued labels. For example,
`small_molecule.is_small_molecule("ATP")` can be True even when the view has no
ATP atoms. It is distinct from the primary-bound legacy amino-acid name
heuristic below. Native case, supported scalar inputs, returns and errors stay
unchanged; no array-vectorization or unknown-name fallback is added.

`get_standard_name` returns a replacement label for a known non-standard name,
such as MSE -> MET. It returns None for an already-standard name or one without
a known replacement. This is a name lookup, not a validation or a transformation
of atoms, elements, connectivity, stereochemistry or protonation. The one-letter
lookup uses the canonical group-level path and preserves native context diagnostics
rather than guessing a vocabulary or code. The retired amino-acid path has no addon alias.

The code lookup, `get_standard_name` and `is_amino_acid` mirror native
`naming_scheme` and `skip_digestion` arguments. Their native skip flags retain
the trusted-caller meaning. The other eleven helpers add keyword-only local
`skip_digestion=False`, consumed without forwarding an unsupported native flag. Calls still
require an open owner, including when retaining a method after view closure.
No molecular reader, pending-edit synchronization or history effect is involved.

Canonical code lookup includes XLE -> J and XAA -> X under explicit
`naming_scheme="sequence"`. Cap predicates use the
protected peptide end: ACE is N-terminal; NME/NHE/NH2 are C-terminal. These
received native corrections do not supply atomic templates for ambiguity
symbols or attach caps to a system.

:::{warning}
The received native cutover under
[MolSysMT#549](https://github.com/uibcdf/molsysmt/issues/549) distinguishes explicit
sequence, Amber, bounded CCD and legacy vocabularies. For example GLH projects
to E under Amber and Q under the explicitly selected historical legacy table.
The scalar helper has no stored system context; ambiguous labels without a
scheme retain the native diagnostic. Recognition/parent projection does not
replace chemical groups or assign protonation. See
{ref}`user-foundations-group-naming-schemes` for assessed profiles and limits.
:::

Native references: {func}`molsysmt.element.component.is_component_type`,
{func}`molsysmt.element.molecule.is_molecule_type`,
{func}`molsysmt.element.group.amino_acid.is_amino_acid`,
{func}`molsysmt.element.group.amino_acid.get_standard_name`,
{func}`molsysmt.element.group.get_1_letter_code_from_name`,
{func}`molsysmt.element.group.ion.is_ion`,
{func}`molsysmt.element.group.lipid.is_lipid`,
{func}`molsysmt.element.group.nucleotide.is_nucleotide`,
{func}`molsysmt.element.group.saccharide.is_saccharide`,
{func}`molsysmt.element.group.small_molecule.is_small_molecule`,
{func}`molsysmt.element.group.terminal_capping.is_terminal_capping`,
{func}`molsysmt.element.group.terminal_capping.is_n_terminal_capping`,
{func}`molsysmt.element.group.terminal_capping.is_c_terminal_capping` and
{func}`molsysmt.element.group.water.is_water`.

## Querying explicit group reference templates

Fourteen further utilities expose native group reference data, independently of
any loaded molecular system. They query reference bond pairs, five family
databases and expected amino-acid heavy/hydrogen names. They do not inspect the
view's connectivity, add atoms or bonds, choose a chemical state or update the
scene. All atom names, index labels and chemical context remain explicit.

```python
import molsysviewer as msv

with msv.new_view() as view:
    group = view.addons.molsysmt.element.group
    names = ["N", "CA", "C", "O", "CB"]
    indices = [1040, 1009, 1030, 1007, 1012]
    common = group.get_bonded_atom_pairs("ALA", names, atom_indices=indices)
    specific = group.amino_acid.get_bonded_atom_pairs(
        "ALA", names, atom_indices=indices
    )
    assert common == specific
    assert group.ion.get_bonded_atom_pairs("SO4", ["S", "O1"]) == [[0, 1]]
    assert group.saccharide.get_bonded_atom_pairs("NAG", ["C1", "C2"]) == [[0, 1]]
    assert group.small_molecule.get_bonded_atom_pairs("ATP", ["PG", "O1G"]) == [[0, 1]]
    assert group.terminal_capping.get_bonded_atom_pairs("ACE", ["C", "O"]) == [[0, 1]]
    assert group.water.get_bonded_atom_pairs(["O", "H1", "H2"]) == [[0, 1], [0, 2]]
    for family, name in [
        (group.amino_acid, "ALA"), (group.ion, "SO4"),
        (group.saccharide, "NAG"), (group.small_molecule, "ATP"),
        (group.terminal_capping, "ACE"),
    ]:
        assert isinstance(family.get_group_db(name), dict)
    assert group.amino_acid.get_expected_heavy_atoms(
        "ALA", present_atom_names=names
    ) == set(names)
    hydrogens = group.amino_acid.get_expected_hydrogens(
        "CYS", present_atom_names=["N", "CA", "C", "O", "CB", "SG"],
        pH=7.4, is_n_terminal=False, is_c_terminal=False, is_disulfide=True,
    )
    assert isinstance(hydrogens, list)
    assert view.molsys is None
```

Bond queries return native index pairs, using your explicit `atom_indices` or
local positions in `atom_names` when omitted. These labels are not resolved
against `view.molsys`. Native ordering, accepted containers, missing-template
None/empty/error distinctions and family support remain unchanged. The general
dispatcher is not a universal bond-perception engine: unsupported families can
return None. No atom-name normalization or automatic template repair is added.
The native return-documentation correction under
[MolSysMT#548](https://github.com/uibcdf/molsysmt/issues/548) is received: all
seven helpers describe index pairs. The addon preserves those native results;
the documentation change does not alter reference connectivity.

The five `get_group_db` helpers return the provider's reference dictionaries,
whose family-specific layouts remain native. The addon introduces no cache or
new normalized database schema. Expected heavy-atom queries keep native exact
modified-group templates, variant selection and unknown-template behavior.
Expected hydrogen queries keep explicit pH, terminal and disulfide context;
their fixed reference thresholds are not predictions of environment-dependent
pKa values. None of these queries protonates or repairs a system.

The group dispatcher, amino-acid bond/heavy/H queries and ion bond helper
retain their native `skip_digestion` arguments. The group and amino-acid
queries expose keyword-only `naming_scheme` where the native signature declares
it; raw `get_group_db` does not acquire a scheme argument. The other helpers
keep a keyword-only local control without forwarding an unsupported flag. All require an
open owner, work with an empty view and leave pending edits/history untouched.

Explicit cap lookup returns the reference data for the supplied name. Protected
peptide-end classification follows ACE at N and NME/NHE/NH2 at C; lookup does
not choose an end, attach atoms or prepare chemistry.

The received native flat-name normalization supports one-dimensional NumPy
arrays, lists and tuples in the saccharide, small-molecule and capping bond
helpers, including through the general dispatcher. Invalid name dimensions
raise the native ArgumentError. The addon forwards inputs without a conversion
or validation bypass; even its local skip control does not disable this native
check. Reference connectivity and valid list results remain unchanged.

Source receiving of
[MolSysMT#554](https://github.com/uibcdf/molsysmt/issues/554) also preserves the
native index-map contract: one nonnegative, unit-free integer per atom name,
within the int64 range. Repeated labels are allowed; booleans, masked arrays,
quantities and noninteger values are rejected with an `ArgumentError`.
Length mismatches raise `ArgumentLengthError` with expected and actual counts.
Valid read-only and strided arrays remain unchanged. These explicit labels
are not checked against the current system's atom count. Native scalar
single-atom compatibility remains available for amino-acid and ion helpers.
Local addon skip controls do not disable native validation; declared native
skip flags retain their trusted-caller meaning. This is source receiving,
separate from published package compatibility.

:::{warning}
The received naming profiles under
[MolSysMT#549](https://github.com/uibcdf/molsysmt/issues/549) keep a reporting
parent distinct from an atomic reference. Explicit scheme context does not
choose atom naming or authorize a parent-template substitution. The addon
preserves native assessed/unassessed outcomes without a chemical-name repair.
No template query prepares a molecule.
:::

Native references: {func}`molsysmt.element.group.get_bonded_atom_pairs`,
{func}`molsysmt.element.group.amino_acid.get_bonded_atom_pairs`,
{func}`molsysmt.element.group.amino_acid.get_expected_heavy_atoms`,
{func}`molsysmt.element.group.amino_acid.get_expected_hydrogens`,
{func}`molsysmt.element.group.amino_acid.get_group_db`,
{func}`molsysmt.element.group.ion.get_bonded_atom_pairs`,
{func}`molsysmt.element.group.ion.get_group_db`,
{func}`molsysmt.element.group.saccharide.get_bonded_atom_pairs`,
{func}`molsysmt.element.group.saccharide.get_group_db`,
{func}`molsysmt.element.group.small_molecule.get_bonded_atom_pairs`,
{func}`molsysmt.element.group.small_molecule.get_group_db`,
{func}`molsysmt.element.group.terminal_capping.get_bonded_atom_pairs`,
{func}`molsysmt.element.group.terminal_capping.get_group_db` and
{func}`molsysmt.element.group.water.get_bonded_atom_pairs`.

## Querying chains and entities

`element.chain` exposes `get_chain_index`, `get_chain_id`, `get_chain_name`
and `get_chain_type`. `element.entity` exposes `get_entity_index`,
`get_entity_id`, `get_entity_name`, `get_entity_type` and `get_n_entities`.
These nine readers use the current loaded system. Their selections, output
levels, missing values, IDs and native result containers are preserved.

```python
import molsysviewer as msv

with msv.demo["pentalanine"] as view:
    element = view.addons.molsysmt.element
    assert element.chain.get_chain_index(element="chain") == [0]
    assert element.entity.get_entity_index() == [0]
    assert element.entity.get_n_entities() == 1
    atom_chain_names = element.chain.get_chain_name()
    atom_chain_types = element.chain.get_chain_type()
    atom_chain_ids = element.chain.get_chain_id()
    entity_names = element.entity.get_entity_name()
    entity_types = element.entity.get_entity_type()
    entity_ids = element.entity.get_entity_id()
    projected_names = element.chain.get_chain_name(
        element="chain", redefine_names=True
    )
```

Defaults match the native readers: chain getters default to output at the atom
level, and entity getters default to the entity level. `get_n_entities`
selects atoms when a subset is supplied. Indices are positions; returned IDs
and names follow MolSysMT and may reflect missing source labels. No label is
invented by the addon.

`redefine_*` controls the native returned projection. It does not assign that
projection to your system or change the scene. Native unsupported combinations
retain their errors. Readers include completed molecular edits that are pending
scene synchronization, while leaving that pending state unchanged. They acquire
the managed molecular reader and require an open view with a loaded system;
there is no `update_view` parameter or automatic representation.

All nine expose `skip_digestion=False`. For `entity.get_n_entities` alone,
this is a keyword-only addon control because the native reader has no skip
parameter. It is consumed locally; native validation stays active. The other
eight preserve and forward their native flags. Component/molecule and group readers are covered next. Other unreceived
explicit-input element utilities remain pending.

Native references: {func}`molsysmt.element.chain.get_chain_index`,
{func}`molsysmt.element.chain.get_chain_id`,
{func}`molsysmt.element.chain.get_chain_name`,
{func}`molsysmt.element.chain.get_chain_type`,
{func}`molsysmt.element.entity.get_entity_index`,
{func}`molsysmt.element.entity.get_entity_id`,
{func}`molsysmt.element.entity.get_entity_name`,
{func}`molsysmt.element.entity.get_entity_type` and
{func}`molsysmt.element.entity.get_n_entities`.

## Querying molecules, components and group types

The `element.molecule` and `element.component` namespaces each expose their
native index, ID, name, type and count readers. `element.group.get_group_type`
queries types from the current system; it remains distinct from the explicit
name lookup `element.group.get_group_type_from_group_name`.

```python
import molsysviewer as msv

with msv.demo["pentalanine"] as view:
    element = view.addons.molsysmt.element
    assert element.molecule.get_molecule_index() == [0]
    assert element.molecule.get_n_molecules() == 1
    molecule_ids = element.molecule.get_molecule_id()
    molecule_names = element.molecule.get_molecule_name()
    molecule_types = element.molecule.get_molecule_type()
    assert element.component.get_component_index() == [0]
    assert element.component.get_n_components() == 1
    component_ids = element.component.get_component_id()
    component_names = element.component.get_component_name()
    component_types = element.component.get_component_type()
    group_types = element.group.get_group_type()
    assert group_types[1] == "amino acid"
```

Molecules belong to stable topology. Components describe connectivity within
`ChemicalStates`; they are not interchangeable. Removing bonds can split one
stable molecule into several components without changing molecule membership.
Component queries preserve native reference-state and explicit reconstruction
semantics. The addon does not select chemistry from the canvas frame, infer
missing chemistry or turn a projection into a molecular edit.

The index/ID/name/type getters default to their named output level; group type
queries default to groups. Count readers interpret a subset as an atom
selection. Selections, syntax, returned containers, missing values and native
unsupported combinations are retained. `redefine_*` controls returned native
projections; these tools never assign them or reconcile pending scene changes.
They require a loaded, open view and use the managed molecular reader.
`molecule.get_n_molecules` adds a keyword-only local `skip_digestion` control;
all other readers here forward their declared native flag unchanged.

Native references: {func}`molsysmt.element.molecule.get_molecule_index`,
{func}`molsysmt.element.molecule.get_molecule_id`,
{func}`molsysmt.element.molecule.get_molecule_name`,
{func}`molsysmt.element.molecule.get_molecule_type`,
{func}`molsysmt.element.molecule.get_n_molecules`,
{func}`molsysmt.element.component.get_component_index`,
{func}`molsysmt.element.component.get_component_id`,
{func}`molsysmt.element.component.get_component_name`,
{func}`molsysmt.element.component.get_component_type`,
{func}`molsysmt.element.component.get_n_components` and
{func}`molsysmt.element.group.get_group_type`.

## Using the legacy amino-acid name heuristic

`element.group.small_molecule.small_molecule_is_amino_acid(group_name)` mirrors
the native legacy helper on the current system. It checks a catalogued
small-molecule group name and the presence of the atom names `CA`, `CB`, `C`,
`O` and `N`. It does not validate chemical connectivity or stereochemistry,
prepare the system or assign a stored classification.

```python
import molsysviewer as msv

with msv.demo["pentalanine"] as view:
    heuristic = view.addons.molsysmt.element.group.small_molecule.small_molecule_is_amino_acid
    assert heuristic("ATP") is False  # No group named ATP is present.
```

This Boolean name-pattern result is not chemical validation. Native errors and
results stay unchanged. The explicit `group_name` is retained; its keyword-only
`skip_digestion` is local because the native helper has no such flag. It still
requires the current loaded open owner and uses the managed molecular reader
without scene/history effects. See
{func}`molsysmt.element.group.small_molecule.small_molecule_is_amino_acid`.

## Querying the current system

```python
import molsysviewer as msv

with msv.demo["pentalanine"] as view:
    tools = view.addons.molsysmt
    count = tools.basic.get(n_atoms=True)
    atoms = tools.basic.select(selection="atom_type=='N'")
    coordinates = tools.basic.get(
        element="atom", selection=atoms,
        structure_indices=[2, 0], coordinates=True,
    )
    summary = tools.basic.info(output_type="dictionary")
```

Coordinates retain the native physical quantity and structure order; the
standard MolSysMT length unit is nm. Scientific choices, defaults, result types,
errors and mutable-result ownership follow the native function. These wrappers
add no whole-trajectory copy or scene update. Native calculation/cache behavior
is unchanged; for example, `get_missing_bonds` retains its documented meaning.

| Bound tool | Native parameter and result reference |
| --- | --- |
| `tools.basic.get(...)` | {doc}`basic/get` |
| `tools.basic.select(...)` | {doc}`basic/select` |
| `tools.basic.info(...)` | {doc}`basic/info` |
| `tools.basic.get_attributes(...)` | {doc}`basic/get_attributes` |
| `tools.basic.has_attribute(...)` | {doc}`basic/has_attribute` |
| `tools.basic.get_label(...)` | {doc}`basic/get_label` |

The bound methods omit the primary `molecular_system` argument. You cannot
override it with another system. Inspect a signature or call `help` on the
method for the remaining native parameters. `skip_digestion` keeps the native
trusted-call contract; it does not bypass view lifetime checks.

## Inspecting and constructing periodic boxes

Use `tools.pbc.has_pbc()` to query the current primary system. This retains
MolSysMT's first-structure criterion, including scientific edits pending scene
synchronization. It does not aggregate every structure or add a structure filter.
The other nine utilities keep their explicit scientific inputs. A box or a
factory result never assigns itself to `view.molsys`.

```python
import numpy as np
import molsysmt as msm

puw = msm.pyunitwizard
with msv.demo["pentalanine"] as view:
    tools = view.addons.molsysmt
    has_box = tools.pbc.has_pbc()
    boxes = tools.pbc.get_box_with_shape(
        shape="cubic", length="4 nm", n_structures=3,
    )
    lengths = tools.pbc.get_lengths_from_box(boxes)
    angles = tools.pbc.get_angles_from_box(boxes)
    both = tools.pbc.get_lengths_and_angles_from_box(boxes)
    volume = tools.pbc.get_volume_from_box(boxes)
    shape = tools.pbc.get_shape_from_box(boxes)
    shape_from_angles = tools.pbc.get_shape_from_angles(angles)
    rebuilt = tools.pbc.get_box_from_lengths_and_angles(lengths, angles)
    direct_volume = tools.pbc.get_volume_from_lengths_and_angles(lengths, angles)
    np.testing.assert_allclose(puw.get_value(volume, to_unit="nm**3"), [64, 64, 64])
    np.testing.assert_allclose(puw.get_value(rebuilt, to_unit="nm"),
                               puw.get_value(boxes, to_unit="nm"), atol=2e-6)
```

Box vectors are rows, with shape `(n_structures, 3, 3)`. Native physical
quantities, active unit policy and six-decimal numerical rounding remain
unchanged. In particular, `get_volume_from_box` returns cubic nanometers;
`get_volume_from_lengths_and_angles` uses the native standard-unit policy and
direct analytical geometry rather than the rounded reconstructed matrix.
The native shape classifier uses mean angles across supplied boxes: its
`"cubic"` label does not guarantee equal edge lengths or classify each structure
independently. Keep that distinction when interpreting heterogeneous boxes.

For selected structures, obtain boxes explicitly with
`tools.basic.get(box=True, structure_indices=[2, 0, 2])`, then pass that quantity
to a utility. Order and repetitions are preserved. These tools do not copy an
entire trajectory or fetch an implicit box for a factory.

```python
with msv.new_view() as empty:
    pbc = empty.addons.molsysmt.pbc
    independent_box = pbc.get_box_with_shape(
        shape="rhombic dodecahedral", length="3 nm",
    )
    independent_volume = pbc.get_volume_from_box(independent_box)
    assert empty.molsys is None
```

Explicit-input utilities work before loading a system while the owning view
remains open. Their inputs stay caller-owned and must remain stable during the
call; they do not lock another system or observe arbitrary raw edits. Only
`has_pbc` requires a loaded system and uses the host's managed reader.
`get_volume_from_box` and `get_volume_from_lengths_and_angles` have an addon-only
keyword `skip_digestion`: it is not passed to native functions, whose ordinary
public validation remains active.

At the reviewed repaired source, omitted or None angles delegate to native
orthogonal box construction under [#465](https://github.com/uibcdf/molsysmt/issues/465).
The addon synthesizes no angles and assigns no box to the view. Native output
is a box series `(n_structures, 3, 3)`. The coordinate editors below use the
separately received managed-effect route.

See {doc}`pbc/index` for native scientific usage. To assign a newly constructed
box, use the separately received `tools.basic.set(box=...)` route with the
actual current structure axis; construction alone does not change the system.

## Editing periodic coordinate images

The three scientific editors keep MolSysMT's `in_place=False` default. They
return an independent native system without replacing the view. Choose
`in_place=True` to edit the current primary; `update_view=True` synchronizes it
immediately. `update_view=False` defers scene projection only. These operations
share the receiver used by the structure editors, including pending-state
protection and retry without scientific replay.

- `wrap_to_pbc` places coordinates in the primary periodic cell using explicit
  `box_origin` or `box_center` parameters.
- `wrap_to_mic` chooses the nearest periodic image around `mic_origin`.
- `unwrap` restores per-atom temporal continuity in the supplied structure order.
  It does not reconstruct covalent components inside one structure. Nonconsecutive
  structures are still an ordered scientific input; no missing history is inferred.

For the two wrapping tools, native `compact="component"` reconstructs covalent
components and keeps each whole; `compact=False` wraps atoms independently.
Choosing that mode, a box, origins, centers, weights and the ordered observation
scope remains the caller's scientific decision. The addon implements no PBC
kernel, box transformation, molecular preparation or additional graph algorithm.

```python
with msv.demo["pentalanine"] as source:
    with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as view:
        tools = view.addons.molsysmt
        # Explicit demonstration cell; this is not solvation or automatic preparation.
        boxes = tools.pbc.get_box_with_shape(length="3 nm", n_structures=3)
        tools.basic.set(box=boxes)
        independent = tools.pbc.wrap_to_pbc(compact="component")
        assert independent is not view.molsys
        tools.pbc.wrap_to_mic(in_place=True, update_view=False)
        tools.pbc.unwrap(in_place=True, update_view=False)
        tools.sync_view()
        assert tools.get_sync_status()["state"] == "synchronized"
```

The current atom/structure axes, topology, source identities and scene-object
identities are retained by received in-place edits. Native coordinate setters
invalidate interaction coverage for the written structures; this does not
recalculate analyses or hide scientific preparation. If scene synchronization
fails after science completes, inspect `science_completed` and
`scientific_result`, then call `sync_view()` rather than repeating the editor.

Centered wrapping now retains the original in-place target through the native
repair under [#467](https://github.com/uibcdf/molsysmt/issues/467). The centering
reference must be contained in the moved selection. Independent output stays
separate; in-place publication retains the primary and participates in the same
managed synchronization/recovery contract. The addon adds no copyback or
replacement centering algorithm.

```python
with msv.demo["pentalanine"] as source:
    with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as view:
        tools = view.addons.molsysmt
        tools.basic.set(box=tools.pbc.get_box_with_shape(length="3 nm", n_structures=3))
        centered = tools.pbc.wrap_to_pbc(
            center_of_selection="atom_name=='CA'", in_place=False,
        )
        assert centered is not view.molsys
```

See {doc}`pbc/wrap_to_pbc`, {doc}`pbc/wrap_to_mic` and {doc}`pbc/unwrap` for
native parameter semantics. Source receiving does not qualify every box shape,
scientific sampling choice, engine or installed package composition.

## Identifying systems and locating attributes

```python
with msv.demo["pentalanine"] as view:
    tools = view.addons.molsysmt
    resident_form = tools.basic.get_form()
    valid_single = tools.basic.is_a_molecular_system()
    molsys, owning_form = tools.basic.where_is_attribute("coordinates")
    with msv.MolSysView() as empty:
        valid_container = empty.addons.molsysmt.basic.are_multiple_molecular_systems(
            [molsys],
        )
```

{doc}`basic/get_form` identifies the current resident system, usually
`molsysmt.MolSys`, rather than the filename or original format passed to loading.
{doc}`basic/is_a_molecular_system` retains native input classification and
consistency checks; it is not a claim that the system is chemically complete or
ready for simulation.

{doc}`basic/where_is_attribute` returns the native item/form pair with its actual
`include_none` and fallback semantics. The item can be the current `view.molsys`
itself; it is a live reference, not a copied snapshot. Locating a possible owner
is not proof that an attribute currently has a non-None value. Use `has_attribute`
for the corresponding availability query. Later direct edits through the returned
item retain explicit reconciliation responsibilities.

{doc}`basic/are_multiple_molecular_systems` is an explicit-input utility: its
`molecular_systems` collection remains required. The addon never prefixes that
collection with the current system and does not merge items or load a result
into the view. Native inspection may still read the supplied inputs. It may
run on an empty view, but the owning view must remain open. Inputs are
caller-owned and must remain stable; this utility takes no managed-edit locks.
Native True for a one-item valid container does not mean there are at least two
systems, nor decide how sources should be composed or loaded.

Native `get_form`, `is_a_molecular_system` and `are_multiple_molecular_systems`
deliberately have no digestion escape-hatch parameter. Their addon wrappers add
keyword-only `skip_digestion=False` for the addon boundary only; they never pass
it to or redecorate the native helper. View lifetime checks still run. The
ordinary native `skip_digestion` parameter of `where_is_attribute` remains native.

## Checking composition and comparing systems

```python
with msv.demo["pentalanine"] as view:
    tools = view.addons.molsysmt
    count = tools.basic.get(n_atoms=True)
    contains_minimum = tools.basic.contains(n_atoms=count - 1)
    matches_exact_count = tools.basic.is_composed_of(n_atoms=count)
    reference = tools.basic.copy()
    differences = tools.basic.compare(
        reference, output_type="dictionary", n_atoms=True, atom_name=True,
    )
```

{doc}`basic/contains` and {doc}`basic/is_composed_of` keep their native condition
semantics. For an integer `n_atoms` condition, the former checks a minimum count,
while the latter checks an exact count. Empty conditions, selections and attribute
synonyms retain native behavior; the addon adds no new interpretation of chemistry.

{doc}`basic/compare` binds only the first system. Pass `molecular_system_2`
explicitly, including when it is another view's molecular system. Keep the two
systems' selections and structure indices separate through `selection`,
`structure_indices`, `selection_2` and `structure_indices_2`. Dictionary output
and `attributes_type`'s native alias for `attribute_type` remain available.
An alias and its canonical argument are alternatives; supplying both is rejected,
even when the explicit canonical value equals its default.

The received comparison route uses `redefine_indices=False`. Native
`redefine_indices=True` forces topology rebuilding in **both** inputs, so it is
an editing operation that still needs separate receiving. The addon rejects it
before either system is changed, including with `skip_digestion=True`.
Use native MolSysMT and explicit reconciliation of affected views when you need
that mode. Other provider limitations and errors, such as the unimplemented
`rule="in"`, are preserved rather than replaced with fallback results.

These tools do not request a scene update or attach analyses. They may read a
pending molecular edit without synchronizing its scene. Native derived caches
retain their own behavior. Keep an explicitly supplied reference stable while
the call runs; this interface does not lock or transact across two views.

## Extracting a molecular subset

```python
with msv.demo["pentalanine"] as view:
    subset = view.addons.molsysmt.basic.extract(
        selection=[0, 2, 4], structure_indices=[2, 0, 2],
        to_form="molsysmt.MolSys",
    )
    selected_groups = view.addons.molsysmt.basic.extract(
        element="group", selection=[2, 1], structure_indices=[2, 0, 2],
    )
```

The keyword-only `element` follows native hierarchy selection: `None` uses
atoms for atomistic systems and groups for atom-free inventories. Explicit
group, chain, molecule, entity and component selections follow the provider's
projection and validation. No topology or coordinates are synthesized.

This returns the native molecular result and leaves the view unchanged. Structure
order and repetitions follow {doc}`basic/extract`, as do output formats/files,
units, attached-analysis projection and the `copy_if_all` ownership policy.
An unrestricted `copy_if_all=False` call may retain native shared/live-reference
behavior; the addon does not add a defensive copy or observe later direct writes.
`view.extract(...)` is a separate operation that returns a new view with migrated
scene state. Neither method implicitly adopts its result into the source view.

## Copying and converting the current system

```python
with msv.demo["pentalanine"] as view:
    tools = view.addons.molsysmt
    snapshot = tools.basic.copy()
    subset = tools.basic.convert(
        selection=[0, 1, 2, 3], structure_indices=[2, 0],
    )
    reports = tools.basic.get_conversion_report(
        to_form=["molsysmt.MolSys", "molsysmt.Structures"],
        structure_indices=[2, 0],
    )
```

{doc}`basic/copy` returns the native independent copy. {doc}`basic/convert`
returns the requested molecular form, collection or file result, with native
selection, structure order and converter options. Neither replaces `view.molsys`
or copies the visual scene. With `return_report=True`, conversion returns its
native result/report pair. Target lists retain their requested order.
`copy_if_all=False` keeps the converter's sharing policy: a full native conversion
may return the current system itself. Later edits through that live reference
are outside automatic synchronization.

{doc}`basic/get_conversion_report` inspects potential losses without creating or
overwriting the destination. An existing destination may be inspected to identify
its form and can produce a native format error. Check each report's `outcome`,
`issues`, `audited_scopes` and `is_exhaustive`; a report is not an unconditional
guarantee that a format preserves every property. `strict=True` on conversion
rejects losses detected by the provider's preflight. It adds no rollback or atomic
publication guarantee across multiple files. Optional converters retain their
own dependencies and scientific limitations.

Both bound operations expose the native keyword-only `from_naming_scheme`.
It declares the input vocabulary; it does not rename groups, prepare chemistry
or change the view's stored declarations. Preflight reports naming metadata
that a target cannot preserve. Conversion retains a new declaration on its
independent native result and applies native analysis invalidation there.
A conflict with known selected declarations rejects without editing the system
or scene. See {ref}`user-foundations-group-naming-schemes` for profiles, defaults
and scientific limits.

## Saving molecular data

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with msv.demo["pentalanine"] as view:
    with TemporaryDirectory() as directory:
        destination = Path(directory) / "system.h5msm"
        filename, report = view.addons.molsysmt.basic.convert(
            to_form=destination, structure_indices=[2, 0],
            return_report=True,
        )
        # Use the saved molecular file with ordinary MolSysMT tools.
        import molsysmt as msm
        restored = msm.convert(filename)
```

H5MSM 0.5 preserves the supported molecular domains and named Interactions.
Other formats are selected through native `to_form` and may retain fewer
properties; use a preflight report and the format reference before exporting.
Only native forms and H5MSM have addon-specific receiving in this delivery;
optional-format qualification remains with its converter owner.

A filename addresses the filesystem of the Python process. In a remote Jupyter
session it is a server path, not an automatic browser download. This operation
saves molecular data; use Viewer session/export tools to preserve the scene or
produce an interactive HTML view. No output is automatically adopted or displayed.
`copy(output_filename=...)` keeps native behavior: file-copy destinations are for
file-based inputs, so use `convert` to serialize the view's native MolSys.

## Removing atoms or structures

`remove` preserves {doc}`basic/remove`: `in_place=False` is the native default
and returns an independent molecular system. It does not replace `view.molsys`.
To edit the actual bound system and update its scene:

```python
with msv.demo["pentalanine"] as view:
    tools = view.addons.molsysmt
    tools.basic.remove(selection=[0], in_place=True)
    tools.basic.remove(structure_indices=[1], in_place=True, update_view=False)
    status = tools.get_sync_status()  # pending: science is already complete
    tools.sync_view()                # update the scene, not the science
```

Successful in-place removal returns native `None`. The keyword-only
`update_view=True` default synchronizes immediately; False defers only visual
reconciliation. Compatible deferred removals compose their atom/structure maps.
Queries read the current edited MolSys, while scene actions using old indices
are blocked until synchronization. Live windows display an Update view action.

The initial receiver supports retained nonempty atom/structure axes. Removing
every atom or structure in place is rejected before scientific execution; use
`in_place=False` for independent empty outputs. Surviving analyses follow native
extraction/projection semantics and retain their original evaluated scope: they
are not new calculations. Regions, saved/active atom selections, shapes and
structure-bound scene data follow the receiving host's map policies. Textual
region/selection queries are reevaluated; explicit atom lists are remapped.

### A completed edit whose display update fails

A scene synchronization error does not mean the removal failed. The host raises
`molsysviewer.system_edits.SystemEditSyncError` with `science_completed=True`,
`operation_id` and `scientific_result` (native None for this removal). Its cause
identifies the projection failure. Call `tools.sync_view()` to retry; do not
repeat the removal. The facade does not permanently retain large results.

If a scientific exception may have left partial writes, status is `uncertain`;
unchanged counts do not certify correspondence. Explicit recovery through
`view.addons.manager.system_edits.replace(molecular_system)` discards pending
scene reconciliation and loads a replacement. This is not scientific Undo and
does not revert caller-held references to the old edited system. Ordinary
`view.load` cannot silently discard unresolved managed edits.

## Setting coordinates and periodic boxes

The source receiver admits `basic.set` for **coordinates** and **box**, with
the current atom and structure axes retained. Its native parameters/defaults
remain visible; `update_view=True` is the additional keyword-only integration
control. Native setting edits the bound system and returns None; it does not
need or invent an `in_place` flag.

```python
import numpy as np
from molsysmt import pyunitwizard as puw

with msv.demo["pentalanine"] as source:
    with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as view:
        tools = view.addons.molsysmt
        coordinates = tools.basic.get(
            element="atom", selection=[2, 0],
            structure_indices=[2, 0], coordinates=True,
        )
        tools.basic.set(
            selection=[2, 0], structure_indices=[2, 0],
            coordinates=coordinates + puw.quantity(0.1, "nm"),
        )
        boxes = puw.quantity(np.tile(np.diag([3, 4, 5]), (3, 1, 1)), "nm")
        tools.basic.set(box=boxes, update_view=False)
        tools.sync_view()
```

Units, selection order and repeated-index writes follow {doc}`basic/set`.
Supply one coordinate block or box matrix per selected structure; no broadcast
is added. Coordinates use atom-level selection with element=None or atom;
element=system keeps native whole-system semantics and ignores atom selection.
Boxes require element=None or system. Initialize a missing box with all
structures before partial replacement; `tools.basic.set(box=None)` clears the
complete series. Coordinate-axis initialization/resizing/clearing and other
attributes are not received yet and fail before writing through this wrapper.

MolSysMT invalidates named interaction analyses only on edited structures,
including previously evaluated-empty ones. Unedited structures and earlier
snapshots remain available; setting geometry never recalculates a detector.
Valid empty selections are native no-ops. Geometry and removal edits can be
deferred together and reconciled once. The existing synchronization-failure and
uncertain-state recovery rules above also apply to this setter.

Multiple attributes are validated before delegation, but an unexpected error
after a native write may leave partial data. This route therefore requires a
host that checks nested geometry/analysis state on rejection; an older receiver
rejects the request before scientific execution. It does not promise scientific
rollback. To use other native attributes, first synchronize pending work, then
use MolSysMT with explicit Viewer reconciliation until their effects are received.

Native geometry storage replaces affected blocks. The current visual receiver
still rebuilds the scene when synchronizing, so a small setter request is not a
promise of incremental or bounded trajectory transfer to the browser.

## Exploring stored topology

```python
with msv.demo["pentalanine"] as view:
    chemical_states = view.addons.molsysmt.chemical_states
    graph = chemical_states.get_bondgraph(structure_indices=[2, 0])
    blocks = chemical_states.get_covalent_blocks()
    paths = chemical_states.get_covalent_paths(path=[
        'atom_name=="C"', 'atom_name=="N"',
        'atom_name=="CA"', 'atom_name=="C"',
    ])
    phi_quartets, phi_blocks = chemical_states.get_dihedral_quartets(
        phi=True, with_blocks=True,
    )
    hypothetical_blocks = chemical_states.get_covalent_blocks(
        remove_bonds=phi_quartets[0][1:3],
    )
```

{doc}`chemical_states/get_bondgraph` returns the native NetworkX graph with source atom
indices as nodes. The graph is an independent result; changing it does not change
the system's bonds. {doc}`chemical_states/get_covalent_blocks` returns native sets or
source-index label arrays. `remove_bonds` cuts the analysis graph only: it neither
removes molecular bonds nor defines scene regions.

{doc}`chemical_states/get_covalent_paths` takes an explicit ordered selection pattern.
{doc}`chemical_states/get_dihedral_quartets` takes native dihedral flags such as `phi`
and `psi`. Request the intended type explicitly. Its `with_blocks=True` result
keeps the native lists of sets with different sizes; the addon does not coerce
that ragged data into a rectangular array.

Selection, output, chemical-state and structure options match each native
function. A reference-state graph is one connectivity graph, not an automatically
calculated graph per displayed structure. Paths and quartets now expose the
native keyword-only chemical-state, structure-index and `skip_digestion` controls.
Graph cuts do not prepare chemistry, certify connectivity, attach analyses or
update the scene. The same view-lifetime and pending-read rules apply as for the
received `basic` readers. Sequence tools keep their stable-inventory namespace.

## Reading chemical graphs and sequences

With sufficient declared chemistry, native graph tools also return ring
memberships, source-bond torsion classifications, explicit-cut fragments,
SMARTS matches and atom correspondences. They never fill missing chemical
metadata or apply their outputs to the scene. RDKit remains optional and is
required by SMARTS/correspondence matching; Biopython supplies sequence alignment.
The example below explicitly chooses the RDKit input-conversion route. That
choice belongs to the caller, not an implicit addon preparation step.

```python
import molsysmt as msm

molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'], to_form='rdkit.Mol')
with msv.new_view(molsys) as view:
    chemical_states = view.addons.molsysmt.chemical_states
    rings = chemical_states.get_rings()
    torsions = chemical_states.get_rotatable_bonds(method='conjugation_restricted')
    fragments = chemical_states.get_rigid_fragments(
        bond_indices=torsions['rotatable_bond_indices'],
    )
    matches = chemical_states.get_substructure_matches(['[#8]', '[#9]'])
    n_atoms = view.addons.molsysmt.basic.get(n_atoms=True)
    identity_map = [[index, index] for index in range(n_atoms)]
    correspondence = chemical_states.get_atom_correspondences(
        fixed_atom_correspondence=identity_map, max_matches=1,
    )
```

{doc}`chemical_states/get_rings` returns sparse sorted memberships of a minimum cycle
basis, not every cycle or an aromaticity assignment. A partial-ring selection
can be rejected. Its block-size limit is not a universal RAM/runtime bound.
{doc}`chemical_states/get_rotatable_bonds` retains explicit experimental graph criteria
and exclusions. {doc}`chemical_states/get_rigid_fragments` cuts chosen source bond
indices analytically: it does not remove bonds or rotate coordinates. Packed
memberships and source-index arrays remain native, without becoming regions.

{doc}`chemical_states/get_substructure_matches` keeps pattern order, query-column
order, empty matrix shapes and its pre-selection match bound.
{doc}`chemical_states/get_atom_correspondences` preserves full chemical context,
independent reference selectors/states, source-index pairs, anchors, supplied
candidates, evidence and search limits. Its default None reference uses the
current system, as native MolSysMT does. It does not infer a visual alignment or
authorize adopting a different atom order. Caller-owned references must remain
stable; the addon does not lock another view. No truncated result is substituted
when a scientific search bound is exceeded.

```python
with msv.demo['pentalanine'] as view:
    reference = view.addons.molsysmt.basic.copy()
    chemical_states = view.addons.molsysmt.chemical_states
    amino_acids = "group_type=='amino acid'"
    aligned = topology.get_sequence_alignment(
        selection=amino_acids, reference_molecular_system=reference,
        reference_selection=amino_acids,
    )
    identity, groups, reference_groups = topology.get_sequence_identity(
        selection=amino_acids, reference_molecular_system=reference,
        reference_selection=amino_acids,
    )
```

{doc}`topology/get_sequence_alignment` preserves the native strings, engine,
alignment index and prettyprint branch, which prints and returns None.
{doc}`topology/get_sequence_identity` returns the native percentage and matched
source group lists. Current source resolves groups that actually contribute
sequence letters, so capped pentalanine self-comparison is 100 percent and
returns source groups [1, 2, 3, 4, 5]. Native empty/pre-gapped selection errors
remain explicit. The repaired native helper declares keyword-only skip_digestion;
the bound method forwards it, preserving all six historical native positional
slots. This is native receiving of
[#439](https://github.com/uibcdf/molsysmt/issues/439), not an addon identity formula.
No sequence result edits topology, fits coordinates or selects scene objects.

## Reusing tool references

A cached `tools` object or method resolves the current `view.molsys` when each
call begins. After `view.load(..., mode="replace")`, later queries use the
replacement system. The facade does not keep a second authoritative MolSys.
Each view has its own binding. Disabling the addon's graphical activation does
not disable expert Python queries. Closing the view makes bound queries fail;
an empty view must first load a molecular system.

Results are native scientific values. These queries do not create scene objects
or attach every result automatically. Use the visual owners in MolSysViewer for
regions, selections, measurements or Interactions. General direct edits made
with MolSysMT or through returned live references retain explicit reconciliation
responsibilities. Only admitted addon writers coordinate their edits; there is
no observer for arbitrary external writes.

## Host and author documentation

MolSysViewer documents discovery, activation, configuration, lifecycle, its
addon catalogue and how to create an addon in its
[addon guide](https://www.uibcdf.org/molsysviewer/content/user/introduction/addons.html).
This MolSysMT guide owns the capabilities and use of the MolSysMT tools addon.

## Inspecting mechanical resources and calculating energy

Four queries and a minimizer are available under `tools.molecular_mechanics`. Resource lookup keeps
its explicit inputs and works before loading a system. Degree counting and energy read
the current primary through the same serialized reader as the other scientific
queries. These queries do not change the scene, adopt an OpenMM object or add an
`update_view` control.

```python
import molsysviewer as msv

with msv.new_view() as view:
    mechanics = view.addons.molsysmt.molecular_mechanics
    resources = mechanics.get_engine_forcefield("AMBER14")
    assert resources == ["amber14-all.xml"]
    assert mechanics.get_engine_forcefield("AMBER14", engine="LEaP") == [
        "leaprc.protein.ff14SB"
    ]
    custom_resources = list(resources)
    custom_resources.append("project-specific.xml")
```

These are resource-name lists: this call does not construct a force-field
object, run an engine, verify an installed executable or prepare a system.
The native lookup keeps its model precedence and errors for unknown names.

:::{warning}
[MolSysMT#560](https://github.com/uibcdf/molsysmt/issues/560) tracks the native
shared-list ownership defect. Until its repair is received, copy a returned
resource list explicitly before customizing it. Editing the native list can
alter later lookups and parameterizations of that same model. The addon does
not hide this with its own registry or automatic copying.
:::

Degree counting performs native OpenMM parameterization, with the selected
force field and the original molecular prerequisites. It does not add missing
hydrogens, choose protonation states or assign stored mechanics. Start with an
explicit single-structure view:

```python
with msv.demo["pentalanine"] as source:
    with msv.new_view(source.molsys, structure_indices=[0]) as view:
        mechanics = view.addons.molsysmt.molecular_mechanics
        dof = mechanics.get_degrees_of_freedom(forcefield="AMBER14")
        assert type(dof) is int
        assert dof == 154
```

The native mechanical definition is `3 * n_particles - n_constraints`. This
example has 62 particles and 32 constraints. It adds no center-of-mass or
thermostat correction and returns a dimensionless integer. Native conversion
can reject multiple-structure boxes; this API does not silently select the
visible structure. Completed pending edits are read without synchronizing the
scene. Cached tools resolve a replaced primary and reject a closed owner.

Potential energy uses native OpenMM conversion with the system's stored or
default mechanical settings. These determine the force field, nonbonded method
and other parameterization choices. No preparation, minimization, charge
assignment or engine object is adopted by the view. Request the total energy
or the native dictionary keyed by force name:

```python
import molsysmt as msm
import numpy as np

with msv.demo["pentalanine"] as source:
    with msv.new_view(source.molsys, structure_indices=[0]) as view:
        mechanics = view.addons.molsysmt.molecular_mechanics
        energy = mechanics.get_potential_energy(platform="CPU")
        terms = mechanics.get_potential_energy(decomposition=True, platform="CPU")
        energy_kj = msm.pyunitwizard.get_value(energy, to_unit="kJ/mol")
        terms_kj = [
            msm.pyunitwizard.get_value(term, to_unit="kJ/mol")
            for term in terms.values()
        ]
        assert np.isfinite(energy_kj)
        np.testing.assert_allclose(sum(terms_kj), energy_kj, rtol=1e-7, atol=1e-5)
```

The result retains physical units under the application's active unit policy;
convert explicitly to the desired unit, as above. `selection` constructs the
native selected subsystem for parameterization: it is not a contribution from
selected atoms interacting with an unchanged surrounding system. Partial groups
can fail parameterization. CPU total and decomposed energies have bounded
single-structure receiving against a separately constructed OpenMM model; this
does not qualify periodic decompositions, GPU execution or arbitrary force
fields. There is no automatic selection of the visible structure or trajectory
loop. Native conversion errors, missing chemistry and optional-engine failures
remain visible. Completed pending edits are read without synchronizing the scene.

### Calculating nonbonded contributions

`get_non_bonded_potential_energy` uses the complete parameterized system and
selects its nonbonded contributions. With `selection_2=None` it returns the
internal nonbonded energy of the selected atoms. Two disjoint atom sets give
their cross contribution; two group partitions give a matrix whose axes follow
the native selection order. Standard Coulomb, Lennard-Jones and scaled/excluded
exception terms retain the selected native force field's definitions.

```python
import molsysviewer as msv
import molsysmt as msm
import numpy as np

with msv.demo["pentalanine"] as source:
    with msv.new_view(source.molsys, structure_indices=[0]) as view:
        mechanics = view.addons.molsysmt.molecular_mechanics
        internal = mechanics.get_non_bonded_potential_energy(
            selection="group_index in [0,1]"
        )
        cross = mechanics.get_non_bonded_potential_energy(
            selection="group_index in [0,1]",
            selection_2="group_index in [4,5]",
        )
        matrix = mechanics.get_non_bonded_potential_energy(
            selection="all in groups of group_index in [0,1]",
            selection_2="all in groups of group_index in [4,5]",
        )
        cross_kj = msm.pyunitwizard.get_value(cross, to_unit="kJ/mol")
        matrix_kj = msm.pyunitwizard.get_value(matrix, to_unit="kJ/mol")
        assert matrix_kj.shape == (2, 2)
        assert np.isfinite(msm.pyunitwizard.get_value(internal, to_unit="kJ/mol"))
        np.testing.assert_allclose(matrix_kj.sum(), cross_kj, rtol=2e-6, atol=2e-4)
```

Results retain physical energy units under the active application policy.
This source receiving covers single-structure CPU NoCutoff calculations against
independent Coulomb/Lennard-Jones pair sums, including native exception terms.
It does not establish binding affinity, free energy, periodic long-range
partition correctness or overlapping-selection semantics. Stored/default native
mechanical settings determine the model; there is no hidden preparation,
visible-structure substitution or trajectory loop.

[#561](https://github.com/uibcdf/molsysmt/issues/561) remains a native limit:
a partitioned first selection and a flat second selection raise TypeError.
The facade propagates that failure without reshaping the scientific inputs.
Use the qualified flat/flat or two-sided partition forms deliberately. Reads
include completed pending edits without scene projection or history changes.

`get_forces` is still unexposed: its native MolSys input route is requested in
[#572](https://github.com/uibcdf/molsysmt/issues/572). An OpenMM-only reader does
not yet supply forces for the current `view.molsys`; the addon adds no implicit
engine conversion or placeholder method.

### Relaxing coordinates

`potential_energy_minimization` delegates the native OpenMM L-BFGS operation.
Its default `in_place=False` returns an independent molecular system. Keep that
result deliberately; the current view is preserved:

```python
with msv.demo["pentalanine"] as source:
    with msv.new_view(source.molsys, structure_indices=[0]) as view:
        tools = view.addons.molsysmt
        original = msm.pyunitwizard.get_value(
            view.molsys.structures.coordinates, to_unit="nm"
        ).copy()
        energy_before = tools.molecular_mechanics.get_potential_energy()
        relaxed = tools.molecular_mechanics.potential_energy_minimization()
        energy_after = msm.molecular_mechanics.get_potential_energy(relaxed)
        assert relaxed is not view.molsys
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(view.molsys.structures.coordinates, to_unit="nm"),
            original,
        )
        assert msm.pyunitwizard.get_value(energy_after, to_unit="kJ/mol") < (
            msm.pyunitwizard.get_value(energy_before, to_unit="kJ/mol")
        )
```

With `in_place=True`, native coordinates change and the call returns `None`.
The addon retains atom/structure identities and reconciles the scene by default.
For a batch of edits, `update_view=False` defers only projection:

```python
with msv.demo["pentalanine"] as source:
    with msv.new_view(source.molsys, structure_indices=[0]) as view:
        tools = view.addons.molsysmt
        assert tools.molecular_mechanics.potential_energy_minimization(
            in_place=True, update_view=False
        ) is None
        assert tools.get_sync_status()["state"] == "pending"
        tools.sync_view()
        assert tools.get_sync_status()["state"] == "synchronized"
```

The native write invalidates evaluated coverage in saved interaction analyses;
it does not recalculate them. A scene-projection failure exposes
`science_completed=True`; call `sync_view()` to retry projection without
repeating minimization. An uncertain scientific write requires explicit recovery.
Scene history is not molecular Undo. Cached tools resolve replacement and reject
closed or empty owners, as for the other bound operations.

The native method, platform, force-field defaults, `to_form`, verbose output
and physical units remain explicit native contracts. The addon-only
`skip_digestion` flag is keyword-only; the native function has no such escape
hatch and always receives ordinary validation. It has no public `tolerance`,
atom selection or structure-selection argument at this source. Select an
appropriate single-structure system before this operation; no visible-structure
inference or trajectory loop is added. No missing atoms, protonation states,
force-field parameters or periodic images are prepared automatically.

The received CPU route uses an explicit single-structure NoCutoff/HBonds model.
Local optimization and an energy decrease do not certify a global minimum,
equilibrium or physical stability. Converged coordinates can depend on model,
platform and numerical execution settings. GPU and arbitrary-system preparation
remain outside this bounded receiving.

The other two native mechanical functions remain unexposed pending their own
input, engine, unit and mutation review. The platform-name validation mismatch
is tracked in [MolSysMT#559](https://github.com/uibcdf/molsysmt/issues/559);
Reference/OpenCL requests are currently rejected by native validation. This
integration does not bypass that validation or choose another platform.
Nonbonded-energy partitioned-selection receiving is tracked separately in
[MolSysMT#561](https://github.com/uibcdf/molsysmt/issues/561); that function is
not exposed by this addon yet.

Native references: {func}`molsysmt.molecular_mechanics.get_engine_forcefield`,
{func}`molsysmt.molecular_mechanics.get_degrees_of_freedom`,
{func}`molsysmt.molecular_mechanics.get_potential_energy`,
{func}`molsysmt.molecular_mechanics.potential_energy_minimization`.

## Computing geometry on the current system

The structure wrappers keep atom/structure selections, endpoint order, weights,
periodic choices, native output formats and execution controls explicit. They
return native results without attaching a measurement, selecting atoms or
changing coordinates. The additional `molecular_system_2` of distances/vectors
is an ordinary caller-owned input with its own selectors; it is not implicitly
the displayed system or another locked view.

```python
with msv.demo['pentalanine'] as view:
    structure = view.addons.molsysmt.structure
    distances = structure.get_distances(
        selection=[0, 2, 4], selection_2=[1, 3],
        structure_indices=[2, 0, 2], pbc=False, heavy_mode='off',
    )
    directed = structure.get_vectors(
        selection=[0, 2, 4], selection_2=[1, 3],
        structure_indices=[2, 0, 2], pbc=False, output_type='dictionary',
    )
```

{doc}`structure/get_distances` keeps native Cartesian/pair and array/dictionary
choices, including their supported index conventions and exceptions.
{doc}`structure/get_vectors` points from the first endpoint to the second,
retaining sparse endpoint memberships, both structure axes, periodic images,
distances and directions in dictionary output. Zero-length vectors retain
undefined NaN directions. Indices are source positions, not scene object IDs.
Repeated/nonconsecutive structure choices and auxiliary selectors stay native.

```python
with msv.demo['pentalanine'] as view:
    structure = view.addons.molsysmt.structure
    centers = structure.get_center(
        selection=[[0, 2], [4, 5]], structure_indices=[2, 0],
        weights='masses', heavy_mode='off',
    )
    radii = structure.get_radius_of_gyration(
        selection="atom_type!='H'", structure_indices=[2, 0],
        weights='masses', heavy_mode='off', use_gpu=False,
    )
```

{doc}`structure/get_center` returns geometric or weighted centers; it does not
center the molecule. Nested atom selections retain separate centers and native
weight interpretation. {doc}`structure/get_radius_of_gyration` returns one
length quantity per selected structure. Neither aligns, unwraps or prepares
coordinates. Inspect or explicitly convert physical units with PyUnitWizard;
the addon does not convert quantities to bare arrays or impose display units.

The current source repairs native heavy endpoint populations and physical-unit
attribution for distances, radius of gyration and RMSF
([#441](https://github.com/uibcdf/molsysmt/issues/441),
[#440](https://github.com/uibcdf/molsysmt/issues/440),
[#442](https://github.com/uibcdf/molsysmt/issues/442)). These repairs are checked
from the addon against independent geometry and fluctuation references across
nm/angstrom/pm contexts and repeated structure scopes. No hidden mode or unit
correction is added by the addon. Native output/resource limits still apply;
source receiving does not qualify older published packages.

```python
with msv.demo['pentalanine'] as view:
    structure = view.addons.molsysmt.structure
    angles = structure.get_angles(
        triplets=[[0, 1, 2]], structure_indices=[2, 0, 2],
        pbc=False, use_gpu=False,
    )
    dihedrals = structure.get_dihedral_angles(
        phi=True, psi=True, structure_indices=[2, 0, 2],
        pbc=False, use_gpu=False,
    )
```

{doc}`structure/get_angles` retains explicit source atom triplets and
{doc}`structure/get_dihedral_angles` retains explicit quartets or named dihedral
flags. Multiple named types retain their native list and order. Angular
quantities follow the active standard-angle policy, including a PyUnitWizard
context; explicitly request radians or degrees when extracting numeric values.
The native dihedral function has no declared skip_digestion parameter: the
addon-only keyword controls addon validation and is never injected into named
scientific flags. Native public validation and view-lifetime checks remain active.

Backend, periodic and streaming behavior stays native; optional GPU routes were
not qualified by these CPU receiving examples. Chunked input processing does
not guarantee constant memory, and returned outputs can still scale with the
requested atom pairs and structures. These are calculations, not automatic
scene measurements or coordinate edits. Fitting transformations and other
unlisted structure tools still need individual addon receiving.


## Comparing structures without modifying their coordinates

```python
with msv.demo['pentalanine'] as view:
    structure = view.addons.molsysmt.structure
    reference = view.addons.molsysmt.basic.copy()
    raw_rmsd = structure.get_rmsd(
        selection='backbone', structure_indices=[2, 0, 2],
        reference_molecular_system=reference, reference_structure_index=0,
        heavy_mode='force', use_gpu=False,
    )
    minimum_rmsd = structure.get_least_rmsd(
        selection='backbone', structure_indices=[2, 0, 2],
        reference_molecular_system=reference, reference_structure_index=0,
        use_gpu=False,
    )
```

{doc}`structure/get_rmsd` measures deviations in the supplied coordinate frame;
no fit is performed. {doc}`structure/get_least_rmsd` computes the minimum after
an optimal superposition internally, returning a length quantity without
changing either system. It does not call a scene alignment or move the displayed
molecule. Explicit reference inputs, their atom selection and reference structure
index stay native and caller-owned; None retains native self-reference behavior.
Matching counts do not infer chemical atom correspondence. Both inputs must have
the intended order and coordinate conventions. No implicit PBC reconstruction,
preparation or alignment is added.

The native `get_rmsd` signature has no skip_digestion parameter. Its addon-only
keyword governs addon digestion and is never forwarded. Scientific validation
still runs. Quantities retain the actual native units; explicitly convert values
when a numeric consumer requires nm or another unit. Supported native streaming
and optional-engine limits remain native, not a universal RAM/GPU guarantee.

## Inspecting axes and fitting planes

```python
with msv.demo['pentalanine'] as view:
    axes, moments = view.addons.molsysmt.structure.get_principal_axes(
        selection='backbone', structure_indices=[2, 0, 2],
        principal_axes_type='geometric', use_gpu=False,
    )
```

{doc}`structure/get_principal_axes` returns native numeric arrays, including the
moment convention and numeric scale of the selected native coordinate/weight
route. The addon does not invent physical unit labels for bare moment arrays.
Axes are rows ordered by ascending eigenvalue, with a right-handed orthonormal
basis. Individual signs are arbitrary; repeated eigenvalues determine a subspace
rather than unique individual directions. Inspecting axes does not align coordinates.

```python
with msv.demo['pentalanine'] as view:
    planes = view.addons.molsysmt.structure.get_least_squares_plane(
        selection=[[0, 10, 25, 40], [4, 14, 27, 45]],
        structure_indices=[2, 0, 2], pbc=False, heavy_mode='force',
    )
```

{doc}`structure/get_least_squares_plane` returns native sparse source memberships,
structure indices, length-quantity centers/deviations and numeric normals. It
fits coordinates without inferring aromaticity, creating rings or adding a plane
shape to the scene. Degenerate groups, missing boxes and split periodic groups
retain their native rejection; no hidden unwrapping or fabricated normal follows.
An explicit empty structure scope retains native typed empty outputs. Plane
normals describe unoriented planes; a deterministic sign is not temporal continuity.

These metric/fitting queries preserve native selection/backend dependencies;
their numeric/property-selection receiving is not a blanket certification of
every selector or optional engine. Additional scientific calculations remain
separate from coordinate fitting, scene measurements and molecular preparation.


## Receiving maxima, contacts and fluctuations

```python
with msv.demo['pentalanine'] as view:
    structure = view.addons.molsysmt.structure
    farthest_positions, farthest_distances = structure.get_maximum_distances(
        selection=[25, 10, 0], selection_2=[0, 25],
        structure_indices=[2, 0, 2], as_entity=True, as_entity_2=False, pbc=False,
    )
    contact_map = structure.get_contacts(
        selection=[0, 10, 25], selection_2=[1, 14, 27],
        structure_indices=[2, 0, 2], threshold='0.6 nm',
        pbc=False, cell_list=True, use_gpu=False,
    )
    fluctuations = structure.get_rmsf(
        selection='backbone', structure_indices=[2, 0, 2], heavy_mode='force',
    )
```

{doc}`structure/get_maximum_distances` returns native endpoint positions and a
length quantity. Its positions are local to the selected populations or pair
list, not automatically global atom indices. `as_entity` and `as_entity_2`
retain native reduction semantics. The extra keyword-only skip_digestion on
this wrapper controls addon digestion only; the native helper has no declared
flag and still validates scientific arguments.

{doc}`structure/get_contacts` retains threshold quantities, native dense/cell-list
choices, pairs/maps and supported source-index mapping. It returns scientific
booleans or pair lists without drawing contacts. Optional GPU execution has not
been qualified by these CPU examples. Native errors and memory limits remain
native; a dense contact map can still scale with both endpoint populations.

{doc}`structure/get_rmsf` returns one length per selected atom. It does not align
structures, unwrap coordinates, create a color scale or attach a scientific
analysis. Prepare the intended common coordinate frame explicitly when that is
the scientific question. Current heavy-mode physical units are received against
independent variance calculations; no alternate formula is implemented here.

## Querying minima and neighborhoods

```python
with msv.demo['pentalanine'] as view:
    structure = view.addons.molsysmt.structure
    nearest_positions, minimum_distances = structure.get_minimum_distances(
        selection=[25, 10, 0], selection_2=[4, 2],
        structure_indices=[2, 0, 2], pbc=False,
    )
    nearest_neighbors, neighbor_distances = structure.get_neighbors(
        selection=[25, 10, 0], selection_2=[4, 2],
        structure_indices=[2, 0, 2], n_neighbors=1, pbc=False,
    )
    within_cutoff, cutoff_distances = structure.get_neighbors(
        selection=[25, 10, 0], selection_2=[4, 2],
        structure_indices=[2, 0, 2], threshold='0.6 nm', pbc=False,
    )
```

{doc}`structure/get_minimum_distances` returns positions local to the selected
populations or explicit pair list, plus length quantities. The entity flags
choose which population axes are reduced. Independent `weights` and `weights_2`
retain their native meaning when computing centers. No endpoint indices are
silently converted into global atom indices.

{doc}`structure/get_neighbors` accepts exactly one search criterion: `threshold`
or `n_neighbors`. Its ordinary array output gives target positions relative to
the second selected population, with fixed-size count results or ragged cutoff
results. Native supported pairs/atom-index and CSR outputs remain available;
unsupported combinations retain native errors. Self-exclusion applies according
to the native source/selection identity contract, not simply to every zero
distance. An explicit `molecular_system_2` remains caller-owned and can use its
own selection and matching structure-index list. Matching index values do not
make two different sources the same system.

The wrappers reuse the native criterion-admission contract before forwarding
defaults, so an omitted search criterion stays omitted. They do not choose a
cutoff, count, engine or alternative scientific route. Both tools read the
current primary MolSys, including pending managed edits, without synchronizing
the scene, adopting data or attaching an analysis.

The fixes tracked by [#444](https://github.com/uibcdf/molsysmt/issues/444) and
[#445](https://github.com/uibcdf/molsysmt/issues/445) are committed in the native
owner and have source receiving in the addon. This is not a published-package
compatibility claim. The original working-tree evidence and follow-up are retained
in the receiving record. Other unlisted
structure operations remain unreceived.


## Assigning secondary structure

```python
with msv.demo['pentalanine'] as view:
    codes = view.addons.molsysmt.structure.get_secondary_structure(
        selection=[3, 1, 3], structure_indices=[2, 0, 2],
        simplified=True, engine='MDTraj',
    )
```

{doc}`structure/get_secondary_structure` uses MDTraj's DSSP implementation.
MDTraj must be available for this explicitly selected route. Codes belong to
groups, with structures on the first output axis. Unlike atom-population metric
queries, numeric selections here address group indices. The native selected
groups are unique and ordered by group index; the example returns groups 1 and
3. Simplified codes are H, E, C and NA; full codes retain DSSP distinctions and
nonprotein groups retain NA. The wrapper does not color or annotate the scene.
Its extra keyword-only skip_digestion controls addon digestion only; native
scientific validation still runs. No second engine is silently selected.

## Comparing chemically equivalent poses

```python
import molsysmt as msm

# You explicitly provide chemistry suitable for the declared matching method.
molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'], to_form='rdkit.Mol')
with msv.new_view(molsys) as view:
    matches = view.addons.molsysmt.chemical_states.get_atom_correspondences()
    pose = view.addons.molsysmt.structure.get_symmetry_corrected_rmsd(
        selection='all', correspondences=matches, structure_indices=[0], heavy_mode='off',
    )
```

{doc}`structure/get_symmetry_corrected_rmsd` returns the native result dictionary:
length-valued RMSD, selected structures, winning correspondence indices,
near-optimal counts, search scope, method/software and scientific attribution.
The correspondence table is shared across observations rather than copied for
every structure. The dictionary retains detached native result ownership.
RDKit and sufficient declared chemical context are prerequisites; the addon
does not infer missing chemistry or add hydrogens.

Keep reference systems, populations and reference structure indices explicit
when needed. Cached correspondences must still match the current chemistry.
Anchors and supplied candidate maps restrict the scientific search scope; the
result need not be the unrestricted chemical minimum. A raw baseline is computed
only when its correspondence is explicitly provided. No fitting, centering,
rotation or periodic imaging occurs: compare poses in the intended common
coordinate frame. Native bounds and experimental method classification remain
visible; this wrapper does not promote the method's scientific stability.

## Computing principal components

```python
import numpy as np

with msv.demo['pentalanine'] as view:
    eigenvectors, eigenvalues = view.addons.molsysmt.structure.principal_component_analysis(
        selection=[0, 2, 4], structure_indices=[2, 0, 2],
        weights=np.array([1., 3., 2.]), use_gpu=False,
    )
```

{doc}`structure/principal_component_analysis` returns one eigenvector per row,
ordered by descending eigenvalue. Features contain all selected x coordinates,
then y, then z. Eigenvalues retain squared-length units, normally nm**2.
Numeric weights scale the centered covariance as defined by the native method;
they are not normalized or reinterpreted by the wrapper. Eigenvector signs and
bases within degenerate subspaces are not unique. Use covariance reconstruction
or subspace comparisons instead of requiring identical degenerate vectors.

PCA centers features over the requested structures; it does not align molecular
structures, edit coordinates, project the trajectory or draw modes. Prepare the
scientifically intended coordinate frame explicitly. The native covariance is
dense in 3*n_atoms features, so this is not a general bounded-memory trajectory
API. CPU use_gpu=False is qualified here; optional GPU execution has separate
requirements.

The native repair of [#448](https://github.com/uibcdf/molsysmt/issues/448) is
received. Numerical lists, tuples and supported array dtypes, including strided
or read-only arrays, are normalized by MolSysMT. Dimensionless quantity weights
retain their physical numerical factors. Invalid lengths, nonfinite/negative or
all-zero weights and dimensioned quantities reject before native computation.
The addon forwards inputs unchanged; it adds no scientific normalization rule.
This receiving qualifies the CPU route, with squared-unit and covariance checks.



## Translating coordinates

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    shifted = tools.structure.translate(translation='[1, 0, 0] nm')
    # The independent result is returned to Python; view.molsys stays in the view.
    tools.structure.translate(
        translation='[0, 1, 0] angstrom', selection='backbone',
        structure_indices=[2, 0], in_place=True, update_view=False,
    )
    pending = tools.get_sync_status()
    tools.sync_view()
```

{doc}`structure/translate` preserves the native in_place=False default and result
ownership. Independent results are never adopted by update_view. To edit the
bound system, request in_place=True; successful translation returns native None.
The default update_view=True reconciles geometry immediately. False leaves
completed scientific edits pending until sync_view(), which never repeats the
translation. Reads use pending coordinates; stale scene/index actions are blocked.

Translation quantities, shape broadcasting, atom selections and structure order
remain native. Supported shapes describe one vector, one vector per selected
structure, or one vector per selected atom and structure. Repeated indices use
the native last supplied value, without added accumulation or deduplication.
The box and atom/structure identities stay fixed. Regions, selections, anchored
shapes, navigation and source accounting survive reconciliation. Native coordinate
setters invalidate named interaction coverage only on edited structures; no
detector runs automatically. Independent output may copy the system according
to the native contract; in-place integration adds no full trajectory copy.

A display failure after successful science raises SystemEditSyncError with
science_completed=True and scientific_result, which is None here. Retry
tools.sync_view() instead of the translation. A possible partial scientific write
enters uncertain state and requires explicit recovery, without an implied rollback.
The skip_digestion flag cannot bypass integration ownership or branch controls.

Native centering is resolved in [#451](https://github.com/uibcdf/molsysmt/issues/451)
with explicit source/destination centers and a consistent in-place None return.
See {ref}`Tutorial_Center` for the new pre-1.0 argument names and containment rules.
The bound structure.center wrapper now receives that exact native contract,
with source containment, initial destinations, weights and native return ownership.
The addon supplies no alternate formula, legacy keyword alias or hidden selection.


## Rotating and reflecting coordinates

Use a proper rotation to change orientation while preserving distances and
handedness. Reflection across a plane is a different operation: it preserves
distances for a unit plane normal but can invert molecular chirality. Neither
operation rotates the periodic box or updates chemical-state assignments.

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    rotated = tools.structure.rotate(
        rotation=[[0, -1, 0], [1, 0, 0], [0, 0, 1]],
        rotation_center='[0.1, 0.2, 0.3] nm',
    )
    # An independent reflected system is returned; the current view stays loaded.
    reflected = tools.structure.flip(vector=[1, 0, 0], point='[0, 0, 0] nm')
    tools.structure.rotate(
        rotation=[[0, -1, 0], [1, 0, 0], [0, 0, 1]],
        selection='backbone', structure_indices=[2, 0],
        in_place=True, update_view=False,
    )
    tools.sync_view()
```

{doc}`structure/rotate` retains native proper-matrix validation, active row-vector
conventions, matrix broadcasting and rotation-like objects with apply(). The
rotation center carries length units. Repeated and nonconsecutive selections keep
native ordering and last supplied coordinate assignments. No matrix conversion,
normalization or alternate algorithm is introduced by the addon.

{doc}`structure/flip` retains native arguments and scientific results. The None
default uses [0, 0, 1]. Native validation normalizes finite nonzero normals, so
[2, 0, 0] and [-1, 0, 0] describe the same plane as [1, 0, 0]. Zero/nonfinite
normals and invalid plane points reject before coordinate publication, preserving
coordinates, boxes and interaction coverage. The native repair is tracked in
[#460](https://github.com/uibcdf/molsysmt/issues/460); the addon forwards its
inputs and does not implement a reflection formula. One finite length-bearing
point defines the plane for all requested structures. Reflection reverses
handedness and leaves stored chemical assignments unchanged. The native flip
signature has no declared skip_digestion: the addon's keyword-only flag controls
addon digestion only and never disables the native boundary.

Both wrappers preserve in_place=False by default. update_view does not adopt an
independent result. In-place edits return None; update_view=True synchronizes the
scene, and False leaves pending work for sync_view(). The same retained identity,
selective interaction invalidation, deferred composition and failure-recovery
contract as translation applies. A synchronization-only retry must not repeat a
rotation or reflection: doing so would execute the science a second time.


## Fitting and sequence-based alignment

Use {doc}`structure/least_rmsd_fit` when you can specify corresponding atoms.
selection_fit and reference_selection_fit are the ordered fit anchors; selection
is the population moved by the resulting rigid transform. Those populations can
be different. Native rank and correspondence checks remain applicable.

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    reference = tools.basic.extract(structure_indices=[0])
    fitted = tools.structure.least_rmsd_fit(
        selection='all', selection_fit='backbone',
        reference_molecular_system=reference, reference_structure_index=0,
        use_gpu=False,
    )
    # The independent result stays in Python; the current view is not replaced.
    tools.structure.least_rmsd_align(
        selection="atom_name=='CA'", reference_molecular_system=reference,
        reference_structure_index=0, in_place=True, update_view=False,
        use_gpu=False,
    )
    tools.sync_view()
```

{doc}`structure/least_rmsd_align` derives correspondence through the declared
sequence-alignment engine. Its selection and reference_selection identify fit
anchors; **complete selected components move**, including their non-anchor atoms.
Other components remain unchanged. Biopython is the native sequence-engine
prerequisite, not an implicit preparation step performed by the addon.

Both tools preserve native in_place=False, native returns, structure ordering,
reference choices and configuration controls. Only independent least_rmsd_fit
output uses to_form; requesting conversion never adopts the result into the
view. An in-place call returns None. update_view=False defers projection only;
sync_view() reconciles the completed science without fitting again. Other view
state, retained object identity, native selected-structure interaction invalidation
and uncertain/synchronization-failure recovery follow the geometry contract above.
The native fit may publish through more than one coordinate setter; a scientific
interruption does not imply rollback.

The reference is caller-owned and must remain stable during the call. The addon
serializes its primary view only: it neither locks nor synchronizes another view
whose molecular system you pass as reference. An independent fit can read pending
primary coordinates; it does not project them or adopt its output. Explicit
coordinate-only native references and independent output forms retain native
units and ownership. No periodic reimaging, atom-correspondence heuristic, box
transformation or chemical preparation is added.

Native least_rmsd_align now preserves omitted/None self-reference using the
original reference_structure_index, including in-place fits. Atomic index lists,
tuples, arrays and full-axis Boolean masks use the query and reference atom axes;
they are projected to original sequence groups and paired atom names by MolSysMT.
The addon forwards these inputs unchanged and does not calculate correspondence
or replace a reference. Repairs and their native guards are tracked in
[#452](https://github.com/uibcdf/molsysmt/issues/452) and
[#453](https://github.com/uibcdf/molsysmt/issues/453). The same semantics are
received in the bound addon with actual scene and selected-structure checks.
This qualification covers CPU calls with explicit precision where tested; forwarding GPU/backend choices is not GPU qualification.


## Centering the current molecular system

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    centered = tools.structure.center(
        selection='backbone', source_center_selection="atom_name=='CA'",
    )
    # The independent centered MolSys stays in Python; the view is unchanged.
    tools.structure.center(
        selection='all', source_center_selection="atom_name=='CA'",
        target_coordinates='[1, 2, 3] angstrom',
        in_place=True, update_view=False,
    )
    tools.sync_view()
```

The three populations in {doc}`structure/center` all address the current
view.molsys. selection is the population moved by one rigid translation per
selected structure. source_center_selection defines the source center; None
uses the moving population, including repeated source indices and their weights.
Every source atom must belong to the moving population. Weights apply only to
that source: None gives its geometric center and 'masses' requests native masses.

Choose either a physical target_coordinates point (possibly one per selected
structure) or target_center_selection. The latter supplies its **initial geometric
center**, captured before any movement. A target population can be disjoint from
or overlap the atoms that move; its final center is not constrained to stay at
that initial position. To use a weighted destination, compute it explicitly with
get_center and pass its coordinates. Both destination modes together reject;
with neither, the destination is the origin.

Defaults and results remain native: in_place=False returns an independent system
without adoption, even when update_view=False. With in_place=True, science edits
the current system and returns None. update_view=True reconciles immediately;
False defers projection until sync_view(). Retained scene handles, sources and
structure navigation follow the managed geometry contract. Native coordinate
setters invalidate interaction coverage only for edited structures; no detector
runs. A failed projection is retried without a second centering calculation.
Potential scientific publication before an exception requires explicit recovery.

The native pre-1.0 redesign retired center_of_selection and center_coordinates;
the addon does not recreate those aliases. Source containment, destination/unit
validation, repeated-structure targets and residual refinement remain native.
No implicit periodic reconstruction or box transformation is added. See the
[placement recipe](../cookbook/placing_selected_centers.md) for the same native
population contract outside a view. The technical fix behind
[#451](https://github.com/uibcdf/molsysmt/issues/451) remains accepted; the requested
administrative closure comment is now restored.


## Moving away from a reference center

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    displaced = tools.structure.move_away(
        selection='all', center_of_selection="atom_name=='CA'",
        direction=[1, 0, 0], distance='2 angstroms', structure_indices=0,
    )
    # The independent result stays in Python; the view is unchanged.
    tools.structure.move_away(
        selection='all', center_of_selection="atom_name=='CA'",
        direction=[1, 0, 0], distance='2 angstroms', structure_indices=0,
        in_place=True, update_view=False,
    )
    tools.sync_view()
```

The bound `structure.move_away` mirrors {func}`molsysmt.structure.move_away`.
Its native default is one structure, index 0, and an independent output.
`selection` determines what moves. `center_of_selection` and its `weights`
determine the source center. These are this function's current native argument
names, distinct from the redesigned arguments of `structure.center`.
`reference_molecular_system=None` uses the current bound system;
`reference_center_of_selection`, `reference_weights` and
`reference_structure_indices` remain independent scientific inputs. A None
reference structure scope uses the moving structure scope. An external reference
remains caller-owned: keep it stable during the call; this addon does not lock or
synchronize another view.

The two direction modes have different meanings. Automatic direction adds the
requested distance along the existing reference-to-source vector; distance is
an **additional displacement**, not the final center separation. With an explicit
finite nonzero direction, native digestion normalizes it and places the source
at the **initial** reference center plus the requested offset. There is no
intermediate centering publication. The explicit
mode requires the source-center atoms to be contained in the moving population.
An overlapping reference is an initial snapshot, not a final constraint. No
periodic reconstruction, reference preparation or box transformation is added.

The addon receives single-structure nondegenerate calls with units and weights,
independent results and native None in-place returns. Native selected-structure
interaction invalidation is retained. Deferred projection, scene identity/maps
and retry after a display failure use the same controls as translation. Retry
`tools.sync_view()` after a projection failure; do not repeat completed science.

:::{warning}
Both modes require one structure and one center in each system. Multiple or
repeated structure requests reject before centering or displacement. Automatic
centers must be distinct and finite, even when distance is zero; explicit
vectors must be finite and nonzero. These rejections preserve coordinates,
boxes and stored interaction coverage and leave the managed scene synchronized.
The native NaN and partial-write defects tracked by
[#456](https://github.com/uibcdf/molsysmt/issues/456) and
[#457](https://github.com/uibcdf/molsysmt/issues/457) are repaired. The addon
forwards the native validation and supplies no substitute geometry. An unrelated
backend failure after actual publication still needs explicit recovery; display
retry must not repeat successful science.
:::


## Aligning principal axes

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    aligned = tools.structure.align_principal_axes(
        selection='all', principal_axes_of_selection="atom_name=='CA'",
        principal_axes_type='inertia', weights='masses', center=False,
    )
    # The independent native result does not replace view.molsys.
    tools.structure.align_principal_axes(
        selection='all', principal_axes_of_selection="atom_name=='CA'",
        principal_axes_type='geometric', structure_indices=[2, 0],
        axes=[[0, 1, 0], [0, 0, 1], [1, 0, 0]],
        center=True, in_place=True, update_view=False,
    )
    tools.sync_view()
```

{func}`molsysmt.structure.align_principal_axes` rotates the atoms in `selection`
using the axes of `principal_axes_of_selection`. None uses the moving population;
an explicit fitting population may overlap or be disjoint from the atoms moved.
All populations address the current bound system. A disjoint fitting population
stays unchanged: its **initial** geometry determines the transformation, rather
than defining a final constraint on atoms that do not move.

The native `principal_axes_type` selects inertia or geometric axes. Eigenvalues
are ordered increasingly within that definition. Individual eigenvector signs
are mathematically arbitrary; repeated principal moments do not define unique
individual axes and reject. The target `axes` are three **row vectors** forming
a right-handed orthonormal basis; None requests the Cartesian basis. The native
operation owns weights, axis signs, degeneracy tolerance and basis validation.
`weights` apply to the fitting population, including native mass weighting.
No eigenvalue correction or eigensolver is supplied by this addon.

By default `center=False`, the rotation uses and restores the initial weighted
fitting center. With `center=True`, that center is subtracted without restoration.
When fitting atoms move along with the selection this places their weighted
center at the origin; it does not promise to center a fitting population that
was deliberately excluded from movement. Both modes preserve relative distances
and handedness within the moved population. They do not rotate the periodic
box, wrap components or prepare periodic coordinates.

Native `in_place=False` returns an independent result; `in_place=True` edits the
bound system and returns None. Nonconsecutive/repeated structures retain native
ordering and selected-structure interaction invalidation. `update_view` controls
only projection. A deferred sequence preserves scene correspondence and is
finished with `sync_view()`; synchronization retry does not repeat the alignment.

The native function currently has no `skip_digestion` argument. The addon's
keyword-only flag controls its own digestion only: native validation always
runs, including when that flag is True. Invalid target bases, degenerate moments
and rejected inputs keep their native exceptions; a possible scientific partial
write and a failed display projection retain their separate recovery contracts.


## Editing dihedral angles

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    quartets = tools.chemical_states.get_dihedral_quartets(phi=True)
    # Keep this one quartet explicit; input angles carry physical angular units.
    edited = tools.structure.set_dihedral_angles(
        dihedral_quartets=quartets[0], angles='60 degrees',
        structure_indices=[0], pbc=False,
    )
    # Independent outputs are returned without replacing the view's system.
    tools.structure.shift_dihedral_angles(
        dihedral_quartets=quartets[0], shifts='15 degrees',
        structure_indices=[0], pbc=False, in_place=True, update_view=False,
    )
    tools.sync_view()
```

{func}`molsysmt.structure.set_dihedral_angles` sets absolute targets;
{func}`molsysmt.structure.shift_dihedral_angles` adds signed angular increments
to the current torsions. Supply ordered atom-index quartets and unit-bearing
angles/shifts. Missing required scientific inputs retain native rejection; the
addon does not infer phi/psi or a preparation workflow. Native `pbc=True` is the
default; use the same periodic convention when measuring and editing. With no
box the native editor falls back to nonperiodic geometry. No box is created,
rotated or changed by the addon.

Automatic blocks come from the native connectivity owner after cutting each
central bond; atoms on the fourth atom's side are rotated. This is a coordinate
edit, not bond deletion or force-field minimization. The receiving layer only
declares retained atom/structure identities and possible coordinate publication;
it does not recompute graph cuts, rewrite quartets or guess a moving selection.
Changes to bond lengths across a deliberately limited explicit block are the
caller's scientific choice, not automatically repaired geometry.

The setter receives its native angle broadcasting, including size-one axes,
and explicit atom-index block collections as understood by that tool. Other
structures and boxes stay unchanged. Native structure ordering/repetitions and
last publication semantics remain intact. Shifts are added by the native tool
before delegation to the setter; no extra accumulation is introduced for repeated
structure indices. General block objects from another tool must match the
editor's actual native input contract; the addon does not reshape ragged data.

Both editors retain native `in_place=False`: return the independent MolSys
without adoption. `in_place=True` returns None and reconciles admitted geometry
by default; `update_view=False` defers only projection. Native coordinate setters
invalidate stored interactions on edited structures. Regions, selections,
anchored shapes, sources and current-structure navigation use the same managed
correspondence as other coordinate edits. Retry `sync_view()` after a display
failure, without repeating the already completed torsion operation. Possible
partial scientific writes still require explicit recovery.

The setter has no native `skip_digestion` parameter: its addon-only keyword
controls local digestion while native public validation still runs. The shifter
retains its native declared flag. Neither flag bypasses integration controls.

Native editors now reject nonfinite angular requests before coordinate publication
and preserve explicit blocks in both set and shift routes. A block pool is a
collection of nonempty atom-index lists: each quartet rotates the union of blocks
containing its fourth atom. Invalid indices, empty pools and incompatible angular
shapes reject without changing geometry, topology or named interaction coverage.
The native and addon guards cover these contracts under
[#461](https://github.com/uibcdf/molsysmt/issues/461) and
[#462](https://github.com/uibcdf/molsysmt/issues/462); they do not qualify every
possible geometric input or an installed release pair.


## Reading physical and chemical properties

The source addon now exposes all thirty-four reviewed tools under
`view.addons.molsysmt.physchem`: the seven readers below, followed by the two
ProtOr tools, four reference-descriptor tables, conformational SASA and two
stored-chemistry reports, plus stored aromatic-ring recognition and detached
aromaticity perception and three chemical-feature readers (formal-charge
centers, hydrophobic atoms and ordered halogen sites), plus the Zimmerman
bulkiness and Levitt secondary-structure propensity reference lookups, and
state-aware TPSA and Wildman–Crippen lipophilicity with native contribution
outputs. Three further readers expose AutoDock types, CIP stereochemistry and
explicit partial-charge models. SASA and the chemical readers have bounded receiving, not universal scientific qualification. The
inspected native inventory has 34 exports; all now have explicit source wrappers.
The final six retain their distinct reader, independent-output and factory contracts. The new reference lookups have their own source receiving; earlier hosted
gates retain their original source identities and scopes.

| Tool | Native result and received scope |
| --- | --- |
| `get_mass` | Physical atomic masses and hierarchy sums, with native quantity units (normally dalton). The system-level value covers the whole system. |
| `get_charge` | Group table charges and hierarchy sums in elementary charge units; explicit OpenMM parameterization retains its separate prerequisites. |
| `get_atomic_radius` | Atom radii in native nm table units; vdw and explicit ProtOr definitions. |
| `get_electronegativity` | Atom Pauling values as a dimensionless quantity. Missing tabulated values retain native NaN. |
| `get_hydrophobicity` | Group values as a NumPy array, with the native choice of 15 reference scales. |
| `get_polarity` | Group values as a list, using grantham or zimmerman. |
| `get_transmembrane_tendency` | Group values as a list: zhao scores or senes three-parameter rows. |

```python
import molsysviewer as msv
import molsysmt as msm

with msv.demo["pentalanine"] as view:
    properties = view.addons.molsysmt.physchem
    atom_masses = properties.get_mass(element="atom")
    group_charges = properties.get_charge(selection="group_name=='ALA'")
    hydrophobicity = properties.get_hydrophobicity(
        selection="group_name=='ALA'", definition="kyte"
    )
    assert msm.pyunitwizard.get_value(atom_masses, to_unit="dalton").shape == (62,)
    assert list(hydrophobicity) == [1.8] * 5
    assert list(msm.pyunitwizard.get_value(group_charges, to_unit="e")) == [0.] * 5
```

These are scientific values. The call does not assign a property to the MolSys,
color a representation, adopt a result, prepare chemistry or update the scene.
The reader resolves the actual current primary at call time, including pending
managed scientific edits; it does not synchronize those edits. Scientific
parameters, skip_digestion and native derived/cache behavior are preserved.
There are no invented root aliases or update_view parameters for these readers.

Choose atom scope for atom tables and group scope for group scales. The addon
does not invent hierarchy support absent from the native implementation.
Native fixed-scope readers now reject unsupported levels explicitly under
uibcdf/molsysmt#471; no sum or mean is inferred for an undefined hierarchy.
Tabulated group charge is not assigned partial charge or a protonation model.
Unknown chemical groups are rejected when missing from a table; ACE/NME caps,
waters, ions and ligands are not automatically excluded or assigned zero.
Native dummy-group conventions remain unchanged.

For OpenMM charge, select the definition and forcefield explicitly. A
single-structure capped peptide is received; the native conversion currently
rejects a multi-frame periodic box. Extract a structure explicitly when needed;
the addon never chooses one or changes force-field settings for you. OpenMM mass
on the bound MolSys remains unsupported by the native function. This receiving
does not certify arbitrary parameter sets, incomplete chemistry or every form.

The repaired native contract under uibcdf/molsysmt#470 forwards the requested
selection syntax, including MDTraj with its optional provider installed.
Receiving compares the selected population with independently resolved intended
atom/group indices. Numeric order and repetitions, empty populations and native
containers remain explicit. Source availability is not installed-artifact
qualification.

## Querying ProtOr and reference descriptors

The two ProtOr helpers keep their native public paths:
`tools.physchem.get_protor_atom_type` returns a tuple of atom-type and rule
provenance arrays; `tools.physchem.get_protor_vdw_radius` returns native nm radii.
Hydrogen typing is ignored while its radius follows the native fallback. Heavy
atom rules and fallback categories remain separate. These calls add no hydrogens,
store no chemical assignments and prepare no molecular system.

The four additional group tables preserve native definitions and containers:

| Tool | Reference and actual result |
| --- | --- |
| `get_surface_area` | Native area quantity, standardized by PyUnitWizard from the provisional Å² table convention. Original unit/normalization verification remains pending under uibcdf/molsysmt#473. |
| `get_volume` | Grantham relative side-chain descriptors as a NumPy array; no dimensional molecular volume is calculated. |
| `get_area_buried` | Rose average buried-area table, documented in Å², as a raw NumPy array; no quantity conversion. |
| `get_buried_fraction` | Janin reference percentages as a raw list; neither values between zero and one nor conformational burial is inferred. |

These descriptors depend on selected group identities, not the visible structure
coordinates. They are not calculated SASA, solvent exclusion, molecular volume
or measured exposure of this particular conformation. Missing real-group entries
still raise the native error. The addon does not filter chemistry, normalize
numbers or append units to bare reference values.

```python
with msv.demo["pentalanine"] as view:
    properties = view.addons.molsysmt.physchem
    types, rules = properties.get_protor_atom_type(selection="group_name=='ALA'")
    radii = properties.get_protor_vdw_radius(selection="group_name=='ALA'")
    volume_descriptors = properties.get_volume(selection="group_name=='ALA'")
    assert types.shape == rules.shape
    assert msm.pyunitwizard.get_value(radii, to_unit="nm").shape == types.shape
    assert list(volume_descriptors) == [31.] * 5
```

The primary, selection and result ownership follow the same serialized-reader
contract, including pending scientific edits without automatic synchronization.
`get_volume` adds a keyword-only skip_digestion control solely for addon
validation; native get_volume has no such flag and always receives its ordinary
public validation. `get_area_buried` has no native syntax parameter, so the addon
does not invent one. Other signatures preserve the native declared parameters.

The native selection/scope repairs under uibcdf/molsysmt#470 and
uibcdf/molsysmt#471 are now received from 825a66d39. ProtOr, volume and buried
fraction honor the requested syntax; fixed atom/group readers reject unsupported
levels before population lookup. The addon adds no selector translation or
aggregation formula. get_area_buried retains its explicit no-syntax signature.
Unit review uibcdf/molsysmt#473 and installed package compatibility remain
separate.


## Calculating conformational solvent-accessible area

`view.addons.molsysmt.physchem.get_sasa(...)` binds the current primary to native
{func}`molsysmt.physchem.get_sasa`. It returns an area quantity with structure and
selected-element axes. Every atom of the primary participates in occlusion,
including atoms outside the output selection. Extract a separate system explicitly
if you need a different set of occluding atoms. No hydrogens are added, no molecular
preparation is inferred, and no colors or representations are created.

:::{warning} Explicit SASA geometry
Areas follow the square of the configured standard length unit, with bounded
nm/angstrom/pm receiving for both CPU engines under
[#478](https://github.com/uibcdf/molsysmt/issues/478). Use `pbc=False` for Cartesian
SASA, including MDTraj on boxed systems. With a box, native `pbc=True` screens
other atom indices with minimum images, excluding self-images; without a box,
it is Cartesian. MDTraj rejects periodic requests with a box under
[#479](https://github.com/uibcdf/molsysmt/issues/479). The addon forwards this
choice without geometric compensation. This receiving covers source CPU
execution, not GPU support or an installed package. See {ref}`Tutorial_Get_sasa`
for small-cell and sampling limits.
:::

```python
import molsysmt as msm
import molsysviewer as msv

with msv.demo["pentalanine"] as view:
    # Keep the CPU and standard length context explicit for this receiving.
    with msm.pyunitwizard.context(
        standard_units=["nm", "ps", "radians", "dalton", "e", "dimensionless"]
    ):
        area = view.addons.molsysmt.physchem.get_sasa(
            selection="atom_name=='CA'",
            structure_indices=[2, 0],
            probe_radius="1.4 angstroms",
            n_sphere_points=960,
            use_cell_list=False,
            use_gpu=False,
        )
        assert area.shape == (2, 5)
        assert msm.pyunitwizard.get_unit(area).is_compatible_with(
            msm.pyunitwizard.unit("nm**2")
        )
```

Keep sampling, probe radius, engine and execution options explicit when they
matter to your workflow. Native hierarchy sums and requested structure ordering
are preserved. Like other readers, SASA can inspect a pending edited primary
without calling `sync_view()`, adopting a result or publishing scene changes.
`skip_digestion` preserves the native public flag; there is no `update_view`
argument on this nonmutating calculation. Runtime results, visual interpretation
and scientific attribution retain their respective owners.


## Inspecting stored chemistry and hydrogen inventory

`view.addons.molsysmt.physchem.get_hydrogen_inventory(...)` and
`get_chemical_readiness(...)` return detached native dictionaries. They do not
add atoms, infer a protonation state, assign charges, repair connectivity or
change the scene. Read their coverage, issues and `unassessed_checks`; neither
report is a chemical-validity certificate or a universal readiness flag.

Choose one structure explicitly when the primary has multiple structures.
Repeated copies of the same structure index are deduplicated; several distinct
indices raise a native argument error. The addon does not replace the native
`structure_indices='all'` default with the currently visible structure. Use
`chemical_state='reference'`, an explicit state index, or `'structure'` according
to the native state/reference-association contract. Ambiguous or unassociated
chemistry remains unassessed rather than silently choosing the first state.

```python
import molsysviewer as msv

with msv.demo["pentalanine"] as view:
    properties = view.addons.molsysmt.physchem
    inventory = properties.get_hydrogen_inventory(
        selection="atom_name=='CA'", structure_indices=[1]
    )
    report = properties.get_chemical_readiness(
        selection="atom_name=='CA'", structure_indices=[1]
    )
    assert inventory["schema"] == "molsysmt.hydrogen_inventory@1"
    assert report["schema"] == "molsysmt.chemical_readiness@1"
    assert len(inventory["atom_indices"]) == len(report["atom_indices"]) == 5
    assert "valence" in inventory["unassessed_checks"]
    assert "ready" not in report
```

The hydrogen inventory separates indexed covalent H neighbors from stored
virtual `n_implicit_hydrogens` and `n_explicit_hydrogens` annotations. Virtual
counts add to the indexed count. The int64 arrays use **-1 for unknown**, never
an invented zero. `parent_hydrogen_pairs` has shape `(n_pairs, 2)`, parent first;
selected parents retain their external H neighbors even when those H atoms are
outside the output selection. `available` describes readable inventory, not
validated valence, protonation or coordinate quality. Full-graph conflicts may
remain visible when selecting only a few parents.

Readiness retains incident bond indices, external endpoints and explicit crossing
bonds. It reports stored-field availability and declared evidence without
validating their scientific origin. Coordinate entries are finite-position
booleans assessed in nm; formal charge is in elementary charge units. Nonfinite
positions and unknown chemistry are reported without repair. Atom selections
are returned as sorted unique source indices, and empty arrays retain defined
types and shapes. Neither reader invents missing group/atom data.

Default-reference external selections, such as `selection="name CA", syntax="MDTraj"`,
are now supported by the native readiness reader under
[#480](https://github.com/uibcdf/molsysmt/issues/480) and forwarded unchanged.
For explicit or structure-associated chemical-state queries, use MolSysMT syntax
or explicit atom indices where required by the public selector. The addon does
not translate selectors or choose another state to conceal a native restriction.

Both calls bind the current resident `view.molsys`, including after replacement
or while managed edits await synchronization. They do not call `sync_view()` or
accept `update_view`. Editing a returned report does not edit the primary;
request a new report after changing molecular data. Native standalone H5MSM
selective-reading guarantees do not turn an already loaded view into a new
out-of-memory file-query interface. No hydrogen-placement or optional chemistry
engine is introduced by these wrappers.

:::{seealso}

- {ref}`Tutorial_Hydrogen_Inventory` — counts, source scopes and scientific limits.
- {ref}`Tutorial_Chemical_Readiness` — stored-field coverage, states and evidence.
:::


## Reading aromatic participants and perceiving aromatic flags

The two bound tools answer different questions:

| Tool | Result and prerequisites |
| --- | --- |
| `physchem.get_aromatic_rings(...)` | Packed complete ring participants from **stored** atom and bond aromatic flags. Requires declared complete connectivity or an explicit native completeness assumption. |
| `physchem.get_aromaticity(...)` | Detached source-indexed atom and bond flags calculated with the explicit optional RDKit model. Requires complete supported closed-shell chemical evidence; known contradictions reject. |

Neither operation stores assignments, repairs chemistry, adds hydrogens, creates
shapes or draws interactions. Planarity alone is not chemical aromaticity.
Perception does not silently prepare the stored-ring reader's input.

This example makes the preparation explicit **before** creating the view. It
requires RDKit for the native perception step; ring recognition itself can use
already declared flags without that provider.

```python
import molsysmt as msm
import molsysviewer as msv

molsys = msm.convert(msm.systems["caffeine"]["caffeine.sdf"])
flags = msm.physchem.get_aromaticity(molsys)
msm.set(molsys, element="atom", atom_is_aromatic=flags["atom_is_aromatic"])
msm.set(molsys, element="bond", bond_is_aromatic=flags["bond_is_aromatic"])

with msv.new_view(molsys) as view:
    tools = view.addons.molsysmt.physchem
    rings = tools.get_aromatic_rings(max_cyclic_block_size=256)
    perceived = tools.get_aromaticity(selection=[11, 1, 11, 4])
    assert rings["atom_offsets"].tolist() == [0, 5, 11]
    assert perceived["atom_indices"].tolist() == [1, 4, 11]
    assert perceived["implementation"] == "rdkit.AROMATICITY_RDKIT"
```

Stored rings use `definition='stored_aromatic_bonds'` and
`method='minimum_cycle_basis'`. Every source atom and bond requires a known
aromatic flag, including explicit False for nonaromatic entries. Numeric output
`atom_indices` and `atom_offsets` packs sorted atom memberships, **not cyclic
traversal order**. Empty output has offsets `[0]`. Shared atoms may occur in
several memberships. A basis is not every possible cycle, and ties can depend
on atom order or NetworkX version.

Select complete rings. A selection that cuts a ring raises instead of completing
it implicitly; in fused systems a whole selected ring can still cut its neighbor.
A nonaromatic fusion bond is omitted from the declared aromatic subgraph, so the
result can be a perimeter instead of separate subrings. The keyword-only cyclic
block limit bounds an expensive graph calculation; raise it only after assessing
cost. `assume_complete_connectivity=True` is an explicit scientific declaration
recorded in evidence, not preparation or a source edit.

Perception uses `method='fused_ring_electron_count'`, implemented by the native
`rdkit.AROMATICITY_RDKIT` route. It evaluates the whole graph before output
selection. Atom indices are sorted and deduplicated; only bonds whose two
endpoints are selected appear in the result. Two aromatic atoms need not have
an aromatic joining bond. Flags, original provider versions, model references
and attribution remain native. This supported model is not a universal
aromaticity definition, a geometric test or a charge/protonation assignment.

`chemical_state` and `structure_indices` retain native resolution. Several
nonconsecutive/repeated structure indices can refer to one chemical state;
a mixed structure-state request rejects instead of choosing the first state.
The result is a chemical participant/flag report, not occurrences per structure.
Full-graph validation precedes empty or subset output. Returned report edits do
not alter the primary, its named analyses or the scene; readers do not call
`sync_view()` or accept `update_view`.

The native repairs under [#482](https://github.com/uibcdf/molsysmt/issues/482)
and [#483](https://github.com/uibcdf/molsysmt/issues/483) preserve default-reference
external syntax and validate explicit ring structure indices. Explicit or
structure-associated chemical-state syntax keeps its native restrictions;
unsupported combinations reject. The addon neither translates selectors nor
adds a separate scientific range checker. This is distinct from installed
MDTraj operator compatibility, tracked under [#484](https://github.com/uibcdf/molsysmt/issues/484).


The primary is the current resident `view.molsys`. Native H5MSM chemistry-only
reading capabilities do not make this bound view a new file-query API.
Optional RDKit absence and unsupported chemistry retain native diagnostics;
there is no provider fallback or hidden molecule preparation.

:::{seealso}

- {ref}`Tutorial_Get_aromatic_rings` — stored flags, sparse membership and basis limits.
- {ref}`Tutorial_Get_Aromaticity` — model, evidence and supported chemistry.
:::


## Reading charge centers, hydrophobic atoms and ordered halogen sites

These tools identify chemical features from the current primary. Their results
are separate from interaction occurrences and representations. No method assigns
charges, adds hydrogens, prepares chemistry, creates shapes or draws contacts.

| Bound tool | Native result and selection contract |
| --- | --- |
| `physchem.get_charge_centers(...)` | Sparse whole-center participants, separate geometry-reference memberships and charge quantities in elementary charge units. Cutting a compound center rejects. |
| `physchem.get_hydrophobic_sites(...)` | Sorted unique int64 source atom indices from the explicit native SMARTS profile. These are atom features, not group hydrophobicity scales. |
| `physchem.get_halogen_bond_sites(...)` | int64 `(n_sites, 2)` donor–halogen and acceptor–reference pairs. Column order encodes roles; only complete selected pairs survive. These are potential sites, not observed halogen bonds. |

The example supplies declared molecular chemistry and explicit viewable 2D
coordinates before constructing the view. Those coordinates are illustration,
not evidence for an interaction. RDKit is required for this example and the
SMARTS readers; charge-center recognition itself does not require that engine
when the resident MolSys already supplies its chemistry.

```python
from rdkit import Chem
from rdkit.Chem import rdDepictor
import molsysmt as msm
import molsysviewer as msv

molecule = Chem.MolFromSmiles("CC(=O)[O-].CCl.C=O.CCC")
rdDepictor.Compute2DCoords(molecule)
with msv.new_view(molecule) as view:
    features = view.addons.molsysmt.physchem
    centers = features.get_charge_centers()
    hydrophobic = features.get_hydrophobic_sites()
    halogen = features.get_halogen_bond_sites(max_matches=100000)
    assert centers["atom_indices"].tolist() == [1, 2, 3]
    assert msm.pyunitwizard.get_value(centers["charges"], to_unit="e").tolist() == [-1.]
    assert 9 in hydrophobic["hydrophobic_atom_indices"]
    assert halogen["donor_halogen_pairs"].tolist() == [[4, 5]]
```

Formal-charge recognition uses `definition='formal_charge'`. It distinguishes
bounded carboxylate/guanidinium motifs, directly connected formal-charge clusters
and isolated charged atoms. It does not infer protonation, partial charges or
every ionic motif. A zero total system charge can coexist with multiple local
centers. Participant atoms and distance-reference atoms can differ; neither
membership array contains a computed center coordinate. Empty sparse outputs
retain offsets `[0]` and a zero-length charge quantity.

The SMARTS profiles are `method='smarts_hydrophobic_atoms'` and
`method='smarts_donor_acceptor'`. They retain the native ProLIF 2.2.2 reference,
actual RDKit producer version and attribution. ProLIF is not an executed
dependency. Hydrophobic typing is a named chemical model, not a universal atom
property. Halogen pair columns must not be independently sorted: an acceptor
index can be larger than its reference-neighbor index. Empty pair outputs have
shape `(0, 2)`. Native `max_matches` bounds full-source matching before output
selection and raises instead of truncating; a small or empty selection cannot
be used to bypass it.

All three tools require their documented stored chemistry and declared complete
connectivity. `assume_complete_connectivity=True` records an explicit scientific
declaration without filling bonds, charges or aromatic flags. Unknown chemistry
still rejects, including before an empty output selection. Structure indices
and `chemical_state` remain explicit; these chemical features are not repeated
occurrences for each structure. Mixed associated states reject instead of
silently choosing the first state. Numeric selections refer to source indices,
not atom IDs.

Default-reference external selections are received for all three readers after
the native repair under [#488](https://github.com/uibcdf/molsysmt/issues/488).
`chemical_state=None` also retains the declared reference, including a reference
at a nonzero state index independent of structure associations. Explicit and
structure-associated SMARTS requests retain the public selector restrictions;
use MolSysMT syntax or explicit atom indices where required. The addon neither
translates selectors nor changes states to make a request succeed.

Numeric feature arrays are independent reports; editing them does not edit
the primary or scene. Result-level reference metadata has a separate ownership
limit: source `02671792f` shares mutable `method_reference` dictionaries between
the SMARTS readers, tracked under [#490](https://github.com/uibcdf/molsysmt/issues/490).
Editing that field can contaminate later reported method references, including
the other reader. Keep reference declarations unchanged until using a qualified
provider repair. This source gate does not certify arbitrary mutation of returned
reference metadata; the addon supplies no consumer-specific copy or transformation.
The repair in native source `6eebcd4ec` has separate local receiving: 172
targeted cases and a bound-reader mutation check. With that source, each result
owns its small method reference independently, including evaluated-empty output.
This does not turn the older hosted gate into a qualification of the repair or
establish installed-package compatibility.
Calls resolve the current resident `view.molsys`,
including after replacement and while managed edits await synchronization;
they neither call `sync_view()` nor accept `update_view`. Optional RDKit absence
and unsupported chemistry retain native diagnostics. These adapters do not
provide a new H5MSM file-query interface or qualify missing-provider behavior.

:::{seealso}

- {ref}`Tutorial_Get_charge_centers` — formal-charge participant/reference memberships.
- {ref}`Tutorial_Get_hydrophobic_sites` — the explicit atomic SMARTS model.
- {ref}`Tutorial_Get_halogen_bond_sites` — ordered chemical roles before geometry.
:::


## Reading bulkiness and secondary-structure reference propensities

These two group-name lookups preserve the native reference data and output type.
They do not calculate the visible conformation's surface, predict secondary
structure, assign a class, color the scene or attach results to the primary.

| Bound tool | Native result and explicit choices |
| --- | --- |
| `physchem.get_bulkiness(...)` | A standardized area quantity, one value per group. Native `definition='zimmerman'` retains its table and published later Å² interpretation. |
| `physchem.get_secondary_structure_propensity(conformation, ...)` | A detached float64 NumPy array of dimensionless weighted frequency ratios. Choose `alpha_helix`, `beta_sheet` or `reverse_turn`; the category is required. |

Select groups supported by the table explicitly. The bundled pentalanine also
contains terminal caps, so this example selects its five ALA groups. The addon
does not silently discard waters, ions, modified groups, caps or placeholders
from a default `selection='all'`: unsupported names retain native errors.

```python
import molsysviewer as msv
import molsysmt as msm

with msv.demo["pentalanine"] as view:
    scales = view.addons.molsysmt.physchem
    areas = scales.get_bulkiness(selection="group_name=='ALA'")
    helix = scales.get_secondary_structure_propensity(
        "alpha_helix", selection="group_name=='ALA'"
    )
    assert msm.pyunitwizard.get_value(areas, to_unit="angstrom**2").round(2).tolist() == [11.5] * 5
    assert msm.pyunitwizard.get_value(areas, to_unit="nm**2").round(3).tolist() == [0.115] * 5
    assert helix.tolist() == [1.29] * 5
```

Both native functions support only `element='group'`. Numeric selections retain
the requested order and repetitions; a scalar group index keeps a one-element
axis. Empty selections retain typed `(0,)` results and the native area unit where
applicable. There is no structure axis or implicit repetition over trajectories.
The lookup itself needs group identities rather than coordinates, but a rich
spatial selection retains the native selector's coordinate requirements and
scope. These functions have no `structure_indices` parameter; use explicit group
indices when you need selection and reference lookup to be separate operations.

Bulkiness is a reference side-chain descriptor, not the input molecule's
measured cross-section, conformational SASA or a physically meaningful total
area obtained by summing groups. PyUnitWizard standardization follows its unit
policy; the adapter adds no scaling. The original 1968 derivation/normalization
remains outside the native source review's audited claim. Read the native
tutorial for the distinct original scale, curation and later unit evidence.

Levitt's `definition='levitt_1978_weighted'` returns reference ratios, not
probabilities. For ALA, helix/sheet/turn values are 1.29, 0.90 and 0.77: they can
exceed one and do not sum to one. There is no clipping, renormalization, inferred
coil remainder or automatic category choice. Use `structure.get_secondary_structure`
for a separate coordinate-based assignment with its own engine requirements.
Reference propensity and observed secondary structure answer different questions.

Returned values are independent; editing them does not change the native tables,
primary or scene. Calls resolve the current `view.molsys` after replacement and
while managed edits await synchronization, without invoking `sync_view()`.
Native definitions, `skip_digestion`, strict unsupported-level/name validation,
selection syntax and optional Ackredit credits are forwarded unchanged. A missing
name never becomes a parent-amino-acid substitution or invented zero. No new
scientific dependency or consumer attribution record is introduced.

:::{seealso}

- {ref}`Tutorial_Get_bulkiness` — the reference area scale and its evidence limits.
- {ref}`Tutorial_Get_secondary_structure_propensity` — required categories and weighted ratios.
:::


## Calculating molecular topological polar surface areas

Use `view.addons.molsysmt.physchem.get_tpsa()` for the experimental native Ertl,
Rohde and Selzer descriptor executed through RDKit. Its default molecule level
returns one area per selected complete molecule, in the configured standard
area unit (nm² by default). Other native levels return atomic contributions or
explicit sums evaluated in complete molecular context. It does not measure the conformation's exposed polar surface or
predict permeability; use conformational SASA for that separate geometric task.

```python
import molsysviewer as msv
import molsysmt as msm

from rdkit import Chem

# Supply an explicitly read graph with RDKit-declared hydrogen inventory.
molsys = Chem.SDMolSupplier(msm.systems["caffeine"]["caffeine.sdf"], removeHs=False)[0]
with msv.new_view(molsys) as view:
    result = view.addons.molsysmt.physchem.get_tpsa(return_report=True)
    area = msm.pyunitwizard.get_value(result["tpsa"], to_unit="angstrom**2")
    assert area.round(2).tolist() == [61.82]
    assert result["report"]["molecule_indices"].tolist() == [0]
    assert result["report"]["method"] == "ertl_rohde_selzer"
```

This example explicitly uses RDKit to read the graph and its hydrogen inventory.
A native SDF source with unspecified CTAB valence/hydrogen evidence is rejected
rather than guessed; loading the same file through a different declared form
can therefore have different chemistry completeness. The addon never changes
the input form or supplements missing counts to make a calculation pass.

Group-free numeric/native-expression selection is supported. With the received
native repairs [#494](https://github.com/uibcdf/molsysmt/issues/494) and
[#495](https://github.com/uibcdf/molsysmt/issues/495), MDTraj selection also works
without source groups: only the external target receives required placeholders,
and source atom order, charges and absent hierarchy remain intact. A selector
using target group metadata describes those external placeholders, not inferred
biological identity. Native group insertion preserves inherited molecule identity.
The separate atom-insertion repair
[#499](https://github.com/uibcdf/molsysmt/issues/499) aligns appended unknown
chemistry across states. Unknown assignments remain unknown and complete
declarations become partial; scientific readers can reject that incomplete
state. These calculations do not insert or prepare atoms. The addon adds no hierarchy or selector workaround.

At the default `element='molecule'`, numeric selections address source molecules;
selecting one atom with a string expression selects its complete parent molecule.
Other supported levels are `atom`, `group`, `component`, `chain`, `entity` and
`system`. Indices address the requested level; `system` selects atoms for a
scalar sum. Ordered/repeated indices keep their multiplicity. A scalar element
index keeps a one-element axis; an empty selection keeps shape `(0,)` except
for `system`, which returns a scalar zero in the descriptor's units. Saved scene
regions do not redefine these scientific indices or contexts.

All calculations retain complete parent molecular chemistry. A selected atom or
group never becomes a capped fragment for recalculation. Source molecule
membership must match covalent connectivity; disconnected salt labels and
covalent bonds crossing a context molecule boundary retain native rejection.

The native default `include_sulfur_phosphorus=False` calculates N/O contributions.
Set it explicitly to `True` to include the model's S/P contributions. These are
different descriptor variants. Native quantities preserve the squared unit
conversion. The wrapper does not rescale values; sums occur only at explicitly
requested native output levels.

`chemical_state='reference'` is explicit. `structure_indices` supplies context for
chemical-state resolution and spatial selection; it adds no structure axis to
the graph descriptor. `chemical_state='structure'` must resolve one state across
the requested structures, including nonconsecutive lists. The visible canvas
structure is not substituted for the requested scope. Protonation, tautomer and
hydrogen inventories are supplied by the caller, never prepared automatically.

The bounded native profile requires complete compatible closed-shell chemistry
and declared indexed/nonindexed hydrogen counts. Metals, radicals, query atoms,
unsupported relationships and inconsistent inventories retain native errors.
Missing RDKit fails explicitly; no engine fallback runs. There is no implicit
hydrogen addition, assignment, topology repair or periodic reconstruction.

The default quantity carries no provenance report. Request `return_report=True`
to obtain the detached `tpsa`/`report` dictionary with source molecule and atom
maps, selected state, method, parameters, software and scientific attribution.
Empty reported selections retain typed maps and provenance. Returned arrays and
nested references remain independent of the primary and later results. Optional
Ackredit records the native executed method; the addon adds no duplicate credit.

Calls resolve current `view.molsys`, including after replacement and during
pending managed edits. They do not adopt a result, color the scene, synchronize
pending edits or change named interaction coverage. Exact native parameters and
`skip_digestion` remain available. The adapter's receiving covers its declared
fixtures and contracts; it does not establish universal model accuracy or
published-package compatibility.

:::{seealso}

- {ref}`Tutorial_Get_tpsa` — complete chemistry, descriptor variants and evidence.
:::

### Reading contributions in complete molecular context

Both bound descriptors preserve native output levels and complete parent
calculation contexts. These outputs are model contributions or explicit sums;
they do not assign a measured exposed area or a new physical property to a group.

```python
import numpy as np
import molsysviewer as msv
import molsysmt as msm
from rdkit import Chem
from rdkit.Chem import rdDepictor

# Explicit caller-owned graph and coordinates; the addon does not prepare them.
molsys = Chem.MolFromSmiles("CCO")
rdDepictor.Compute2DCoords(molsys)
with msv.new_view(molsys) as view:
    tools = view.addons.molsysmt.physchem
    areas = tools.get_tpsa(element="atom", selection=[2, 0, 2], return_report=True)
    scores = tools.get_lipophilicity(element="atom")
    np.testing.assert_allclose(msm.pyunitwizard.get_value(areas["tpsa"], to_unit="angstrom**2"), [20.23, 0.0, 20.23], atol=1e-12)
    np.testing.assert_allclose(scores, [0.5131, 0.0425, -0.5570], atol=1e-12)
    assert areas["report"]["element_indices"].tolist() == [2, 0, 2]
    assert areas["report"]["element_atom_indices"].tolist() == [2, 0, 2]
    assert areas["report"]["atom_indices"].tolist() == [0, 1, 2]
    assert areas["report"]["molecule_indices"].tolist() == [0]
    assert tools.get_lipophilicity(element="system", selection=[]) == 0.0
    selected = tools.get_lipophilicity(element="atom", selection="index 2", syntax="MDTraj")
    np.testing.assert_allclose(selected, [-0.5570], atol=1e-12)
    assert view.molsys.topology.n_groups == 0
```

The report separates `element_indices`, `element_atom_indices` and
`element_atom_offsets` (output rows and their source atoms) from
`molecule_indices`, `atom_indices` and `atom_offsets` (evaluated complete
contexts). Their row counts can differ. Nonmolecular repeated outputs retain
repeated rows while each needed parent molecule is evaluated once. These maps
refer to the supplied source, not new atoms or scene selections.

Indexed hydrogens retain their own contribution rows. Contributions from
nonindexed hydrogens are attributed to their retained attachment atom. The
provider may materialize declared H on a temporary calculation graph; it never
adds guessed H or new source indices. Individual heavy-atom contributions
therefore depend on H presentation. Sums over equivalent atoms and their attached
H agree. Preserve this attribution convention when comparing atom-level results.

`structure_indices` resolves chemistry and spatial selectors; the graph output
has no structure axis. Explicit nonconsecutive indices remain available.
`chemical_state='structure'` must select one state. Changing the visible canvas
structure does not replace the declared scope. Returned reports, values and
nested references remain detached from the primary and later calls. The
functions neither color the scene nor synchronize pending edits.

## Calculating state-preserving lipophilicity scores

`view.addons.molsysmt.physchem.get_lipophilicity()` mirrors native
`method='wildman_crippen'` through RDKit. It returns a float64 array at ordinary
element levels and a float64 scalar at `element='system'`. Values are
**dimensionless**, may be negative and do not change with length-unit policy.
This is separate from tabulated group hydrophobicity scales. It has no implicit
force field, normalization, method fallback, neutralization, counterion stripping
or pH-dependent chemical preparation.

```python
import molsysviewer as msv
from rdkit import Chem
from rdkit.Chem import rdDepictor

molsys = Chem.MolFromSmiles("c1ccccc1")
rdDepictor.Compute2DCoords(molsys)
with msv.new_view(molsys) as view:
    result = view.addons.molsysmt.physchem.get_lipophilicity(return_report=True)
    assert result["lipophilicity"].round(4).tolist() == [1.6866]
    assert result["report"]["method"] == "wildman_crippen"
    assert result["report"]["value_kind"] == "wildman_crippen_model_score"
    assert result["report"]["value_unit"] == "dimensionless"
```

For an appropriate uncharged species this model is conventionally used as a
calculated logP estimate. A score for an ion or zwitterion does not certify a
physical partition coefficient. Net charge zero alone does not establish
applicability; report `charged_atom_indices` and `charged_atom_offsets` retain
formally charged sites, including within net-neutral molecules. No logD, pKa,
pH-dependent species population or ensemble is inferred. A contribution sum
spanning molecules is not a mixture logP.

`return_report=True` returns the detached `lipophilicity`/`report` dictionary with
source output/context maps, chemical state, formal charges, method, parameters,
producer versions and native scientific attribution. The default array carries
no report; request it explicitly for exported scientific results. Neither output
is automatically attached to MolSys or stored as a new analysis. Optional
Ackredit records the native executed model and software once; the addon adds no
duplicate scientific credit.

The explicit chemical-state, completeness, H inventory, provider and selection
requirements above apply to both descriptors. Native #494/#495 repairs retain
their exact-source receiving. Group/chain contribution rows require actual source
membership; absent groups are not invented. Both functions are headless and
resolve current `view.molsys` after replacement and during pending managed edits.
Expert parameters and `skip_digestion` remain native; there is no addon-specific
preparation or scene parameter.

:::{seealso}

- {ref}`Tutorial_Get_tpsa` — area descriptors and complete-context contributions.
- {ref}`Tutorial_Get_lipophilicity` — model scores, charged states and evidence.
:::


## Calculating chemical labels and partial charges

The experimental `physchem` namespace mirrors three independent native readers.
`get_autodock_atom_types(typing_scheme='autodock4')` returns AutoDock U2 labels;
it does not assign the primary's `atom_ff_type`. `get_partial_charges(method=...)`
requires an explicit model and returns native charge quantities, distinct from
formal charge or the existing `get_charge` table lookup.
`get_cip_stereochemistry()` returns atom/bond CIP labels and source maps.

The full source chemistry is evaluated before the requested atoms are returned.
These readers sort and deduplicate atom indices. All H must already be indexed
for AutoDock/Gasteiger-Marsili; no protonation, H placement, valence guessing,
neutralization or fragment capping runs. CIP can use declared virtual H evidence.
Structures resolve chemistry and spatial selectors; the visible structure is
never substituted for a native default. Mixed associated states require an
explicit state or compatible structure selection. Scientific exceptions remain
native, including provider absence and unsupported chemistry.

```python
import molsysmt as msm
import molsysviewer as msv
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDepictor

# Explicit example preparation happens before the view, never inside a reader.
molsys = Chem.AddHs(Chem.MolFromSmiles("CO"))
rdDepictor.Compute2DCoords(molsys)
with msv.new_view(molsys) as view:
    tools = view.addons.molsysmt.physchem
    labels = tools.get_autodock_atom_types(typing_scheme="autodock4")
    assert labels.tolist() == ["C", "OA", "H", "H", "H", "HD"]
    result = tools.get_partial_charges(
        method="gasteiger_marsili", selection=[1, 0, 1], return_report=True
    )
    assert result["report"]["atom_indices"].tolist() == [0, 1]
    assert result["report"]["evaluated_atom_indices"].tolist() == list(range(6))
    charges = msm.pyunitwizard.get_value(result["partial_charge"], to_unit="e")
    np.testing.assert_allclose(charges, [0.0319, -0.3996], atol=5e-5, rtol=0)
```

AutoDock's required scheme and its bounded chemical-environment profile are
parameter choices, not universal donor/acceptor definitions or proof of docking
readiness. Scheme labels remain separate from chemical element symbols. Optional
reports retain ordered rules, winners, full coverage and software attribution.

Gasteiger-Marsili uses the explicit native RDKit model and twelve iterations.
For force-field charges, pass `method='forcefield'` and an explicit `forcefield`
(and water model when required). Native OpenMM must match the unchanged source
atom inventory; unmatched chemistry, missing H and extra particles fail. This
reader does not parameterize arbitrary ligands or reuse stored partial charges.
Declare `expected_total_charge` when the complete formal-charge inventory is
absent. Native checks cover the full-system total, including when output is a
subset; they do not certify electrostatic accuracy. Units follow the active
PyUnitWizard charge standard; a policy without one raises `NoStandardsError`.

```python
import molsysviewer as msv
from rdkit import Chem
from rdkit.Chem import rdDepictor

molsys = Chem.AddHs(Chem.MolFromSmiles("N[C@@H](C)C(=O)O"))
rdDepictor.Compute2DCoords(molsys)
with msv.new_view(molsys) as view:
    result = view.addons.molsysmt.physchem.get_cip_stereochemistry(selection=[1])
    assert result["atom_stereochemistry"].tolist() == ["S"]
    assert result["bonded_atom_pairs"].shape == (0, 2)
    assert result["evidence"] == "declared_stereochemistry"
```

CIP assigns the complete graph before filtering. A returned bond requires both
selected endpoints. None means no assigned label; lowercase r/s and absolute
E/Z remain distinct from cis/trans relative to the reported reference atoms.
`from_coordinates=True` is keyword-only and requires exactly one explicit 3D
structure. It changes tags only on the native detached graph. The reader does
not reconstruct periodic molecules or infer a preferred structure.

On the receiving baseline f9ca3e1b0, CIP's nested plain-reference author list is
shared under [#503](https://github.com/uibcdf/molsysmt/issues/503): editing it can
pollute later bibliography and attribution. Treat that nested metadata as
read-only until the owner repair is received. Independent numeric arrays and
scalar metadata do not establish independence of every nested field. The addon
adds no consumer-specific deepcopy. AutoDock/partial-charge reports preserve
native provenance and optional credits without duplicate consumer attribution.

All three readers return scientific data, not scene objects or stored assignments.
They neither color atoms nor update the primary. They resolve current view.molsys
at each call, including pending managed edits, and do not synchronize pending
projection. `update_view` is not a reader parameter. See
{ref}`Tutorial_AutoDock_Typing`, {ref}`Tutorial_Get_CIP_stereochemistry` and
{ref}`Tutorial_Partial_Charge_Assignment` for native method profiles and limits.


## Recognizing waters and metal participants

`physchem.get_water_sites()` recognizes whole neutral O-H-H graphs with indexed
hydrogens. An oxygen-only water name or implicit H does not create a water site.
`get_metal_coordination_sites()` returns the native bounded metal/ligand roles.
These are chemical candidates, not measured interactions or assigned bonds.
Full-source recognition and match budgets precede output selection. Requested
structures resolve chemistry and selectors; the visible structure is not chosen
implicitly. An explicit completeness assumption is recorded without preparing
or changing the input.

```python
import molsysviewer as msv
from rdkit import Chem
from rdkit.Chem import rdDepictor

molsys = Chem.AddHs(Chem.MolFromSmiles("O.CO.[Zn+2]"))
rdDepictor.Compute2DCoords(molsys)
with msv.new_view(molsys) as view:
    sites = view.addons.molsysmt.physchem
    assert sites.get_water_sites()["water_atom_indices"].shape == (1, 3)
    assert sites.get_water_sites(selection=[0])["water_atom_indices"].shape == (0, 3)
    assert sites.get_metal_coordination_sites()["metal_atom_indices"].tolist() == [3]
```

Metal and ligand arrays retain separate roles, including permitted overlap.
They do not determine oxidation states, geometry or coordination numbers.
Water recognition does not certify a water force field or hydrogen-bond roles.
No H, coordinates, charges or aromatic assignments are generated. See
{ref}`Tutorial_Get_water_sites` and {ref}`Tutorial_Get_metal_coordination_sites`.

## Assessing and applying explicit chemical templates

`assess_chemical_template()` assesses the current primary against an explicit
caller-owned template, exhaustive atom correspondence and provenance.
`apply_chemical_template()` returns a new native system and report. It does not
replace `view.molsys`. Existing conflicting declarations are not overwritten.
Map columns address template then full source indices; explicit context mapping
and connectivity policies retain the native scoped contract. A checksum/identity
is a declaration, not authentication or proof that the template is correct.

```python
import molsysmt as msm
import molsysviewer as msv
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDepictor

template = Chem.AddHs(Chem.MolFromSmiles("CO"))
rdDepictor.Compute2DCoords(template)
provenance = dict(identity="methanol", version="1", source_uri="example:methanol",
                  checksum="caller-declared", hydrogen_policy="explicit_atoms")
with msv.new_view(template) as view:
    options = dict(template=template, template_provenance=provenance,
                   atom_correspondence=np.column_stack((np.arange(6), np.arange(6))))
    tools = view.addons.molsysmt.physchem
    assert tools.assess_chemical_template(**options)["status"] == "compatible"
    primary, scene = view.molsys, view.export_state()
    result = tools.apply_chemical_template(**options)
    assert result["report"]["status"] == "applied"
    assert result["molecular_system"] is not primary
    assert view.molsys is primary and view.export_state() == scene
```

The default requires the same stored graph. Explicit native completion may add
missing declared template edges to the returned copy; context transfer keeps its
native restrictions. Partial assessment does not certify unrelated atoms or
silently change global completeness. Source and reference inputs stay unchanged.
The returned copy retains native history, remapping and interaction invalidation;
its arrays can include all source structures and follow native copy costs.
The wrapper adds no second copy, molecular matching, protonation choice, H
placement, pose transfer or automatic adoption. See {ref}`Tutorial_Chemical_Templates`.

`normalize_aromatic_bond_orders()` is also an independent-result operation. It
normalizes only stored aromatic declarations to fractional order 1.5, preserving
native reports/history and invalidation on the returned copy. It does not perceive
aromaticity, choose Kekule structures or repair unknown chemistry. An unchanged
normalization retains native interaction coverage. No scene or source is adopted.
See {ref}`Tutorial_Normalize_Aromatic_Bond_Orders`.

## Constructing an independent peptide template

`get_peptide_chemical_template()` keeps every native scientific input explicit.
It can run in an empty, open view because it does not use the primary system.
The template has stored H counts and no geometry; it is not loaded automatically.

```python
import molsysviewer as msv

with msv.new_view() as view:
    factory = view.addons.molsysmt.physchem.get_peptide_chemical_template
    result = factory(["GLY", "GLY"], "ammonium", "carboxylate")
    assert result["template"].get_n_atoms() == 9
    assert result["report"]["n_stored_hydrogens"] == 8
    assert view.molsys is None
```

Sequence names, terminal states and disulfide group pairs are declarations.
This factory does not infer pH, L stereochemistry, H positions, atom matches or
force-field parameters. Its provenance/history keeps the synthetic operation
indices; later extraction or edits do not turn them into current source indices.
All wrappers retain closed-view lifetime checks and native `skip_digestion`.
Independent-result operations/factories do not accept `update_view`.

## Inspecting preparation needs without editing

The first `build` tools separate diagnostics and candidates from molecular repair.
`get_residue_chemical_coverage()` selects source groups, including whole groups
containing atoms selected by an expression. Unsupported identities remain
unassessed. `get_covalent_bond_candidates()` and `get_peptide_bond_candidates()`
select source atoms and retain a candidate only when both endpoints are selected.
Group audits and full-source competition follow the chosen native policy.

```python
import molsysviewer as msv

with msv.demo["181L"] as view:
    tools = view.addons.molsysmt.build
    coverage = tools.get_residue_chemical_coverage(structure_indices=[0])
    covalent = tools.get_covalent_bond_candidates(structure_indices=[0])
    peptide = tools.get_peptide_bond_candidates(structure_indices=[0], pbc=False)
    assert coverage["groups"]
    assert covalent["bonded_atom_pairs"].shape[1] == 2
    assert peptide["bonded_atom_pairs"].shape[1] == 2
```

Select one structure when the native diagnostic requires it. Native defaults
are preserved; the addon never substitutes the visible structure. The legacy
pentalanine demo has unknown atom-chain membership and returns no peptide
candidates under the current policy; no chain is inferred to make it pass.
The PDB demo above supplies declared chain membership. Candidate distance units,
cutoffs and PBC remain explicit. A candidate does not certify valence, protonation,
a declared bond or chemical validity. No missing atom/bond is assigned and no
result is colored or adopted. See {ref}`Tutorial_Residue_Chemical_Coverage`,
{ref}`Tutorial_Covalent_Bond_Candidates` and {ref}`Tutorial_Peptide_Bond_Candidates`.


### Auditing missing content and preparation state

Eight further native readers are available under `view.addons.molsysmt.build`:

| Reader | Meaning and native scope |
| --- | --- |
| `get_missing_heavy_atoms` | Exact supported amino-acid templates; numeric selection addresses groups. Unsupported chemistry is not certified. |
| `get_missing_terminal_cappings` | Missing terminal OXT within the selected group scope. A partial selection can define a different apparent terminus. |
| `get_non_standard_residues` | Native standard-name suggestions; no replacement, graph validation or preparation. Unknown groups may be absent from the report. |
| `get_missing_residues` | Comparison against an explicit chain-ID-to-name-list reference; returned chain indices/insertion positions belong to the selected subsystem. |
| `get_missing_bonds` | Heuristic missing source-atom pairs from templates/geometry, using singular `structure_index` where applicable. |
| `get_disulfide_bonds` | Distance-based sulfur candidate pairs from one structure; these may already be declared bonds. |
| `has_hydrogens` | Presence of any selected indexed hydrogen, not hydrogen completeness or correct protonation. |
| `is_solvated` | Native water-count/box-density predicate per selected structure; bool for one structure or a Boolean vector for multiple/empty selections. Not a preparation or solvent-completeness check. |

```python
with msv.demo["181L"] as view:
    tools = view.addons.molsysmt.build
    assert tools.get_missing_heavy_atoms() == {}
    assert tools.get_missing_terminal_cappings() == {161: ["OXT"]}
    assert not tools.has_hydrogens()
    assert not tools.is_solvated()
    chain_id = view.addons.molsysmt.get(element="chain", chain_id=True)[0]
    names = view.addons.molsysmt.get(
        element="group", selection="chain_index==0", group_name=True,
    )
    reference = {chain_id: names + ["ASN", "LEU"]}
    assert tools.get_missing_residues(sequence=reference) == {
        (0, len(names)): ["ASN", "LEU"],
    }
    candidates = tools.get_missing_bonds(structure_index=0, pbc=False)
    sulfur_candidates = tools.get_disulfide_bonds(structure_index=0, pbc=False)
```

The bound input is the resident MolSys, not its original PDB/BCIF source file.
Without an explicit usable sequence, the native missing-residue reader warns and
returns `{}`. Do not interpret that result as evidence of a complete sequence.
Selection syntax, engine choices, cutoffs, units, PBC and provider rejection stay
native. Numeric group selection in the first three readers differs from atom
selection in the two bond readers. No visible-structure substitution occurs.
Optional PDBFixer/pytraj routes keep their own dependencies and limitations;
source availability is not blanket backend qualification.

All eight use the serialized primary reader, including completed pending
scientific edits. Returned reports stay separate from the source and scene;
there is no `update_view`, repair, bond assignment or automatic attachment.
Each method has `skip_digestion`. Where the native function has no such
parameter, a keyword-only addon control affects only addon validation and is
never passed to the native function.

`is_solvated(structure_indices='all')` preserves source structure order and
repetitions. Selecting one structure returns a Python bool; multiple or empty
selections return a Boolean NumPy vector. There is no implicit first/any/all
aggregation or visible-structure substitution. Empty output is not evidence of
solvation; check its size before a deliberate reduction. The criterion uses a
global density above 15 waters/nm³ with a machine-roundoff equality tolerance,
not solvent coverage, containment or equilibration. Missing waters/box yield
false per structure; unknown water inventory and unusable volumes are explicit
diagnostics. The source and scene remain unchanged. See the
{ref}`solvation-predicate tutorial <Tutorial_Is_solvated>`.


## Preparing independent molecular systems

Three `build` methods return a new molecular system from the current primary:
`infer_covalent_bonds`, `assign_autodock_atom_types` and
`assign_partial_charges`. Their native methods, chemical-state choices,
structure scope and optional reports remain explicit. The source system and
scene stay unchanged, including regions, saved analyses and pending edits.
These are separate prepared outputs, distinct from the diagnostic/candidate
readers above and from `physchem` calculations that return unattached values.

For typing and charges, prepare the input chemistry explicitly before loading
it. This example constructs a small complete graph with indexed hydrogens;
the addon never performs this preparation for you:

```python
import molsysviewer as msv
import molsysmt as msm
import numpy as np
from rdkit import Chem

molecule = Chem.AddHs(Chem.MolFromSmiles("CO"))
conformer = Chem.Conformer(molecule.GetNumAtoms())
conformer.SetPositions(np.asarray([
    (0.0, 0.0, 0.0), (1.4, 0.0, 0.0),
    (-0.5, 0.8, 0.0), (-0.5, -0.8, 0.0),
    (0.0, 0.0, 1.0), (1.8, 0.6, 0.0),
], dtype=float))
molecule.AddConformer(conformer)
with msv.new_view(msm.convert(molecule)) as view:
    source = view.molsys
    typed = view.addons.molsysmt.build.assign_autodock_atom_types(
        typing_scheme="autodock4", return_report=True,
    )
    charged = view.addons.molsysmt.build.assign_partial_charges(
        method="gasteiger_marsili", expected_total_charge=0,
        return_report=True,
    )
    assert typed["molecular_system"] is not source
    assert charged["molecular_system"] is not source
    assert view.molsys is source
    assert source.molecular_mechanics.partial_charge is None
    assert source.molecular_mechanics.atom_ff_type is None
```

Each call above starts from the current primary. The charge result does not
inherit the independently returned typing result. To chain preparation, pass
the returned system to public MolSysMT, or explicitly load it before the next
addon call. `view.load(result, mode="replace")` uses the ordinary Viewer
replacement contract; the addon does not adopt results automatically. There
is no `in_place` or `update_view` argument on these three native-independent
routes. Methods require an open loaded owner, resolve replacement at call time,
and read completed pending molecular edits without synchronizing the scene.

Covalent inference is also an explicit native preparation policy. It returns a
new system with eligible bonds and preparation evidence, retaining source atoms,
structures and declared edges. Select a source structure explicitly when
geometry is ambiguous; the visible canvas structure is never substituted:

```python
import molsysviewer as msv
import molsysmt as msm
import numpy as np

builder = msm.MolSysBuilder()
names = ["N", "CA", "C", "O", "CB", "H", "HN1"]
elements = ["N", "C", "C", "O", "C", "H", "H"]
atoms = [builder.add_atom(atom_name=n, atom_type=t)
         for n, t in zip(names, elements)]
builder.add_group(atoms, group_name="ALA", group_id="100")
builder.set_coordinates(msm.pyunitwizard.quantity(np.zeros((1, 7, 3)), "nm"))
with msv.new_view(builder.build()) as view:
    source = view.molsys
    result = view.addons.molsysmt.build.infer_covalent_bonds(
        structure_indices=0, method="supported_group_templates", return_report=True,
    )
    assert result["report"]["n_added_bonds"] == 5
    assert view.molsys is source
    assert len(source.chemical_states.get_bonds()) == 0
```

This reference-name example does not model a physical pose. Native inference
combines supported exact heavy-group templates, observed-H parent evidence and
bounded same-chain peptide candidates. It is not universal graph perception,
protonation, bond-order assignment or a chemical-validity certificate. Added
bonds invalidate named interactions on the returned system; the view's saved
analyses remain unchanged. No graph change retains native analysis snapshots.

AutoDock typing requires the named scheme and a complete nonempty single
chemical state. Charge assignment requires an explicit model; the force-field
route also requires a named force field and a usable template match. RDKit or
OpenMM availability follows that native choice. Atom types, charges and their
provenance are attached to the output's experimental MolecularMechanics; they
do not establish complete force-field parameterization. Stored charges retain
native elementary-charge units even under another presentation policy. Named
analyses preserve their snapshots; recalculation of mechanics-dependent
analyses remains explicit. Full native copies can materialize source coordinates;
these calls offer no out-of-core trajectory guarantee.

:::{warning}
MolecularMechanics remains experimental and is excluded from H5MSM 0.5. Saving
these assigned types/charges to that format rejects rather than silently
losing the mechanical data. A type/charge assignment alone is not complete
force-field parameterization.
:::

Native references: {func}`molsysmt.build.infer_covalent_bonds`,
{func}`molsysmt.build.assign_autodock_atom_types` and
{func}`molsysmt.build.assign_partial_charges`.

## Projecting atom names for export

`view.addons.molsysmt.build.project_atom_names` applies the native naming
constraints for `file:pdbqt` or `string:pdbqt_text`. It returns a separate
MolSys, optionally with a `molsysmt.atom_map@1` report. The required `target_form`
selects the label policy; it does not write a file or choose the returned form.
The current primary and scene remain unchanged.

```python
import molsysviewer as msv
import numpy as np

with msv.demo["pentalanine"] as view:
    source = view.molsys
    result = view.addons.molsysmt.build.project_atom_names(
        target_form="file:pdbqt", selection="all", return_report=True,
    )
    output, report = result["molecular_system"], result["report"]
    assert output is not source and view.molsys is source
    assert output.get_n_atoms() == source.get_n_atoms()
    assert output.structures.n_structures == source.structures.n_structures
    np.testing.assert_array_equal(
        report["source_to_output_atom_indices"], np.arange(source.get_n_atoms()),
    )
    composed = view.addons.molsysmt.basic.compose_atom_maps([report])
    assert composed["source_to_output_atom_indices"].shape == (source.get_n_atoms(),)
```

The experimental native preserve-or-base36 policy retains valid printable ASCII
names of at most four characters, including existing duplicates. Invalid
selected names get a lexical prefix and collision-free counter within the
native group or conservative system-wide scope. A lexical prefix is not an
atom-type or element assignment. Unselected invalid names remain invalid; a
later writer can still reject the system. Namespace exhaustion raises rather
than returning a partial rename. See the [native projection guide](build/project_atom_names.md)
for explicit invalid-name examples and mapping details.

Selections are sorted/deduplicated, but output atoms and structures keep their
full source axes and IDs. Original/projected names and identity index maps are
returned explicitly; the addon does not match atoms back by their names.
Mutable native domains are independent. Geometry uses protected shared blocks
until a public native edit detaches them, so this label-only projection does
not require a trajectory-sized coordinate copy.

The method requires a loaded open view and reads completed pending edits
without synchronizing or adopting the result. There is no `in_place` or
`update_view` control. This projection does not infer chemistry, choose a torsion
tree, recalculate charges or recertify template-sensitive assignments. Existing
provenance is retained and can fail its native export checks after names change;
project before such assignment when its naming contract requires that order.
Actual export and result adoption remain separate explicit operations.

Native reference: {func}`molsysmt.build.project_atom_names`.

## Constructing independent molecular representations

### Expanding a biological assembly

`view.addons.molsysmt.build.make_bioassembly` expands declared chains using
stored or explicit assembly operators. It returns an independent molecular
system. For example, use the stored assembly in bundled Barnase–Barstar data:

```python
import molsysviewer as msv
import molsysmt as msm

molsys = msm.convert(msm.systems["Barnase-Barstar"]["1brs.bcif.gz"])
with msv.new_view(molsys) as view:
    source = view.molsys
    assembly = view.addons.molsysmt.build.make_bioassembly(bioassembly="1")
    assert assembly is not source and view.molsys is source
    assert assembly.structures.n_structures == 1
    chain_ids = msm.get(assembly, element="chain", chain_id=True)
    assert len(chain_ids) == len(set(chain_ids))
```

The default `structure_indices=0` selects the first stored structure, independent
of the visible canvas frame. Explicit lists retain order and repetitions, such
as `[2, 0, 2]` for an ensemble with at least three structures. Times and structure
IDs follow that order. `bioassembly=None` selects the first stored assembly;
a missing assembly rejects rather than inferring one. Explicit operators require
proper rotations and compatible declared chain memberships. Different chain
sets across operators currently reject. Native collision handling generates
unique chain IDs while retaining author chain names; `to_form` controls final
conversion.

This operation requires valid source chain membership. It does not infer chains,
repair periodic images or certify that a constructed assembly is a physically
correct biological model. It returns no atom-map report or Viewer source-region
mapping. The output is resident; this is not an out-of-core ensemble operation.
See {ref}`Make bioassembly <Tutorial_Make_bioassembly>` and
{func}`molsysmt.build.make_bioassembly` for native operator and form contracts.

### Merging explicitly typed nonpolar hydrogens

`view.addons.molsysmt.build.merge_nonpolar_hydrogens` requires an explicit
`typing_scheme="autodock4"`. After preparation, it merges atoms labelled `H`
into their retained covalent parents and adds their partial charges. Polar
hydrogens labelled `HD` remain indexed. Atom names do not determine this choice.
Prepare the complete graph, hydrogen inventory, atom types and finite partial
charges explicitly before loading the view:

```python
import molsysviewer as msv
import molsysmt as msm

molsys = msm.convert(msm.systems["caffeine"]["caffeine.sdf"], to_form="rdkit.Mol")
molsys = msm.build.assign_autodock_atom_types(molsys, typing_scheme="autodock4")
molsys = msm.build.assign_partial_charges(molsys, method="gasteiger_marsili")
with msv.new_view(molsys) as view:
    source = view.molsys
    result = view.addons.molsysmt.build.merge_nonpolar_hydrogens(
        typing_scheme="autodock4", return_report=True,
    )
    projected, report = result["molecular_system"], result["report"]
    assert projected.get_n_atoms() == 14 and source.get_n_atoms() == 24
    assert report["schema"] == "molsysmt.atom_projection@1"
    assert report["charge_unit"] == "elementary_charge"
    assert abs(report["selected_total_charge"] - report["output_total_charge"]) <= (
        report["charge_conservation_tolerance"]
    )
    lineage = view.addons.molsysmt.basic.compose_atom_maps([report])
    assert len(lineage["source_to_representative_atom_indices"]) == 24
    assert view.molsys is source
```

This example uses optional RDKit for explicit typing/charge preparation. The
addon adds no hidden preparation, protonation or charge calculation. Native
single-state chemistry and complete hydrogen-inventory requirements still apply.
The default structures are `"all"`; explicit structure lists retain order and
repetitions. Atom selections are normalized by the native projection; a merged
hydrogen needs its retained parent in the selection.

With `return_report=False`, the result is the independent MolSys itself. The
optional report keeps direct output/source identity, omitted atoms, merged
hydrogen–parent pairs and charge transfers separate. Its charge fields declare
canonical elementary-charge units even under another presentation policy.
`basic.compose_atom_maps` can compose this lineage; a representative parent
index is not the removed hydrogen's identity or coordinate. Retained coordinates
belong to retained atoms. Native typing/charge assignment records become derived
and preserve their source provenance. Native scientific attribution remains
available through the report.

After a merge, named interaction analyses on the returned system are cleared;
the source analyses, source chemistry and scene remain unchanged. This is a
representation projection, not a general united-atom force field or a new
protonation state. Experimental MolecularMechanics types/charges are not stored
by H5MSM 0.5; that writer rejects unsupported mechanical data explicitly. See the
[native projection guide](build/merge_nonpolar_hydrogens.md) and
{func}`molsysmt.build.merge_nonpolar_hydrogens` for prerequisites and export maps.

Both construction methods require an open loaded view, use its current primary
at call time and read completed pending edits without scene synchronization.
They preserve native `skip_digestion` and validation semantics. Neither offers
`in_place` or `update_view`; deliberately chain the independent result or load it
with the ordinary Viewer replacement API when that is your intention.

## Expanding independent atom inventories

### Attaching declared terminal atoms

`view.addons.molsysmt.build.add_terminal_atoms` attaches each declared atom to
one existing parent. You supply both the atom records and finite length
coordinates covering every source structure. The method always returns a
dictionary containing `molecular_system` and `report`; it does not place atoms
for you or replace `view.molsys`:

```python
import molsysviewer as msv
import molsysmt as msm
import numpy as np

builder = msm.MolSysBuilder()
builder.add_atom(atom_type="C", atom_name="C", atom_id="original")
builder.set_coordinates(msm.pyunitwizard.quantity([[[0., 0., 0.]]], "nm"))
with msv.new_view(builder.build()) as view:
    source = view.molsys
    result = view.addons.molsysmt.build.add_terminal_atoms(
        new_atoms=[{"parent_atom_index": 0, "atom_type": "H", "atom_id": 40}],
        coordinates=msm.pyunitwizard.quantity([[[0., 0., 1.09]]], "angstrom"),
    )
    output, report = result["molecular_system"], result["report"]
    assert source.get_n_atoms() == 1 and output.get_n_atoms() == 2
    assert output.topology.atoms.atom_id.tolist() == ["original", "40"]
    assert report["schema"] == "molsysmt.terminal_attachment@1"
    assert report["coordinate_unit"] == "nm"
    assert report["coordinate_evidence"] == "supplied_coordinates"
    np.testing.assert_array_equal(report["atom_correspondence"], [[0, 0]])
    np.testing.assert_array_equal(report["parent_atom_pairs"], [[0, 1]])
    assert view.molsys is source
```

This small example declares a bond and a position; it is not a complete
molecular preparation. Existing atoms keep their indices, IDs and coordinates.
New atoms inherit their parent's membership; optional records declare names,
IDs, isotopes, bond orders and chemical attributes. There is no automatic
hydrogen-inventory correction, protonation, charge or force-field assignment.
The native operation requires exactly one chemical state. Coordinates have
shape `(n_structures, n_new_atoms, 3)`, independent of the visible frame.

The report records the original source axes, old/new correspondence, parent
pairs, generated string IDs and discarded attributes. It declares canonical nm
units and supplied-coordinate evidence; it does not embed coordinate arrays.
An independent copy enters the output's ChemicalStates preparation history,
which H5MSM preserves. Historical indices describe the operation's original
domain, not a live map after later extraction or reordering. Editing the returned
report does not rewrite that history or authenticate its source.

Nonempty attachment invalidates evaluated coverage on output analyses while
preserving their definitions and source mappings; added atoms have source index
`-1`. The original view's analyses stay unchanged. `attribute_policy="intersection"`
reports unsupported structural/mechanical attributes that are dropped instead
of fabricating values for new atoms. `"strict"` rejects such loss. An empty
addition returns an independent unchanged system, retains attributes and
analysis coverage, and records the examined scope in preparation history.
See {ref}`Attaching terminal atoms <Tutorial_Add_Terminal_Atoms>` and
{func}`molsysmt.build.add_terminal_atoms` for record fields and native limits.

### Repairing supported missing heavy atoms

`view.addons.molsysmt.build.add_missing_heavy_atoms` returns a new molecular
system. Its native engine estimates supported missing non-H positions from
bounded local templates. For example, explicitly remove one serine oxygen from
a generated peptide before loading it, then repair that selected group:

```python
import molsysviewer as msv
import molsysmt as msm

molsys = msm.build.build_peptide("SerAla", engine="MolSysMT")
molsys = msm.extract(molsys, selection="atom_type!='H' and atom_name!='OG'")
with msv.new_view(molsys) as view:
    source = view.molsys
    output = view.addons.molsysmt.build.add_missing_heavy_atoms(
        selection="group_name=='SER'", engine="MolSysMT",
        attribute_policy="intersection",
    )
    assert output.get_n_atoms() == source.get_n_atoms() + 1
    assert msm.select(output, selection="atom_name=='OG'")
    assert not msm.select(source, selection="atom_name=='OG'")
    assert view.molsys is source
```

The example can emit the native attribute-drop warning for the peptide's old
atom parameters. The tool assigns no parameters to newly added atoms. The native engine
preserves observed coordinates, old atom IDs, time, box and declared state
metadata, but sorting by group can change indices. Use the output's native
identity/source maps when relating it to earlier results; do not assume all
old indices remain fixed. New chemical fields remain unknown and connectivity
completeness becomes partial. Output analyses keep remapped provenance but
lose occurrences and evaluated coverage after atom expansion; source analyses
are preserved. No-change results retain their original analysis snapshots.

The native engine supports bounded standard-residue placement and curated
MSE/SEP/TPO cases. An ambiguous or unsupported gap can remain unchanged with
`UnassessedResidueWarning`; absence of an exception does not mean every gap was
repaired. Observed-anchor and bond-geometry checks do not certify clashes,
stereochemistry, rotamers or an energy minimum. Repair examines all source
structures; there is no implicit visible-frame selection. Full native copies
can materialize trajectory coordinates.

`engine="PDBFixer"` explicitly selects the optional external provider with its
own chemistry, conversion and preservation limits. It is not an automatic
fallback and currently supports only intersection attribute policy here. The
native engine's multi-state and strict-loss rejections remain explicit. There
is no `return_report`, `in_place` or `update_view` argument on this method.
See {ref}`Adding heavy atoms <Tutorial_Add_missing_heavy_atoms>` and
{func}`molsysmt.build.add_missing_heavy_atoms` for native scope and alternatives.

Both expansion tools read the current primary through the serialized reader,
including completed pending edits, and never synchronize or adopt the result.
Cached methods follow ordinary replacement/close behavior. Use the returned
system in later native calculations or deliberately load it with the ordinary
Viewer replacement API; molecular construction and scene adoption are separate.

## Preparing hydrogens and termini independently

### Materializing a declared hydrogen inventory

`view.addons.molsysmt.build.add_missing_hydrogens` retains two different native
workflows. Fixed-state mode adds missing H to an isolated, prepared component;
it does not select a protonation state. Supply explicit chemistry and geometry
before loading the view, then request the mode and backend explicitly:

```python
import molsysviewer as msv
import molsysmt as msm
from rdkit import Chem

molsys = Chem.MolFromSmiles("CO")
conformer = Chem.Conformer(2)
conformer.SetAtomPosition(0, (0., 0., 0.))
conformer.SetAtomPosition(1, (1.4, 0., 0.))  # RDKit positions use angstroms.
conformer.Set3D(True)
molsys.AddConformer(conformer)
with msv.new_view(msm.convert(molsys)) as view:
    source = view.molsys
    result = view.addons.molsysmt.build.add_missing_hydrogens(
        pH=None, engine="RDKit", mode="fixed_chemical_state", return_report=True,
    )
    output, report = result["molecular_system"], result["report"]
    assert output.get_n_atoms() == 6 and source.get_n_atoms() == 2
    assert report["n_added_hydrogens"] == 4
    assert report["coordinate_unit"] == "nm"
    assert report["coordinate_evidence"] == "generated_local_geometry"
    assert [item["report"]["schema"] for item in
            output.chemical_states.get_preparation_history()] == [
        "molsysmt.terminal_attachment@1", "molsysmt.hydrogen_addition@1",
    ]
    assert view.molsys is source
```

The example's SMILES declares connectivity, formal charges and hydrogen
inventory; the supplied pose is explicit. The addon performs no additional
curation. Fixed-state mode requires `pH=None`, explicit RDKit, one chemical
state, one source structure and one supported prepared component. Existing
coordinates and atom indices remain; appended H carry parent maps, typed
inventory and native generation/attachment evidence. No heavy-atom conformer,
minimization or periodic reconstruction is introduced. Unsupported chemistry,
unresolved inventory and split periodic molecules retain native rejection.

`chemical_state`, `structure_indices`, `return_report` and `attribute_policy`
keep their native fixed-state contracts. A structure selector does not extract
a multi-structure source automatically: extract the required single structure
and chemical state first. This does not select the visible canvas structure.
The default `return_report=False` returns the independent MolSys; both forms
retain the native preparation history. Reports declare canonical nm evidence
and original operation axes, not live maps after later edits. H5MSM preserves
that historical evidence. Expanded output analyses become unevaluated; a
no-addition result retains its analysis coverage. The original view stays intact.

### Using residue and pH rules

The default `mode="pH", pH=7.4, engine="OpenMM"` follows native residue-based
preparation. Explicit `"PDBFixer"` and `"MolSysMT"` retain their own native
routes; there is no backend fallback. These approximate rules use standard
pKa thresholds and do not calculate environment-dependent pKa values. Existing
H are not removed just because a different pH would exclude them. Check the
intended chemistry before interpreting the result as prepared for simulation.

The fixed-state-only options above reject in legacy pH mode. Optional backend
conversion, structure and metadata preservation limits remain engine-specific;
the receiving examples cover single-structure legacy input. They do not qualify
trajectory-wide legacy hydrogenation. OpenMM placement is not promised to
reproduce an identical new-H pose across independent calls. See
{func}`molsysmt.build.add_missing_hydrogens`,
{ref}`Adding hydrogens <Tutorial_Add_missing_hydrogens>` and
{ref}`Fixed-state hydrogens <Tutorial_Fixed_State_Hydrogens>` for native details.

### Completing or capping peptide termini

`view.addons.molsysmt.build.add_missing_terminal_cappings` returns a separate
molecular system with native terminal preparation. With no explicit caps it
completes supported terminal atoms; with ACE/NME it inserts the requested groups.
A single cap can also complete the opposite free terminus. Each call starts
from the same current primary unless you deliberately replace it:

```python
import molsysviewer as msv
import molsysmt as msm

molsys = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
with msv.new_view(molsys) as view:
    source = view.molsys
    one_cap = view.addons.molsysmt.build.add_missing_terminal_cappings(
        N_terminal="ACE", C_terminal=None, pH=7.4, engine="MolSysMT",
    )
    both_caps = view.addons.molsysmt.build.add_missing_terminal_cappings(
        N_terminal="ACE", C_terminal="NME", pH=7.4, engine="MolSysMT",
    )
    assert source.get_n_atoms() == 40
    assert one_cap.get_n_atoms() == 47  # Six ACE atoms and the free C-terminal OXT.
    assert both_caps.get_n_atoms() == 52
    assert msm.get(both_caps, element="group", group_name=True) == [
        "ACE", "ALA", "VAL", "PRO", "NME",
    ]
    assert view.molsys is source
```

These generated peptide geometries are initial models, not refined structures.
The native engine retains bounded heavy-atom preflight and unassessed warnings.
It preserves observed coordinates and old IDs while insertion can reorder atom
indices. New chemical fields remain unknown; terminal geometry does not assign
a complete protonation or force-field model. Unsupported structural/mechanical
attributes are dropped with native diagnostics. Expanded output analyses retain
remapped provenance but lose occurrences and evaluated coverage. All source
structures are processed by the received native capping route.

`selection`, `syntax`, `pH` and `keep_ids` follow native engine-specific behavior.
PDBFixer is optional and explicit; `keep_ids=True` remains unsupported by that
route. No report, strict attribute policy, `in_place` or `update_view` control
is invented. See {func}`molsysmt.build.add_missing_terminal_cappings` and
{ref}`Preparing termini <Tutorial_Add_missing_terminal_cappings>`.

Both preparation methods use the serialized current primary, including
completed pending edits, without synchronizing or adopting their output.
Cached methods follow replacement and reject closed/empty owners. Explicitly
chain returned systems or use ordinary Viewer replacement when you intend to
change the scene; preparation and scene adoption remain separate operations.

## Staging edits and filtering overlapping molecules

### Working on a separate builder

`view.addons.molsysmt.build.editable()` initializes a native `MolSysBuilder`
from the current system. You can stage supported edits without changing the
molecule or scene in the view, then build a separate molecular system:

```python
import molsysviewer as msv

with msv.demo["dialanine"] as view:
    source = view.molsys
    builder = view.addons.molsysmt.build.editable()
    before = builder.n_bonds
    builder.remove_bonds([0])
    output = builder.build()
    assert output.chemical_states.get(n_bonds=True) == before - 1
    assert source.chemical_states.get(n_bonds=True) == before
    assert view.molsys is source
```

Deleting a bond here illustrates ownership; it does not prepare a chemically
valid peptide. Native builder validation and chemical-state choices apply to
each edit. For example, adding atoms to a builder carrying atom-dependent
coordinates is rejected; existing structural arrays are not silently expanded.

Conversion copies the native topology, chemical states, structures and declared
structure/state associations. A builder does not store molecular mechanics or
named interaction analyses; building it does not restore those domains from the
source. Inspect the output's actual domain availability before downstream work.
Full native copying can materialize structural data and is not an out-of-core
trajectory interface.

The builder and its outputs remain usable after the view is replaced or closed.
A new call through the cached addon method reads the replacement system, and
calls through a closed or empty view reject. The addon requires a loaded system;
use ordinary `msm.build.editable()` to start an empty builder. Its native
`skip_digestion` flag is retained. Builder edits are not managed scene edits,
and `sync_view()` does not adopt a builder's output. Deliberately load the
returned system if you want to replace the scene. See
{func}`molsysmt.build.editable` and {ref}`Editing systems <Tutorial_Editable>`.

### Removing candidate molecules near reference atoms

`view.addons.molsysmt.build.remove_overlapping_molecules()` finds candidate
atoms closer than the requested distance to reference atoms and removes their
entire declared molecules from the returned system. Choose the two sides
explicitly when filtering solvent near a protein:

```python
import molsysviewer as msv
import molsysmt as msm

with msv.demo["181L"] as view:
    source = view.molsys
    before = msm.get(source, n_waters=True)
    output = view.addons.molsysmt.build.remove_overlapping_molecules(
        selection="molecule_type=='water'",
        selection_2="molecule_type=='protein'",
        structure_index=0, threshold="3 angstroms", pbc=False,
    )
    assert msm.get(output, n_waters=True) < before
    assert msm.get(source, n_waters=True) == before
    assert view.molsys is source
```

`selection` supplies removable candidate atoms; `selection_2` supplies reference
atoms. A single contacting candidate atom removes its whole molecule. With
`selection_2=None`, the reference is the **atom complement** of `selection`.
If you select only part of a candidate molecule, its unselected atoms can be
reference contacts too: there is no automatic exclusion of contacts within the
same molecule. Select complete candidate molecules or supply an explicit
reference selection when that is your intent.

The decision uses one explicit `structure_index` (default 0), independently of
the structure visible in the canvas. Removal and native remapping then apply
to all retained structures. Coordinates, box and time follow native removal;
saved analyses follow its subset maps and coverage contract. `syntax` retains
native MolSysMT/MDTraj selection behavior. `threshold` is a length quantity;
`pbc=True` uses native periodic contacts when a box is present and falls back
to nonperiodic contacts without one. No fitting, wrapping, chemistry repair,
trajectory-wide contact decision or physical relaxation is added.

When molecules are removed, the output is separate and the source is preserved.
When nothing is removed, native MolSysMT returns the **original system**:
`output is view.molsys`. Copy it explicitly before independent raw edits if
needed. The addon does not disguise that alias or automatically observe raw
changes. Its keyword-only `skip_digestion` controls addon validation only;
it is not forwarded and never bypasses native validation. Neither tool adds
`in_place`, `update_view` or automatic scene adoption. Completed pending edits
are read without synchronizing the scene. See
{func}`molsysmt.build.remove_overlapping_molecules` and
{ref}`Filtering overlaps <Tutorial_Remove_overlapping_molecules>`.

## Adding missing covalent bonds to the loaded system

`view.addons.molsysmt.build.add_missing_bonds()` keeps the native default
`in_place=True`: it modifies `view.molsys`, returns `None` and reconciles the
scene. `in_place=False` returns an independent system without adopting it,
regardless of `update_view`. This differs from the independent
`infer_covalent_bonds` route.

```python
import molsysviewer as msv
import molsysmt as msm

molsys = msm.build.build_peptide("AlaAla", engine="MolSysMT")
molsys.chemical_states.remove_bonds("all")  # Explicit fixture preparation.
with msv.new_view(molsys) as view:
    tools = view.addons.molsysmt
    tools.build.add_missing_bonds(update_view=False)
    assert msm.get(view.molsys, n_bonds=True) > 0
    assert tools.get_sync_status()["state"] == "pending"
    tools.sync_view()  # Project the completed graph; do not repeat the calculation.
```

Selection addresses source atom indices; both endpoints must belong. The
single native `structure_index=0` determines geometric candidates, independently
of the visible frame. Explicit `max_bond_length` quantities, template/chain
rules, periodic criteria and selection syntax remain native. The operation
updates the reference chemical state and rebuilds its components, retaining
atom/structure/state indices, stable topology, other states and coordinate
storage. It does not assign bond orders/types, prepare hydrogens or certify
complete chemistry. Inspect native prerequisites and heuristics in
{func}`molsysmt.build.add_missing_bonds` and
{ref}`Tutorial_Add_missing_bonds`.

A changed graph invalidates all named analysis coverage, including evaluated
structures with no observations; old snapshots remain separate. Detectors are
not rerun. Empty candidate results preserve coverage, history and managed
revision. Each attempt still has an audit identifier. A no-op with
`update_view=True` can synchronize earlier pending work; `False` defers only
scene projection. Compatible pending removals/coordinate edits compose through
the existing identity maps. Scene actions that depend on stale indices reject
while work is pending.

Scientific rejection retains the prior synchronized or pending state when the
native atomic publication contract certifies preservation. A scene failure
after successful science instead exposes `SystemEditSyncError` with
`science_completed=True` and `scientific_result=None`: retry `sync_view()`, not
bond reconstruction. Potentially partial writes require explicit recovery.
Cached methods use the current loaded owner; empty and closed views reject.
Native `skip_digestion` is forwarded; it never disables integration safeguards.
This is bounded source receiving, not a new published-package guarantee.

## Resolving alternate crystallographic sites

`view.addons.molsysmt.build.solve_atoms_with_alternate_location(...)` runs the
native in-place operation on the current loaded system and returns `None`.
It preserves source atom/structure indices and chemistry while applying the
selected stored sites. It has no `in_place` switch or independent result.

```python
import molsysviewer as msv
import molsysmt as msm

molsys = msm.convert(
    msm.systems["Barnase-Barstar"]["1brs.bcif.gz"], to_form="molsysmt.MolSys"
)
with msv.new_view(molsys) as view:
    tools = view.addons.molsysmt
    tools.build.solve_atoms_with_alternate_location(
        selection=[2686, 2687], location_id="B", update_view=False
    )
    assert msm.get(view.molsys, selection=[2686, 2687], atom_id=True) == ["2688", "2690"]
    tools.sync_view()
```

`structure_indices` retains native order, including nonconsecutive selections;
its default is all structures, independently of the visible structure. A list
of `location_id` values follows the atom order returned by the native selection,
including an explicit non-sorted list. Repeated atoms must request the same site.
Atom-ID labels are topology-wide: selected structures must agree on each updated
label. Conflicting labels are rejected before any publication. These labels do
not establish or change retained scene/source correspondence.

Primary coordinates, occupancy and B factors follow the chosen site. Missing
optional observations become unknown instead of retaining measurements from a
previous site; occupancy is unit-free and B factors carry squared-length units.
The occupancy criterion chooses the largest known value; its documented half
occupancy tie rule favors A only when A shares that maximum. Unknown occupancies
are ignored by this criterion; choosing an explicit label can retain unknown
occupancy. Alternate-site records remain available without renormalization.

All selected sites and admitted writers are validated before the first native
write. A rejected request preserves source observations and analysis identities.
Named analysis coverage follows successful coordinate publication for affected
structures, including evaluated-empty analyses; no detector is rerun. A call
without selected sites preserves managed revision and scene history. Repeating
a real native write can invalidate coverage even when coordinates compare equal.
No conformer generation, occupancy fitting or molecular preparation is added.

`update_view=False` defers projection only. Compatible pending edits compose
through the existing maps. A subsequent no-op with `update_view=True` can finish
earlier pending projection. After successful science, a scene error carries
`science_completed=True` and `scientific_result=None`; retry `sync_view()`.
Unexpected failures within mutable adapters retain their partial-write limit;
if native geometry was published, status becomes `uncertain` and requires
explicit replacement without scientific replay. This is not a transaction across
arbitrary backends or files. `skip_digestion` mirrors and forwards the native
flag; scientific site validation remains active even when digestion is skipped.

The owner corrections for [#569](https://github.com/uibcdf/molsysmt/issues/569),
[#570](https://github.com/uibcdf/molsysmt/issues/570) and
[#571](https://github.com/uibcdf/molsysmt/issues/571) are received from published
source `532d03622`. Earlier receipts retain the previous provider's outcomes;
this source receiving is not a published dependency floor or installed-package
qualification. No scientific repair is implemented in the facade. See
{func}`molsysmt.build.solve_atoms_with_alternate_location` and
{ref}`Tutorial_Solve_atoms_with_alternate_locations` for native usage.

## Constructing an independent solvated system

`view.addons.molsysmt.build.solvate()` delegates explicit solvent/ion construction
to the selected MolSysMT engine and returns a separate system. It requires one
structure with chemistry that the engine can parameterize. Hydrogen completion,
protonation and terminal preparation are separate operations; the addon does
not perform them implicitly or select the visible structure from an ensemble.

This small example constructs and caps its input explicitly before loading it:

```python
import molsysviewer as msv
import molsysmt as msm

molsys = msm.build.build_peptide("AlaValPro")
molsys = msm.build.add_missing_terminal_cappings(molsys)
with msv.new_view(molsys) as view:
    solvated = view.addons.molsysmt.build.solvate(
        engine="OpenMM", box_shape="cubic", clearance="0.35 nm",
        water_model="TIP3P", ionic_strength="0 molar",
    )
    assert solvated is not view.molsys
    assert msm.get(solvated, n_waters=True) > 0
    assert msm.get(solvated, n_structures=True) == 1
    # Adopt it deliberately if desired:
    # view.load(solvated, mode="replace")
```

The current view, regions, shapes, history and pending synchronization state
remain unchanged. Reads use the current molecular system, including completed
pending edits. Results use the native box-origin convention; the whole output
may undergo a rigid translation. Source-coordinate labels are not an atom map
between this new system and the existing scene. Output metadata, named-analysis
losses and explicit `to_form` availability follow the native engine/conversion
contract rather than being silently reconstructed by the facade.

The native stored water model and force field can take precedence over requested
settings. Explicitly choose the engine and model you need; the addon performs no
engine fallback. Scientific receiving here covers OpenMM/TIP3P single-structure
construction, independent direct-OpenMM parity, nominal water geometry at bundled
PDB precision and cubic/triclinic box geometry. It does not establish equilibrium,
packing quality for every solute or suitable simulation conditions.

Two native OpenMM limits remain visible: a nonnumeric first atom ID currently
raises ValueError, and explicit `n_anions`/`n_cations` counts are not applied or
rejected. Only the qualified default neutralization workflow is demonstrated
above; no input renumbering or count compensation occurs in the addon. These
limits are being handed to the scientific owner separately from the facade.
`skip_digestion` controls only addon validation because the native function has
no such argument; it does not add a validation bypass to the native operation.

## Constructing and mutating independent peptides

### Building a new geometry from the current sequence

`view.addons.molsysmt.build.build_peptide()` converts the loaded system to a
peptide sequence and constructs a new native model from it. This can give you
an independent starting geometry while retaining the original view:

```python
import molsysviewer as msv
import molsysmt as msm

molsys = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
with msv.new_view(molsys) as view:
    source = view.molsys
    output = view.addons.molsysmt.build.build_peptide(engine="MolSysMT")
    assert msm.get(output, element="group", group_name=True) == ["ALA", "VAL", "PRO"]
    assert output is not source and view.molsys is source
    assert output.structures.n_structures == 1
```

The operation builds fresh coordinates and native template chemistry; it does
not repair observed coordinates or reproduce a source trajectory. A source with
several structures still supplies one sequence for a new model. Source boxes,
named analyses and arbitrary metadata are not transferred to that model, and
there is no inferred correspondence between original and newly built atoms.
Initial geometry is not an energy-minimum or simulation-readiness certificate.

`to_form` selects the native output form; native MolSys, MDTraj trajectory and
three-letter sequence output have explicit receiving. LEaP remains an explicitly
requested optional engine with its executable, force-field, conversion and
scratch-file requirements; this addon receiving does not qualify its execution.
Native construction now reads exact stored group labels and their naming
context. `from_naming_scheme=None` preserves that context; an explicit value
must agree with known source declarations. It is not an override or a global
preference. Named-state construction and atom/H layouts retain their bounded
native support; source naming is distinct from chemical preparation. This does
not certify every deposited label or chain composition. The addon adds no selection, structure selector, fitting or engine
fallback. Use ordinary `msm.build.build_peptide(sequence)` for a new explicit
sequence before loading a view. See {func}`molsysmt.build.build_peptide` and
{ref}`Building peptides <Tutorial_Build_peptide>`.

### Substituting amino-acid groups independently

`view.addons.molsysmt.build.mutate()` passes the requested substitutions to
MolSysMT and returns its independent result. A supported shrinking substitution
keeps observed backbone coordinates while changing the target group's inventory:

```python
import molsysviewer as msv
import molsysmt as msm

molsys = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
with msv.new_view(molsys) as view:
    source = view.molsys
    output = view.addons.molsysmt.build.mutate(
        mutations={1: "GLY"}, keys="group_index", engine="MolSysMT",
    )
    assert msm.get(output, element="group", group_name=True) == ["ALA", "GLY", "PRO"]
    assert msm.build.get_missing_heavy_atoms(output) == {}
    assert msm.get(source, element="group", group_name=True) == ["ALA", "VAL", "PRO"]
    assert output is not source and view.molsys is source
```

The native specifications also accept group-ID dictionaries (`keys="group_id"`),
source-name dictionaries (`keys="group_name"`) and mutation strings such as
`"VAL-1-GLY"`, whose middle field is the source group ID. Group IDs are labels,
whereas group indices are positions. Selection and naming rules remain native;
no caller atom/group mapping or selector translation is invented by the addon.

There is a received native limitation in masked name/ID lookup, tracked in
[MolSysMT#568](https://github.com/uibcdf/molsysmt/issues/568): MDTraj masks
can be passed to the MolSysMT parser, and a list of atom indices can be treated
as group indices. Native MolSysMT expressions, such as `selection="group_index==1"`,
work for the qualified name-keyed route. The addon preserves the current native
diagnostic for the unsupported masks; it does not reinterpret the input or
advertise those modes as successful.

Mutation can leave an unsupported side chain incomplete with
`UnassessedResidueWarning`. For example, the received native VAL-to-TRP case
retains only the target's observed backbone heavy atoms and reports ten missing
side-chain atoms. A renamed TRP is not proof of a reconstructed indole or a
validated rotamer. Inspect `msm.build.get_missing_heavy_atoms(output)` and all
native warnings before downstream use. An explicit optional PDBFixer request
has its own reconstruction behavior; inventory receiving does not independently
validate its pose or certify resolved clashes.

When the source contains H, native mutation can rebuild hydrogens using its
native preparation rules and report attribute loss. That received path is
single-structure. Heavy-only mutation is separately checked across three
structures, preserving observed geometry, box, time and IDs. There is no implicit
visible-structure selection or promise of trajectory-wide hydrogen preparation.
Output atom order/maps, chemistry, mechanics and saved-analysis behavior follow
the actual native reconstruction; source analyses are preserved and the addon
never recalculates them. This is not hidden protonation, minimization or a new
force-field assignment by the addon. See {func}`molsysmt.build.mutate` and
{ref}`Mutating groups <Tutorial_Mutate>`.

Both methods resolve the serialized current primary, including completed pending
edits, without scene synchronization or result adoption. Cached methods follow
replacement and reject closed/empty owners. Mutation keeps its addon-only keyword `skip_digestion`, never forwarded to
a native function without that argument. Peptide construction now mirrors and
forwards native `skip_digestion` and keyword-only `from_naming_scheme`; its
native trusted-caller validation contract applies. Neither wrapper adds `in_place` or `update_view`.
Use a returned system explicitly in further calculations or deliberately replace
the view when that is your intent.

## Recognizing hydrogen-bond sites and local directions

The expert route follows the native family path:
`view.addons.molsysmt.interactions.hbonds`. Recognition and directional hypotheses
do not require a previously detected interaction. The primary is the current
resident `view.molsys`; rules, state, selection, structure indices, execution
mode and scientific assumptions stay explicit. These are experimental source
bindings, not a new detector or a stable electronic-structure model.

```python
from rdkit import Chem
import numpy as np

# Explicit fixture chemistry and coordinates are supplied before loading the view.
molecule = Chem.MolFromSmiles("C#N")
conformer = Chem.Conformer(2)
conformer.SetAtomPosition(0, (0, 0, 0))
conformer.SetAtomPosition(1, (1.2, 0, 0))  # RDKit positions use angstroms.
molecule.AddConformer(conformer)
molsys = msm.convert(molecule)
with msv.new_view(molsys) as view:
    tools = view.addons.molsysmt.interactions.hbonds
    sites = tools.get_hbond_sites(
        method="smarts_donor_acceptor", structure_indices=[0],
    )
    directions = tools.get_hbond_site_directions(
        structure_indices=[0], pbc=False,
    )
    assert sites["acceptor_atom_indices"].tolist() == [1]
    np.testing.assert_allclose(directions["directions"], [[1, 0, 0]])
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(directions["origins"], to_unit="nm"),
        [[0.12, 0, 0]],
    )
    assert not view.molsys.interactions
```

`get_hbond_sites()` matches the complete declared source graph before filtering.
A donor and its indexed H must both be selected; an acceptor anchor must be
selected. No implicit H is converted to an indexed atom. Elemental N/O,
elemental F/O/N and attributed SMARTS definitions differ: elemental rules can
include chemically unsuitable acceptors. Complete declared connectivity and
profile-specific bond/charge/aromatic chemistry remain prerequisites. The
explicit completeness assumption does not fill missing chemical columns.
Match limits reject excessive matches rather than truncating a result.

`get_hbond_site_directions()` returns observed donor-to-H directions and a
bounded set of ideal acceptor hypotheses. Directions are normalized and
dimensionless; origins are length quantities. `status` keeps unsupported,
defined and undefined geometry distinct. Unsupported sites and degenerate
local planes do not acquire an arbitrary axis or virtual H. These hypotheses
are not orbitals, interaction occurrences or an optimized hydrogen network.

Nonconsecutive and repeated structure requests retain source indices and
separate request positions: use `direction_structure_positions` to distinguish
repeated occurrences of the same structure. Supporting atoms can be outside the
selected anchors. Packed support images use box vectors as rows and refer to
the site anchor; reconstruct with the reported images and physical box units.
The uint8 status matrix scales with requested structures times sites, while
directional records are packed sparsely. Full source graphs and maps also scale
with the system. Execution/output budgets remain native estimates, excluding some source/Python
overhead. They do not establish a universal RSS bound or file-backed query API.

Site recognition validates structure indices on the original source axis;
negative, out-of-range, malformed and boolean positions raise native errors.
For this chemical tool, `None` means `all`. An empty structure list can still
return reference/explicit-state chemical sites, but cannot resolve an assigned
state or evaluate a spatial selection. Spatial selection needs coordinates and
uses the first requested structure. Source receiving for
[#509](https://github.com/uibcdf/molsysmt/issues/509) is separate from published
package qualification; the addon retains the native policy. Coordinate-free
native recognition and a resident view's loading requirements are separate contracts.

### Keeping the classic role rules explicit

```python
with msv.demo["pentalanine"] as view:
    roles = view.addons.molsysmt.interactions.hbonds
    donor_hydrogen_pairs = roles.get_donor_atoms()
    acceptor_indices = roles.get_acceptor_atoms()
    assert donor_hydrogen_pairs.shape[1] == 2
    assert len(donor_hydrogen_pairs) > 0 and len(acceptor_indices) > 0
```

These classic rules preserve their own semantics. Their donor selection filters
the donor anchor and can retain its covalently attached H outside that selection;
this differs from the modern whole-pair output filter. Default rules do not
certify universal donor/acceptor chemistry, protonation or hydrogen completeness.
Native ordering preserves donor-H membership, including interleaved indices.

The native repairs [#506](https://github.com/uibcdf/molsysmt/issues/506) and
[#507](https://github.com/uibcdf/molsysmt/issues/507) preserve supplied rule lists
and separate the default-rule language from user selections and custom rules.
`syntax` governs user expressions; built-in criteria retain MolSysMT syntax.
Repeated calls and shared rule lists are safe. Malformed queries reject rather
than being translated or retried. Custom donors without matching indexed H return a native empty
`int64` array with shape `(0, 2)` after the owner repair
([#508](https://github.com/uibcdf/molsysmt/issues/508)). This outcome does not add
hydrogens or certify chemical completeness. No consumer copy, parser translation
or scientific fallback is added.
The two classic methods have a keyword-only addon `skip_digestion` flag; it is
not forwarded because their native signatures do not declare that escape hatch.

All four tools use the serialized current primary, including pending scientific
edits, and follow replacement/closed-view handling. Their results remain ordinary
native values: no named analysis, saved interaction set, visual selection, shape,
color, preparation or scene synchronization is added. `update_view` is rejected.
Use the core `view.interactions` API separately for qualified visual workflows.


## Calculating raw hydrogen-bond observations

Use `view.addons.molsysmt.interactions.hbonds.get_hbonds()` for the native modern
criterion/profile API. It returns `molsysmt.Interactions` by default, or the
explicit typed `molsysmt.InteractionsDict` output. Methods, explicit donor-H/
acceptor arrays, selections, chemistry, PBC, cutoffs, execution mode and match
budgets remain scientific inputs. The wrapper supplies only current view.molsys.

```python
from pathlib import Path
import tempfile
import numpy as np
from rdkit import Chem

# Declare chemistry and indexed H explicitly before starting the molecular view.
molsys = msm.convert(Chem.AddHs(Chem.MolFromSmiles("O.O")))
molsys.structures.append(coordinates=msm.pyunitwizard.quantity(
    [[[0, 0, 0], [.28, 0, 0], [.1, 0, 0], [0, .1, 0],
      [.28, .1, 0], [.28, 0, .1]]], "nm",
))
with msv.new_view(molsys) as view:
    tools = view.addons.molsysmt.interactions.hbonds
    observed = tools.get_hbonds(
        method="baker_hubbard", structure_indices=[0], pbc=False,
    )
    assert observed.n_interactions == 1
    assert observed.participant_atoms.tolist() == [0, 2, 1]
    np.testing.assert_allclose(observed.measurements["hydrogen_acceptor_distance"], .18)
    assert observed.measure_units["hydrogen_acceptor_distance"] == "nm"
    triples, distances = tools.get_buch_hbonds(structure_indices=[0], pbc=False)
    angular = tools.get_luzard_chandler_hbonds(structure_indices=[0], pbc=False)
    assert triples.tolist() == [[[0, 2, 1]]] and len(angular) == 3
    assert not view.molsys.interactions
    # Saving is an explicit operation on an independent molecular copy.
    saved = view.addons.molsysmt.basic.copy()
    saved.interactions = {**saved.interactions, "calculated-hbonds": observed}
    with tempfile.TemporaryDirectory() as directory:
        path = str(Path(directory) / "observations.h5msm")
        msm.convert(saved, to_form=path)
        restored = msm.convert(path).interactions["calculated-hbonds"]
        assert restored.n_interactions == observed.n_interactions
```

Modern `selection_mode` preserves the native internal/incident/between calculation
scopes. These are different from result-query modes. Choose the profile explicitly
when recognition or geometric conventions matter; the facade adds no hydrogen,
partial-charge, aromatic or connectivity preparation and no alternative engine.
Record-level measurements carry declared nm/radian units even under another
application unit policy. Read native mappings/arrays through their supported
interfaces; occurrence references belong to one version of an analysis.

The classic `get_buch_hbonds` and `get_luzard_chandler_hbonds` defaults stay tuples.
Their triples contain donor, indexed H and acceptor source indices. Equal counts
use rectangular arrays; varying counts use aligned lists with shaped empty
entries. Tuple requests retain structure order/repetition. Optional sparse
`output_type="molsysmt.Interactions"` keeps evaluated-empty coverage and native
deduplication; each method's native ordering remains intact. The classic methods
retain eager execution and their optional-analysis limitations. Modern native
sparse output deduplicates repeated structures in sorted order. No common
ordering policy is imposed on these distinct returns.

Caller-supplied roles and secondary systems remain explicit inputs. Native
unsupported combinations reject, including a second molecular system and
provided roles/secondary axes in the classic sparse-output route. The classic
supplied-donor tuple path is independently reproduced as failing under
[#511](https://github.com/uibcdf/molsysmt/issues/511). Precomputed acceptors with automatic donors work. The
facade does not flatten donor pairs, rebuild missing roles or translate selectors
to conceal a provider limitation. The modern explicit-site route retains its
separate validated pair/acceptor-array contract.

Evaluated structures with no observations remain evaluated; unrequested
structures stay unevaluated. The visible canvas structure never replaces the
native `structure_indices` argument. Periodic observations retain the images
actually used, with box vectors as rows, rather than guessed display offsets.
The modern execution/result budgets remain native estimates and exclude some
caller/source/Python overhead. No universal RSS or out-of-memory-file claim is
added. The wrapper itself adds no whole-trajectory conversion or scientific cache.

All calls use the serialized primary reader, including pending scientific edits.
Returned analyses are independent of the view lifetime and are not stored in
view.molsys.interactions, given a name or represented. The native map property is
read-only; explicit assignment of a new named map validates correspondence.
Use the core `view.interactions` API separately when you choose visual attachment.
`update_view` is not a detector argument.

## Calculating disulfide candidates

`view.addons.molsysmt.interactions.disulfides.get_disulfide_candidates()` preserves
the native eligible group names, S-S cutoff, source atom indices, PBC, structure
scope, sorting and default pair/distance lists. Its optional sparse analysis
records observed images, coverage, method, units and producer provenance.

```python
builder = msm.MolSysBuilder()
first = builder.add_atom(atom_name="SG", atom_type="S")
second = builder.add_atom(atom_name="SG", atom_type="S")
builder.add_group([first], group_name="CYS")
builder.add_group([second], group_name="CYS")
builder.set_coordinates(msm.pyunitwizard.quantity([[0, 0, 0], [.2, 0, 0]], "nm"))
with msv.new_view(builder.build()) as view:
    tools = view.addons.molsysmt.interactions.disulfides
    pairs, distances = tools.get_disulfide_candidates(structure_indices=[0], pbc=False)
    assert pairs[0].tolist() == [[0, 1]]
    observed = tools.get_disulfide_candidates(
        structure_indices=[0], pbc=False, output_type="molsysmt.Interactions",
    )
    assert observed.n_interactions == 1
    assert not view.molsys.interactions
```

A geometric candidate can already be a recorded covalent bond; it is not proof
of a missing bond, oxidation state or chemically valid disulfide. Calculation
neither inserts nor removes bonds. Default and extended group-name filters are
native scientific choices. Scope, quantities and sparse coverage remain distinct
from a rendered connection.


## Calculating ionic contacts with an explicit cutoff

Use `view.addons.molsysmt.interactions.ionic.get_ionic_interactions()` when you
want minimum-distance observations between opposite formal-charge centers.
A unit-bearing `distance_threshold` is required. This bounded geometric criterion
is not an electrostatic energy, parameterized partial charge or universal
salt-bridge assignment. Select every atom of a compound center; its recorded
geometry references can be a subset of those participant atoms.

```python
import numpy as np
import molsysviewer as msv
import molsysmt as msm
from rdkit import Chem

molsys = msm.convert(Chem.MolFromSmiles("[Na+].[Cl-]"))
coordinates = np.array([
    [[0, 0, 0], [.30, 0, 0]],
    [[0, 0, 0], [.80, 0, 0]],
    [[0, 0, 0], [.25, 0, 0]],
])
molsys.structures.append(coordinates=msm.pyunitwizard.quantity(coordinates, "nm"))
with msv.new_view(molsys) as view:
    analysis = view.addons.molsysmt.interactions.ionic.get_ionic_interactions(
        "4 angstrom", structure_indices=[2, 0, 2], pbc=False,
    )
    assert analysis.participant_roles == ("positive", "negative")
    assert analysis.evaluated_structure_indices.tolist() == [0, 2]
    np.testing.assert_allclose(analysis.measurements["distance"], [.30, .25])
    assert analysis.measure_units["positive_charge"] == "e"
    assert not view.molsys.interactions
```

The selected chemical state needs explicit formal charges and declared
connectivity. The current recognizer treats its documented carboxylate,
guanidinium and literal-charge definitions; it does not universally resolve
phosphate, sulfate or aromatic delocalization. Direct covalent center links are
excluded natively. Periodic images move each whole participant; a center split
across the cell boundary retains native rejection rather than implicit unwrapping.
See {func}`molsysmt.interactions.ionic.get_ionic_interactions` for the complete contract.

## Calculating chemically typed hydrophobic atom pairs

Use `view.addons.molsysmt.interactions.hydrophobic.get_hydrophobic_interactions()`
for the native SMARTS profile and inclusive atom-pair distance criterion. Its
ProLIF 2.2.2 reference core is not a group hydrophobicity scale, interaction
energy, Mol* rule or ligand/protein fingerprint. RDKit is required by this native
route; the ProLIF package itself is not required. The source declares its chemistry
before the addon reads it; no hydrogen, charge or aromatic preparation is hidden.

```python
import numpy as np
import molsysviewer as msv
import molsysmt as msm
from rdkit import Chem

molsys = msm.convert(Chem.MolFromSmiles("CCC.CCC"))
xyz = np.array([[0, 0, 0], [.15, 0, 0], [.30, 0, 0],
                [0, .30, 0], [.15, .30, 0], [.30, .30, 0]])
molsys.structures.append(coordinates=msm.pyunitwizard.quantity(xyz[None], "nm"))
with msv.new_view(molsys) as view:
    analysis = view.addons.molsysmt.interactions.hydrophobic.get_hydrophobic_interactions(
        selection=[4], selection_2=[1], selection_mode="between", pbc=False,
    )
    assert analysis.participant_atoms.tolist() == [1, 4]
    assert analysis.participant_roles == ("hydrophobic_1", "hydrophobic_2")
    np.testing.assert_allclose(analysis.measurements["distance"], [.30])
    assert analysis.measure_units["distance"] == "nm"
    assert not view.molsys.interactions
```

Pairs have canonical source-index order even when selections are reversed;
roles do not identify a ligand. The default cutoff is 0.45 nm. Distinct
coincident atoms can be observed, and the declared reference core adds no extra
covalent or intramolecular exclusion. Full-source recognition precedes selection;
`max_matches` remains an explicit native cap rather than silent truncation.
See {func}`molsysmt.interactions.hydrophobic.get_hydrophobic_interactions`.

## Calculating directional halogen observations

Use `view.addons.molsysmt.interactions.halogen_bonds.get_halogen_bonds()` for
the D-X...A-R profile's distance and two inclusive angular intervals. All four
roles count for calculation selection, including the donor neighbor and acceptor
reference. Selecting X and A alone is not a complete internal search. Distinct
acceptor-reference neighbors retain separate observations. Undefined angles do
not become fabricated directions or evidence of an attractive energy.

```python
import numpy as np
import molsysviewer as msv
import molsysmt as msm
from rdkit import Chem

molsys = msm.convert(Chem.MolFromSmiles("CCl.C=O"))
xyz = np.array([[-.15, 0, 0], [0, 0, 0],
                [.36, .12*np.sqrt(.75), 0], [.30, 0, 0]])
molsys.structures.append(coordinates=msm.pyunitwizard.quantity(xyz[None], "nm"))
with msv.new_view(molsys) as view:
    analysis = view.addons.molsysmt.interactions.halogen_bonds.get_halogen_bonds(
        selection=[0, 1], selection_2=[2, 3], selection_mode="between",
        donor_angle_range=msm.pyunitwizard.quantity([130, 180], "degrees"),
        acceptor_angle_range=msm.pyunitwizard.quantity([80, 140], "degrees"),
        pbc=False,
    )
    assert analysis.participant_atoms.tolist() == [0, 1, 3, 2]
    assert analysis.participant_roles == ("donor", "halogen", "acceptor", "acceptor_reference")
    np.testing.assert_allclose(analysis.measurements["donor_angle"], np.pi)
    np.testing.assert_allclose(analysis.measurements["acceptor_angle"], 2*np.pi/3)
    assert analysis.measure_units["acceptor_angle"] == "radians"
    assert not view.molsys.interactions
```

The default X-A cutoff is 0.35 nm. The adapted ProLIF core is not the paper's
exact element-specific van der Waals criterion. Coherent chain MIC images
reconstruct the measured adjacent D-X-A-R vectors, with box vectors as rows;
this does not provide arbitrary molecular or ring unwrapping. Read distances
in nm and angles in radians from the result's declared units even when the
application uses another unit policy. See
{func}`molsysmt.interactions.halogen_bonds.get_halogen_bonds`.

All three families preserve native `internal`, `incident` and `between`
calculation modes, separately from the explicit result-query modes.
Nonconsecutive structure indices remain source indices; repeats are evaluated
once in sorted order. Evaluated-empty and unrequested structures remain distinct.
The visible structure is not an implicit calculation default. Methods, profiles,
chemical state, completeness declarations, units and attribution remain explicit.
The legacy pentalanine H5MSM demo lacks the formal-charge/bond-chemistry evidence
these detectors require; native rejection is preserved, not repaired in the facade.

`heavy_mode` keeps native projected-coordinate execution for admitted native/H5MSM
routes. Rich-selection and unsupported-form restrictions remain native. Sparse
results stay resident; estimates exclude some source/Python overhead and do not
guarantee process RAM. There is no automatic named storage or scene attachment.
Use the explicit independent-copy H5MSM procedure above when you choose to save
an analysis, or the separate core `view.interactions` workflow to represent one.


## Observing metal-ligand proximity candidates

Use `view.addons.molsysmt.interactions.metal_coordination.get_metal_coordination()`
for the native broad, experimental proximity profile. Metal and ligand roles stay
directed even when the selections are reversed. This does not assign a
coordination bond, oxidation state, coordination number or binding energy.
Stored dative bonds remain independent and unchanged. RDKit supplies the declared
SMARTS profile; the reference ProLIF package is not required at runtime.

```python
import numpy as np
import molsysviewer as msv
import molsysmt as msm
from rdkit import Chem

molsys = msm.convert(Chem.MolFromSmiles("[Zn+2].O.N"))
xyz = np.array([[[0, 0, 0], [.20, 0, 0], [0, .27, 0]]])
molsys.structures.append(coordinates=msm.pyunitwizard.quantity(xyz, "nm"))
with msv.new_view(molsys) as view:
    analysis = view.addons.molsysmt.interactions.metal_coordination.get_metal_coordination(
        selection=[1, 2], selection_2=[0], selection_mode="between", pbc=False,
    )
    assert analysis.n_interactions == 2
    assert analysis.participant_roles == ("metal", "ligand", "metal", "ligand")
    np.testing.assert_allclose(analysis.measurements["distance"], [.20, .27])
    assert analysis.measure_units["distance"] == "nm"
    assert not view.molsys.interactions
```

The default inclusive cutoff is 0.28 nm. Water oxygen may be eligible, and this
reference core adds no universal covalent-neighbor exclusion. If a site has both
roles, reversed role assignments are distinct native relations. Full declared
chemistry, method/profile and match caps stay explicit. See
{func}`molsysmt.interactions.metal_coordination.get_metal_coordination`.

## Comparing declared aromatic-ring geometries

Use `view.addons.molsysmt.interactions.pi_pi.get_pi_pi_interactions()` with a
scientific method/profile chosen explicitly. The default custom
`centroid_angle_offset` / `least_squares` proposal requires four unit-bearing
cutoffs; the addon does not fill them. An adapted reference geometry has different
recognition, plane construction, exclusions and acceptance rules. A selected
geometry tester does not reproduce a complete reference feature pipeline.

```python
import numpy as np
import molsysviewer as msv
import molsysmt as msm
from rdkit import Chem

angles = np.arange(6)*np.pi/3
ring = np.column_stack((.14*np.cos(angles), .14*np.sin(angles), np.zeros(6)))
coordinates = np.array([np.vstack((ring, ring+[0, 0, z])) for z in [.35, 2, .4]])
molsys = msm.convert(Chem.MolFromSmiles("c1ccccc1.c1ccccc1"))
molsys.structures.append(coordinates=msm.pyunitwizard.quantity(coordinates, "nm"))
with msv.new_view(molsys) as view:
    tools = view.addons.molsysmt.interactions.pi_pi
    custom = tools.get_pi_pi_interactions(
        ".6 nm", "30 degrees", ".2 nm", ".02 nm",
        geometry="parallel", structure_indices=[2, 0, 2], pbc=False,
    )
    assert custom.participant_roles == ("ring_a", "ring_b")
    assert custom.participant_atom_offsets.tolist() == [0, 6, 12]
    assert custom.evaluated_structure_indices.tolist() == [0, 2]
    np.testing.assert_allclose(custom.measurements["distance"], [.35, .4])
    reference = tools.get_pi_pi_interactions(
        method="plane_angle_intersection", profile="smarts_5_6", pbc=False,
    )
    assert reference.n_interactions == 2
    assert reference.measure_units["plane_angle"] == "radians"
    assert not view.molsys.interactions
```

The custom `geometry` filter distinguishes parallel, edge-to-face and both.
Canonical reference profiles include `three_atom_plane` with
`centroid_angle_offset`, or `smarts_5_6` / `aromatic_cycles` with
`plane_angle_intersection`. Historical software selectors remain native aliases.
Do not mix custom-only cutoffs into reference criteria that reject them. A
measurement that does not apply to a reference geometry can legitimately be NaN;
its declared unit and that meaning survive typed output and H5MSM persistence.
Whole declared rings must be selected, including required fused neighbors.
Aromatic chemistry is not perceived or repaired implicitly. Split periodic rings
retain native rejection. These are geometric observations, not attractive energy.
See {func}`molsysmt.interactions.pi_pi.get_pi_pi_interactions`.

## Observing cations relative to aromatic participants

Use `view.addons.molsysmt.interactions.cation_pi.get_cation_pi_interactions()`.
The default `centroid_distance_angle` / `smarts_5_6` profile and the adapted
`centroid_distance_offset` / `three_atom_plane` profile have distinct cation,
normal and cutoff definitions. The separate custom `centroid_angle_offset` /
`least_squares` proposal again requires four explicit cutoffs. Keep formal-charge
centers distinct from partial charges, energy and protonation assignments.

```python
import numpy as np
import molsysviewer as msv
import molsysmt as msm
from rdkit import Chem

angles = np.arange(6)*np.pi/3
ring = np.column_stack((.14*np.cos(angles), .14*np.sin(angles), np.zeros(6)))
molsys = msm.convert(Chem.MolFromSmiles("c1ccccc1.[NH4+]"))
molsys.structures.append(coordinates=msm.pyunitwizard.quantity(
    np.vstack((ring, [0, 0, .35]))[None], "nm"))
with msv.new_view(molsys) as view:
    analysis = view.addons.molsysmt.interactions.cation_pi.get_cation_pi_interactions(
        selection=[6], selection_2=list(range(6)), selection_mode="between", pbc=False,
    )
    assert analysis.participant_roles == ("cation", "ring")
    assert analysis.participant_atoms.tolist() == [6, 0, 1, 2, 3, 4, 5]
    np.testing.assert_allclose(analysis.measurements["distance"], [.35])
    assert analysis.measure_units["normal_angle"] == "radians"
    assert analysis.measure_units["cation_charge"] == "e"
    assert not view.molsys.interactions
```

Selections include every atom of an intersected ring or compound center; neither
selection is assumed to be the cation side. The selected native profile determines
whether a cation is a singleton or a compound center and which exclusions apply.
The addon adds no protonation, charges, aromaticity, ring fitting or periodic
unwrapping beyond the chosen native calculation. See
{func}`molsysmt.interactions.cation_pi.get_cation_pi_interactions`.

The current native pi-pi/cation-pi reference-state selector path rejects MDTraj
string selections even though equivalent explicit atom indices work. Keep this
provider limitation ([#516](https://github.com/uibcdf/molsysmt/issues/516)) visible;
the facade does not translate selectors or override
the requested chemical state. MolSysMT string and numerical scopes retain their
native semantics. This limitation is tracked separately from geometry/profile
qualification.

## Following simultaneous hydrogen bonds through indexed waters

Use `view.addons.molsysmt.interactions.water_bridges.get_water_bridges()` for
paths made from observed D-H-A legs. `order=1` requires exactly one mediator
water and two simultaneous legs; `order=2` requires exactly two distinct waters
and three legs. It is not a maximum-order request. Every water needs two indexed
hydrogens. This example creates its declared source explicitly, outside the addon.

```python
import numpy as np
import molsysviewer as msv
import molsysmt as msm
from rdkit import Chem

molecule = Chem.AddHs(Chem.MolFromSmiles("O.C=O.C=O"))
molsys = msm.convert(molecule)
xyz = np.zeros((molecule.GetNumAtoms(), 3))
xyz[:, 2] = np.arange(molecule.GetNumAtoms())*3 + 3
water_h = sorted(a.GetIdx() for a in molecule.GetAtomWithIdx(0).GetNeighbors())
xyz[0] = [0, 0, 0]
xyz[water_h] = [[.1, 0, 0], [0, .1, 0]]
xyz[2], xyz[4] = [.3, 0, 0], [0, .3, 0]
molsys.structures.append(coordinates=msm.pyunitwizard.quantity(xyz[None], "nm"))
with msv.new_view(molsys) as view:
    tools = view.addons.molsysmt.interactions.water_bridges
    analysis = tools.get_water_bridges(order=1, pbc=False)
    assert analysis.n_interactions == 1
    assert len(analysis.participant_roles) == 6
    np.testing.assert_allclose(analysis.measurements["leg_1_dha_angle"], np.pi)
    assert analysis.measure_units["leg_1_donor_acceptor_distance"] == "nm"
    assert tools.get_water_bridges(order=2, pbc=False).n_interactions == 0
    assert not view.molsys.interactions
```

This controlled fixture demonstrates leg geometry, not an optimized solvent
configuration. Order-two results contain nine roles. Repeated water oxygens and
alternative observed hydrogens retain their actual leg identities/images and
per-leg parameters. Internal/between calculation scopes include the used mediator
atoms and hydrogens; endpoint-only sets need explicit `incident` semantics.
The detector never adds waters, hydrogens or an optimized network. It does not
compute global occurrence frequency or paths beyond order two. Accepted leg,
join and bridge arrays remain resident; bounded coordinate execution is not an
incremental file writer or process-RAM guarantee. See
{func}`molsysmt.interactions.water_bridges.get_water_bridges`.

All four families return independent native results, with original atom/structure
axes, sorted unique evaluated coverage, occurrence references, evidence and declared
units. No source, named analysis or scene is changed automatically. Read incomplete
chemistry as a diagnostic, not an evaluated absence. Use explicit named storage on
an independent copied system when saving H5MSM; graphical attachment remains a
separate qualified core workflow. All detector contracts remain experimental.


## Keeping atom correspondence and independent atom order

Use `tools.basic.compose_atom_maps(atom_maps)` to compose explicit native map
reports, including before loading a system. It carries declared correspondence;
it does not match molecules, authenticate identity, transfer coordinates or
recalculate charges. Direct absent-origin `-1` and merged representatives have
different meanings. Inputs can contain JSON lists; the result keeps native typed
arrays and quantity records. Keep reports as sidecars: they are not an H5MSM 0.5
domain. See {func}`molsysmt.basic.compose_atom_maps`.

```python
import molsysviewer as msv

first = dict(schema="molsysmt.atom_map@1", n_source_atoms=2, n_output_atoms=3,
             source_to_output_atom_indices=[0, 1],
             output_to_source_atom_indices=[0, 1, -1])
second = dict(schema="molsysmt.atom_map@1", n_source_atoms=3, n_output_atoms=2,
              source_to_output_atom_indices=[1, -1, 0],
              output_to_source_atom_indices=[2, 0])
with msv.new_view() as view:
    report = view.addons.molsysmt.basic.compose_atom_maps([first, second])
    assert report["output_to_source_atom_indices"].tolist() == [-1, 0]
    assert view.molsys is None
```

`tools.basic.permute_atoms(atom_indices, return_report=True)` reads the current
primary and returns an independent MolSys plus its atom map. The order is a full
new-to-old positional bijection, not an extraction selection. Native bonds,
chemical states, structural series, mechanics and named interactions follow their
remapping contracts; historical preparation records keep their original axes.
Native consistency and unsupported-domain errors remain visible. In particular,
legacy demo systems with inconsistent chain metadata are not silently repaired.
The source and scene keep their atom order. There is no `update_view` switch:
load the independent output explicitly only if you want to replace the scene.
Full output remains resident; a numeric estimate is not a universal RAM bound.
See {func}`molsysmt.basic.permute_atoms`.

```python
import molsysviewer as msv
import molsysmt as msm
from rdkit import Chem

source = msm.convert(Chem.MolFromSmiles("CCO"))
source.structures.append(coordinates=msm.pyunitwizard.quantity(
    [[[0, 0, 0], [.15, 0, 0], [.25, .1, 0]]], "nm"))
with msv.new_view(source) as view:
    original = view.molsys
    result = view.addons.molsysmt.basic.permute_atoms([2, 0, 1], return_report=True)
    assert result["report"]["output_to_source_atom_indices"].tolist() == [2, 0, 1]
    assert result["molecular_system"] is not original
    assert view.molsys is original
```

## Working with molecular files explicitly

`tools.h5msm.write(output_filename)` writes the current primary, including pending
native edits, through the serialized reader. It does not synchronize the scene.
All other H5MSM utilities keep filenames and domain objects explicit and work
before loading a system while the view is open. Paths refer to the Python process
filesystem, which may be remote. They are molecular-domain operations, not a
Viewer scene/session save or a browser download.

- `read(filename)` returns an independent native MolSys, including supported
  partial files; it does not load it into the view.
- `read_layers(filename, layers=None, analysis_names=None)` returns selected native
  domains/analyses. An absent layer is `None`; present-empty interactions are `{}`.
  This is not a public out-of-core interaction query.
- `write_layers(output_filename, *, topology=None, chemical_states=None,
  structures=None, interactions=None, associations=None)` writes only explicit
  caller-owned domains and declared associations, never implicitly adding the
  primary's topology, analyses or structures.
- `append_structures(filename, structures, *, structure_state_indices=None,
  block_size=256)` extends an explicit topology/interaction-free file. It neither
  edits nor reloads a loaded primary, even if the original path is the same.
  Native validation precedes resize; this is not a crash-transactional editor.
- `migrate_04_to_05(filename, output_filename)` and
  `migrate_to_05(filename, output_filename)` preserve the legacy source and write
  a distinct destination under native schema and information-loss restrictions.

Native units, sparse coverage, associations, producer metadata, return types,
errors and overwrite behavior remain unchanged. H5MSM 0.5 rejects nonempty
molecular-mechanics data rather than silently discarding it. Explicit external
inputs/files must remain stable during calls; the view's molecular edit lock does
not lock those resources. See {func}`molsysmt.h5msm.read`,
{func}`molsysmt.h5msm.write`, {func}`molsysmt.h5msm.read_layers`,
{func}`molsysmt.h5msm.write_layers`, {func}`molsysmt.h5msm.append_structures`,
{func}`molsysmt.h5msm.migrate_04_to_05` and {func}`molsysmt.h5msm.migrate_to_05`.

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import molsysviewer as msv
import molsysmt as msm

with TemporaryDirectory() as directory, msv.new_view() as view:
    files = view.addons.molsysmt.h5msm
    path = str(Path(directory) / "times.h5msm")
    from molsysmt.native import Structures
    times = Structures(time=msm.pyunitwizard.quantity([0, 1], "ps"))
    files.write_layers(path, structures=times)
    files.append_structures(path, times, block_size=1)
    restored = files.read(path)
    assert restored.structures.n_structures == 4
    assert restored.topology is None and view.molsys is None
```

## Inspecting submitted FASTA records without admitting a molecular system

`tools.form.file_fasta.read_records(item)` and
`parse_records(fasta_text, *, source_label=None)` keep explicit file/text inputs.
They work before loading and return fresh JSON-compatible `fasta_source@1`
records. Record indices identify occurrences within that source, not biological
identity. Headers, case, whitespace, modifications, empty/repeated records and
CR/LF/CRLF endings remain raw. Source spans are half-open **decoded character**
offsets, not UTF-8 byte offsets. Native UTF-8 and pre-header validation remains
visible. These readers do not normalize/admit sequences, create topology or
coordinates, load a view, or require Biopython. Ordinary sequence conversion is
a separate scientific operation. See
{func}`molsysmt.form.file_fasta.read_records` and
{func}`molsysmt.form.file_fasta.parse_records`.

```python
import molsysviewer as msv

text = ">β  \r\n acD*\n>β\r\n"
with msv.new_view() as view:
    result = view.addons.molsysmt.form.file_fasta.parse_records(text)
    assert [record["record_index"] for record in result["records"]] == [0, 1]
    assert "".join(record["raw_record"] for record in result["records"]) == text
    assert view.molsys is None
```


## Composing molecular systems and extending their structures

The expert API preserves the native two-by-two composition model:

| Axis | Edit the current primary | Return an independent result |
| --- | --- | --- |
| Atoms | `basic.add(from_molecular_system, ...)` | `basic.merge(molecular_systems, ...)` |
| Structures | `basic.append_structures(from_molecular_system, ...)` | `basic.concatenate_structures(molecular_systems, ...)` |

`add` and `append_structures` bind only the destination to `view.molsys`.
`from_molecular_system` stays explicit. Their native `in_place=True` default
modifies that actual object and returns `None`. With `in_place=False`, the
serialized reader returns the native independent result, without adoption.
`update_view=True` synchronizes an admitted in-place edit; False performs the
science now and leaves a pending scene update for `tools.sync_view()`.

```python
import molsysviewer as msv

with msv.demo["dialanine"] as view:
    tools = view.addons.molsysmt
    incoming = tools.basic.copy()
    independent = tools.basic.add(incoming, in_place=False)
    assert independent.get_n_atoms() == 44
    assert view.molsys.get_n_atoms() == 22
    region = view.regions.add(atom_indices=[0, 1], tag="original-atoms")
    tools.basic.add(incoming, update_view=False)
    structures = tools.basic.copy()
    tools.basic.append_structures(structures, update_view=False)
    assert tools.get_sync_status()["state"] == "pending"
    tools.sync_view()
    assert view.molsys.get_n_atoms() == 44 and view.player.n_structures == 2
    assert view.regions["original-atoms"] is region
```

Native prefix identities retain existing regions, colors, selections, anchored
objects and original source indices. Added atoms have an explicitly unmapped
upstream origin; new structures do not acquire invented original indices.
These scientific edits do not create the source regions that `view.load` owns.
Managed growth, retained-axis removal and further edits compose from the last
synchronized scene. Rendering checks coordinate presence with one bounded
atom/structure query rather than a full additional trajectory scan. Native
operations and their independent outputs retain their own allocation costs.

Before adding new structures, clear per-structure shapes and trajectory plot
cards: the addon cannot invent their new values. Static atom-anchored shapes
and explicit filters selecting old structures keep their meaning. Keep source
inputs stable during calls; the view's edit lock does not lock unrelated systems.

`merge` and `concatenate_structures` keep their complete ordered input collection
explicit. They do not insert the current primary or synchronize the scene, and
work on an open empty view. If the current primary is one input, include it
explicitly and keep its data stable. Native `to_form` controls the result form;
for file inputs, request `to_form="molsysmt.MolSys"` when you want an in-memory
result. Unsupported file-output defaults retain native `NotImplementedMethodError`.

```python
import molsysviewer as msv
import molsysmt as msm

molsys = msm.convert(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"])
with msv.new_view() as view:
    tools = view.addons.molsysmt
    merged = tools.basic.merge([molsys, molsys])
    ensemble = tools.basic.concatenate_structures([molsys, molsys])
    assert merged.get_n_atoms() == 44
    assert ensemble.structures.n_structures == 2
    assert view.molsys is None
```

Lists/tuples in collection `selections` and `structure_indices` express
per-system intent; NumPy arrays or ranges express a common index collection.
In contrast, a list passed as one `from_molecular_system` describes complementary
items of one system, not successive independent systems. Keep native selection,
structure order/repetition, units and scientific parameters explicit. The addon
adds no atom matching, alignment, structural broadcasting or chemical preparation.
Structure addition requires matching atom correspondence; coordinate-only sources
cannot authenticate that correspondence. Atom addition preserves the target box
and native warnings. `attribute_policy="intersection"` retains native attribute
loss warnings; `"strict"` rejects one-sided structural attributes. Charge/type
columns, assignment-report invalidation and state associations follow native
rules, without a new joint scientific calculation.

Native target analyses retain their declared evaluation universe. Atom growth
does not mean new atoms were evaluated; structure growth leaves new structures
unevaluated. Incoming analyses retain native rejection until an explicit merge
policy exists. Native [#520](https://github.com/uibcdf/molsysmt/issues/520)
currently affects named target analyses with explicit structure/state links:
append can raise after partially extending structures. The host marks that
outcome uncertain and requires explicit replacement; the facade does not clear
analyses or reorder the scientific operation to conceal it. Implicit single-state
association and explicit no-analysis paths are qualified separately.

A native operation can also complete successfully yet produce coordinate-free
data under its attribute policy. Such a result is valid independently, but cannot
be displayed. In-place synchronization then raises `SystemEditSyncError` with
`science_completed=True` and the native result. Supply the missing scientific
data explicitly and retry synchronization, or replace the system; retry never
repeats addition. Atomic native rejection retains scientific data and pending
maps/revisions; an attempted operation may receive a new diagnostic ID.

See {func}`molsysmt.basic.add`, {func}`molsysmt.basic.append_structures`,
{func}`molsysmt.basic.merge` and {func}`molsysmt.basic.concatenate_structures`.
The managed prefix-addition route requires a Viewer host with the explicit
`axis_growth` capability. An older retained-axis-only host rejects it before
science. Independent outputs and explicit collection routes keep their separate
contracts. This is source receiving, not published-package or universal scientific
qualification.
