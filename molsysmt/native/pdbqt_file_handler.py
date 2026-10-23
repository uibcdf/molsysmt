"""Keeping validated PDBQT document metadata and selected coordinate blocks."""

from pathlib import Path

import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, FormatError
from molsysmt._private.variables import is_all


class PDBQTFileHandler:
    """Managing validated PDBQT snapshots or source-bound indexed file reads.

    Resident storage retains the complete source text. Indexed storage retains
    a read-only descriptor, byte ranges and one reference model; requested
    coordinate blocks are materialized on demand. Both modes validate every
    model before returning. Trees and remarks are document evidence, not
    inferred complete chemistry.
    """

    @arg_digest()
    def __init__(self, item, skip_digestion=False, *, storage_mode="resident"):
        """Opening a PDBQT path or explicit pdbqt_text: snapshot.

        Parameters
        ----------
        item : str or pathlib.Path
            File path or explicit pdbqt_text: string. All structures are validated
            on opening; atom identity, charges, types and trees must be invariant.
        skip_digestion : bool, default=False
            Whether to skip argument digestion.
        storage_mode : str, default='resident'
            'resident' owns a text snapshot independent of later file changes.
            'indexed' requires an uncompressed UTF-8 file, retains source-bound
            byte offsets and reads selected model bodies. File changes or path
            replacement invalidate indexed queries. Opening always validates
            every model; retained text/index/reference metadata and coordinate
            blocks have distinct memory costs.

        Notes
        -----
        Copies have independent close ownership. Indexed copies share a guarded
        descriptor until the final owner closes or is collected. Use a context
        manager for deterministic release. The file-form StructuresIterator uses
        indexed storage automatically; text is already resident. Reusing one
        indexed handler avoids repeated opening/validation through file queries.
        Source binding checks identity, size and nanosecond timestamps, not
        cryptographic authenticity or an immutable filesystem snapshot.

        .. versionadded:: 1.0.0
        """
        from molsysmt._private.pdbqt import PREFIX
        from molsysmt._private.pdbqt_document import PDBQTDocument

        self._document = None
        self._native_cache = None
        from molsysmt.basic import get_form

        if get_form(item) not in {"file:pdbqt", "string:pdbqt_text"}:
            raise ArgumentError("item", value=item, caller="PDBQTFileHandler")
        self._storage_mode = storage_mode
        if isinstance(item, str) and item.startswith(PREFIX):
            if storage_mode == "indexed":
                raise ArgumentError(
                    "storage_mode",
                    value=storage_mode,
                    caller="PDBQTFileHandler",
                    message="Indexed storage requires an uncompressed PDBQT file path.",
                )
            self._document = PDBQTDocument(item, start_offset=len(PREFIX))
        elif storage_mode == "indexed":
            from molsysmt._private.pdbqt_indexed_document import PDBQTIndexedDocument

            self._document = PDBQTIndexedDocument(item)
        else:
            self._document = PDBQTDocument(Path(item).read_bytes().decode("utf-8"))
        from weakref import finalize

        self._finalizer = finalize(self, self._document.release)

    def __repr__(self):
        document = getattr(self, "_document", None)
        mode = getattr(self, "_storage_mode", None)
        count = None if document is None else len(document.labels)
        return f"PDBQTFileHandler(closed={document is None}, storage_mode={mode!r}, n_structures={count})"

    @property
    def closed(self):
        return self._document is None

    @property
    def storage_mode(self):
        """Report resident snapshot or source-bound indexed storage."""
        return self._storage_mode

    def _require_open(self):
        if self.closed:
            raise FormatError(
                reason="PDBQTFileHandler is closed.", caller="PDBQTFileHandler"
            )

        self._document.validate_source()

    @property
    def n_atoms(self):
        self._require_open()
        return len(self._document.first["atoms"])

    @property
    def n_structures(self):
        self._require_open()
        return len(self._document.labels)

    @arg_digest()
    def close(self, skip_digestion=False):
        """Closing this handler and releasing its document ownership.

        Parameters
        ----------
        skip_digestion : bool, default=False
            Whether to skip argument digestion.

        Returns
        -------
        None
            Closure is idempotent. Other independently copied handlers remain usable.
        """
        self._document = None
        self._native_cache = None
        finalizer = getattr(self, "_finalizer", None)
        if finalizer is not None:
            finalizer()

    def __enter__(self):
        self._require_open()
        return self

    def __exit__(self, *args):
        self.close()
        return False

    @arg_digest()
    def copy(self, skip_digestion=False):
        """Copying independent ownership of the validated PDBQT document.

        Parameters
        ----------
        skip_digestion : bool, default=False
            Whether to skip argument digestion.

        Returns
        -------
        PDBQTFileHandler
            Open copy sharing immutable source text or an indexed-source lease.
            Each handle closes independently; projection caches are not shared.
            Indexed copies retain the same source-change checks.
        """
        self._require_open()
        output = object.__new__(type(self))
        self._document.acquire()
        output._document = self._document
        output._native_cache = None
        output._storage_mode = self._storage_mode
        from weakref import finalize

        output._finalizer = finalize(output, output._document.release)
        return output

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        output = self.copy()
        memo[id(self)] = output
        return output

    def _axis(self, value, size, name):
        from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis

        value = flat_axis(value, name, "PDBQTFileHandler")
        if value is None or is_all(value):
            return np.arange(size, dtype=np.int64)
        if np.any(value >= size):
            raise ArgumentError(name, value=value, caller="PDBQTFileHandler")
        return value

    def _native(self):
        from molsysmt._private.pdbqt import to_native

        self._require_open()
        if self._native_cache is None:
            self._native_cache = to_native(
                self._document.first, discard_torsion_tree=True
            )
        return self._native_cache

    def _series(self, attribute, indices, structure_indices):
        from molsysmt import pyunitwizard as puw

        atoms = self._axis(indices, self.n_atoms, "indices")
        structures = self._axis(
            structure_indices, self.n_structures, "structure_indices"
        )
        shape = (
            (len(structures), len(atoms), 3)
            if attribute == "coordinates"
            else (len(structures), len(atoms))
        )
        output = np.empty(shape, dtype=float)
        for row, index in enumerate(structures) if len(atoms) else []:
            record = self._document.record(index)
            output[row] = [
                np.nan
                if record["atoms"][atom][attribute] is None
                else record["atoms"][atom][attribute]
                for atom in atoms
            ]
        if attribute in {"coordinates", "b_factor"}:
            return puw.standardize(
                puw.quantity(
                    output, "angstrom" if attribute == "coordinates" else "angstrom**2"
                )
            )
        return output

    def _block(self, arguments, atoms, structures):
        from molsysmt import pyunitwizard as puw

        self._require_open()
        output = {}
        for attribute in arguments:
            if attribute == "structure_index":
                output[attribute] = structures.copy()
            elif attribute == "structure_id":
                labels = self._document.labels[structures].copy()
                output[attribute] = (
                    labels
                    if any(value is not None for value in self._document.labels)
                    else None
                )
            elif attribute == "n_structures":
                output[attribute] = len(structures)
            else:
                shape = (
                    (len(structures), len(atoms), 3)
                    if attribute == "coordinates"
                    else (len(structures), len(atoms))
                )
                output[attribute] = np.empty(shape, dtype=float)
        physical = [
            name
            for name in arguments
            if name in {"coordinates", "occupancy", "b_factor"}
        ]
        for row, index in enumerate(structures) if physical and len(atoms) else []:
            record = self._document.record(index)
            for attribute in physical:
                output[attribute][row] = [
                    np.nan
                    if record["atoms"][atom][attribute] is None
                    else record["atoms"][atom][attribute]
                    for atom in atoms
                ]
        for attribute, unit in [
            ("coordinates", "angstrom"),
            ("b_factor", "angstrom**2"),
        ]:
            if attribute in output:
                output[attribute] = puw.standardize(
                    puw.quantity(output[attribute], unit)
                )
        return output

    @arg_digest()
    def get_coordinates(
        self, indices="all", structure_indices="all", skip_digestion=False
    ):
        """Getting selected coordinate blocks with explicit length units.

        Parameters
        ----------
        indices : int, list, tuple or numpy.ndarray, default='all'
            Source atom positions, preserving supplied order and repetitions.
        structure_indices : int, list, tuple or numpy.ndarray, default='all'
            Source structure positions, independent of MODEL labels. Order and
            repetitions are retained; empty selections retain three coordinate axes.
        skip_digestion : bool, default=False
            Whether to skip argument digestion.

        Returns
        -------
        quantity
            Coordinates shaped (n_structures, n_atoms, 3), standardized through
            PyUnitWizard from explicit angstrom values. Default output lengths are nm.

        Raises
        ------
        ArgumentError
            If positional selections are invalid or carry quantity wrappers.
        FormatError
            If the handler is closed.
        """
        return self._series("coordinates", indices, structure_indices)

    @arg_digest()
    def get_torsion_tree(self, structure_index=0, skip_digestion=False):
        """Getting detached declared torsion evidence for one structure.

        Parameters
        ----------
        structure_index : int, default=0
            Source structure position, not its MODEL label.
        skip_digestion : bool, default=False
            Whether to skip argument digestion.

        Returns
        -------
        dict or None
            Detached molsysmt.pdbqt-torsion-tree@1 arrays and TORSDOF, or None for a
            rigid receptor. This is declared evidence, not complete bond perception.
        """
        index = self._axis(structure_index, self.n_structures, "structure_index")
        if len(index) != 1:
            raise ArgumentError(
                "structure_index", value=structure_index, caller="PDBQTFileHandler"
            )
        return self._document.detached_tree(int(index[0]))

    @arg_digest(argument_digestion=False)
    def get(
        self,
        element="system",
        selection="all",
        structure_indices="all",
        syntax="MolSysMT",
        output_type="values",
        skip_digestion=False,
        **kwargs,
    ):
        """Getting molecular attributes through the registered PDBQT contract.

        Parameters
        ----------
        element : str, default='system'
            Hierarchical level requested, such as atom, group or system.
        selection : str, list, tuple or numpy.ndarray, default='all'
            Elements selected with the standard basic.get semantics.
        structure_indices : int, list, tuple or numpy.ndarray, default='all'
            Source structure positions, preserving order and repetitions.
        syntax : str, default='MolSysMT'
            Selection language interpreted by the standard public query boundary.
        output_type : str, default='values'
            Return values in requested attribute order or a dictionary keyed by name.
        skip_digestion : bool, default=False
            Whether to skip this entry boundary's digestion. Delegated basic.get
            performs the value and attribute validation for these shared arguments.
        **kwargs : bool
            Attribute switches, for example coordinates=True or atom_name=True.

        Returns
        -------
        object
            Selected attribute values, or their dictionary. Coordinates and B factors
            carry explicit units; stored partial charges use elementary charge.
        """
        from molsysmt.basic import get

        self._require_open()
        return get(
            self,
            element=element,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
            output_type=output_type,
            **kwargs,
        )

    @arg_digest()
    def info(
        self,
        element="system",
        selection="all",
        structure_indices="all",
        syntax="MolSysMT",
        output_type="styler",
        skip_digestion=False,
        *,
        mask=None,
    ):
        """Summarizing selected document atoms and structures.

        Parameters
        ----------
        element : str, default='system'
            Hierarchical level summarized by the standard info implementation.
        selection : str, list, tuple or numpy.ndarray, default='all'
            Source element positions or a selection expression.
        structure_indices : int, list, tuple or numpy.ndarray, default='all'
            Source structures included in the summary.
        syntax : str, default='MolSysMT'
            Selection language for selection and mask.
        output_type : str, default='styler'
            Summary representation: styler, dataframe or dictionary.
        skip_digestion : bool, default=False
            Whether to skip argument digestion.
        mask : str, list, tuple, numpy.ndarray or None, default=None
            Optional scope intersected with the source selection.

        Returns
        -------
        object
            Summary of available attributes; no complete chemical graph is inferred.
        """
        from molsysmt.basic import info

        self._require_open()
        return info(
            self,
            element=element,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
            output_type=output_type,
            mask=mask,
        )

    @arg_digest()
    def read_poses(
        self,
        molecular_system,
        atom_map,
        structure_indices="all",
        missing_atoms="error",
        return_report=False,
        skip_digestion=False,
    ):
        """Reading mapped pose structures against a known chemical source.

        Parameters
        ----------
        molecular_system : molecular system
            Known prepared source with one explicit chemical state.
        atom_map : dict
            Completed molsysmt.atom_export@1 report from the source PDBQT writer.
        structure_indices : int, list, tuple or numpy.ndarray, default='all'
            Source structure positions, preserving order and repetitions. All models
            are checked against the export map before selection is returned.
        missing_atoms : str, default='error'
            Error on omitted source atoms; omit explicitly returns the retained
            subsystem. Missing H never inherit parent or source coordinates.
        return_report : bool, default=False
            Return molecular_system and a detached pose-read report when True.
        skip_digestion : bool, default=False
            Whether to skip argument digestion.

        Returns
        -------
        MolSys or dict
            Known chemistry with the selected pose coordinates in native nm storage,
            optionally accompanied by correspondence, units and producer evidence.
        """
        from molsysmt._private.pdbqt_poses import read_poses

        self._require_open()
        return read_poses(
            self,
            molecular_system,
            atom_map,
            structure_indices,
            missing_atoms,
            return_report,
        )

    def _domain(self, domain, atom_indices, structure_indices, discard_torsion_tree):
        from molsysmt._private.pdbqt import fail

        self._require_open()
        self._axis(structure_indices, self.n_structures, "structure_indices")
        if (
            self._document.first["torsion_tree"] is not None
            and not discard_torsion_tree
        ):
            fail(
                "Native domains omit the PDBQT torsion tree; explicitly authorize discard_torsion_tree=True."
            )
        output = self._native().copy(deep=False)
        if not is_all(atom_indices):
            output = output.extract(
                atom_indices=self._axis(atom_indices, self.n_atoms, "atom_indices")
            )
        return getattr(output, domain)

    def _to_native(self, atom_indices, structure_indices, discard_torsion_tree):
        from molsysmt._private.pdbqt import fail
        from molsysmt.native import Structures

        self._require_open()
        if (
            self._document.first["torsion_tree"] is not None
            and not discard_torsion_tree
        ):
            fail(
                "Native MolSys has no torsion-tree store; retain get_torsion_tree() and explicitly set discard_torsion_tree=True."
            )
        selected = self._axis(structure_indices, self.n_structures, "structure_indices")
        output = self._native().copy(deep=False)
        ids = self._document.labels[selected].copy()
        output.structures = Structures(
            coordinates=self._series("coordinates", "all", selected),
            structure_id=ids
            if any(v is not None for v in ids)
            else np.asarray(["0"] * len(ids), dtype=str),
        )
        for attribute in self._document.present:
            setattr(
                output.structures, attribute, self._series(attribute, "all", selected)
            )
        if not is_all(atom_indices):
            atoms = self._axis(atom_indices, self.n_atoms, "atom_indices")
            output = output.extract(atom_indices=atoms)
        return output

    def _payload(self, atom_indices="all", structure_indices="all"):
        from molsysmt._private.pdbqt import fail
        from molsysmt._private.pdbqt_writer import serialize

        self._require_open()
        selected = self._axis(structure_indices, self.n_structures, "structure_indices")
        atoms = self._axis(atom_indices, self.n_atoms, "atom_indices")
        from molsysmt._private.pdbqt_adapter import full_projection

        atoms_full = np.array_equal(np.unique(atoms), np.arange(self.n_atoms))
        if full_projection(
            self.n_atoms, atoms, selected, n_structures=self.n_structures
        ):
            return self._document.payload
        if not len(selected) or len(np.unique(selected)) != len(selected):
            fail(
                "PDBQT serialized structure selections must be nonempty and unique; getters/iterators preserve repeated indices."
            )
        if not atoms_full and self._document.first["torsion_tree"] is not None:
            fail(
                "PDBQT tree subsets require an explicitly remapped torsion_tree and native writer."
            )
        bodies = []
        for index in selected:
            if atoms_full:
                body = self._document.body(index)
            else:
                body = serialize(
                    self._to_native(atoms, [index], True), typing_scheme="autodock4"
                )
            if self._document.labels[index] is not None:
                body = (
                    f"MODEL {self._document.labels[index]}\n"
                    + body.rstrip("\r\n")
                    + "\nENDMDL\n"
                )
            bodies.append(body)
        return self._document.prefix + "".join(bodies)

    def _write_file(self, output_filename, atom_indices, structure_indices):
        from molsysmt._private.pdbqt import fail

        self._require_open()
        structures = self._axis(
            structure_indices, self.n_structures, "structure_indices"
        )
        atoms = self._axis(atom_indices, self.n_atoms, "atom_indices")
        if not len(structures) or len(np.unique(structures)) != len(structures):
            fail(
                "PDBQT serialized structure selections must be nonempty and unique; getters/iterators preserve repeated indices."
            )
        if np.array_equal(np.unique(atoms), np.arange(self.n_atoms)):
            return self._document.stream_to(output_filename, structures)

        def chunks():
            for position, index in enumerate(structures):
                payload = self._payload(atom_indices, [int(index)])
                if position:
                    payload = payload.removeprefix(self._document.prefix)
                for offset in range(0, len(payload), 64 * 1024):
                    try:
                        yield payload[offset : offset + 64 * 1024].encode("utf-8")
                    except UnicodeEncodeError:
                        fail("PDBQT text must be encodable as UTF-8.")

        return self._document.write_chunks(output_filename, chunks())
