"""Acquire one explicit CCD definition without retaining an entire catalogue."""

import base64
import gzip
import io
import os
import re
from contextlib import contextmanager
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.error import HTTPError

from molsysmt._private.smonitor import (
    ChemicalReferenceLookupError,
    FileContentError,
    MemoryBudgetExceededError,
)

CALLER = "molsysmt.physchem.get_chemical_template"
_HEADER = re.compile(rb"^[ \t]*data_([^ \t\r\n#]+)(?:[ \t\r\n#]|$)", re.I)


class _DigestReader(io.RawIOBase):
    def __init__(self, source):
        self.source = source
        self.digest = sha256()
        self.n_bytes = 0

    def readable(self):
        return True

    def readinto(self, buffer):
        count = self.source.readinto(buffer)
        if count:
            self.digest.update(memoryview(buffer)[:count])
            self.n_bytes += count
        return count


def _stamp(stat):
    return (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns)


def _lookup_error(component_id, resource, reason):
    return ChemicalReferenceLookupError(component_id, resource, reason, caller=CALLER)


def _http_status(error):
    seen = set()
    while error is not None and id(error) not in seen:
        seen.add(id(error))
        if isinstance(error, HTTPError):
            return error.code
        error = error.__cause__ or error.__context__
    return None


def _directory_component(directory, component_id):
    names = {
        component_id.casefold() + extension
        for extension in (".cif", ".cif.gz", ".mmcif", ".mmcif.gz")
    }
    with os.scandir(directory) as entries:
        matches = [
            Path(entry.path) for entry in entries if entry.name.casefold() in names
        ]
    if not matches:
        raise _lookup_error(component_id, str(directory), "not_found")
    if len(matches) != 1:
        raise _lookup_error(component_id, str(directory), "ambiguous")
    return matches[0]


@contextmanager
def _resource(component_id, source):
    if isinstance(source, bytes):
        with io.BytesIO(source) as stream:
            yield stream, dict(kind="caller_bytes", resource="caller:bytes")
        return
    if isinstance(source, str) and source == "rcsb":
        from molsysmt._private.download import download_with_retries

        url = f"https://files.rcsb.org/ligands/download/{component_id}.cif"
        with TemporaryDirectory(prefix="molsysmt-ccd-") as temporary:
            path = Path(temporary) / "component.cif"
            try:
                download_with_retries(url, str(path), component_id, "RCSB CCD", CALLER)
            except Exception as error:
                reason = "not_found" if _http_status(error) == 404 else "unavailable"
                raise _lookup_error(component_id, url, reason) from error
            with path.open("rb") as stream:
                yield (
                    stream,
                    dict(
                        kind="rcsb",
                        resource=url,
                        acquired_at=datetime.now(timezone.utc).isoformat(),
                    ),
                )
        return
    path = Path(source)
    try:
        if path.is_dir():
            path = _directory_component(path, component_id)
        with path.open("rb") as stream:
            before = _stamp(os.fstat(stream.fileno()))
            yield stream, dict(kind="local_file", resource=path.resolve().as_uri())
            if (
                _stamp(os.fstat(stream.fileno())) != before
                or _stamp(path.stat()) != before
            ):
                raise _lookup_error(component_id, str(path), "source_changed")
    except ChemicalReferenceLookupError:
        raise
    except OSError as error:
        reason = "not_found" if isinstance(error, FileNotFoundError) else "unavailable"
        raise _lookup_error(component_id, str(path), reason) from error


def _input_budget():
    from molsysmt import configure

    return configure.max_ram_usage // 4


def _check_input_budget(predicted, available, reason):
    if predicted > available:
        raise MemoryBudgetExceededError(
            reason=reason,
            predicted_bytes=predicted,
            available_bytes=available,
            caller=CALLER,
        )


def _bounded_lines(stream, available):
    """Bound raw reads and buffered physical lines, including unselected data."""
    parts, predicted = [], 0
    while part := stream.readline(65536):
        predicted += len(part) + 64
        _check_input_budget(
            predicted, available, "A CCD physical line exceeds the input buffer budget."
        )
        parts.append(part)
        if part.endswith(b"\n"):
            yield b"".join(parts)
            parts, predicted = [], 0
    if parts:
        yield b"".join(parts)


