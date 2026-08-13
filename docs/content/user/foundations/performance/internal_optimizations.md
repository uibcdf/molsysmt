(user-foundations-performance-internal-optimizations)=
# Internal Optimizations

To achieve maximum throughput in high-frequency internal loops, MolSysMT implements low-overhead optimization protocols that bypass redundant argument validation and unit conversions.

---

## Validated boundaries

The public MolSysMT API validates input types, selections, and shapes using the `@digest` decorator from `argdigest`. While essential for user safety, evaluating these rules inside loops executed millions of times introduces overhead.

MolSysMT pays that cost at clear public boundaries. Preparation helpers next to the
native kernels extract canonical, unit-free arrays without turning the low-level kernel
layer into another user-facing validation surface. A controlled internal delegation may
use `skip_digestion=True` only after the caller has established the complete callee
contract. MolSysMT has no value-passport protocol.

---

## Fast-Track Physical Units (`puw.fast_track`)

Physical unit enforcement via `pyunitwizard` ensures dimensional safety across MolSysMT. For canonical internal units (`nanometers` for length, `picoseconds` for time, `elementary charge` for charge), MolSysMT registers **Fast-Track handlers** in `puw.fast_track`, allowing instant unit stripping and re-wrapping without full dimensional AST parsing.

---

## Digestion Bypass and Zero-Copy Array Views

- **Digestion Bypass (`skip_digestion=True`)**: Controlled internal calls may skip the public wrapper only when all input invariants are already established.
- **Zero-Copy Views**: Form adapters share NumPy array memory pointers and strided views directly without duplicating heavy coordinate data in memory.
