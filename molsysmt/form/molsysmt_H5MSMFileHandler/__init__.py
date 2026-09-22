# Form metadata and export initialization retain their established import order.
# isort: off
from molsysmt._private.argdigest import arg_digest

form_name = "molsysmt.H5MSMFileHandler"
form_type = "class"
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = "molsysmt.Structures"
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = True

_convert_to = {
    "molsysmt.H5MSMFileHandler": "to_molsysmt_H5MSMFileHandler",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "nglview.NGLWidget": "to_nglview_NGLWidget",
}
_heavy_support = {
    "coordinates": True,
    "box": True,
}

from .is_form import is_form  # noqa: E402
from .has_attribute import has_attribute  # noqa: E402
from . import iterators  # noqa: E402
from .iterators import StructuresIterator  # noqa: E402

from .attributes import attributes  # noqa: E402
from .copy import copy  # noqa: E402
from .add import add  # noqa: E402
from .merge import merge  # noqa: E402
from .append_structures import append_structures  # noqa: E402
from .get_topological_attributes import *  # noqa: E402, F403
from .get_structural_attributes import *  # noqa: E402, F403
from .set import *  # noqa: E402, F403
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


@arg_digest(form=form_name)
def extract(
    item,
    selection="all",
    structure_indices="all",
    syntax="MolSysMT",
    output_filename=None,
    copy_if_all=True,
    skip_digestion=False,
):
    from molsysmt.basic import extract as msm_extract

    return msm_extract(
        item,
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
        output_filename=output_filename,
        copy_if_all=copy_if_all,
        skip_digestion=True,
    )
