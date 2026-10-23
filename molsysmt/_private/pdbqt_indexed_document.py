"""Indexing uncompressed PDBQT bytes without retaining the complete source text."""

import os
from pathlib import Path
from threading import RLock

from molsysmt._private.pdbqt import fail
from molsysmt._private.pdbqt_document import PDBQTDocument, _model_ranges


class PDBQTIndexedDocument(PDBQTDocument):
    """Own a source-bound descriptor, byte ranges and one parsed reference model."""

    storage_mode = "indexed"

    def __init__(self, filename):
        self._path = Path(filename).absolute()
        self._lock = RLock()
        self._owners = 1
        self._file = self._path.open("rb")
        try:
            self._stamp = self._signature(os.fstat(self._file.fileno()))
            self.validate_source()
            spans = list(_model_ranges(self._lines()))
            self._prefix_stop = spans[0][3] if spans else 0
            prefix = self._body_range(0, self._prefix_stop)
            self._initialize(
                (label, start, stop, prefix) for label, start, stop, _ in spans
            )
            self.validate_source()
        except BaseException:
            self._file.close()
            self._owners = 0
            raise

    @staticmethod
    def _signature(stat):
        return (
            stat.st_dev,
            stat.st_ino,
            stat.st_size,
            stat.st_mtime_ns,
            stat.st_ctime_ns,
        )

    def validate_source(self):
        with self._lock:
            try:
                current = self._signature(os.fstat(self._file.fileno()))
                path = self._signature(self._path.stat())
            except (OSError, ValueError) as error:
                fail(f"PDBQT indexed source is unavailable: {error}")
            if current != self._stamp or path != self._stamp:
                fail(
                    "PDBQT indexed source changed or was replaced; reopen and revalidate it."
                )

    def _lines(self):
        start = 0
        while line := self._file.readline():
            stop = self._file.tell()
            try:
                text = line.decode("utf-8")
            except UnicodeDecodeError:
                fail("PDBQT indexed sources must contain UTF-8 text.")
            yield start, stop, text
            start = stop

    def _bytes(self, start, stop):
        with self._lock:
            self.validate_source()
            self._file.seek(start)
            data = self._file.read(stop - start)
            self.validate_source()
            if len(data) != stop - start:
                fail("PDBQT indexed source was truncated during reading.")
            return data

    def _body_range(self, start, stop):
        try:
            return self._bytes(start, stop).decode("utf-8")
        except UnicodeDecodeError:
            fail("PDBQT indexed sources must contain UTF-8 text.")

    @property
    def payload(self):
        # Explicit text output necessarily materializes its complete string.
        return self._body_range(0, self._stamp[2])

    def record(self, index):
        self.validate_source()
        return super().record(index)

    def acquire(self):
        with self._lock:
            self.validate_source()
            self._owners += 1

    def release(self):
        with self._lock:
            self._owners -= 1
            if self._owners == 0:
                self._file.close()

    def _source_bounds(self):
        return 0, self._stamp[2]

    def _byte_chunks(self, start, stop):
        for offset in range(start, stop, 64 * 1024):
            yield self._bytes(offset, min(stop, offset + 64 * 1024))
