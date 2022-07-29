from molsysmt import get_form, convert
from molsysmt.item.mdtraj_Trajectory.iterate import iterate_mdtraj_trajectory
from molsysmt._private.exceptions.not_implemented_errors import MolSysNotImplementedError
import molsysmt._private.exceptions.value_errors as exc


class Iterator:
    """ A class that allows to iterate trough trajectories of any type.
    """
    def __init__(self,
                 molecular_system,
                 start=0,
                 interval=1,
                 stop=None,
                 chunk_size=1,
                 selection="all",
                 syntaxis="MolSysMT"
                 ):
        self._molecular_system, self._form = self._get_molecular_system_and_form(molecular_system)
        self._start = start
        self._interval = interval
        self._stop = stop
        self._chunk_size = chunk_size
        self._selection = selection

        self._n_atoms = self._get_num_atoms()
        self._n_structures = self._get_num_structures()

        self._iterator = self._get_iterator()

    @property
    def molecular_system(self):
        """ Returns the molecular system this iterator is associated with.
        """
        return self._molecular_system

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if start < 0 or start >= self._n_structures:
            raise exc.IteratorStartError(
                f"Start should be > 0 and < {self._n_structures}"
            )
        self._start = start

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, interval):
        if interval < 1 or interval > self._n_structures:
            raise exc.IteratorIntervalError(
                f"Interval should be > 0 and < {self._n_structures}"
            )
        self._interval = interval

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, stop):
        if stop < 1 or stop > self._n_structures:
            raise exc.IteratorStopError(
                f"Stop should be > 0 and < {self._n_structures}"
            )
        self._stop = stop

    @property
    def chunk_size(self):
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, chunk_size):
        if chunk_size < 1 or chunk_size > self._n_structures:
            raise exc.IteratorChunkSizeError(
                f"Chunk size should be > 0 and < {self._n_structures}")
        self._chunk_size = chunk_size

    @staticmethod
    def _get_molecular_system_and_form(item):
        """ Returns a molecular system. """
        form = get_form(item)
        if form == "molsysmt.MolSys" or form == "molsysmt.Structures"\
                or form == "mdtraj.Trajectory":
            return item, form
        elif isinstance(form, list) or form.startswith("file"):
            return convert(item, to_form="molsysmt.MolSys"), "molsysmt.MolSys"

        else:
            raise MolSysNotImplementedError(
                f"Iterator has not been implemented for form {form}")

    def _get_iterator(self):
        """ Returns a generator function corresponding to the
            molecular system form passed
        """
        if self._form == "molsysmt.MolSys":
            return self.molecular_system.structures.iterate(
                start=self._start,
                stop=self._stop,
                interval=self._interval,
                selection=self._selection,
                chunk_size=self._chunk_size
            )
        elif self._form == "molsysmt.Structures":
            return self.molecular_system.iterate(
                start=self._start,
                stop=self._stop,
                interval=self._interval,
                selection=self._selection,
                chunk_size=self._chunk_size
            )
        elif self._form == "mdtraj.Trajectory":
            return iterate_mdtraj_trajectory(
                self.molecular_system,
                start=self._start,
                stop=self._stop,
                interval=self._interval,
                selection=self._selection,
                chunk_size=self._chunk_size
            )
        else:
            raise MolSysNotImplementedError(
                f"Iterator has not been implemented for form {self._form}")

    def _get_num_atoms(self):
        """ Returns the number of atoms in the molecular system."""
        if self._form == "molsysmt.MolSys":
            return self.molecular_system.structures.n_atoms
        elif self._form == "molsysmt.Structures" or self._form == "mdtraj.Trajectory":
            return self.molecular_system.n_atoms
        else:
            raise MolSysNotImplementedError(
                f"Iterator has not been implemented for form {self._form}")

    def _get_num_structures(self):
        """ Returns the number of atoms in the molecular system."""
        if self._form == "molsysmt.MolSys":
            return self.molecular_system.structures.n_structures
        elif self._form == "molsysmt.Structures":
            return self.molecular_system.n_structures
        elif self._form == "mdtraj.Trajectory":
            return self.molecular_system.n_frames
        else:
            raise MolSysNotImplementedError(
                f"Iterator has not been implemented for form {self._form}")

    def __iter__(self):
        return self._iterator

    def __next__(self):
        return next(self._iterator)
