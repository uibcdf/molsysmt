(user-tools-interactions)=
# Interactions

`molsysmt.Interactions` stores observations from one analysis method over a
molecular system. It supports hydrogen-bond triples, disulfide candidate pairs,
ring groups, and relations with more participants. The class is experimental.
Detectors retain their established outputs by default; the disulfide
candidate detector can also return an `Interactions` analysis explicitly.

- {doc}`result` — building, querying, and saving sparse interaction results.

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :hidden:

   result
```
