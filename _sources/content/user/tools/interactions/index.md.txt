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
The experimental pi-pi detector uses declared aromatic rings, fitted planes,
and explicit distance, angle, offset and planarity cutoffs for its custom proposal.
Attributed ProLIF and Mol*/MDTraj geometric profiles are available separately.
The new hydrogen-bond entry point offers named per-structure scientific criteria;
its default sparse output is independent of the established Buch/Luzard–Chandler defaults.

- {doc}`get_metal_coordination` — observing directed metal-ligand proximity candidates.
- {doc}`get_water_bridges` — joining two simultaneous hydrogen bonds through indexed water.
- {doc}`get_hydrophobic_interactions` — calculating typed hydrophobic atom proximity.
- {doc}`get_halogen_bonds` — calculating four-role halogen geometry.
- {doc}`get_hbonds` — calculating attributed hydrogen-bond observations.
- {doc}`result` — building, querying, and saving sparse interaction results.
- {doc}`get_ionic_interactions` — calculating scoped formal-charge contacts.
- {doc}`get_pi_pi_interactions` — calculating parallel and edge-to-face ring geometry.
- {doc}`get_cation_pi_interactions` — reproducing ProLIF cation–π observations and examining a separate proposal.

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :hidden:

   get_metal_coordination
   get_water_bridges
   get_hydrophobic_interactions
   get_halogen_bonds
   result
   get_hbonds
   get_ionic_interactions
   get_pi_pi_interactions
   get_cation_pi_interactions
```
