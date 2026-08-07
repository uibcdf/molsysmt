(user-foundations-performance-internal-optimizations)=
# Fast-Track & Passports

To achieve maximum throughput in high-frequency internal loops, MolSysMT implements low-overhead optimization protocols that bypass redundant argument validation and unit conversions.

---

## Validation Passports (`ValidatedPayload`)

The public MolSysMT API validates input types, selections, and shapes using the `@digest` decorator from `argdigest`. While essential for user safety, evaluating these rules inside loops executed millions of times introduces overhead.

MolSysMT solves this with the **Passport Protocol**:

- **Normalizing Passports**: When a system is validated once, `argdigest` issues a `ValidatedPayload` passport.
- **Bypassing Validation**: Internal functions recognize `ValidatedPayload` passports and bypass redundant type and shape checks, accelerating nested workflows.

---

## Fast-Track Physical Units (`puw.fast_track`)

Physical unit enforcement via `pyunitwizard` ensures dimensional safety across MolSysMT. For canonical internal units (`nanometers` for length, `picoseconds` for time, `elementary charge` for charge), MolSysMT registers **Fast-Track handlers** in `puw.fast_track`, allowing instant unit stripping and re-wrapping without full dimensional AST parsing.

---

## Digestion Bypass and Zero-Copy Array Views

- **Digestion Bypass (`skip_digestion=True`)**: Internal high-frequency functions accept `skip_digestion=True` to skip public wrapper overhead completely.
- **Zero-Copy Views**: Form adapters share NumPy array memory pointers and strided views directly without duplicating heavy coordinate data in memory.
