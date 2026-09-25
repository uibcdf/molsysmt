# Argument Digestion Architecture

MolSysMT uses **ArgDigest** (`@digest` and `@arg_digest`) to enforce input contracts, argument normalization, and error reporting across the public API without compromising execution speed.

---

## 1. Validated Boundary Philosophy

MolSysMT strictly distinguishes between **public API boundaries** and **internal execution paths**:

- **Public Functions**: Every function exposed to users (e.g. in `molsysmt.*`) is decorated with `@digest`. The decorator intercepts arguments, validates types and shapes, resolves selection strings, casts identifiers, and ensures physical units meet library standards before the function body executes.
- **Private and Internal Functions**: Functions in `_private/` or internal helpers must **never** be decorated with `@digest`.
- **Trusted Delegation**: When a public function delegates work to another function whose contract is already satisfied, it explicitly passes `skip_digestion=True` to bypass redundant validation:

```python
# Boundary call (digestion active)
def public_algorithm(molecular_system, selection='all', skip_digestion=False):
    # Internal delegation (digestion bypassed)
    return internal_worker(molecular_system, selection=selection, skip_digestion=True)
```

---

## 2. Standard Digestion Arguments

Public functions consistently accept and process standardized argument conventions:

| Argument | Purpose | Digestion Rule |
| :--- | :--- | :--- |
| `molecular_system` | Input system | Validates recognized form item, file path, or string representation |
| `selection` | Atom or element filter | Resolves string syntax, list of integers, or array; converts to 0-based indices |
| `structure_indices` | Coordinate frame filter | Resolves integer list, slice, or `'all'` into 0-based structure indices |
| `syntax` | Grammar for `selection` | Validates selection engine (`'MolSysMT'`, `'MDTraj'`, `'NGLView'`, etc.) |
| `to_form` | Conversion target | Validates supported destination form name |
| `skip_digestion` | Validation bypass | Boolean flag; defaults to `False` on public APIs |

---

## 3. Fast-Track and Performance Safety

Argument digestion validates inputs in microseconds. Because validation occurs once at the public entry point, compute-intensive loops and internal algorithms execute at native C/Numba/Rust speed with pure arrays and trusted parameters.
