import uuid


def _build_nglview_adapter():
    from nglview.adaptor import Structure, Trajectory

    class MolSysMTTrajectory(Trajectory, Structure):
        """Providing an NGLView adapter for molsysmt.MolSys objects."""

        def __init__(self, molsys, selection='all', structure_indices='all'):
            import molsysmt as msm
            from molsysmt import pyunitwizard as puw
            from molsysmt.form.nglview_NGLWidget._topology_sidecar import (
                SIDECAR_ATTRIBUTE,
            )

            snapshot = msm.extract(
                molsys,
                selection=selection,
                structure_indices=structure_indices,
                skip_digestion=True,
            )
            setattr(self, SIDECAR_ATTRIBUTE, snapshot.topology.copy())
            self.pdb = msm.convert(
                snapshot,
                to_form='string:pdb_text',
                structure_indices=[0],
                skip_digestion=True,
            )
            coordinates = msm.get(
                snapshot,
                element='system',
                coordinates=True,
                skip_digestion=True,
            )
            self.coordinates = puw.get_value(coordinates, to_unit='angstroms')
            self.ext = 'pdb'
            self.params = {}
            self.id = str(uuid.uuid4())

        def get_coordinates(self, index):
            return self.coordinates[index]

        @property
        def n_frames(self):
            return self.coordinates.shape[0]

        def get_structure_string(self):
            return self.pdb

    return MolSysMTTrajectory


def get_molsysmt_trajectory():
    """Returning the NGLView adapter class for molsysmt.MolSys objects."""
    return _build_nglview_adapter()


def show_molsysmt(molsys, selection='all', structure_indices='all', **kwargs):
    """Showing an NGLView widget from a molsysmt.MolSys object."""
    from nglview import NGLWidget

    trajectory_cls = get_molsysmt_trajectory()
    structure_trajectory = trajectory_cls(
        molsys,
        selection=selection,
        structure_indices=structure_indices,
    )
    return NGLWidget(structure_trajectory, **kwargs)
