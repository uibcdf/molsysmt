"""Attach detached references for general graph/geometry tools at completion."""

from copy import deepcopy


def attach_graph_attribution(result, caller):
    """Credit methodological inspiration separately from executed software."""
    from molsysmt import _ackredit
    from molsysmt._private.scientific_citations import ARTICLES, SOFTWARE

    references = []
    for name in ("bell_zhang_2019", "meli_biggin_2020"):
        record = deepcopy(ARTICLES[name])
        references.append(
            dict(
                id="doi:" + record["doi"],
                type="article",
                url="https://doi.org/" + record["doi"],
                **record,
                roles=["methodological_inspiration"],
            )
        )
    items = deepcopy(references)
    if result.get(
        "evidence", result.get("correspondences", {}).get("evidence", {})
    ).get("cip_labeling", False):
        from molsysmt._private.stereochemistry import REFERENCE

        record = deepcopy(REFERENCE)
        record["url"] = "https://doi.org/" + record["doi"]
        record["roles"] = ["scientific_criterion"]
        references.append(record)
        items.append(deepcopy(record))
    for name, version in result["software"].items():
        items.append(
            dict(
                id=f"software:{name}:{version}",
                type="software",
                **deepcopy(SOFTWARE.get(name, dict(title=name))),
                version=version,
                roles=["executed_software"],
            )
        )
    result["references"] = references
    result["attribution"] = dict(
        schema="molsysmt.scientific_attribution@1", target=caller, items=items
    )
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, items, caller, contextual=True)
