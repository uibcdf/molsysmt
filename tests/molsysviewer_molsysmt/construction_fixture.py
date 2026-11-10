"""Explicit preparation inputs and independent native witnesses for GUI receiving."""


def notebook_cells(prefix):
    return [
        prefix
        + "import numpy as np\nfrom molsysmt.native import Structures\nview=msv.new_view()\nview\n",
        "assert msm.get(view.molsys,n_waters=True)==268\n"
        "_water_before=msm.copy(view.molsys)\n"
        "_assembly=msm.copy(view.molsys)\n"
        "_assembly.structures=Structures(coordinates=_assembly.structures.coordinates,box=_assembly.structures.box,bioassembly={'declared':{'chain_indices':[0],'rotations':[np.eye(3),np.eye(3)],'translations':msm.pyunitwizard.quantity([[0,0,0],[3,0,0]],'nm')}})\n"
        "view.load(_assembly,mode='replace')\n"
        "print('CONSTRUCTION_ASSEMBLY_READY')\n",
        "from tests.molsysviewer_molsysmt.test_solvation_tools import source\n"
        "view.load(source(),mode='replace')\n"
        "_solute_before=msm.copy(view.molsys)\n"
        "print('CONSTRUCTION_SOLVATION_READY')\n",
        "from tests.molsysviewer_molsysmt.test_build_assignment_tools import same\n"
        "same(view.molsys,_solute_before)\n"
        "_records=view.addons.manager.presentations.records()\n"
        "assert len(_records)==5,_records\n"
        "_outputs={row['title']:view.addons.manager.presentations.get(row['id']).molsys for row in _records}\n"
        "assert msm.get(_outputs['Constructed water cell'],n_waters=True)==268\n"
        "assert msm.get(_outputs['Ion placement'],n_ions=True,n_waters=True)==[3,265]\n"
        "assert _outputs['Biological assembly'].get_n_atoms()==1608\n"
        "assert msm.get(_outputs['Solvated system'],n_waters=True)>0\n"
        "_expected=msm.build.add_ions(_water_before,n_cations=2,n_anions=1,random_seed=19)\n"
        "np.testing.assert_array_equal(msm.pyunitwizard.get_value(_outputs['Ion placement'].structures.coordinates,to_unit='nm'),msm.pyunitwizard.get_value(_expected.structures.coordinates,to_unit='nm'))\n"
        "assert all(result is not view.molsys for result in _outputs.values())\n"
        "print('JUPYTER_CONSTRUCTION_NATIVE_OK')\n",
    ]
