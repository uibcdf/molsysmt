from molsysmt.attribute.attributes import attributes as _catalogue
from molsysmt.form.molsysmt_MolSys.attributes import attributes as _molsys
from molsysmt.form.molsysmt_Topology.attributes import attributes as _topology

# Version 0.1 can carry chemical declarations. Instance availability separates
# that legacy reader from the pure stable-inventory 0.2 schema.
attributes = {
    name: flag
    or bool(_molsys.get(name))
    and (
        (_catalogue[name]["chemical_state"] or "bond" in name or "component" in name)
        and not _catalogue[name]["mechanical"]
    )
    for name, flag in _topology.items()
}
