(user-foundations-governance-argument-digestion)=
# Argument Digestion & Passports

Argument digestion is MolSysMT's centralized input validation and normalization protocol managed through the **ArgDigest** framework.

---

## The `@digest` Decorator

Public API functions in MolSysMT are wrapped with the `@digest` decorator from ArgDigest ([https://www.uibcdf.org/argdigest](https://www.uibcdf.org/argdigest)). When a user calls a public function, the decorator automatically performs:

- **Selection Interpretation**: Converts selection strings, atom indices, boolean masks, or query objects into canonical index lists.
- **Form Normalization**: Resolves input representations and validates structure indices.
- **Unit & Shape Checking**: Ensures coordinate arrays, box vectors, and physical quantities satisfy required dimensions.

---

## What is `skip_digestion`?

For ultra-high-frequency execution—such as running a distance calculation inside a loop with millions of iterations—evaluating argument digestion on every single call adds measurable Python overhead.

Public functions in MolSysMT accept the **`skip_digestion=True`** argument to bypass the `@digest` wrapper completely:

- **What You Gain**: Maximum raw execution speed (up to **20x–30x speedup**), matching raw compiled kernel performance.
- **What You Lose**: Automatic selection parsing, type checking, unit conversions, and shape validation. Inputs must be pre-validated and formatted in canonical internal types (`nm` arrays, integer index arrays).

### Code Example: Using `skip_digestion`

```python
import molsysmt as msm

# Standard public call (full validation, selection parsing, unit wrapping)
distances = msm.structure.get_distances(system, selection='all')

# High-frequency loop pass (bypassing digestion overhead)
# System coordinates must be pre-converted to canonical NumPy arrays in nanometers
raw_coords = msm.get(system, element='system', coordinates=True, skip_digestion=True)

for i in range(1_000_000):
    # Maximum execution speed inside tight loop
    dist = msm.structure.get_distances(raw_coords, skip_digestion=True)
```

---

## Validation Passports (`ValidatedPayload`)

In addition to `skip_digestion=True`, ArgDigest provides the **Passport Protocol**:

- **Normalizing Passports**: When a system is validated once, `argdigest` issues a `ValidatedPayload` passport.
- **Bypassing Validation**: Downstream functions recognize `ValidatedPayload` passports and skip redundant shape and selection parsing automatically.
