# Conversion execution coverage

This operational guide accompanies uibcdf/molsysmt#181. Reachability evidence,
conversion fidelity and scientific accuracy are distinct claims.

## Inventory and execution

The declared graph comes from each form adapter's `_convert_to` mapping.
Discovery temporarily enables all capabilities and restores the caller's policy;
installed optional providers must not silently change the declared inventory.

```bash
# Check the plan against the graph; does not execute converters
python devtools/scripts/audit_conversion_execution.py --json

# Execute the resident-native profile, including direct and public routes
python -m pytest tests/conversion_truth/test_declared_native_edges.py --receptor=llm -n 12

# Exercise the inventory's adversarial controls
python -m pytest devtools/tests/test_audit_conversion_execution.py --receptor=llm
```

`devtools/data/conversion_execution_baseline.json` defines the
`resident-native-engines-v2` profile: thirteen native containers/dictionary
forms and four resident MDTraj/OpenMM forms. The original native-v1 subset
remains covered.
Every currently declared direct edge between its source/target forms becomes a
parametrized case. A small fresh four-atom, two-structure system supplies each
input; domain fixtures include mechanics parameters and a nonempty interaction
analysis. External water fixtures are built with their providers' own topology
APIs and literal coordinates. Dictionary fixture preparation is not an independent
fidelity oracle. Topology-only sources receive explicit coordinate quantities for
coordinate-bearing targets; a topology alone is not treated as a trajectory.

Each case calls the declared converter with normal argument digestion, then
calls public `convert` with a separately prepared source. Both must return the
declared target form. No runtime exceptions are converted into skips or accepted
failures. Two adversarial controls prove that a broken callable or wrong output
form fails this check. Existing fidelity suites add their separate assertions.

## Coverage debt

Edges outside the profile are explicitly listed by source and target, with a
reason, in `accepted_unexecuted_edges`. They are coverage debt, not demonstrated
impossible routes, and existing adapter tests may exercise some of them.
The audit rejects an unaccounted edge and stale debt. New edges within the
profile become cases automatically. Extending a profile requires a real source
fixture and removal of the corresponding debt; do not regenerate the baseline
to absorb a failure. The audit reports planned cases, never successful execution.

Further profiles need file/string fixtures, other external objects and
separately marked network cases. Optional dependencies should produce clear
skips only when genuinely unavailable; a provider-complete qualification must
report those skips explicitly. The thirteen-form native subset needs no external provider; the expanded cases
skip only when MDTraj/OpenMM is genuinely unavailable during setup. Conversion
exceptions are never interpreted as optional-provider skips.
Neither a green inventory nor this bounded profile establishes that every
conversion in MolSysMT executes. See [form adapter testing](testing_form_adapters.md)
for value, unit, hierarchy and loss checks.
