"""Validating a detached, caller-declared template identity and hydrogen policy."""

import json
from copy import deepcopy

from molsysmt._private.smonitor import ArgumentError


def digest_template_provenance(template_provenance, caller=None):
    required = ("identity", "version", "source_uri", "checksum", "hydrogen_policy")
    if (
        not isinstance(template_provenance, dict)
        or any(
            not isinstance(template_provenance.get(key), str)
            or not template_provenance[key].strip()
            for key in required
        )
        or template_provenance["hydrogen_policy"]
        not in {"explicit_atoms", "stored_counts"}
    ):
        raise ArgumentError(
            "template_provenance", value=template_provenance, caller=caller
        )
    try:
        json.dumps(template_provenance, allow_nan=False)
    except (ValueError, TypeError) as error:
        raise ArgumentError(
            "template_provenance", value=template_provenance, caller=caller
        ) from error
    return deepcopy(template_provenance)
