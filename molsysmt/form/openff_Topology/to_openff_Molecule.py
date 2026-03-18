from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError

@arg_digest(form='openff.Topology')
def to_openff_Molecule(item, skip_digestion=False):

    molecules = list(item.molecules)
    if len(molecules) == 1:
        return molecules[0]
    raise NotImplementedMethodError(
        "Cannot convert an openff.Topology with multiple molecules to a single openff.Molecule."
    )