def _select_block(stream, component_id):
    """Retain selected bytes and at most one fallback block, respecting CIF text."""
    selected, first = [], []
    first_name = current_name = None
    n_blocks = 0
    matched = 0
    in_text = False
    offset = 0
    selected_offset = 0
    prefix = []
    available = _input_budget()
    retained = first_size = 0
    for line in _bounded_lines(stream, available):
        header = None if in_text else _HEADER.match(line)
        if header is not None:
            try:
                current_name = header.group(1).decode("utf-8")
            except UnicodeDecodeError as error:
                raise FileContentError(
                    "CCD data-block identifiers must be UTF-8", caller=CALLER
                ) from error
            n_blocks += 1
            if n_blocks == 1:
                first_name = current_name
                first.extend(prefix)
                prefix.clear()
                first_size = retained
            elif n_blocks == 2:
                # A multi-block resource cannot use the single-block fallback.
                first.clear()
                retained -= first_size
            if current_name.casefold() == component_id.casefold():
                matched += 1
                if matched > 1:
                    raise _lookup_error(component_id, "CCD data blocks", "ambiguous")
                selected_offset = offset
        if n_blocks == 0:
            retained += len(line) + 64
            prefix.append(line)
        elif n_blocks == 1:
            retained += len(line) + 64
            first_size += len(line) + 64
            first.append(line)
        if (
            current_name is not None
            and current_name.casefold() == component_id.casefold()
        ):
            retained += len(line) + 64
            selected.append(line)
        _check_input_budget(
            retained,
            available,
            "Retained CCD definition bytes exceed the input buffer budget.",
        )
        if line.startswith(b";"):
            in_text = not in_text
        offset += len(line)
    if not n_blocks:
        raise FileContentError("No CCD data block is present", caller=CALLER)
    if matched:
        # A one-block resource also retains its original preamble exactly.
        if n_blocks == 1:
            return b"".join(first), first_name, 0
        return b"".join(selected), component_id, selected_offset
    if n_blocks == 1:
        return b"".join(first), first_name, 0
    raise _lookup_error(component_id, "CCD data blocks", "not_found")


def read_definition(component_id, source):
    from mmcif.io.PdbxReader import PdbxReader

    with _resource(component_id, source) as (raw, metadata):
        digest = _DigestReader(raw)
        with io.BufferedReader(digest, buffer_size=65536) as buffered:
            compressed = buffered.peek(2)[:2] == b"\x1f\x8b"
            try:
                if compressed:
                    with gzip.GzipFile(fileobj=buffered) as stream:
                        definition, block_name, offset = _select_block(
                            stream, component_id
                        )
                else:
                    definition, block_name, offset = _select_block(
                        buffered, component_id
                    )
            except (gzip.BadGzipFile, EOFError) as error:
                raise FileContentError(
                    "The compressed CCD resource is invalid or incomplete",
                    caller=CALLER,
                ) from error
            # The selector reads through EOF, including later blocks, so the
            # digest identifies the full original resource rather than a prefix.
            resource_digest = digest.digest.hexdigest()
            resource_bytes = digest.n_bytes
    blocks = []
    try:
        PdbxReader(io.StringIO(definition.decode("utf-8"))).read(
            blocks,
            selectList=[
                "chem_comp",
                "chem_comp_atom",
                "chem_comp_bond",
                "pdbx_chem_comp_descriptor",
            ],
        )
    except Exception as error:
        raise FileContentError(
            "The selected CCD block cannot be parsed", caller=CALLER
        ) from error
    if len(blocks) != 1:
        raise FileContentError(
            "One selected CCD component block is required", caller=CALLER
        )
    component = blocks[0].getObj("chem_comp")
    if (
        component is None
        or component.getRowCount() != 1
        or not component.hasAttribute("id")
    ):
        raise FileContentError(
            "One chem_comp.id declaration is required", caller=CALLER
        )
    actual_id = component.getValue("id", 0)
    if (
        not isinstance(actual_id, str)
        or not actual_id.strip()
        or actual_id in {".", "?"}
    ):
        raise FileContentError(
            "A nonempty chem_comp.id declaration is required", caller=CALLER
        )
    if actual_id.casefold() != component_id.casefold():
        raise _lookup_error(component_id, metadata["resource"], "not_found")
    modified = (
        component.getValue("pdbx_modified_date", 0)
        if component.hasAttribute("pdbx_modified_date")
        else None
    )
    return blocks[0], dict(
        **metadata,
        component_id=actual_id,
        block_name=block_name,
        version=modified if modified not in {None, ".", "?", ""} else "unversioned",
        resource_sha256=resource_digest,
        resource_n_bytes=resource_bytes,
        compression="gzip" if compressed else "none",
        definition_sha256=sha256(definition).hexdigest(),
        definition_n_bytes=len(definition),
        definition_decompressed_offset=offset,
        definition=dict(
            encoding="base64", data=base64.b64encode(definition).decode("ascii")
        ),
    )
