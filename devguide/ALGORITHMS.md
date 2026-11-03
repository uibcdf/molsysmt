# MolSysMT Core Algorithms

This document records current normalization and native-rebuild behavior. It
describes implemented algorithms, not desired chemical perception capabilities.

## Atom-type inference from atom names

`molsysmt.element.atom.get_atom_type_from_atom_name()` performs an exact lookup
in `molsysmt/element/atom/names.py`.

- Known names return the mapped element symbol.
- An unknown name emits `UnknownAtomNameWarning` and returns `"UNK"`.
- The lookup does not perform a general element inference algorithm from an
  arbitrary PDB atom-name grammar.
Unexpected mapping failures propagate instead of being treated as unknown
names.

## Group-type inference

Name-based classification is implemented by
`molsysmt.element.group.get_group_type_from_group_name()` with this precedence:

1. water;
2. ion;
3. amino acid;
4. terminal capping;
5. nucleotide;
6. small molecule;
7. lipid;
8. saccharide;
9. unknown.

These decisions use maintained name collections. A group is not classified as an
ion merely because it contains one atom, and arbitrary atomic composition does
not by itself establish a group type.

During native topology rebuild,
`molsysmt.native._topology_infer.infer_group_types_from_topology()` first applies
the name-based classifier. A name reserved as a small molecule is reclassified
as an amino acid only when its atom names contain the set `N`, `CA`, `C`, `O`,
and `CB`. This heuristic does not cover every chemically valid amino acid, such
as glycine identified only by composition, and must not be described as general
chemical perception.

## Component inference

Components are a selected chemical state's connected atom sets under its
stored-edge participation policy. ChemicalStates stores their atom-aligned
indices and state-local metadata; Topology and its groups do not store a
canonical `component_index` column. Coordination/dative edges contribute only
when the stored participation declaration admits them.

With no participating edges, graph reconstruction gives singleton components.
That does not promote unavailable/partial connectivity to complete chemistry.
Callers must not reinterpret stable molecule membership from these components.

`ChemicalStates.rebuild_components()` treats its redefinition flags independently.
When reconstructing indices, false metadata flags preserve component IDs, names
or types only for exactly unchanged atom memberships. Matching ignores row
numbers: per-new-component minimum/maximum old row reductions exclude merges,
and equality of old/new atom counts excludes splits. Missing and out-of-table old
indices cannot authorize transfer. The helper costs linear time and memory in
the atom/component counts and uses no Python object per atom or component set.
Unmatched fields remain genuinely missing; the legacy constructor's string
`"nan"` is not a newly inferred name/type. True flags retain their regeneration
or inference behavior. Only the resolved chemical state is rebuilt. Labels
preserve declared metadata, not chemical identity or completeness evidence.

## Molecule inference

When explicitly requested, group-based molecule inference operates over ordered
groups and their atom-level chain membership. Polymer-like group types may continue the current molecule within a
chain. Standalone types (`ion`, `water`, and `small molecule`) start distinct
molecules. Chain changes and transitions between polymer and standalone classes
split molecules.

Component and molecule partitions are orthogonal: a covalent component may span
more than one semantic molecule.

Ordinary membership queries read the stable inventory instead of reconstructing
it. Grouped atoms inherit their group's molecule, and ungrouped atoms may have
an explicitly declared atom-aligned molecule index. A builder can initialize
missing molecule membership from a selected chemical partition during
construction. Later connectivity edits do not repeat that initialization or
change declared stable molecules.

## Entity inference

Entities are derived from rebuilt molecule information. Molecules sharing the
same inferred semantic identity may map to one entity; water molecules are
grouped according to the native entity rules. Entity inference must use local
topology evidence and must not fetch external chemical metadata.

## Precision and units

Native `Structures` stores coordinates and box vectors as read-only `float64`
arrays in nm behind quantity-returning properties. Time is stored in ps.

The default kernel boundary is double precision. Selected execution paths can
use `molsysmt.configure.precision = "single"`, so documentation and tests must
state when single precision is supported and use tolerances appropriate to that
path. Trajectory file precision is format- and writer-dependent; it is not
correct to state that every XTC or DCD value is always stored in one universal
dtype.

## Rebuild discipline

Native rebuild functions use only evidence already present in their owning
native domain and explicitly supplied context. They must not call public
dispatchers or enrich the system from network services. Chemical graph
reconstruction belongs to ChemicalStates; inventory reconstruction belongs to
Topology. Component labels may use explicit stable context without redefining
molecules. Group-based molecule inference consumes represented group/chain
membership, and entity inference consumes the resulting stable molecules.
