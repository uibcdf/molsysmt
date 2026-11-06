"""Replace only coordinate fields in an already validated prepared document."""

import io
import re
from hashlib import sha256
from pathlib import Path

import numpy as np

from molsysmt._private.pdbqt import PREFIX, fail
from molsysmt._private.smonitor import ArgumentError, MemoryBudgetExceededError

CALLER = "molsysmt.native.PDBQTFileHandler.project_coordinates"


def _source_identity(document):
    """Hash exact UTF-8 payload bytes and count remarks with bounded token storage."""
    digest, count, head, size = sha256(), 0, b"", 0
    begin, end = document._source_bounds()
    document.validate_source()
    for chunk in document._byte_chunks(begin, end):
        digest.update(chunk)
        size += len(chunk)
        parts = re.split(rb"[\r\n]", chunk)
        for part in parts[:-1]:
            head = (head + part).lstrip()[:7]
            count += head.split(None, 1)[:1] == [b"REMARK"]
            head = b""
        head = (head + parts[-1]).lstrip()[:7]
    count += head.split(None, 1)[:1] == [b"REMARK"]
    document.validate_source()
    return dict(sha256=digest.hexdigest(), n_bytes=size), int(count)


def _without_remarks(text):
    return "".join(
        line
        for line in text.splitlines(keepends=True)
        if line.split(None, 1)[:1] != ["REMARK"]
    )


def _replace_body(body, coordinates):
    lines, atom_index, error = [], 0, 0.0
    for line in body.splitlines(keepends=True):
        kind = line.split(None, 1)[:1]
        if kind == ["REMARK"]:
            continue
        if kind in (["ATOM"], ["HETATM"]):
            if not line.isascii():
                fail("Coordinate projection requires ASCII fixed-column atom records.")
            values = coordinates[atom_index]
            fields = [f"{value:8.3f}" for value in values]
            if any(len(field) != 8 for field in fields):
                fail("Projected PDBQT coordinate exceeds the 8.3 angstrom field.")
            rounded = np.asarray([float(field) for field in fields])
            error = max(error, float(np.max(np.abs(rounded - values))))
            line = line[:30] + "".join(fields) + line[54:]
            atom_index += 1
        lines.append(line)
    if atom_index != len(coordinates):
        fail("Projected PDBQT atom inventory does not match replacement coordinates.")
    return "".join(lines), error


def _budget(predicted):
    from molsysmt import configure

    if predicted > configure.max_ram_usage:
        raise MemoryBudgetExceededError(
            reason="Prepared PDBQT projection buffers exceed the configured budget; use bounded serial file output.",
            predicted_bytes=int(predicted),
            available_bytes=configure.max_ram_usage,
            caller=CALLER,
        )


