# OpenMM OBC1 regression reference

The small PDB and force vectors are retained from OpenMM commit
`ba0aa236ac4d07241382869604c4d2ea58c4f3f5`. See
[the upstream numerical test](https://github.com/openmm/openmm/blob/ba0aa236ac4d07241382869604c4d2ea58c4f3f5/wrappers/python/tests/TestForceField.py#L473).
The JSON records original paths, hashes, units and that test's vector tolerances.
PDB coordinates are in angstroms; reference forces are in kJ/mol/nm. Only trailing line padding was normalized in the PDB; atom/coordinate fields
are unchanged. The XML force array was projected to JSON.

This is a frozen upstream validation fixture, not a new independent Amber run.
Upstream identifies AmberPrmtopFile as its comparison construction route but
retains no generation command/version here. The data verify the actual OBC1
force response through MolSysMT and require no sibling checkout at test time.
The applicable upstream notice is retained in OPENMM_LICENSE.txt.
