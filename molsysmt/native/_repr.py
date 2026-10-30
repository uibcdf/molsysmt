"""Summarizing stored native metadata without validation, rendering or I/O."""

from numbers import Integral


def summary(instance, *, class_name=None, **fields):
    """Format bounded scalar fields without invoking a payload's representation."""

    def scalar(value):
        if value is None or isinstance(value, bool):
            return repr(value)
        if isinstance(value, Integral):
            return str(int(value))
        if isinstance(value, str):
            return repr(value[:48] + ("..." if len(value) > 48 else ""))
        return "<assigned>"

    contents = ", ".join(f"{name}={scalar(value)}" for name, value in fields.items())
    return f"{class_name or type(instance).__name__}({contents})"


def size(value):
    """Read a stored container length without iterating or converting it."""
    return None if value is None else len(value)


def structure_dimensions(structures):
    """Read the first stored axes without calling the alignment validator."""
    if structures is None:
        return None, None
    data = vars(structures)
    if not data:
        return None, None
    atom_fields = ("_coordinates", "_velocities", "_b_factor", "_occupancy")
    n_atoms = None
    for name in atom_fields:
        value = data.get(name)
        if value is not None:
            shape = getattr(value, "shape", ())
            if len(shape) >= 2:
                n_atoms = shape[1]
                break
    n_structures = 0
    for name in (
        *atom_fields,
        "structure_id",
        "_time",
        "_box",
        "alternate_location",
        "_temperature",
        "_potential_energy",
        "_kinetic_energy",
    ):
        value = data.get(name)
        if value is not None:
            shape = getattr(value, "shape", None)
            n_structures = shape[0] if shape else len(value)
            break
    return n_structures, n_atoms


def reference_index(states):
    """Describe a resolvable reference without restoring or selecting a state."""
    if states is None:
        return None
    records = vars(states).get("_states")
    if records is None:
        return None
    count = len(records)
    if count == 1:
        return 0
    index = vars(states).get("_reference_index")
    if (
        isinstance(index, Integral)
        and not isinstance(index, bool)
        and 0 <= index < count
    ):
        return int(index)
    return None


def topology_fields(topology):
    """Count only stable inventory, without resolving a chemical owner."""
    return dict(
        n_atoms=size(vars(topology).get("atoms")),
        n_groups=size(vars(topology).get("groups")),
        n_molecules=size(vars(topology).get("molecules")),
        n_chains=size(vars(topology).get("chains")),
    )


def system_fields(system):
    """Read dimensions from present domains without validation or public dispatch."""
    data = vars(system)
    topology = data.get("_topology", data.get("topology"))
    states = data.get("_chemical_states_domain")
    structures = data.get("_structures", data.get("structures"))
    analyses = data.get("_interactions", {})
    first_analysis = next(iter(analyses.values()), None)
    n_structures, n_atoms = structure_dimensions(structures)
    if topology is not None:
        n_atoms = len(topology.atoms)
    elif states is not None:
        n_atoms = states._n_atoms
    elif n_atoms is None and first_analysis is not None:
        n_atoms = first_analysis.n_atoms
    if n_structures is None and first_analysis is not None:
        n_structures = first_analysis.n_structures
    return dict(
        n_atoms=n_atoms,
        n_structures=n_structures,
        topology=topology is not None,
        structures=structures is not None,
        n_chemical_states=None if states is None else len(states._states),
        n_interaction_analyses=len(analyses),
        molecular_mechanics=data.get("molecular_mechanics") is not None,
    )
