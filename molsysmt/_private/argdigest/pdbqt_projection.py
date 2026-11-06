"""Validate explicit coordinate and provenance boundaries for prepared PDBQT."""

import json

import numpy as np

from molsysmt._private.smonitor import ArgumentError

from .argument._correspondence_axes import flat_axis
from .argument.atom_correspondence import digest_atom_correspondence
from .argument.coordinates import digest_coordinates
from .argument.item import digest_item
from .argument.output_filename import digest_output_filename
from .argument.skip_digestion import digest_skip_digestion

DIGEST_OPTIONS = {
    "digestion_source": "molsysmt._private.argdigest.pdbqt_projection",
    "digestion_style": "registry",
    "strictness": "error",
}


def _coordinates(value, caller=None):
    from molsysmt import pyunitwizard as puw

    try:
        value = puw.ensure_quantity(
            value, dimensionality={"[L]": 1}, standardized=False
        )
        if np.asarray(puw.get_value(value)).dtype.kind not in "iuf":
            raise TypeError("Replacement coordinates require real numeric magnitudes.")
    except Exception as error:
        raise ArgumentError("coordinates", value=value, caller=caller) from error
    return digest_coordinates(value, caller=caller)


def _structures(value, caller=None):
    return flat_axis(value, "structure_indices", caller)


def _discard_remarks(value, caller=None):
    if type(value) is not bool:
        raise ArgumentError("discard_remarks", value=value, caller=caller)
    return value


def _provenance(value, caller=None):
    if value is None:
        return None
    if isinstance(value, dict):
        try:
            encoded = json.dumps(value, allow_nan=False)
            pending = [value]
            while pending:
                item = pending.pop()
                if isinstance(item, dict):
                    if any(not isinstance(key, str) for key in item):
                        raise TypeError("Provenance JSON object keys must be strings.")
                    pending.extend(item.values())
                elif isinstance(item, (list, tuple)):
                    pending.extend(item)
            return json.loads(encoded)
        except (ValueError, TypeError, OverflowError) as error:
            raise ArgumentError(
                "chemical_state_provenance", value=value, caller=caller
            ) from error
    raise ArgumentError("chemical_state_provenance", value=value, caller=caller)


ARGUMENT_DIGESTERS = dict(
    item=digest_item,
    coordinates=_coordinates,
    atom_correspondence=digest_atom_correspondence,
    structure_indices=_structures,
    output_filename=digest_output_filename,
    discard_remarks=_discard_remarks,
    chemical_state_provenance=_provenance,
    skip_digestion=digest_skip_digestion,
)
