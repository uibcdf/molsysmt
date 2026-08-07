from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError, FormatError, ArgumentLengthError
from molsysmt import pyunitwizard as puw

## System

@arg_digest(form='openmm.Topology')
def set_box_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    if value is None:

        item.setPeriodicBoxVectors(None)

    else:

        box = puw.convert(value, to_unit='nanometers', to_form='openmm.unit')

        n_structures = box.shape[0]

        if n_structures == 1:

            item.setPeriodicBoxVectors(box[0])

        else:

            raise ArgumentLengthError(argument='value (box frames)', expected=1, actual=n_structures,
                                      caller='molsysmt.form.openmm_Topology.set.set_box_to_system',
                                      message='openmm.Topology only accepts a single-frame box.')

        pass

