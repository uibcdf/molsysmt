(developer-return-types)=

# Return Types: the container decides

MolSysMT returns two kinds of thing, and the kind determines the scalar type inside it.

:::{admonition} The rule
:class: tip

- **Rectangular, homogeneous data** → `numpy.ndarray` with an explicit `dtype`, or a PyUnitWizard `Quantity` wrapping one.
- **Ragged, nested, `set` or `dict` data** → **native Python scalars**: `int`, `float`, `str`, `bool`.
:::

The normative statement lives in `devguide/INTERFACES.md`, section *Scalar types in returned values*. This page explains why, because the reasoning is what tells you what to do in a case the rule does not name explicitly.

---

### 1. Why a NumPy scalar in a Python list is not a compromise

It is tempting to read `list[np.int64]` as something between a list and an array — a list that kept a bit of NumPy. It is not. NumPy's advantages come from the **array**: contiguous memory and vectorised operations over a typed buffer. A scalar extracted into a Python container has left that buffer behind and carries only NumPy's object overhead.

Measured over 200 000 integers:

| Container | Memory | `sum()` |
| :--- | ---: | ---: |
| `list` of `np.int64` | 8.02 MB | 7.7 ms |
| `list` of `int` | 7.22 MB | 2.5 ms |
| `ndarray` of `int64` | **3.20 MB** | **0.2 ms** |

A `list` of `np.int64` is worse than a `list` of `int` on both axes, and far worse than the array on both. It is not a middle option; it is the worst of the three.

So the question is never "NumPy or Python?" in the abstract. It is: **can this data live in an array?** If it can, put it in one and keep the `dtype`. If it cannot — because rows have different lengths, or the result is a set, or it is a mapping — then you are in Python's world already, and NumPy scalars are pure cost.

### 2. Three consequences that make this a contract

**Serialisation.** `json.dumps` and `yaml.safe_dump` raise on a NumPy scalar. A user who dumps what a public function returned gets an exception:

```python
json.dumps(msm.get(molsys, element='system', bonded_atom_pairs=True))
# TypeError: Object of type int64 is not JSON serializable
```

**Type identity.** Under NumPy 2.x, `isinstance(np.int64(1), int)` is `False`. Downstream code that validates with `isinstance` — in a user's script, or in a sister library such as TopoMT or PharmacophoreMT — rejects values that MolSysMT's own docstrings call integers.

**Range.** Python's `int` has arbitrary precision. `np.int64` overflows silently.

### 3. Nothing is lost by choosing native scalars

The usual objection is that native types discard `dtype` information. In a ragged container there is no `dtype` to discard: the container holds one Python object per element either way.

```python
np.array([1, 2, 3]).dtype     # int64 — recovered on the way back
a[int(1)] == a[np.int64(1)]   # both index identically
```

### 4. How to comply

Prefer `ndarray.tolist()` over iterating an array in Python. `tolist()` converts NumPy scalars to native types recursively and preserves the shape, which is exactly the required behaviour, and it is how the flat attribute paths already produce `list[int]` today.

The failure mode this rule prevents is a **mixed container**: some elements `int`, others `np.int64`. It appears when a structure is assembled element by element from arrays instead of through `tolist()`, and it is not cosmetic — the elements of one collection then answer `isinstance` differently from one another.

:::{seealso} Related
:class: dropdown

- {doc}`declarative_serialization_forms`: the YAML formats that require natively serialisable values.
- {doc}`pyunitwizard`: how physical magnitudes are returned as `Quantity`, the other half of the return contract.
- {func}`molsysmt.basic.get`: the public entry point where most of these values are delivered.
:::
