"""Reading versioned H-name alternatives without rewriting molecular identity."""

import json
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from importlib.resources import files


@lru_cache(maxsize=1)
def _load():
    raw = (
        files("molsysmt.data.databases.amino_acids")
        .joinpath("pdb_hydrogen_aliases.json")
        .read_bytes()
    )
    data = json.loads(raw)
    if data["schema"] != "molsysmt.pdb_hydrogen_aliases@1":
        raise ValueError("Unsupported hydrogen-name reference schema.")
    return data, sha256(raw).hexdigest()


def resolve(group_name, atom_name):
    """Return literal and declared alternative names, leaving chemistry untouched."""
    data, digest = _load()
    aliases = (
        {**data["common"], **data["groups"][group_name]}
        if group_name in data["groups"]
        else {}
    )
    alternate = aliases.get(atom_name)
    names = (
        [atom_name]
        if alternate is None or alternate == atom_name
        else [atom_name, alternate]
    )
    reference = deepcopy(data["source"])
    reference["packaged_sha256"] = digest
    return names, reference


def bibliography(reference):
    """Retain dataset identity rather than claiming execution of OpenMM."""
    return dict(
        id="dataset:openmm-pdb-hydrogen-aliases:" + reference["sha256"],
        type="dataset",
        title=reference["title"],
        url=reference["url"],
        version=reference["commit"],
        roles=["chemical_name_reference_data"],
    )


def credit(reference, caller):
    """Credit the inspected data through the optional application-owned provider."""
    from molsysmt import _ackredit

    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, [bibliography(reference)], caller, contextual=True)
