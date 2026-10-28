"""Explicit file/text operations; no result is adopted into the scene implicitly."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


class _FormTools:
    def __init__(self, owner):
        self.file_fasta = _FastaTools(owner)

    def __dir__(self):
        return ["file_fasta"]


class _H5MSMTools:
    _NAMES = (
        "read",
        "write",
        "read_layers",
        "write_layers",
        "append_structures",
        "migrate_04_to_05",
        "migrate_to_05",
    )

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    @_native_documentation("read", module="h5msm", bind_primary=False)
    @signal(tags=["addon", "io"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def read(self, filename, skip_digestion=False):
        from molsysmt.h5msm import read

        self._owner._view()
        return read(
            filename=filename,
            skip_digestion=skip_digestion,
        )

    @_native_documentation("write", module="h5msm", bind_primary=True)
    @signal(tags=["addon", "io"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def write(self, output_filename, skip_digestion=False):
        from molsysmt.h5msm import write

        return self._owner._read(
            write,
            {
                "output_filename": output_filename,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("read_layers", module="h5msm", bind_primary=False)
    @signal(tags=["addon", "io"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def read_layers(
        self, filename, layers=None, analysis_names=None, skip_digestion=False
    ):
        from molsysmt.h5msm import read_layers

        self._owner._view()
        return read_layers(
            filename=filename,
            layers=layers,
            analysis_names=analysis_names,
            skip_digestion=skip_digestion,
        )

    @_native_documentation("write_layers", module="h5msm", bind_primary=False)
    @signal(tags=["addon", "io"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def write_layers(
        self,
        output_filename,
        *,
        topology=None,
        chemical_states=None,
        structures=None,
        interactions=None,
        associations=None,
        skip_digestion=False,
    ):
        from molsysmt.h5msm import write_layers

        self._owner._view()
        return write_layers(
            output_filename=output_filename,
            topology=topology,
            chemical_states=chemical_states,
            structures=structures,
            interactions=interactions,
            associations=associations,
            skip_digestion=skip_digestion,
        )

    @_native_documentation("append_structures", module="h5msm", bind_primary=False)
    @signal(tags=["addon", "io"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def append_structures(
        self,
        filename,
        structures,
        *,
        structure_state_indices=None,
        block_size=256,
        skip_digestion=False,
    ):
        from molsysmt.h5msm import append_structures

        self._owner._view()
        return append_structures(
            filename=filename,
            structures=structures,
            structure_state_indices=structure_state_indices,
            block_size=block_size,
            skip_digestion=skip_digestion,
        )

    @_native_documentation("migrate_04_to_05", module="h5msm", bind_primary=False)
    @signal(tags=["addon", "io"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def migrate_04_to_05(self, filename, output_filename, skip_digestion=False):
        from molsysmt.h5msm import migrate_04_to_05

        self._owner._view()
        return migrate_04_to_05(
            filename=filename,
            output_filename=output_filename,
            skip_digestion=skip_digestion,
        )

    @_native_documentation("migrate_to_05", module="h5msm", bind_primary=False)
    @signal(tags=["addon", "io"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def migrate_to_05(self, filename, output_filename, skip_digestion=False):
        from molsysmt.h5msm import migrate_to_05

        self._owner._view()
        return migrate_to_05(
            filename=filename,
            output_filename=output_filename,
            skip_digestion=skip_digestion,
        )


class _FastaTools:
    _NAMES = ("read_records", "parse_records")

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    @_native_documentation("read_records", module="form.file_fasta", bind_primary=False)
    @signal(tags=["addon", "io"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def read_records(self, item, *, skip_digestion=False):
        from molsysmt.form.file_fasta import read_records

        self._owner._view()
        return read_records(
            item=item,
            skip_digestion=skip_digestion,
        )

    @_native_documentation(
        "parse_records", module="form.file_fasta", bind_primary=False
    )
    @signal(tags=["addon", "io"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def parse_records(self, fasta_text, *, source_label=None, skip_digestion=False):
        from molsysmt.form.file_fasta import parse_records

        self._owner._view()
        return parse_records(
            fasta_text=fasta_text,
            source_label=source_label,
            skip_digestion=skip_digestion,
        )
