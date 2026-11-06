"""Adapting the owning local cap catalogue to shared chemical-coverage audits."""

from copy import deepcopy
from hashlib import sha256
from importlib.resources import files


def template(name, names, cache, naming_scheme):
    """Keep one agreed heavy layout without interpreting a bare cap label."""
    if naming_scheme not in ("amber", "legacy"):
        return None
    from molsysmt._private.amino_acid_templates import is_hydrogen
    from molsysmt.element.atom import get_atom_type_from_atom_name
    from molsysmt.element.group.terminal_capping import (
        get_group_db,
        group_names,
        n_terminal_capping_names,
    )

    if name not in group_names:
        return None
    key = ("terminal_cap_reference", name)
    if key not in cache:
        variants = get_group_db(name)["topology"]
        basename = (
            "n_terminal.json" if name in n_terminal_capping_names else "c_terminal.json"
        )
        package = "molsysmt.data.databases.terminal_cappings"
        digest = sha256(files(package).joinpath(basename).read_bytes()).hexdigest()
        resource = f"{package}/{basename}"
        elements = {
            atom: get_atom_type_from_atom_name(atom)
            for variant in variants
            for atom in variant["atoms"]
        }
        cache[key] = variants, elements, resource, digest
        from molsysmt import _ackredit

        reference = dict(
            id=f"dataset:molsysmt-terminal-cap-catalogue:{digest}",
            type="dataset",
            title="Historical MolSysMT terminal-cap atom/bond catalogue",
            url=f"https://github.com/uibcdf/molsysmt/blob/main/molsysmt/data/databases/terminal_cappings/{basename}",
            roles=["chemical_reference_data"],
        )
        caller = "molsysmt.build.get_residue_chemical_coverage"
        with _ackredit.scope(caller) as provider:
            _ackredit.credit(provider, [reference], caller, contextual=True)
    variants, elements, resource, digest = cache[key]
    heavy_sets = [
        {atom for atom in variant["atoms"] if not is_hydrogen(atom)}
        for variant in variants
    ]
    compatible = [heavy for heavy in heavy_sets if names <= heavy]
    signatures = {frozenset(heavy) for heavy in (compatible or heavy_sets)}
    if len(signatures) != 1:
        # NME may use C or CH3. A missing methyl name cannot choose either axis.
        return None
    expected = set(next(iter(signatures)))
    candidates = [
        (index, variant)
        for index, (variant, heavy) in enumerate(zip(variants, heavy_sets))
        if heavy == expected
    ]
    return dict(
        expected=expected,
        elements=elements,
        orders=None,
        candidates=candidates,
        modified=False,
        identity=dict(
            group_name=name,
            naming_scheme=naming_scheme,
            family="terminal_capping",
            backbone_roles=["C"] if name in n_terminal_capping_names else ["N"],
            resource=resource,
            variant_indices=[index for index, _ in candidates],
            variant_sources={
                str(index): dict(resource=resource, packaged_sha256=digest)
                for index, _ in candidates
            },
            provenance=deepcopy(
                dict(packaged_sha256=digest, original_sources="unassessed")
            ),
            element_reference="standard_atom_name_mapping",
        ),
    )
