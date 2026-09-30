(user-tools-interactions)=
# Interactions

`molsysmt.Interactions` stores observations from one analysis method over a
molecular system. It supports hydrogen-bond triples, disulfide candidate pairs,
ring groups, and relations with more participants. The class is experimental.
Detectors retain their established outputs by default; both hydrogen-bond
and the disulfide candidate detectors can also return an `Interactions` analysis
explicitly.

The new experimental ionic detector returns sparse analyses by default, using
selected-state formal-charge centers and an explicit minimum-distance cutoff.

- {doc}`result` — building, querying, and saving sparse interaction results.
- {doc}`get_ionic_interactions` — calculating scoped formal-charge contacts.

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :hidden:

   result
   get_ionic_interactions
```
