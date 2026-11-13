import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.indices import indices_iterator
from molsysmt._private.smonitor import ArgumentError, NotImplementedIteratorError
from molsysmt._private.variables import is_all
from molsysmt.pbc import get_box_from_lengths_and_angles

_FIELDS = {
    "coordinates": ("coordinates", "nm"),
    "velocities": ("velocities", "nm/ps"),
    "time": ("time", "ps"),
    "temperature": ("temperature", "K"),
    "kinetic_energy": ("kineticEnergy", "kJ/mol"),
    "potential_energy": ("potentialEnergy", "kJ/mol"),
}


class StructuresIterator:
    @arg_digest(form="mdtraj.HDF5TrajectoryFile")
    def __init__(
        self,
        molecular_system,
        atom_indices="all",
        start=0,
        stop=None,
        step=1,
        chunk=1,
        structure_indices=None,
        output_type="values",
        skip_digestion=False,
        **kwargs,
    ):
        """Iterating over selected HDF5 structures with bounded coordinate reads.

        Parameters
        ----------
        molecular_system : mdtraj.HDF5TrajectoryFile
            Open, readable provider handle. The caller retains ownership.
        atom_indices : int, list, tuple, numpy.ndarray or str, default='all'
            Atom positions for coordinates and velocities, preserving query order
            and repeated positions.
        start, stop, step : int, optional
            Start, exclusive stop and stride over the selected structure sequence.
            Defaults are zero, its length and one, respectively.
        chunk : int, default=1
            Maximum selected structures per result.
        structure_indices : int, list, tuple, numpy.ndarray or str, optional
            Source structure positions, preserving order and repeats. None and
            'all' traverse the complete structure axis.
        output_type : {'values', 'dictionary'}, default='values'
            Ordered attribute values (one value if only one is requested) or a
            reusable attribute mapping. Copy the mapping when retaining chunks.
        skip_digestion : bool, default=False
            Whether to skip MolSysMT's internal argument digestion mechanism.
        **kwargs : bool
            Requested attributes: coordinates, velocities, time, box, temperature,
            kinetic_energy, potential_energy, total_energy or structure_index.
            The legacy structure_id fallback also reports source positions.

        Notes
        -----
        Missing optional series yield None. MDTraj decodes stored unit metadata;
        PyUnitWizard then applies the active application unit policy. The reader
        position is restored after every chunk, including failed reads, and this
        iterator never closes the caller's handle. Each provider read selects one
        structure; available unrequested fields may also be read by MDTraj.

        Examples
        --------
        >>> import mdtraj as md
        >>> import molsysmt as msm
        >>> path = msm.systems["pentalanine"]["traj_pentalanine.h5"]
        >>> with md.open(str(path), mode="r") as molsys:
        ...     iterator = StructuresIterator(
        ...         molsys, structure_indices=[2, 0], chunk=2, structure_index=True
        ...     )
        ...     next(iterator).tolist()
        [2, 0]

        .. versionadded:: 1.0.0
        """
        self.molecular_system = molecular_system
        self.atom_indices = atom_indices
        self.structure_indices = structure_indices
        self.start, self.stop, self.step, self.chunk = start, stop, step, chunk
        self.structure_index = None
        self.arguments = [key for key, requested in kwargs.items() if requested]
        self._output_dictionary = dict.fromkeys(self.arguments)
        self._output_type = output_type
        supported = {*_FIELDS, "box", "total_energy", "structure_index", "structure_id"}
        unsupported = set(self.arguments) - supported
        if unsupported:
            raise ArgumentError(
                argument="kwargs",
                caller="molsysmt.form.mdtraj_HDF5TrajectoryFile.StructuresIterator",
                message=f"Unsupported iterator attributes: {sorted(unsupported)}.",
            )

        if is_all(structure_indices):
            structure_indices = None
        if self.stop is None:
            self.stop = (
                len(molecular_system)
                if structure_indices is None
                else len(structure_indices)
            )
        self._indices_iterator = indices_iterator(
            indices=structure_indices,
            start=self.start,
            stop=self.stop,
            step=self.step,
            chunk=self.chunk,
        )
        self._read_atom_indices = None
        self._atom_inverse = None
        if not is_all(atom_indices):
            # PyTables indexing needs sorted unique positions; restore the query
            # axis after the provider read, without changing stored topology.
            self._read_atom_indices, self._atom_inverse = np.unique(
                atom_indices, return_inverse=True
            )

    def __iter__(self):
        return self

    def _quantity(self, rows, name, unit):
        values = [getattr(row, name) for row in rows]
        if any(value is None for value in values):
            return None
        values = np.concatenate(values, axis=0)
        if name in {"coordinates", "velocities"} and self._atom_inverse is not None:
            values = values[:, self._atom_inverse, :]
        return puw.standardize(puw.quantity(values, unit))

    def __next__(self):
        indices = np.atleast_1d(next(self._indices_iterator)).astype(np.int64)
        reader = self.molecular_system
        if np.any(indices < 0) or np.any(indices >= len(reader)):
            raise ArgumentError(
                argument="structure_indices",
                caller="molsysmt.form.mdtraj_HDF5TrajectoryFile.StructuresIterator",
                message="Structure positions must lie within the source structure axis.",
            )
        position = reader.tell()
        rows = []
        try:
            for index in indices:
                reader.seek(int(index))
                rows.append(
                    reader.read(n_frames=1, atom_indices=self._read_atom_indices)
                )
        finally:
            reader.seek(position)

        for argument in self.arguments:
            if argument in _FIELDS:
                field, unit = _FIELDS[argument]
                value = self._quantity(rows, field, unit)
            elif argument in {"structure_index", "structure_id"}:
                value = indices.copy()
            elif argument == "box":
                lengths = self._quantity(rows, "cell_lengths", "nm")
                angles = self._quantity(rows, "cell_angles", "degrees")
                value = None
                if lengths is not None and angles is not None:
                    value = get_box_from_lengths_and_angles(lengths, angles)
            elif argument == "total_energy":
                kinetic = self._quantity(rows, "kineticEnergy", "kJ/mol")
                potential = self._quantity(rows, "potentialEnergy", "kJ/mol")
                value = (
                    None
                    if kinetic is None or potential is None
                    else kinetic + potential
                )
            self._output_dictionary[argument] = value
        self.structure_index = indices
        if self._output_type == "dictionary":
            return self._output_dictionary
        values = list(self._output_dictionary.values())
        return values[0] if len(values) == 1 else values


class TopologyIterator:
    def __init__(self, molecular_system=None, **kwargs):
        raise NotImplementedIteratorError(form="mdtraj.HDF5TrajectoryFile")

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteratorError(form="mdtraj.HDF5TrajectoryFile")
