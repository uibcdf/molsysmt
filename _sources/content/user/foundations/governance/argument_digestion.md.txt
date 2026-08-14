(user-foundations-governance-argument-digestion)=
# Argument Digestion

Argument digestion is MolSysMT's centralized input validation and normalization protocol managed through the **ArgDigest** framework.

---

## The `@digest` Decorator

Public API functions in MolSysMT are wrapped with the `@digest` decorator from ArgDigest ([https://www.uibcdf.org/argdigest](https://www.uibcdf.org/argdigest)). When a user calls a public function, the decorator automatically performs:

- **Selection Interpretation**: Converts selection strings, atom indices, boolean masks, or query objects into canonical index lists.
- **Form Normalization**: Resolves input representations and validates structure indices.
- **Unit & Shape Checking**: Ensures coordinate arrays, box vectors, and physical quantities satisfy required dimensions.

---

## What is `skip_digestion`?

For high-frequency internal delegation, evaluating argument digestion repeatedly can add measurable Python overhead.

Public functions in MolSysMT accept the **`skip_digestion=True`** argument to bypass the `@digest` wrapper completely:

- **What You Gain**: Avoiding repeated Python-side validation after the complete contract has already been established.
- **What You Lose**: Automatic selection parsing, type checking, unit conversions, and shape validation. Inputs must be pre-validated and formatted in canonical internal types (`nm` arrays, integer index arrays).

There is deliberately no user-facing recipe for this bypass. Ordinary calls should
keep their default validation path. A MolSysMT implementation may use it only at a
private delegation point where the caller itself established the complete callee
contract.

---

## Trust boundary

MolSysMT does not use value passports or certification wrappers. The bypass applies to
the whole call, so its caller owns every type, shape, physical-unit, selection, and
cross-argument invariant. If any value still requires interpretation, use the normal
decorated call. This keeps one validation model instead of making users or digester
authors coordinate a second identity-based protocol.
