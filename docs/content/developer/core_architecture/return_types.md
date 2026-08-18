(developer-return-types)=

# Return Types: what the datum is decides how it comes back

MolSysMT returns two kinds of thing, and which one you are holding is decided by **what the datum is**, not by what shape it happens to have.

:::{admonition} The rule
:class: tip

- **Numeric physical magnitudes** — the things you compute on — come back as a `numpy.ndarray` with an explicit `dtype`, or as a PyUnitWizard `Quantity` when they carry units.
- **Identifiers, labels, categories and relations** come back in Python containers, holding **native Python scalars**: `int`, `float`, `str`, `bool`.
- **A single count or measure** comes back as a native scalar, or a `Quantity` if it has units.
:::

The normative statement lives in `devguide/INTERFACES.md`, section *Scalar types in returned values*. This page explains the reasoning, because the reasoning is what settles a case the rule does not name.

---

### 1. Shape decides nothing

This is the tempting mistake: to look at `bonded_atom_pairs`, see *n* rows of exactly two integers, and conclude that something so rectangular ought to be an array.

It ought not. `bonded_atom_pairs` is a **relation between atoms** — a list of bonds. Nobody multiplies it by a rotation matrix or takes its mean. It is a collection of discrete items you iterate and inspect, and a `list` is the honest container for that. `coordinates` is the opposite case: a numeric magnitude that exists to be computed on, so it is a `Quantity` wrapping a `float64` array.

The library already draws that line consistently:

| Returned as `ndarray` / `Quantity` | Returned as a Python container |
| :--- | :--- |
| `coordinates`, `box`, `b_factor`, `occupancy` | `atom_index`, `atom_name`, `atom_id`, `atom_type` |
| numeric magnitudes, `float64` | `group_name`, `chain_id`, `bond_order`, `bond_type` |
| | `bonded_atom_pairs` — rectangular, and correctly a list |

There is a second reason not to reason from shape: **shape is a property of the data, not of the attribute**. `component_index` per molecule is rectangular in every system where each molecule has one component, and ragged the moment one does not. An attribute cannot switch container between one molecular system and the next without becoming impossible to program against.

### 2. Why the scalars inside must be native

Whatever the container, a NumPy scalar inside a Python one is not a middle ground between list and array. NumPy's advantages come from the **array**: contiguous memory and vectorised operations over a typed buffer. A scalar extracted into a Python container has left that buffer behind and carries only NumPy's object overhead.

Measured over 200 000 integers:

| Container | Memory | `sum()` |
| :--- | ---: | ---: |
| `list` of `np.int64` | 8.02 MB | 7.7 ms |
| `list` of `int` | 7.22 MB | 2.5 ms |
| `ndarray` of `int64` | **3.20 MB** | **0.2 ms** |

A `list` of `np.int64` is worse than a `list` of `int` on both axes, and far worse than the array on both. It is not a middle option; it is the worst of the three.

### 3. Three consequences that make this a contract

**Serialisation.** `json.dumps` and `yaml.safe_dump` raise on a NumPy scalar. A user who dumps what a public function returned gets an exception:

```python
json.dumps(msm.get(molsys, element='system', bonded_atom_pairs=True))
# TypeError: Object of type int64 is not JSON serializable
```

**Type identity.** Under NumPy 2.x, `isinstance(np.int64(1), int)` is `False`. Downstream code that validates with `isinstance` — in a user's script, or in a sister library such as TopoMT or PharmacophoreMT — rejects values that MolSysMT's own docstrings call integers.

**Range.** Python's `int` has arbitrary precision. `np.int64` overflows silently.

Nothing is lost in exchange. `np.array` over a list of Python `int` infers `int64`, and both types index an array identically; there is no `dtype` to preserve in a container that holds one Python object per element.

### 4. How to comply

Prefer `ndarray.tolist()` over iterating an array in Python, and `.item()` over indexing out a single element. `tolist()` converts NumPy scalars to native types recursively in C, in one pass, and never materialises the boxed scalars — which is why it is roughly six times faster than building the list and converting it afterwards. It is also how the flat attribute paths already produce `list[int]` today.

Do not normalise at the return boundary instead. Walking every returned structure in Python to find out whether anything needs fixing costs more than doing the conversion at the source even when there is nothing to fix. The correctness net belongs in the test suite, where it costs nothing at run time.

The failure mode this rule prevents is a **mixed container**: some elements `int`, others `np.int64`. It appears when a structure is assembled element by element from arrays instead of through `tolist()`, and it is not cosmetic — the elements of one collection then answer `isinstance` differently from one another.

:::{seealso} Related
:class: dropdown

- {doc}`declarative_serialization_forms`: the YAML formats that require natively serialisable values.
- {doc}`pyunitwizard`: how physical magnitudes are returned as `Quantity`, the other half of the return contract.
- {func}`molsysmt.basic.get`: the public entry point where most of these values are delivered.
:::
