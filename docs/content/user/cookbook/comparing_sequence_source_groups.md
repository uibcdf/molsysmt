(Cookbook_Sequence_source_groups)=
# Comparing sequences with source groups

*Comparing selected sequences while retaining their molecular correspondence.*

A capped protein and an extracted uncapped protein can have identical sequence
letters with different group indices. Use those source maps when interpreting
an alignment or annotating the systems in a viewer.

:::{versionadded} 1.0.0
:::

1. Choose the query and reference systems and their independent selections.
   Group selections refer to each source inventory; they need not have the same
   group count or labels.
2. Calculate `msm.topology.get_sequence_identity`. The three outputs are the
   query-normalized percentage and corresponding source group-index lists.
   Molecular groups that supply no amino-acid letter contribute to neither
   list nor the denominator. Empty sequence selections raise an argument error.
3. Pair the returned lists positionally to annotate the original sources.
   For capped pentalanine compared with its extracted amino-acid inventory,
   identity is 100%, query indices are `[1, 2, 3, 4, 5]` and reference indices
   are `[0, 1, 2, 3, 4]`. Do not treat either list as group IDs.
4. Preserve comparison direction when reporting the percentage. The denominator
   is query length, so reversing sequences with different lengths can change it.
   Biopython supplies alignment; counting is adapted from Ensembler with this
   explicit normalization difference. Ackredit can record that runtime credit.

The {ref}`identity tutorial <Tutorial_Get_sequence_identity>` executes this
complete capped/extracted comparison. The {ref}`Topology foundation <user-foundations-native-world-classes-molsysmt-topology>`
explains the distinction between molecular groups and sequence positions.


For the optional Biopython object conversion, the source
`amino_acids_3:AceAlaGlyNme` converts to `Seq("AG")`. Selecting original groups
`[2, 1, 2, 0]` first produces `Seq("GAG")`: the selected cap contributes no
letter. An empty selection produces an empty Seq/SeqRecord, whereas an empty
alignment selection still rejects. Explicit prefixes are representation markers,
not sequence characters. Native one/three-letter translation and extraction do
not require Biopython; only the requested object output and alignment do.


## Inspecting FASTA sources

For submitted FASTA libraries, first inspect
`msm.form.file_fasta.read_records(path)` (or `parse_records(text)`) before
conversion or alignment. Retain each source record index, full header, raw
record and character span. Repeated and empty proposals remain distinct;
scientific admission belongs to your workflow. The joined sequence preserves
spaces, case, leading M and symbols, so an admitted molecular sequence view
must be chosen explicitly. Source record indices are separate from molecular
group indices and alignment positions. See
{ref}`FASTA ingestion <Tutorial_Form_file_fasta>` for the complete contract.


## Choosing native inventory

After admitting a sequence view, convert it to `molsysmt.Topology` or
`molsysmt.MolSys` when you need native group names and molecule membership.
The one-/three-letter string routes require no Biopython; FASTA conversion
retains its existing optional normalized reader. Three-letter caps survive,
and each FASTA record remains a separate declared occurrence. Keep the raw
source report alongside the result when source attribution matters.

These outputs contain no representative CA atoms or coordinates. Choose a
separate atomic-construction workflow when required by a downstream method.
You can query and select represented groups and their parents without atoms:

```python
molsys = msm.convert("AGW", to_form="molsysmt.MolSys")
assert molsys.get(element="chain", group_index=True) == [[0, 1, 2]]
subset = msm.extract(molsys, element="group", selection=[2, 0])
assert subset.get(element="group", group_name=True) == ["TRP", "ALA"]
assert subset.topology.chain_groups == ((1, 0),)
```

The group table follows your requested extraction order; chain membership keeps
its source sequence order with remapped group indices. Choose `element="chain"`
when you want to retain a chain as a whole, including an empty record. FASTA
chains receive generated IDs `A`, `B`, ..., `Z`, `AA`, `AB`, ...; record headers
remain separate metadata. A global one-letter string cannot encode boundaries
between multiple molecules. The
{ref}`Topology foundation <user-foundations-native-world-classes-molsysmt-topology>`
explains the partial inventory, and {ref}`FASTA adapter <Tutorial_Form_file_fasta>`
documents its conversion contract.
