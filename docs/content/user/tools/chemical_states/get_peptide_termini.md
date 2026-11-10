(Tutorial_Get_peptide_termini)=
# Getting peptide termini

*Recognizing observed peptide ends without sorting inventory or ID labels.*

Use {func}`molsysmt.chemical_states.get_peptide_termini` to inspect the ends of
a stored peptide backbone. Supply any supported molecular-system form with
stable atom, group and chain context and a chemical state containing bonds.
Coordinates are unnecessary. Topology alone cannot provide chemical endpoints.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

See {func}`molsysmt.chemical_states.get_peptide_termini` for the complete argument
contract and a small executable peptide example.
:::

## Following stored bonds

The experimental `stored_backbone_connectivity` rule recognizes unique named
N-CA-C motifs and follows the stored inter-group C-N bonds in their chemical
direction. Each examined chain must form one connected path or cycle covering
its amino-acid groups. IDs are labels: numeric, repeated, insertion-code-like
or arbitrary string group IDs do not determine the result. Neither do atom or
group storage positions. Sulfur crosslinks do not order a peptide backbone.

A path has an N-side and a C-side endpoint. An attached ACE blocks the free
N side; attached NME, NHE or NH2 blocks the free C side. The recognized cap
must have the expected named connecting atom and an actual stored bond.
A neighboring cap label alone does not cap an endpoint. A cycle has no free
ends. Unknown end attachments, multiple partners, missing local backbone bonds,
disconnected paths and branches are refused rather than repaired or guessed.
The default `on_ambiguous='raise'` stops with a structural diagnostic. Choose
`on_ambiguous='report'` explicitly to retain unassessed chain rows, their reasons
and `unassessed_chain_indices`, alongside endpoints from other assessed chains.
Unassessed rows have no inferred order, cycle flag, cap flags or endpoints; their
group population is sorted only for source-index reporting. This explicit report
mode does not emit warnings or turn disconnected fragments into free peptides.

## Selecting context and reading indices

`selection` addresses source atoms, including numeric atom indices. Complete
chains containing selected amino-acid groups are examined first. The four flat
endpoint arrays then retain only endpoints whose amino-acid group intersects
the selection. Selecting one internal atom creates no new terminus.

The returned `n_terminal_group_indices` and `c_terminal_group_indices` identify
free endpoints; `n_capped_group_indices` and `c_capped_group_indices` identify
blocked endpoints. All are int64 source group positions, including typed empty
arrays. Each `chains` row retains the complete ordered amino-acid population,
the source chain position, assessment status, cap flags and endpoint positions. Assessed cyclic rows use
None for both endpoint positions. Complete context rows are not a selection of
new terminal groups.

Choose `chemical_state` explicitly when the reference is absent or ambiguous.
`chemical_state='structure'` requires one state across `structure_indices`.
Neither request changes the reference. Structure indices scope association and
spatial selection; there is no per-structure endpoint occurrence calculation.
Numeric/all modular H5MSM queries read chemistry without the structural series
or saved analyses. A spatial query may require coordinate access.

## Distinguishing recognition from chemical preparation

This rule reads an observed named backbone. It does not certify bond order,
valence, stereochemistry, protonation or global completeness. Explicit dative
edges are excluded. Legacy untyped stored edges remain admitted and their
count appears in `evidence`, alongside the state's completeness and provenance.
The report records its method, selected state and original producer version.
It stores no coordinate copy and modifies no molecular domain.

{func}`molsysmt.build.get_missing_terminal_cappings` reuses this rule to report
missing OXT at selected free C-side groups. Its legacy dictionary retains the
assessed subset and emits `UnassessedPeptideBackboneWarning`
(`MSM-WARN-BUILD-003`) for every omitted chain; an empty dictionary under that
warning does not establish complete terminal chemistry. Its numeric selection remains
**group indices**, while the recognizer's and terminal adder's numeric selections
are **atom indices**. {func}`molsysmt.build.add_missing_terminal_cappings` uses
the same endpoints for local completion and cap anchors. Explicit capping
currently requires one linear backbone per selected covalent component;
crosslinked components containing several backbones are refused. Geometry
placement does not assign a complete chemical state or a force-field model.

:::{seealso}
:class: dropdown

**Related Tools & References**

- {ref}`Getting covalent paths <Tutorial_Get_covalent_paths>` for general
  ordered patterns over stored bonds.
- {ref}`Getting missing terminal cappings <Tutorial_Get_missing_terminal_cappings>`
  for the separate missing-OXT assessment.
- {ref}`Adding missing terminal cappings <Tutorial_Add_missing_terminal_cappings>`
  for explicit preparation and its geometry limits.
:::

## Reading the bundled incomplete 1BRS model

In the fixed bundled model, chains 3 and 4 have two observed backbone fragments
each, separated between source labels 63 and 66. Those labels describe the file;
the recognizer does not use them to reconnect the missing chemistry or choose
one fragment end. Its explicit partial report marks both chains unassessed. The
legacy native adder retains the five existing OXT atoms while repairing supported
heavy atoms; PDBFixer has an independent reconstruction profile and can add OXT at
group 412. Their counts are not interchangeable evidence of the same method.
