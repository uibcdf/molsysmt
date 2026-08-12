import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


nglview = pytest.importorskip("nglview")


def test_topology_converts_to_a_topology_only_molsys(builder_pdb_molsys):
    source = builder_pdb_molsys.topology

    output, report = msm.convert(
        source,
        to_form="molsysmt.MolSys",
        return_report=True,
    )

    assert output.topology is not source
    assert output.topology.n_atoms == source.n_atoms
    assert output.structures.n_structures == 0
    assert output.structures.coordinates is None
    assert report.is_exhaustive is True
    assert report.outcome == "equivalent"


def test_topology_widget_requires_coordinates(builder_pdb_molsys):
    with pytest.raises(msm.NotCompatibleConversionError, match="coordinates"):
        msm.convert(
            builder_pdb_molsys.topology,
            to_form="nglview.NGLWidget",
        )


def test_topology_with_coordinates_builds_a_widget(builder_pdb_molsys):
    source = builder_pdb_molsys

    widget = msm.convert(
        source.topology,
        to_form="nglview.NGLWidget",
        coordinates=source.structures.coordinates,
        box=source.structures.box,
    )

    assert isinstance(widget, nglview.NGLWidget)
    observed = msm.convert(widget, to_form="molsysmt.MolSys")
    assert observed.topology.n_atoms == source.topology.n_atoms
    np.testing.assert_allclose(
        puw.get_value(observed.structures.coordinates, to_unit="nm"),
        puw.get_value(source.structures.coordinates, to_unit="nm"),
    )
