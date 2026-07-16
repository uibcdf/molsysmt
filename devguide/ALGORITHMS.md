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

Components are covalently connected atom sets. Native component indices are
computed from the bond pairs and stored at atom level. Groups do not store a
canonical `component_index` column.

With no bonds, the connectivity routine determines the fallback component
partition. Callers must not infer semantic molecules from components without the
separate molecule-rebuild rules.

## Molecule inference

Molecule inference operates over ordered groups and their atom-level chain
membership. Polymer-like group types may continue the current molecule within a
chain. Standalone types (`ion`, `water`, and `small molecule`) start distinct
molecules. Chain changes and transitions between polymer and standalone classes
split molecules.

Component and molecule partitions are orthogonal: a covalent component may span
more than one semantic molecule.

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

Native rebuild functions use only evidence already present in the native
topology and canonical local tables. They must not call public dispatchers or
silently enrich the system from network services. Rebuild order matters because
later molecule and entity inference consumes earlier group, component, and chain
results.