def project_coordinates(
    handler,
    coordinates,
    atom_correspondence,
    structure_indices,
    output_filename,
    discard_remarks,
    chemical_state_provenance,
):
    from molsysmt import __version__
    from molsysmt import pyunitwizard as puw
    from molsysmt._private.files_and_directories import validate_copy_destination

    handler._require_open()
    document = handler._document
    structures = handler._axis(
        structure_indices, handler.n_structures, "structure_indices"
    )
    if len(structures) == 0 or len(np.unique(structures)) != len(structures):
        raise ArgumentError(
            "structure_indices",
            caller=CALLER,
            message="Serialized PDBQT selections must be nonempty and unique.",
        )
    values = np.asarray(puw.get_value(coordinates))
    n_atoms = handler.n_atoms
    pairs = atom_correspondence
    complete_axis = np.arange(n_atoms, dtype=np.int64)
    if values.shape != (len(structures), n_atoms, 3):
        raise ArgumentError(
            "coordinates",
            caller=CALLER,
            message="Supply one complete all-atom coordinate block per selected source structure, including all prepared H atoms.",
        )
    if (
        pairs.shape != (n_atoms, 2)
        or not np.array_equal(np.sort(pairs[:, 0]), complete_axis)
        or not np.array_equal(np.sort(pairs[:, 1]), complete_axis)
    ):
        raise ArgumentError(
            "atom_correspondence",
            caller=CALLER,
            message="Coordinates and correspondence must cover every prepared atom exactly once, including H, and every selected structure.",
        )
    source_to_coordinate = np.empty(n_atoms, dtype=np.int64)
    coordinate_to_source = np.empty(n_atoms, dtype=np.int64)
    source_to_coordinate[pairs[:, 1]] = pairs[:, 0]
    coordinate_to_source[pairs[:, 0]] = pairs[:, 1]
    if output_filename is not None:
        source_path = handler._source_path
        if source_path is not None:
            validate_copy_destination(source_path, output_filename, caller=CALLER)
        elif Path(output_filename).is_dir():
            raise ArgumentError("output_filename", value=output_filename, caller=CALLER)
    spans = document.offsets[structures]
    model_bytes = int(np.max(spans[:, 1] - spans[:, 0]))
    working_estimate = 12 * model_bytes + n_atoms * 3 * 8 * 2
    _budget(working_estimate)
    if output_filename is None:
        output_estimate = (
            int(np.sum(spans[:, 1] - spans[:, 0]))
            + len(document.prefix.encode("utf-8"))
            + sum(len(str(label)) + 20 for label in document.labels[structures])
        )
        # Includes bytes, decoded text and prefixed result simultaneously;
        # the budget describes these buffers, not the complete process RSS.
        _budget(working_estimate + 8 * output_estimate)
    source_identity, remark_count = _source_identity(document)
    if remark_count and not discard_remarks:
        fail(
            "Prepared source contains REMARK metadata that may include stale scores; explicitly set discard_remarks=True to remove all remarks and retain source identity in the report."
        )
    report = dict(
        schema_version="molsysmt.pdbqt_coordinate_projection@1",
        source_payload=source_identity,
        output_payload={},
        coordinate_to_source_atom_indices=coordinate_to_source.tolist(),
        output_to_source_atom_indices=complete_axis.tolist(),
        output_to_coordinate_atom_indices=source_to_coordinate.tolist(),
        output_to_source_structure_indices=structures.tolist(),
        source_structure_ids=document.labels[structures].tolist(),
        coordinate_input=dict(
            digest_encoding="float64 little-endian angstrom; C order; input atom and structure order"
        ),
        coordinate_precision=dict(
            unit="angstrom", decimals=3, field_width=8, max_absolute_error=[]
        ),
        metadata_disposition=dict(
            remarks="discarded" if remark_count else "absent",
            discarded_remark_count=remark_count,
            model_wrappers="canonical whitespace; source labels retained; terminal document END omitted for MODEL output",
            prepared_fields="all non-coordinate atom fields and torsion-tree records retained",
            chemistry="source declarations only; no reconstruction or reassignment",
        ),
        chemical_state_provenance=chemical_state_provenance,
        software={"molsysmt": __version__},
        execution=dict(
            source_storage_mode=handler.storage_mode,
            output="resident_text" if output_filename is None else "streamed_file",
            estimated_model_working_bytes=working_estimate,
            resident_coordinate_input_bytes=values.nbytes,
            model_count=len(structures),
        ),
    )
    output_digest, coordinate_digest, output_bytes = sha256(), sha256(), 0

    def chunks():
        prefix = _without_remarks(document.prefix).encode("utf-8")
        if prefix:
            yield prefix
        for row, source_index in enumerate(structures):
            block = puw.change_value(coordinates, values[row])
            block = np.asarray(
                puw.get_value(block, to_unit="angstrom"), dtype=np.float64
            )
            if not np.isfinite(block).all():
                fail("Projected PDBQT coordinates must be finite lengths.")
            coordinate_digest.update(block.astype("<f8", copy=False).tobytes())
            body, error = _replace_body(
                document.body(source_index), block[source_to_coordinate]
            )
            report["coordinate_precision"]["max_absolute_error"].append(error)
            label = document.labels[source_index]
            if label is not None:
                yield f"MODEL {label}\n".encode("ascii")
            yield body.encode("utf-8")
            if label is not None:
                yield ("" if body.endswith(("\r", "\n")) else "\n").encode("ascii")
                yield b"ENDMDL\n"
        document.validate_source()

    def hashed_chunks():
        nonlocal output_bytes
        for chunk in chunks():
            output_digest.update(chunk)
            output_bytes += len(chunk)
            yield chunk

    if output_filename is None:
        with io.BytesIO() as output:
            for chunk in hashed_chunks():
                output.write(chunk)
            result = PREFIX + output.getvalue().decode("utf-8")
    else:
        result = document.write_chunks(output_filename, hashed_chunks())
    report["output_payload"] = dict(
        sha256=output_digest.hexdigest(), n_bytes=output_bytes
    )
    report["coordinate_input"]["sha256"] = coordinate_digest.hexdigest()
    return dict(molecular_system=result, report=report)
