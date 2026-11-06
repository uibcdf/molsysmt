"""Keep deposited model label spelling separate from the numeric model axis."""

import numpy as np

from molsysmt._private.smonitor import FormatError

CALLER = "molsysmt.form.mmcif_PdbxContainers_DataContainer"


def model_axis(item):
    """Return per-atom integer model keys and original label spelling by key."""
    category = item.getObj("atom_site")
    columns = category.getAttributeList()
    size = len(category.data)
    if "pdbx_PDB_model_num" not in columns:
        return np.zeros(size, dtype=np.int64), ({0: None} if size else {})
    column = columns.index("pdbx_PDB_model_num")
    numbers = np.zeros(size, dtype=np.int64)
    original_labels = {}
    missing = False
    for atom_index, row in enumerate(category.data):
        value = row[column]
        if value is None or str(value).strip() in {"", ".", "?"}:
            missing = True
            continue
        label = str(value)
        try:
            number = int(label)
            if not np.iinfo(np.int64).min <= number <= np.iinfo(np.int64).max:
                raise ValueError("model number exceeds the supported integer range")
        except (ValueError, TypeError, OverflowError) as error:
            raise FormatError(
                reason=f"Invalid mmCIF model number label {label!r}.", caller=CALLER
            ) from error
        if number in original_labels and original_labels[number] != label:
            raise FormatError(
                reason="Conflicting source spellings for one numeric mmCIF model label.",
                caller=CALLER,
            )
        original_labels[number] = label
        numbers[atom_index] = number
    if missing and original_labels:
        raise FormatError(
            reason="Partially missing mmCIF model labels cannot establish a model axis.",
            caller=CALLER,
        )
    return numbers, original_labels or ({0: None} if size else {})
