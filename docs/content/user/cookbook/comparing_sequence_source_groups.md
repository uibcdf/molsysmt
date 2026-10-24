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
