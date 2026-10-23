"""Indexing validated PDBQT model bodies in a resident immutable text snapshot."""

from copy import deepcopy

import numpy as np

from molsysmt._private.pdbqt import fail, parse


def model_spans(payload, start_offset=0):
    """Yield labels and character ranges without splitting the whole document."""
    position = start_offset
    active = None
    label = None
    seen = set()
    wrapped = ended = nonremarks = False
    prefix = ""
    while position < len(payload):
        end = payload.find("\n", position)
        end = len(payload) if end < 0 else end + 1
        tokens = payload[position:end].split()
        if tokens:
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
                    prefix = payload[start_offset:position]
                wrapped = True
                active = end
            elif kind == "ENDMDL":
                if len(tokens) != 1 or active is None:
                    fail("Unmatched PDBQT ENDMDL record.")
                yield label, active, position, prefix
                active = None
            elif active is None:
                if wrapped:
                    if kind == "END" and len(tokens) == 1 and not ended:
                        ended = True
                    elif kind != "REMARK":
                        fail("PDBQT record outside MODEL structures.")
                elif kind != "REMARK":
                    nonremarks = True
        position = end
    if active is not None:
        fail("PDBQT MODEL is missing ENDMDL.")
    if not wrapped:
        yield None, start_offset, len(payload), ""


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

    def __init__(self, payload, start_offset=0):
        self._text = payload
        self._start_offset = start_offset
        offsets, labels = [], []
        self.first = None
        self.prefix = ""
        self.present = set()
        baseline = None
        for label, start, stop, prefix in model_spans(payload, start_offset):
            record = parse(prefix + payload[start:stop])
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

    def record(self, index):
        if index == 0:
            return self.first
        start, stop = self.offsets[index]
        return parse(self.prefix + self._text[start:stop])

    def detached_tree(self, index):
        return deepcopy(self.record(index)["torsion_tree"])
