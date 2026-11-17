"""Attach detached references for general graph/geometry tools at completion."""

from copy import deepcopy


def result_attribution(items, target, context):
    """Project a result bibliography, without inventing an observed call trace.

    Keep the host wrapper compatible and encode the optional provider's public
    portable schema directly. No provider import or session state is needed;
    loading this metadata therefore cannot credit a new scientific operation.
    """
    portable_items = []
    uses = []
    for item in items:
        portable_items.append(
            deepcopy({key: value for key, value in item.items() if key != "roles"})
        )
        uses.append(
            dict(
                item_id=item["id"],
                used_by=target,
                roles=deepcopy(item.get("roles", [])),
                context={
                    "relationship": deepcopy(item.get("roles", [])),
                    "version": item.get("version"),
                    **deepcopy(context),
                },
            )
        )
    return dict(
        schema="molsysmt.scientific_attribution@1",
        target=target,
        items=deepcopy(items),
        portable=dict(
            schema="ackredit.attribution@1",
            name=target,
            context=deepcopy(context),
            items=portable_items,
            uses=uses,
            usage_tree={
                target: {
                    "items": sorted(item["id"] for item in items),
                    "children": [],
                }
            },
        ),
    )


def attach_reconstruction_attribution(report, caller):
    """Credit the quaternion fit only when a reconstruction actually used it."""
    from molsysmt import _ackredit
    from molsysmt._private.scientific_citations import ARTICLES

    references = {}
    for step in report["steps"]:
        for item in step.get("references", []):
            references[item["id"]] = deepcopy(item)
        if step["method"] == "least_rmsd_template_alignment":
            record = deepcopy(ARTICLES["horn_1987"])
            item = dict(
                id="doi:" + record["doi"],
                type="article",
                **record,
                roles=["scientific_criterion"],
                url="https://doi.org/" + record["doi"],
            )
            references[item["id"]] = item
    report["references"] = list(references.values())
    items = report["references"] + [
        executed_software_reference("molsysmt", report["software"]["molsysmt"])
    ]
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(
            provider,
            items,
            caller,
            contextual=True,
            context=dict(method=report["method"], report_schema=report["schema"]),
        )


def executed_software_reference(software, version):
    """Build a detached record for software actually reached by an operation."""
    from molsysmt._private.scientific_citations import SOFTWARE

    return dict(
        id=f"software:{software}:{version}",
        type="software",
        **deepcopy(SOFTWARE.get(software, dict(title=software))),
        version=version,
        roles=["executed_software"],
    )


def credit_executed_software(software, version, caller, **context):
    """Credit software actually used by a completed scientific operation."""
    from molsysmt import _ackredit

    items = [executed_software_reference(software, version)]
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, items, caller, contextual=True, context=context)


def credit_implicit_solvent(
    method, software, version, caller, *, forcefield, resources
):
    """Credit a constructed physical model and the engine actually executing it."""
    if method not in {"OBC1", "OBC2"}:
        return
    from molsysmt import _ackredit
    from molsysmt._private.scientific_citations import ARTICLES, SOFTWARE

    record = deepcopy(ARTICLES["onufriev_2004"])
    items = [
        dict(
            id="doi:" + record["doi"],
            type="article",
            **record,
            url="https://doi.org/" + record["doi"],
            roles=["scientific_criterion"],
        ),
        dict(
            id=f"software:{software}:{version}",
            type="software",
            **deepcopy(SOFTWARE.get(software, dict(title=software))),
            version=version,
            roles=["executed_software"],
        ),
    ]
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(
            provider,
            items,
            caller,
            contextual=True,
            context={
                "implicit_solvent": method,
                "engine": software,
                "forcefield": forcefield,
                "resources": list(resources),
                "configuration": "engine_defaults",
            },
        )


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


def attach_scientific_attribution(result, caller, references=()):
    """Retain references even when optional citation collection is unavailable."""
    from molsysmt import _ackredit

    result["references"] = deepcopy(list(references))
    items = deepcopy(list(references)) + [
        executed_software_reference(name, version)
        for name, version in result["software"].items()
    ]
    result["attribution"] = dict(
        schema="molsysmt.scientific_attribution@1", target=caller, items=items
    )
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, items, caller, contextual=True)


def credit_secondary_structure(version, caller, *, simplified):
    """Record the executed DSSP criterion and provider, once after completion."""
    from molsysmt import _ackredit
    from molsysmt._private.scientific_citations import ARTICLES

    items = []
    for name, role in [
        ("kabsch_sander_1983", "scientific_criterion"),
        ("mdtraj", "reference_implementation"),
    ]:
        record = deepcopy(ARTICLES[name])
        items.append(
            dict(
                id="doi:" + record["doi"],
                type="article",
                url="https://doi.org/" + record["doi"],
                roles=[role],
                **record,
            )
        )
    items.append(executed_software_reference("mdtraj", version))
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(
            provider,
            items,
            caller,
            contextual=True,
            context={
                "method": "kabsch_sander_1983",
                "implementation": "MDTraj DSSP",
                "simplified": simplified,
            },
        )
