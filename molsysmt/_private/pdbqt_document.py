"""Indexing validated PDBQT model bodies in a resident immutable text snapshot."""

from copy import deepcopy

import numpy as np

from molsysmt._private.pdbqt import fail, parse


def _model_ranges(lines, start_offset=0):
    """Share MODEL grammar across character-addressed text and byte-addressed files."""
    active = None
    label = None
    seen = set()
    wrapped = ended = nonremarks = False
    prefix_stop = start_offset
    end = start_offset
    for position, end, line in lines:
        tokens = line.split()
        if not tokens:
            continue
        kind = tokens[0]
        if kind == "MODEL":
            if (
                active is not None
                or ended
                or len(tokens) != 2
                or not tokens[1].isdigit()
                or int(tokens[1]) <= 0
            ):
                fail("Invalid, nested or misplaced PDBQT MODEL record.")
            label = str(int(tokens[1]))
            if label in seen:
                fail("Repeated PDBQT MODEL label.")
            seen.add(label)
            if not wrapped:
                if nonremarks:
                    fail("PDBQT cannot mix unwrapped atoms and MODEL structures.")
                prefix_stop = position
            wrapped = True
            active = end
        elif kind == "ENDMDL":
            if len(tokens) != 1 or active is None:
                fail("Unmatched PDBQT ENDMDL record.")
            yield label, active, position, prefix_stop
            active = None
        elif active is None:
            if wrapped:
                if kind == "END" and len(tokens) == 1 and not ended:
                    ended = True
                elif kind != "REMARK":
                    fail("PDBQT record outside MODEL structures.")
            elif kind != "REMARK":
                nonremarks = True
    if active is not None:
        fail("PDBQT MODEL is missing ENDMDL.")
    if not wrapped:
        yield None, start_offset, end, start_offset


def _text_lines(payload, start):
    while start < len(payload):
        stop = payload.find("\n", start)
        stop = len(payload) if stop < 0 else stop + 1
        yield start, stop, payload[start:stop]
        start = stop


def model_spans(payload, start_offset=0):
    """Yield labels and character ranges without splitting the whole document."""
    for label, start, stop, prefix_stop in _model_ranges(
        _text_lines(payload, start_offset), start_offset
    ):
        yield label, start, stop, payload[start_offset:prefix_stop]


def identity(record):
    """Separate invariant molecular fields from structure-dependent observables."""
    return [
        tuple(
            (key, value)
            for key, value in atom.items()
            if key not in {"coordinates", "occupancy", "b_factor"}
        )
        for atom in record["atoms"]
    ]


def same_tree(first, second):
    if first is None or second is None:
        return first is second
    return first.keys() == second.keys() and all(
        np.array_equal(first[key], second[key]) for key in first
    )


class PDBQTDocument:
    """Keep source text, compact model ranges and one atom-scale reference record."""

    storage_mode = "resident"

    def __init__(self, payload, start_offset=0):
        self._text = payload
        self._start_offset = start_offset
        self._initialize(model_spans(payload, start_offset))

    def _initialize(self, spans):
        offsets, labels = [], []
        self.first = None
        self.prefix = ""
        self.present = set()
        baseline = None
        for label, start, stop, prefix in spans:
            record = parse(prefix + self._body_range(start, stop))
            current = identity(record)
            if self.first is None:
                self.first = record
                baseline = current
                self.prefix = prefix
            elif current != baseline or not same_tree(
                self.first["torsion_tree"], record["torsion_tree"]
            ):
                fail(
                    "PDBQT MODEL atom identity, charges, types or torsion tree changed."
                )
            for attribute in ("occupancy", "b_factor"):
                if any(atom[attribute] is not None for atom in record["atoms"]):
                    self.present.add(attribute)
            offsets.append((start, stop))
            labels.append(label)
        if self.first is None:
            fail("PDBQT requires at least one structure.")
        self.offsets = np.asarray(offsets, dtype=np.int64)
        self.offsets.flags.writeable = False
        self.labels = np.asarray(labels, dtype=object)
        self.labels.flags.writeable = False

    @property
    def payload(self):
        return self._text[self._start_offset :]

    def _source_bounds(self):
        return self._start_offset, len(self._text)

    def _byte_chunks(self, start, stop):
        for offset in range(start, stop, 64 * 1024):
            try:
                yield self._text[offset : min(stop, offset + 64 * 1024)].encode("utf-8")
            except UnicodeEncodeError:
                fail("PDBQT text must be encodable as UTF-8.")

    def stream_to(self, filename, structures):
        """Atomically stream source ranges without a complete output string."""

        def chunks():
            begin, end = self._source_bounds()
            if np.array_equal(structures, np.arange(len(self.labels))):
                yield from self._byte_chunks(begin, end)
                return
            yield from self._byte_chunks(
                begin,
                begin + len(self.prefix.encode("utf-8"))
                if self.storage_mode == "indexed"
                else begin + len(self.prefix),
            )
            for index in structures:
                label = self.labels[index]
                if label is not None:
                    yield f"MODEL {label}\n".encode("ascii")
                start, stop = self.offsets[index]
                yield from self._byte_chunks(int(start), int(stop))
                if label is not None:
                    yield b"ENDMDL\n"

        return self.write_chunks(filename, chunks())

    def write_chunks(self, filename, chunks):
        """Protect a destination while consuming bounded, source-validated bytes."""
        import os
        import tempfile
        from pathlib import Path

        if filename is None:
            fail("An output_filename is required for PDBQT serialization.")
        self.validate_source()
        target = Path(filename)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", prefix=".molsysmt-pdbqt-", dir=target.parent, delete=False
            ) as output:
                temporary = Path(output.name)
                for chunk in chunks:
                    output.write(chunk)
            self.validate_source()
            os.replace(temporary, target)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        return filename

    def validate_source(self):
        """Resident snapshots do not depend on their original file after opening."""

    def acquire(self):
        """Resident copies share immutable data without external resources."""

    def release(self):
        """Resident data are reclaimed when their final Python owner disappears."""

    def _body_range(self, start, stop):
        return self._text[start:stop]

    def body(self, index):
        start, stop = self.offsets[index]
        return self._body_range(start, stop)

    def record(self, index):
        if index == 0:
            return self.first
        start, stop = self.offsets[index]
        return parse(self.prefix + self._body_range(start, stop))

    def detached_tree(self, index):
        return deepcopy(self.record(index)["torsion_tree"])
