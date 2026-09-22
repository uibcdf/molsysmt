from molsysmt._private.argdigest import arg_digest

form_name = "nglview.NGLWidget"
form_type = "class"
form_info = [""]

piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = "molsysmt.Structures"
piped_any_attribute = "molsysmt.MolSys"
bonds_are_explicit = True
bonds_can_be_computed = True

_convert_to = {
    "nglview.NGLWidget": "to_nglview_NGLWidget",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "openmm.Topology": "to_openmm_Topology",
    "string:amino_acids_1": "to_string_amino_acids_1",
    "string:amino_acids_3": "to_string_amino_acids_3",
    "string:pdb_text": "to_string_pdb_text",
}

# Form metadata and export initialization must retain their established order.
# The wildcard imports expose the form's iterator and getter functions.
# isort: off
from .is_form import is_form  # noqa: E402
from .has_attribute import has_attribute  # noqa: E402
from .attributes import attributes  # noqa: E402
from .extract import extract  # noqa: E402
from .add import add  # noqa: E402
from .append_structures import append_structures  # noqa: E402
from .copy import copy  # noqa: E402
from .merge import merge  # noqa: E402
from .iterators import *  # noqa: E402, F403
from .get_topological_attributes import *  # noqa: E402, F403
from .get_structural_attributes import *  # noqa: E402, F403
# isort: on


@arg_digest(form=form_name)
def get(
    item,
    element="system",
    selection="all",
    syntax="MolSysMT",
    structure_indices="all",
    output_type="values",
    skip_digestion=False,
    **kwargs,
):
    from molsysmt.basic import get as msm_get

    return msm_get(
        item,
        element=element,
        selection=selection,
        syntax=syntax,
        structure_indices=structure_indices,
        output_type=output_type,
        skip_digestion=True,
        **kwargs,
    )


@arg_digest(form=form_name)
def set(
    item,
    element="system",
    selection="all",
    syntax="MolSysMT",
    structure_indices="all",
    skip_digestion=False,
    **kwargs,
):
    from molsysmt.basic import set as msm_set

    return msm_set(
        item,
        element=element,
        selection=selection,
        syntax=syntax,
        structure_indices=structure_indices,
        skip_digestion=True,
        **kwargs,
    )
