"""Projecting amino-acid letters and their source group positions together."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all


def amino_acid_groups(group_names, group_types, group_indices):
    """Share the native converter's filtering and one-letter interpretation."""
    from molsysmt.element.group.amino_acid import get_1_letter_code_from_name

    letters, indices = [], []
    for name, kind, index in zip(group_names, group_types, group_indices, strict=True):
        if kind in {"amino acid"}:
            letters.append(get_1_letter_code_from_name(str(name).upper()))
            indices.append(int(index))
    return "".join(letters), indices


def sequence_with_groups(source, selection, syntax, *, caller):
    """Resolve one sequence and its source mapping through declared attributes."""
    from molsysmt.basic import get, has_attribute

    if has_attribute(source, "group_type", include_none=True):
        data = get(
            source,
            element="group",
            selection=selection,
            syntax=syntax,
            group_index=True,
            group_name=True,
            group_type=True,
            output_type="dictionary",
        )
        sequence, indices = amino_acid_groups(
            data["group_name"], data["group_type"], data["group_index"]
        )
    else:
        # Sequence-only forms expose names and source positions without an atom
        # inventory or a molecular group-type classification.
        data = get(
            source,
            element="group",
            group_index=True,
            group_name=True,
            output_type="dictionary",
        )
        names = data["group_name"]
        if names is None:
            raise ArgumentError(
                "molecular_system",
                caller=caller,
                message="Sequence characters must be defined.",
            )
        positions = np.arange(len(names), dtype=np.int64)
        if not is_all(selection):
            if isinstance(selection, str) or selection is None:
                raise ArgumentError(
                    "selection",
                    caller=caller,
                    message="Sequence-only inputs require integer group positions or all.",
                )
            positions = np.asarray(selection)
            if positions.size == 0:
                positions = np.empty(0, dtype=np.int64)
            if (
                positions.ndim != 1
                or positions.dtype.kind not in "iu"
                or np.any((positions < 0) | (positions >= len(names)))
            ):
                raise ArgumentError(
                    "selection",
                    caller=caller,
                    message="Sequence positions must be valid integer group indices.",
                )
        names = [names[index] for index in positions]
        indices = [int(data["group_index"][index]) for index in positions]
        if all(len(name) == 1 for name in names):
            sequence = "".join(names)
        else:
            from molsysmt.element.group.terminal_capping import group_names as caps

            kinds = [
                "terminal capping" if str(name).upper() in caps else "amino acid"
                for name in names
            ]
            sequence, indices = amino_acid_groups(names, kinds, indices)
    if not sequence or "-" in sequence:
        raise ArgumentError(
            "selection",
            caller=caller,
            message="Each selection must supply a nonempty, ungapped sequence.",
        )
    return sequence, indices


def identity_attribution(software_version):
    """Build detached offline declarations for the reached identity calculation."""
    return [
        dict(
            id="ensembler-sequence-identity-reference",
            type="software",
            title="Ensembler sequence identity counting (adapted reference implementation)",
            revision="264930d28d3d4987c4fc0c03caba6cf0066e12ca",
            url="https://github.com/choderalab/ensembler/blob/264930d28d3d4987c4fc0c03caba6cf0066e12ca/ensembler/modeling.py",
            roles=["reference_implementation"],
        ),
        dict(
            id=f"software:biopython:{software_version}",
            type="software",
            title="Biopython",
            version=software_version,
            url="https://biopython.org/",
            roles=["executed_software"],
        ),
    ]
