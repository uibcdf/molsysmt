"""Attach result-level bibliography and mirror successful use to Ackredit.

This bounded host adapter uses only Ackredit's public API. Portable contextual
capture is requested in uibcdf/ackredit#75; the host declarations here remain
scientific method metadata even after that provider capability arrives.
"""

from copy import deepcopy
from functools import wraps
from inspect import signature

from molsysmt._private.interaction_methods import resolve_method
from molsysmt._private.scientific_citations import ARTICLES, SOFTWARE


def _article(name, role):
    record = deepcopy(ARTICLES[name])
    return dict(id="doi:" + record["doi"], type="article", url="https://doi.org/" + record["doi"],
                **record, roles=[role])


def _bibliography(definition, software, parameters):
    """Produce detached records for this result, independent of session state."""
    items = []
    method = definition["method"]
    implementation = definition["implementation"]
    if method in ARTICLES:
        items.append(_article(method, "scientific_criterion"))
    reference = parameters.get("method_reference")
    if reference is not None:
        name = reference.get("software", "").lower().replace("*", "star")
        if name in ARTICLES:
            items.append(_article(name, "reference_implementation"))
        else:
            url = reference.get("documentation", reference.get("implementation"))
            if url:
                items.append(dict(id="reference:" + url, type="web", title=reference["software"] + " reference definition",
                                  url=url, roles=["reference_implementation"]))
    elif implementation in {"prolif", "cpptraj", "mdtraj", "mdtraj_geometry", "molstar_geometry"}:
        name = implementation.replace("_geometry", "")
        items.append(_article(name, "reference_implementation"))
    for name, version in sorted(software.items()):
        record = deepcopy(SOFTWARE.get(name, dict(title=name)))
        items.append(dict(id=f"software:{name}:{version}", type="software", **record,
                          version=version, roles=["executed_software"]))
    # A paper can play several roles, but is still one bibliographic work.
    unique = {}
    for item in items:
        if item["id"] in unique:
            unique[item["id"]]["roles"] = sorted(set(unique[item["id"]]["roles"] + item["roles"]))
        else:
            unique[item["id"]] = item
    return list(unique.values())


def attributed(family, fixed_method=None):
    """Wrap one completed scientific calculation, never an occurrence loop."""
    def decorate(function):
        call_signature = signature(function)
        target = function.__module__

        @wraps(function)
        def wrapped(*args, **kwargs):
            from molsysmt import __version__, _ackredit

            bound = call_signature.bind(*args, **kwargs)
            bound.apply_defaults()
            if fixed_method is None:
                definition = resolve_method(family, bound.arguments["method"],
                                            bound.arguments.get("profile"), caller=target)
            else:
                definition = dict(method=fixed_method, profile="native", implementation=fixed_method,
                                  definition=f"molsysmt.{family}.{fixed_method}.native@1")
            with _ackredit.scope(target) as provider:
                result = function(*args, **kwargs)
                if hasattr(result, "parameters"):
                    parameters, software = result.parameters, result.software
                elif hasattr(result, "data") and result.data.get("schema") == "molsysmt.interactions_dict":
                    parameters, software = result.data["parameters"], result.data["software"]
                elif isinstance(result, dict) and "donor_hydrogen_pairs" in result:
                    parameters, software = result, result["software"]
                else:
                    parameters, software = {}, {"molsysmt": __version__}
                items = _bibliography(definition, software, parameters)
                parameters.update(method=definition["method"], profile=definition["profile"],
                                  method_definition=definition["definition"])
                parameters["attribution"] = dict(schema="molsysmt.scientific_attribution@1",
                                                 target=target, items=items)
                _ackredit.credit(provider, items, target)
                return result

        return wrapped
    return decorate
