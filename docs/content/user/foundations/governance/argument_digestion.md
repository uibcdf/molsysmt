(user-foundations-governance-argument-digestion)=
# Argument Digestion & Passports

Argument digestion is MolSysMT's centralized input validation and normalization protocol managed through the **`argdigest`** framework.

---

## The `@digest` Decorator

Public API functions in MolSysMT are wrapped with the `@digest` decorator from `argdigest`. When a user calls a public function, the decorator automatically performs:

- **Selection Interpretation**: Converts selection strings, atom indices, boolean masks, or query objects into canonical index lists.
- **Form Normalization**: Resolves input representations and validates structure indices.
- **Unit & Shape Checking**: Ensures coordinate arrays, box vectors, and physical quantities satisfy required dimensions.

---

## High-Frequency Fast Paths

While `@digest` provides complete input safety for user calls, evaluating digestion rules inside nested loops executed millions of times introduces overhead. MolSysMT provides two mechanisms for high-frequency internal execution:

- **Digestion Bypass (`skip_digestion=True`)**: Internal functions accept `skip_digestion=True` to bypass public wrapper overhead completely when caller parameters are pre-validated.
- **Validation Passports (`ValidatedPayload`)**: When an input payload is validated once, `argdigest` issues a `ValidatedPayload` passport. Downstream internal functions recognize the passport and skip redundant shape and selection parsing.
