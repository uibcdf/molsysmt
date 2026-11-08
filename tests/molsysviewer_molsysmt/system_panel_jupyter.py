"""Run the real Jupyter/popup gate without modifying an installed environment.

Invoke with the qualified Python 3.14 interpreter, --viewer-root pointing to
the received host source and --output pointing to a new private artifact folder.
--provider-root optionally selects the recorded public PyUnitWizard overlay.
JupyterLab, ipykernel, anywidget and the host's Playwright must already exist.
This local receiving script is separate from human-visible Qt qualification.
"""

import argparse
import importlib.metadata
import json
import os
import secrets
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


def _notebook(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "name": "receiving",
                "display_name": "Isolated molecular tools receiving",
                "language": "python",
            }
        },
        "cells": [
            {
                "id": f"receiving-{i}",
                "cell_type": "code",
                "metadata": {},
                "source": source.splitlines(True),
                "execution_count": None,
                "outputs": [],
            }
            for i, source in enumerate(cells)
        ],
    }


def _periodic_setup(*, general):
    cells = (
        [
            [[0.0, 3.0, 0.0], [-4.0, 0.0, 0.0], [0.0, 0.0, 5.0]],
            [[0.0, 0.0, 3.0], [4.0, 0.0, 0.7], [0.6, 5.0, 0.2]],
            [[0.0, -6.0, 0.0], [8.0, 0.0, 0.0], [0.0, 0.0, 10.0]],
        ]
        if general
        else [[[3.0, 0.0, 0.0], [0.7, 4.0, 0.0], [0.2, 0.6, 5.0]]] * 3
    )
    return f"""import itertools
import json
import numpy as np
_periodic_boxes=np.array({cells!r})
_periodic_general={general!r}
_periodic_before=source_coordinates+[8.,7.,6.]
view.addons.molsysmt.basic.set(coordinates=msm.pyunitwizard.quantity(_periodic_before,'nm'),box=msm.pyunitwizard.quantity(_periodic_boxes,'nm'))
_periodic_revision=view.addons.molsysmt.get_sync_status()['target_revision']
_origin=np.array([0.2,-0.4,0.7])
_periodic_component=_periodic_before.copy()
for structure in [2,0]:
    box=_periodic_boxes[structure]
    center=_periodic_before[structure].mean(axis=0)
    fractional=(center-_origin)@np.linalg.inv(box)
    target=_origin+(fractional-np.floor(fractional+0.5))@box
    _periodic_component[structure]+=target-center
_shifts=np.array(list(itertools.product(range(-2,3),repeat=3)))
def _nearest_lattice(vectors,box):
    seed=np.rint(vectors@np.linalg.inv(box))
    candidates=vectors[:,None]-(seed[:,None]+_shifts[None])@box
    return candidates[np.arange(len(vectors)),np.argmin(np.sum(candidates*candidates,axis=-1),axis=1)]
_periodic_source=_periodic_component.copy()
_periodic_source[0]=np.array([10.,10.,10.])+_nearest_lattice(_periodic_component[0]-[10.,10.,10.],_periodic_boxes[0])
assert np.max(np.abs(_periodic_source[0]-_periodic_component[0]))>1
_periodic_result=_periodic_source.copy()
_periodic_wrong_cell=_periodic_source.copy()
for structure in [1,2]:
    _periodic_result[structure]=_periodic_result[structure-1]+_nearest_lattice(_periodic_source[structure]-_periodic_result[structure-1],_periodic_boxes[structure-1])
    _periodic_wrong_cell[structure]=_periodic_wrong_cell[structure-1]+_nearest_lattice(_periodic_source[structure]-_periodic_wrong_cell[structure-1],_periodic_boxes[structure])
_periodic_control=float(np.max(np.abs(_periodic_result-_periodic_wrong_cell)))
if _periodic_general:
    assert _periodic_control>0.1, 'General fixture must distinguish the previous/current transition cells'
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--viewer-root", type=Path, required=True)
    parser.add_argument("--provider-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--scenario",
        choices=(
            "system",
            "results",
            "geometry",
            "rotate",
            "axes",
            "center",
            "center-errors",
            "fit",
            "fit-external",
            "periodic",
            "periodic-general",
            "chemistry",
            "chemistry-pending",
            "chemistry-preparation",
            "analysis",
        ),
        default="system",
    )
    parser.add_argument("--node", default="/usr/bin/node")
    parser.add_argument(
        "--chromium",
        default=os.environ.get("PW_CHROMIUM_BIN", "/usr/bin/google-chrome"),
    )
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[2]
    viewer = args.viewer_root.resolve()
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError(
            "Choose a new empty output directory; retained evidence is not overwritten."
        )
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    output.chmod(0o700)
    for directory in (
        "config",
        "runtime",
        "data/kernels/receiving",
        "notebooks",
        "workspaces",
        "settings",
    ):
        (output / directory).mkdir(parents=True)
    providers = [str(source), str(viewer)]
    if args.provider_root:
        providers.append(str(args.provider_root.resolve()))
    env = {
        **os.environ,
        "PYTHONPATH": os.pathsep.join(providers),
        "JUPYTER_CONFIG_DIR": str(output / "config"),
        "JUPYTER_RUNTIME_DIR": str(output / "runtime"),
        "JUPYTER_PATH": str(output / "data"),
        "JUPYTER_DATA_DIR": str(output / "data"),
        "JUPYTERLAB_WORKSPACES_DIR": str(output / "workspaces"),
        "JUPYTERLAB_SETTINGS_DIR": str(output / "settings"),
        "IPYTHONDIR": str(output / "ipython"),
        "MPLCONFIGDIR": str(output / "matplotlib"),
        "MOLSYSVIEWER_JUPYTER_SETTINGS": str(output / "settings.json"),
    }
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    token = secrets.token_hex(32)
    settings = {
        "port": port,
        "token": token,
        "contribution": str(source),
        "viewer_root": str(viewer),
        "chromium": args.chromium,
        "scenario": args.scenario,
    }
    (output / "settings.json").write_text(json.dumps(settings))
    (output / "settings.json").chmod(0o600)
    (output / "data/kernels/receiving/kernel.json").write_text(
        json.dumps(
            {
                "argv": [
                    sys.executable,
                    "-m",
                    "ipykernel_launcher",
                    "-f",
                    "{connection_file}",
                ],
                "display_name": "Isolated molecular tools receiving",
                "language": "python",
                "env": {"PYTHONPATH": env["PYTHONPATH"]},
            }
        )
    )
    config = output / "config/jupyter_server_config.py"
    config.write_text(
        "c = get_config()\n"
        f"c.IdentityProvider.token = {token!r}\n"
        "c.ServerApp.ip = '127.0.0.1'\n"
        f"c.ServerApp.port = {port}\n"
        "c.ServerApp.port_retries = 0\n"
        "c.ServerApp.open_browser = False\n"
        f"c.ServerApp.root_dir = {str(output / 'notebooks')!r}\n"
    )
    config.chmod(0o600)
    initial = (
        "from pathlib import Path\nimport molsysviewer as msv\nimport molsysmt as msm\n"
        f"assert Path(msm.__file__).resolve() == Path({str(source / 'molsysmt/__init__.py')!r})\n"
        f"assert Path(msv.__file__).resolve() == Path({str(viewer / 'molsysviewer/__init__.py')!r})\n"
        "view = msv.demo['1TCD']\nassert view.molsys.get_n_atoms() == 3983\nview\n"
    )
    if args.provider_root:
        provider_check = (
            "import pyunitwizard as puw\n"
            f"assert Path(puw.__file__).resolve() == Path({str(args.provider_root.resolve() / 'pyunitwizard/__init__.py')!r})\n"
        )
        initial = initial.replace("view = msv.demo", provider_check + "view = msv.demo")
    final = (
        "assert view.molsys.get_n_atoms() == 3817\n"
        "status = view.addons.molsysmt.get_sync_status()\n"
        "assert status['state'] == 'synchronized'\nassert status['target_revision'] == 2\n"
        "print('JUPYTER_SYSTEM_NATIVE_OK', view.molsys.get_n_atoms())\n"
    )
    if args.scenario == "results":
        initial = initial[: initial.index("view = msv.demo")] + (
            "with msv.demo['pentalanine'] as seed:\n"
            "    view = msv.new_view(seed.molsys, structure_indices=[0, 8, 3])\n"
            "source_coordinates = msm.pyunitwizard.get_value(view.molsys.structures.coordinates, to_unit='nm').copy()\nview\n"
        )
        final = (
            "import numpy as np\n"
            "records = view.addons.manager.presentations.records()\n"
            "assert len(records) == 2, records\n"
            "subset = next(item for item in records if item['title'] == 'Subset review')\n"
            "copy = next(item for item in records if item['title'] == 'Copy review')\n"
            "subset_view = view.addons.manager.presentations.get(subset['id'])\n"
            "copy_view = view.addons.manager.presentations.get(copy['id'])\n"
            "assert subset_view.molsys.get_n_atoms() == 3\n"
            "np.testing.assert_equal(msm.pyunitwizard.get_value(subset_view.molsys.structures.coordinates, to_unit='nm'), source_coordinates[[2,0]][:,[2,4,6]])\n"
            "np.testing.assert_equal(msm.pyunitwizard.get_value(view.molsys.structures.coordinates, to_unit='nm'), source_coordinates)\n"
            "assert not np.shares_memory(msm.pyunitwizard.get_value(copy_view.molsys.structures.coordinates, to_unit='nm'), msm.pyunitwizard.get_value(view.molsys.structures.coordinates, to_unit='nm'))\n"
            "view.close()\nassert not subset_view.closed and not copy_view.closed\n"
            "print('JUPYTER_INDEPENDENT_RESULTS_OK', len(records))\n"
        )
    if args.scenario in {
        "geometry",
        "rotate",
        "axes",
        "center",
        "center-errors",
        "fit",
        "fit-external",
        "periodic",
        "periodic-general",
    }:
        initial = initial[: initial.index("view = msv.demo")] + (
            "with msv.demo['pentalanine'] as seed:\n"
            "    view = msv.new_view(seed.molsys, structure_indices=[0, 8, 3])\n"
            "view.selections.add('chosen', atom_indices=[2,4])\n"
            "source_coordinates = msm.pyunitwizard.get_value(view.molsys.structures.coordinates, to_unit='nm').copy()\nview\n"
        )
        final = (
            "import numpy as np\n"
            "expected = source_coordinates.copy()\n"
            "expected[np.ix_([2,0],[2,4],range(3))] += [0.1,-0.2,0.3]\n"
            "np.testing.assert_allclose(msm.pyunitwizard.get_value(view.molsys.structures.coordinates, to_unit='nm'), expected)\n"
            "assert view.addons.molsysmt.get_sync_status()['target_revision'] == 1\n"
            "records = view.addons.manager.presentations.records()\nassert len(records) == 1\n"
            "result = view.addons.manager.presentations.get(records[0]['id'])\n"
            "expected[0,[2,4]] += [2,0,0]\n"
            "np.testing.assert_allclose(msm.pyunitwizard.get_value(result.molsys.structures.coordinates, to_unit='nm'), expected)\n"
            "assert result.molsys is not view.molsys and result.player.n_structures == 3\n"
            "print('JUPYTER_GEOMETRY_NATIVE_OK', len(records))\n"
        )
    if args.scenario == "axes":
        initial = initial.removesuffix("view\n") + (
            "import numpy as np\n"
            "import json\n"
            "view.addons.molsysmt.basic.set(box=msm.pyunitwizard.quantity(np.tile(np.eye(3)*5,(3,1,1)),'nm'))\n"
            "_axes_revision=view.addons.molsysmt.get_sync_status()['target_revision']\n"
            "_axes_box=msm.pyunitwizard.get_value(view.molsys.structures.box,to_unit='nm').copy()\n"
            "_axes_chemistry=msm.convert(view.molsys.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict()\n"
            "_axes_analysis=msm.interactions.hbonds.get_buch_hbonds(view.molsys,structure_indices='all',pbc=False,output_type='molsysmt.Interactions')\n"
            "view.interactions.attach(_axes_analysis,name='science',assume_aligned=True)\n"
            "_axes_basis=np.array([[0.,1.,0.],[0.,0.,1.],[1.,0.,0.]])\n"
            "_axes_weights=msm.pyunitwizard.get_value(msm.physchem.get_mass(view.molsys,element='atom',selection=list(range(8))),to_unit='dalton')\n"
            "def _principal_oracle(base,weights,kind,basis,centered):\n"
            "    center=np.average(base[:8],axis=0,weights=weights)\n"
            "    delta=base[:8]-center\n"
            "    covariance=(delta*weights[:,None]).T@delta/weights.sum()\n"
            "    eigenvalues=np.linalg.eigvalsh(covariance)\n"
            "    if kind=='inertia': eigenvalues=eigenvalues[::-1]\n"
            "    return {'before_angstrom':(base*10).tolist(),'target_center_angstrom':(np.zeros(3) if centered else center*10).tolist(),'target_variances_angstrom2':(eigenvalues*100).tolist(),'weights':weights.tolist(),'basis':basis.tolist()}\n"
        )
        initial += f"Path({str(output / 'axes-source-oracle.json')!r}).write_text(json.dumps(_principal_oracle(source_coordinates[0],np.ones(8),'inertia',np.eye(3),False)))\nview\n"
        axes_middle = (
            "_axes_source_received=msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm').copy()\n"
            "assert view.addons.molsysmt.get_sync_status()['target_revision']==_axes_revision+1\n"
        )
        axes_middle += f"Path({str(output / 'axes-result-oracle.json')!r}).write_text(json.dumps(_principal_oracle(_axes_source_received[0],_axes_weights,'geometric',_axes_basis,True)))\nprint('JUPYTER_AXES_REFERENCE_OK')\n"
        final = (
            "def _verify_principal_native(base,after,structures,weights,kind,basis,centered):\n"
            "    for structure in structures:\n"
            "        center=np.average(base[structure,:8],axis=0,weights=weights)\n"
            "        delta=base[structure,:8]-center\n"
            "        covariance=(delta*weights[:,None]).T@delta/weights.sum()\n"
            "        _,vectors=np.linalg.eigh(covariance)\n"
            "        if kind=='inertia': vectors=vectors[:,::-1]\n"
            "        projected=(after[structure,:8]-(0 if centered else center))@basis.T\n"
            "        np.testing.assert_allclose(projected**2,(delta@vectors)**2,atol=1e-10)\n"
            "        np.testing.assert_allclose(np.linalg.norm(after[structure,:8,None]-after[structure,None,:8],axis=-1),np.linalg.norm(base[structure,:8,None]-base[structure,None,:8],axis=-1),atol=1e-12)\n"
            "        np.testing.assert_allclose(np.linalg.det(after[structure,[1,2,3]]-after[structure,0]),np.linalg.det(base[structure,[1,2,3]]-base[structure,0]),atol=1e-12)\n"
            "        np.testing.assert_array_equal(after[structure,8:],base[structure,8:])\n"
            "    for structure in set(range(3))-set(structures):\n"
            "        np.testing.assert_array_equal(after[structure],base[structure])\n"
            "source_after=msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm')\n"
            "_verify_principal_native(source_coordinates,source_after,[2,0],np.ones(8),'inertia',np.eye(3),False)\n"
            "np.testing.assert_array_equal(source_after,_axes_source_received)\n"
            "assert view.addons.molsysmt.get_sync_status()['target_revision']==_axes_revision+1\n"
            "records=view.addons.manager.presentations.records()\n"
            "assert len(records)==1\n"
            "result=view.addons.manager.presentations.get(records[0]['id'])\n"
            "candidate=msm.pyunitwizard.get_value(result.molsys.structures.coordinates,to_unit='nm')\n"
            "_verify_principal_native(_axes_source_received,candidate,[0],_axes_weights,'geometric',_axes_basis,True)\n"
            "assert result.molsys is not view.molsys and result.player.n_structures==3\n"
            "assert not np.shares_memory(msm.pyunitwizard.get_value(result.molsys.structures.coordinates),msm.pyunitwizard.get_value(view.molsys.structures.coordinates))\n"
            "for molecular_system in [view.molsys,result.molsys]:\n"
            "    np.testing.assert_array_equal(msm.pyunitwizard.get_value(molecular_system.structures.box,to_unit='nm'),_axes_box)\n"
            "    np.testing.assert_equal(msm.convert(molecular_system.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict(),_axes_chemistry)\n"
            "    np.testing.assert_array_equal(molecular_system.interactions['science'].evaluated_structure_indices,[1])\n"
            "np.testing.assert_array_equal(_axes_analysis.evaluated_structure_indices,[0,1,2])\n"
            "print('JUPYTER_AXES_NATIVE_OK',len(records))\n"
        )
    if args.scenario == "rotate":
        initial = (
            initial.removesuffix("view\n")
            + "import numpy as np\nview.addons.molsysmt.basic.set(box=msm.pyunitwizard.quantity(np.tile(np.eye(3)*5,(3,1,1)),'nm'))\n_rotation_revision=view.addons.molsysmt.get_sync_status()['target_revision']\n_rotation_box=msm.pyunitwizard.get_value(view.molsys.structures.box,to_unit='nm').copy()\n_rotation_chemistry=msm.convert(view.molsys.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict()\n_rotation_analysis=msm.interactions.hbonds.get_buch_hbonds(view.molsys,structure_indices='all',pbc=False,output_type='molsysmt.Interactions')\nview.interactions.attach(_rotation_analysis,name='science',assume_aligned=True)\nview\n"
        )
        final = "expected=source_coordinates.copy()\nfor structure in [2,0]:\n    center=source_coordinates[structure,:10].mean(axis=0)\n    relative=source_coordinates[structure,:10]-center\n    expected[structure,:10,0]=center[0]-relative[:,1]\n    expected[structure,:10,1]=center[1]+relative[:,0]\nnp.testing.assert_allclose(msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm'),expected,atol=1e-12)\nassert view.addons.molsysmt.get_sync_status()['target_revision']==_rotation_revision+1\nrecords=view.addons.manager.presentations.records()\nassert len(records)==1\nresult=view.addons.manager.presentations.get(records[0]['id'])\ncandidate=expected.copy()\ncenter=np.array([0.1,-0.2,0.3])\nrelative=expected[0,:10]-center\ncandidate[0,:10,0]=center[0]+relative[:,1]\ncandidate[0,:10,1]=center[1]-relative[:,0]\nnp.testing.assert_allclose(msm.pyunitwizard.get_value(result.molsys.structures.coordinates,to_unit='nm'),candidate,atol=1e-12)\nassert result.molsys is not view.molsys and result.player.n_structures==3\nassert not np.shares_memory(msm.pyunitwizard.get_value(result.molsys.structures.coordinates),msm.pyunitwizard.get_value(view.molsys.structures.coordinates))\nfor molecular_system in [view.molsys,result.molsys]:\n    np.testing.assert_array_equal(msm.pyunitwizard.get_value(molecular_system.structures.box,to_unit='nm'),_rotation_box)\n    np.testing.assert_equal(msm.convert(molecular_system.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict(),_rotation_chemistry)\n    np.testing.assert_array_equal(molecular_system.interactions['science'].evaluated_structure_indices,[1])\nnp.testing.assert_array_equal(_rotation_analysis.evaluated_structure_indices,[0,1,2])\nprint('JUPYTER_ROTATE_NATIVE_OK',len(records))\n"
    if args.scenario == "center":
        final = (
            "import numpy as np\nexpected = source_coordinates.copy()\n"
            "for frame in [2,0]:\n"
            "    expected[frame,:10] += np.array([0.1,0.2,0.3])-source_coordinates[frame,[2,4]].mean(axis=0)\n"
            "np.testing.assert_allclose(msm.pyunitwizard.get_value(view.molsys.structures.coordinates, to_unit='nm'), expected, atol=1e-12)\n"
            "assert view.addons.molsysmt.get_sync_status()['target_revision'] == 1\n"
            "records = view.addons.manager.presentations.records()\nassert len(records) == 1\n"
            "result = view.addons.manager.presentations.get(records[0]['id'])\n"
            "candidate = expected.copy()\n"
            "candidate[0,:10] += expected[0,[10,12]].mean(axis=0)-expected[0,[2,4]].mean(axis=0)\n"
            "np.testing.assert_allclose(msm.pyunitwizard.get_value(result.molsys.structures.coordinates, to_unit='nm'), candidate, atol=1e-12)\n"
            "assert result.molsys is not view.molsys and result.player.n_structures == 3\n"
            "print('JUPYTER_CENTER_NATIVE_OK', len(records))\n"
        )
    if args.scenario == "fit":
        initial = initial.removesuffix("view\n") + (
            "import json\nimport numpy as np\n"
            "def _fit_oracle(base, frames, ref_frame):\n"
            "    expected = base.copy()\n"
            "    anchor = np.asarray(msm.select(view.molsys, selection=\"atom_name=='CA'\"), dtype=int)\n"
            "    reference = base[ref_frame,anchor]\n"
            "    qc = reference.mean(axis=0)\n"
            "    for frame in frames:\n"
            "        query = base[frame,anchor]\n"
            "        pc = query.mean(axis=0)\n"
            "        u, _, vt = np.linalg.svd((query-pc).T@(reference-qc))\n"
            "        proper = np.eye(3); proper[-1,-1] = np.linalg.det(u@vt)\n"
            "        expected[frame,:10] = (base[frame,:10]-pc)@(u@proper@vt)+qc\n"
            "    return expected\n"
            "_fit_source_expected = _fit_oracle(source_coordinates,[2,0],1)\n"
            "_fit_result_expected = _fit_oracle(_fit_source_expected,[0],2)\n"
            f"Path({str(output / 'fit-expected.json')!r}).write_text(json.dumps({{'source_angstrom':(_fit_source_expected*10).tolist(),'result_angstrom':(_fit_result_expected*10).tolist()}}))\nview\n"
        )
        final = (
            "np.testing.assert_allclose(msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm'),_fit_source_expected,atol=1e-10)\n"
            "assert view.addons.molsysmt.get_sync_status()['target_revision']==1\n"
            "records=view.addons.manager.presentations.records()\nassert len(records)==1\n"
            "result=view.addons.manager.presentations.get(records[0]['id'])\n"
            "np.testing.assert_allclose(msm.pyunitwizard.get_value(result.molsys.structures.coordinates,to_unit='nm'),_fit_result_expected,atol=1e-10)\n"
            "assert result.molsys is not view.molsys and result.player.n_structures==3\n"
            "print('JUPYTER_FIT_NATIVE_OK',len(records))\n"
        )
    if args.scenario == "fit-external":
        initial = initial.removesuffix("view\n") + (
            "import hashlib\nimport json\nimport numpy as np\n"
            "from molsysmt.native import Structures\n"
            "_base=source_coordinates[0].copy()\n"
            "_turn=np.array([[0,-1,0],[1,0,0],[0,0,1]],dtype=float)\n"
            "source_coordinates=np.stack([_base@r.T+t for r,t in [(_turn,[1.2,-.3,.6]),(np.eye(3),[-.5,.4,.2]),(_turn.T,[.3,1.4,-.8])]])\n"
            "_boxes=msm.pyunitwizard.quantity(np.tile(np.eye(3)*3,(3,1,1)),'nm')\n"
            "view.addons.molsysmt.basic.set(coordinates=msm.pyunitwizard.quantity(source_coordinates,'nm'),box=_boxes)\n"
            "_source_revision=view.addons.molsysmt.get_sync_status()['target_revision']\n"
            "view.molsys.interactions={'coverage':msm.Interactions.from_records([],n_atoms=62,n_structures=3,method='existing-coverage',evaluated_structure_indices=[0,1,2])}\n"
            "_original_coverage=view.molsys.interactions['coverage']\n"
            "_ref_turn=np.array([[1,0,0],[0,0,-1],[0,1,0]],dtype=float)\n"
            "_reference=np.stack([_base[[7,19,0,11,3,0,2,4,6,8]]@_ref_turn.T+np.array([3.1,-2.2,.7])+i*.1 for i in range(7)])\n"
            f"_reference_path=Path({str(output / 'external-reference.h5msm')!r})\n"
            "msm.h5msm.write_layers(_reference_path,structures=Structures(coordinates=msm.pyunitwizard.quantity(_reference,'nm')))\n"
            "_reference_digest=hashlib.sha256(_reference_path.read_bytes()).hexdigest()\n"
            "_fit_source_expected=source_coordinates.copy()\n"
            "_fit_source_expected[np.ix_([2,0],range(10))]=_base[:10]@_ref_turn.T+np.array([3.1,-2.2,.7])+.6\n"
            "_fit_result_expected=_fit_source_expected.copy()\n"
            "_fit_result_expected[0,:10]=_base[:10]@_ref_turn.T+np.array([3.1,-2.2,.7])\n"
            f"Path({str(output / 'fit-external-expected.json')!r}).write_text(json.dumps({{'reference_filename':str(_reference_path),'source_angstrom':(_fit_source_expected*10).tolist(),'result_angstrom':(_fit_result_expected*10).tolist()}}))\n"
            "_unit_policy=msm.pyunitwizard.context(standard_units=['pm','ps','radians'])\n"
            "_unit_policy.__enter__()\nview\n"
        )
        final = (
            "np.testing.assert_allclose(msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm'),_fit_source_expected,atol=1e-10)\n"
            "assert view.addons.molsysmt.get_sync_status()['target_revision']==_source_revision+1\n"
            "records=view.addons.manager.presentations.records()\nassert len(records)==1\n"
            "result=view.addons.manager.presentations.get(records[0]['id'])\n"
            "np.testing.assert_allclose(msm.pyunitwizard.get_value(result.molsys.structures.coordinates,to_unit='nm'),_fit_result_expected,atol=1e-10)\n"
            "np.testing.assert_array_equal(msm.pyunitwizard.get_value(view.molsys.structures.box,to_unit='nm'),msm.pyunitwizard.get_value(_boxes,to_unit='nm'))\n"
            "np.testing.assert_array_equal(msm.pyunitwizard.get_value(result.molsys.structures.box,to_unit='nm'),msm.pyunitwizard.get_value(_boxes,to_unit='nm'))\n"
            "assert result.molsys is not view.molsys and result.player.n_structures==3\n"
            "np.testing.assert_array_equal(view.molsys.interactions['coverage'].evaluated_structure_indices,[1])\n"
            "np.testing.assert_array_equal(result.molsys.interactions['coverage'].evaluated_structure_indices,[1])\n"
            "np.testing.assert_array_equal(_original_coverage.evaluated_structure_indices,[0,1,2])\n"
            "assert hashlib.sha256(_reference_path.read_bytes()).hexdigest()==_reference_digest\n"
            "_unit_policy.__exit__(None,None,None)\n"
            "print('JUPYTER_EXTERNAL_FIT_NATIVE_OK',len(records))\n"
        )
    if args.scenario in {"periodic", "periodic-general"}:
        initial = initial.removesuffix("view\n") + _periodic_setup(
            general=args.scenario == "periodic-general"
        )
        initial += f"Path({str(output / 'periodic-expected.json')!r}).write_text(json.dumps({{'before_angstrom':(_periodic_before*10).tolist(),'component_angstrom':(_periodic_component*10).tolist(),'source_angstrom':(_periodic_source*10).tolist(),'result_angstrom':(_periodic_result*10).tolist(),'boxes_nm':_periodic_boxes.tolist(),'general_cells':_periodic_general,'transition_control_difference_nm':_periodic_control}}))\nview\n"
        final = (
            "np.testing.assert_allclose(msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm'),_periodic_source,atol=5e-12)\n"
            "np.testing.assert_array_equal(msm.pyunitwizard.get_value(view.molsys.structures.box,to_unit='nm'),_periodic_boxes)\n"
            "assert view.addons.molsysmt.get_sync_status()['target_revision']==_periodic_revision+2\n"
            "records=view.addons.manager.presentations.records()\nassert len(records)==1\n"
            "result=view.addons.manager.presentations.get(records[0]['id'])\n"
            "np.testing.assert_allclose(msm.pyunitwizard.get_value(result.molsys.structures.coordinates,to_unit='nm'),_periodic_result,atol=5e-12)\n"
            "np.testing.assert_array_equal(msm.pyunitwizard.get_value(result.molsys.structures.box,to_unit='nm'),_periodic_boxes)\n"
            "assert result.molsys is not view.molsys and result.player.n_structures==3\n"
            "result.player.go_to_structure(1)\n"
            "print('JUPYTER_PERIODIC_NATIVE_OK',len(records))\n"
        )
    if args.scenario == "center-errors":
        initial = initial.removesuffix("view\n") + (
            "from molsysviewer_molsysmt._geometry_panel import _GeometryPanel\n"
            "_GeometryPanel._esm = _GeometryPanel._esm.replace('export function render({model,el}) {', 'export function render({model,el}) { window.__errorPanelModel=model;')\n"
            "_mass_policy = msm.pyunitwizard.context(standard_units=['pm','ps','radians'])\n"
            "_mass_policy.__enter__()\nview\n"
        )
        final = (
            "import numpy as np\n"
            "np.testing.assert_array_equal(msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm'),source_coordinates)\n"
            "assert view.addons.molsysmt.get_sync_status()['state']=='synchronized'\n"
            "assert view.addons.molsysmt.get_sync_status()['target_revision']==0\n"
            "_mass_policy.__exit__(None,None,None)\n"
            "print('JUPYTER_NATIVE_ERROR_PRESERVED')\n"
        )
    if args.scenario == "chemistry":
        initial = initial.removesuffix("view\n") + (
            "import numpy as np\n"
            "source_coordinates=msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm').copy()\n"
            "source_chemistry=msm.convert(view.molsys.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict()\n"
            "source_scene=view.export_state()\n"
            "view\n"
        )
        final = (
            "np.testing.assert_array_equal(msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm'),source_coordinates)\n"
            "np.testing.assert_equal(msm.convert(view.molsys.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict(),source_chemistry)\n"
            "import json\n"
            "current_scene=view.export_state()\n"
            f"Path({str(output / 'chemistry-scene-comparison.json')!r}).write_text(json.dumps({{'before':source_scene,'after':current_scene}}))\n"
            "assert 'camera' not in source_scene['view'] and 'camera' in current_scene['view']\n"
            "source_objects={k:v for k,v in source_scene.items() if k!='view'}\n"
            "assert {k:v for k,v in current_scene.items() if k!='view'}==source_objects\n"
            "assert {k:v for k,v in current_scene['view'].items() if k!='camera'}==source_scene['view']\n"
            "assert view.addons.molsysmt.get_sync_status()['target_revision']==0\n"
            "assert not view.addons.manager.presentations.records()\n"
            "print('JUPYTER_CHEMISTRY_UNCHANGED',view.molsys.get_n_atoms())\n"
        )
    if args.scenario == "chemistry-pending":
        initial = initial.removesuffix("view\n") + (
            "import numpy as np\n"
            "source_coordinates=msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm').copy()\n"
            "source_chemistry=msm.convert(view.molsys.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict()\n"
            "view.regions.add(selection=[0,2],tag='owned-before-edit')\n"
            "source_regions=view.export_state()['regions']\n"
            "def defer_reader_box():\n"
            "    revision=view.addons.molsysmt.get_sync_status()['target_revision']\n"
            "    view.addons.molsysmt.basic.set(box=msm.pyunitwizard.quantity((np.eye(3)*(3+revision))[None],'nm'),update_view=False)\n"
            "    assert view.addons.molsysmt.get_sync_status()['state']=='pending'\n"
            "    print('READER_PENDING',revision+1)\n"
            "def verify_reader_pending(expected_revision):\n"
            "    status=view.addons.molsysmt.get_sync_status()\n"
            "    assert status['state']=='pending' and status['target_revision']==expected_revision, status\n"
            "    np.testing.assert_array_equal(msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm'),source_coordinates)\n"
            "    np.testing.assert_equal(msm.convert(view.molsys.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict(),source_chemistry)\n"
            "    print('READER_PENDING_UNCHANGED',expected_revision)\n"
            "view\n"
        )
        final = (
            "assert view.addons.molsysmt.get_sync_status()['state']=='synchronized'\n"
            "assert view.addons.molsysmt.get_sync_status()['target_revision']==3\n"
            "np.testing.assert_array_equal(msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm'),source_coordinates)\n"
            "np.testing.assert_equal(msm.convert(view.molsys.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict(),source_chemistry)\n"
            "assert view.export_state()['regions']==source_regions\n"
            "assert not view.addons.manager.presentations.records()\n"
            "print('JUPYTER_PENDING_READERS_OK',view.molsys.get_n_atoms())\n"
        )
    if args.scenario == "chemistry-preparation":
        initial = initial.removesuffix("view\n") + (
            "import numpy as np\n"
            "original_system=view.molsys\n"
            "source_coordinates=msm.pyunitwizard.get_value(original_system.structures.coordinates,to_unit='nm').copy()\n"
            "source_chemistry=msm.convert(original_system.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict()\n"
            "view.regions.add(selection=[0,2],tag='before-preparation')\n"
            "def verify_preparation_source():\n"
            "    assert view.molsys is original_system\n"
            "    assert view.addons.molsysmt.get_sync_status()['target_revision']==0\n"
            "    np.testing.assert_array_equal(msm.pyunitwizard.get_value(original_system.structures.coordinates,to_unit='nm'),source_coordinates)\n"
            "    np.testing.assert_equal(msm.convert(original_system.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict(),source_chemistry)\n"
            "    print('PREPARATION_SOURCE_UNCHANGED')\n"
            "view\n"
        )
        final = (
            "np.testing.assert_array_equal(msm.pyunitwizard.get_value(original_system.structures.coordinates,to_unit='nm'),source_coordinates)\n"
            "assert view.molsys is not original_system and view.molsys.get_n_atoms()==7868\n"
            "assert 'before-preparation' not in view.regions\n"
            "status=view.addons.molsysmt.get_sync_status()\n"
            "assert status['state']=='synchronized' and status['target_revision']==1, status\n"
            "records=view.addons.manager.presentations.records()\nassert len(records)==2, records\n"
            "hydrogens=next(x for x in records if x['title']=='TcTIM with hydrogens')\n"
            "child=view.addons.manager.presentations.get(hydrogens['id'])\n"
            "assert child.molsys is not view.molsys and child.molsys.get_n_atoms()==7868\n"
            "np.testing.assert_array_equal(msm.pyunitwizard.get_value(child.molsys.structures.coordinates,to_unit='nm'),msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm'))\n"
            "assert not np.shares_memory(msm.pyunitwizard.get_value(child.molsys.structures.coordinates,to_unit='nm'),msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm'))\n"
            "print('JUPYTER_PREPARATION_NATIVE_OK',view.molsys.get_n_atoms())\n"
        )
    if args.scenario == "analysis":
        initial = initial.removesuffix("view\n") + (
            "import numpy as np\nimport json\n"
            "source_coordinates=msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm').copy()\n"
            "source_chemistry=msm.convert(view.molsys.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict()\n"
            "source_scene=view.export_state()\n"
            "_distances=np.linalg.norm(source_coordinates[0][[0,2]][:,None,:]-source_coordinates[0][[3,5,7]][None,:,:],axis=-1)\n"
            "_centers=np.stack([source_coordinates[0,[0,2]].mean(axis=0),source_coordinates[0,[3,5,7]].mean(axis=0)])\n"
            f"Path({str(output / 'analysis-expected.json')!r}).write_text(json.dumps({{'distances':_distances.ravel().tolist(),'minimum':float(_distances.min()),'maximum':float(_distances.max()),'page51':float(np.linalg.norm(source_coordinates[0,50]-source_coordinates[0,3])),'center_points_angstrom':(_centers*10).tolist(),'focus_points_angstrom':(source_coordinates[0,[0,3]]*10).tolist()}}))\n"
            "view\n"
        )
        final = (
            "np.testing.assert_array_equal(msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm'),source_coordinates)\n"
            "np.testing.assert_equal(msm.convert(view.molsys.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict(),source_chemistry)\n"
            "assert view.addons.molsysmt.get_sync_status()['state']=='synchronized'\n"
            "assert view.addons.molsysmt.get_sync_status()['target_revision']==0\n"
            "current_scene=view.export_state()\n"
            "assert {k:v for k,v in current_scene.items() if k!='view'}=={k:v for k,v in source_scene.items() if k!='view'}\n"
            "assert {k:v for k,v in current_scene['view'].items() if k!='camera'}==source_scene['view']\n"
            "assert not view.addons.manager.presentations.records()\n"
            "print('JUPYTER_ANALYSIS_UNCHANGED',view.molsys.get_n_atoms())\n"
        )
    # Keep a native stack if initialization stalls. The shell event closes the
    # diagnostic after the actual display hook, without warming that hook first.
    initial = (
        "import faulthandler as _source_faults\nimport time as _source_clock\n"
        f"_source_trace = open({str(output / 'kernel-initialization-trace.log')!r}, 'w')\n"
        "_source_started = _source_clock.monotonic()\n"
        "_source_trace.write('Initial cell started\\n'); _source_trace.flush()\n"
        "_source_faults.dump_traceback_later(15, repeat=True, file=_source_trace)\n"
        "def _source_initialized(_result):\n"
        "    _source_faults.cancel_dump_traceback_later()\n"
        "    _source_trace.write(f'Initial cell completed in {_source_clock.monotonic()-_source_started:.6f} s\\n')\n"
        "    _source_trace.close()\n"
        "    get_ipython().events.unregister('post_run_cell', _source_initialized)\n"
        "get_ipython().events.register('post_run_cell', _source_initialized)\n"
        + initial
    )
    cells = [initial, final]
    if args.scenario == "axes":
        cells = [initial, axes_middle, final]
    if args.scenario == "chemistry-preparation":
        cells = [initial, "verify_preparation_source()\n", final]
    if args.scenario == "chemistry-pending":
        cells = [initial]
        for revision in range(1, 4):
            cells.extend(
                ["defer_reader_box()\n", f"verify_reader_pending({revision})\n"]
            )
        cells.append(final)
    if args.scenario == "analysis":
        cells.extend(
            [
                "np.testing.assert_array_equal(msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm'),source_coordinates)\n"
                "np.testing.assert_equal(msm.convert(view.molsys.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict(),source_chemistry)\n"
                "assert view.addons.molsysmt.get_sync_status()['target_revision']==0\n"
                "assert set(view.active_selection.atom_indices)=={0,2,3,5,7}\n"
                "_measures=view.measurements.info()\nassert len(_measures)==3\n"
                "for _measure in _measures:\n"
                "    assert _measure['picks_atom_indices']==[[0,2],[3,5,7]]\n"
                "    np.testing.assert_allclose(msm.pyunitwizard.get_value(view.measurements.series(_measure['tag']),to_unit='nm'),[np.linalg.norm(_centers[0]-_centers[1])])\n"
                "_scene=view.export_state()\n"
                "_effects={'view','active_selection','measurements','order_high_water_mark','uid_high_water_mark','tag_high_water_marks'}\n"
                "assert {k:v for k,v in _scene.items() if k not in _effects}=={k:v for k,v in source_scene.items() if k not in _effects}\n"
                "assert {k:v for k,v in _scene['view'].items() if k!='camera'}=={k:v for k,v in source_scene['view'].items() if k!='camera'}\n"
                "print('JUPYTER_ANALYSIS_SCENE_OK',len(_measures))\n",
                "view.close()\n"
                "with msv.demo['pentalanine'] as _seed:\n"
                "    view=msv.new_view(_seed.molsys,structure_indices=[0,8,3])\n"
                "_ensemble_xyz=msm.pyunitwizard.get_value(view.get_coordinates(),to_unit='nm').copy()\n"
                "_ensemble_chemistry=msm.convert(view.molsys.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict()\n"
                "_ensemble_points=np.stack([_ensemble_xyz[:,[4,0,4]].mean(axis=1),_ensemble_xyz[:,[5,2]].mean(axis=1)],axis=1)\n"
                f"Path({str(output / 'analysis-ensemble-expected.json')!r}).write_text(json.dumps({{'points_angstrom':(_ensemble_points*10).tolist(),'distances_nm':np.linalg.norm(_ensemble_points[:,0]-_ensemble_points[:,1],axis=1).tolist()}}))\nview\n",
                "np.testing.assert_array_equal(msm.pyunitwizard.get_value(view.get_coordinates(),to_unit='nm'),_ensemble_xyz)\n"
                "np.testing.assert_equal(msm.convert(view.molsys.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict(),_ensemble_chemistry)\n"
                "_measures=view.measurements.info()\nassert len(_measures)==1\n"
                "assert _measures[0]['picks_atom_indices']==[[4,0,4],[5,2]]\n"
                "np.testing.assert_allclose(msm.pyunitwizard.get_value(view.measurements.series(_measures[0]['tag']),to_unit='nm'),np.linalg.norm(_ensemble_points[:,0]-_ensemble_points[:,1],axis=1))\n"
                "assert view.player.index==2 and view.addons.molsysmt.get_sync_status()['target_revision']==0\n"
                "print('JUPYTER_ANALYSIS_ENSEMBLE_OK',view.player.n_structures)\n",
            ]
        )
    if args.scenario == "analysis":
        cells.extend(
            [
                "_conformation_atoms=[4,0,2,4]\n"
                "_conformation_xyz=_ensemble_xyz[:,_conformation_atoms]\n"
                "_conformation_reference=_conformation_xyz[1]\n"
                "_conformation_rmsd=np.sqrt(np.mean(np.sum((_conformation_xyz-_conformation_reference)**2,axis=2),axis=1))\n"
                "_conformation_rg=np.sqrt(np.mean(np.sum((_conformation_xyz-_conformation_xyz.mean(axis=1)[:,None])**2,axis=2),axis=1))\n"
                "_conformation_rmsf=np.sqrt(np.mean(np.sum((_conformation_xyz[[2,0,2]]-_conformation_xyz[[2,0,2]].mean(axis=0))**2,axis=2),axis=0))\n"
                "_conformation_least=[]\n"
                "_reference_centered=_conformation_reference-_conformation_reference.mean(axis=0)\n"
                "for _pose in _conformation_xyz:\n"
                "    _centered=_pose-_pose.mean(axis=0)\n"
                "    _u,_singular,_vt=np.linalg.svd(_centered.T@_reference_centered)\n"
                "    _rotation=_u@np.diag([1.,1.,np.linalg.det(_u@_vt)])@_vt\n"
                "    _conformation_least.append(float(np.sqrt(np.mean(np.sum((_centered@_rotation-_reference_centered)**2,axis=1)))))\n"
                f"Path({str(output / 'conformation-expected.json')!r}).write_text(json.dumps({{'rmsd':_conformation_rmsd.tolist(),'least_rmsd':_conformation_least,'gyration':_conformation_rg.tolist(),'rmsf':_conformation_rmsf.tolist()}}))\n"
                "_conformation_callbacks=[]\nview.on_frame_change(_conformation_callbacks.append)\n"
                "print('JUPYTER_CONFORMATION_ORACLES_OK',3)\n",
                "np.testing.assert_array_equal(msm.pyunitwizard.get_value(view.get_coordinates(),to_unit='nm'),_ensemble_xyz)\n"
                "np.testing.assert_equal(msm.convert(view.molsys.chemical_states,to_form='molsysmt.ChemicalStatesDict').to_dict(),_ensemble_chemistry)\n"
                "assert view.addons.molsysmt.get_sync_status()['target_revision']==0\n"
                "assert [event['frame'] for event in _conformation_callbacks]==[1,2], repr(_conformation_callbacks)\n"
                "assert view.player.index==2, f'Expected current structure 2, got {view.player.index}'\n"
                "assert len(view.measurements.info())==1\n"
                "_plots=view.trajectory_plot.records()\nassert len(_plots)==2\n"
                "_plot_values={_plot['title']:_plot['series'][0]['values'] for _plot in _plots}\n"
                "assert set(_plot_values)=={'Radius of gyration','RMSD without superposition'}\n"
                "np.testing.assert_allclose(_plot_values['Radius of gyration'],_conformation_rg)\n"
                "np.testing.assert_allclose(_plot_values['RMSD without superposition'],_conformation_rmsd,atol=1e-12)\n"
                "assert all(_plot['n_frames']==3 and _plot['x_label']=='Structure index' and _plot['y_label']=='Length (nm)' for _plot in _plots)\n"
                "print('JUPYTER_CONFORMATION_SCENE_OK',len(_plots))\n",
            ]
        )
    (output / "notebooks/system.ipynb").write_text(json.dumps(_notebook(cells)))
    (output / "notebooks/plain.ipynb").write_text(
        json.dumps(_notebook(["print('PLAIN_JUPYTER_CONTROL_OK', 1 + 1)\n"]))
    )
    (output / "environment.json").write_text(
        json.dumps(
            {
                "python": sys.version,
                "packages": {
                    name: importlib.metadata.version(name)
                    for name in ("jupyterlab", "ipykernel", "anywidget", "ipywidgets")
                },
                "node": subprocess.check_output(
                    [args.node, "--version"], text=True
                ).strip(),
            },
            indent=2,
        )
    )
    server = None
    startup = {
        "scope": "Jupyter server readiness, before any browser or molecular cell"
    }
    startup_path = output / "server-startup.json"
    server_command = [sys.executable, "-m", "jupyterlab", "--no-browser"]
    if os.environ.get("MOLSYSVIEWER_TRACE_JUPYTER_STARTUP") == "1":
        # Diagnostic only: preserve the readiness deadline and server behavior.
        server_command = [
            sys.executable,
            "-c",
            "import faulthandler, runpy, sys; "
            "faulthandler.enable(); "
            "faulthandler.dump_traceback_later(15, repeat=False); "
            "sys.argv = ['jupyterlab', '--no-browser']; "
            "runpy.run_module('jupyterlab', run_name='__main__')",
        ]
        startup["diagnostic_trace_after_seconds"] = 15
    try:
        with (output / "server.log").open("w") as log:
            startup_started = time.monotonic()
            server = subprocess.Popen(
                server_command,
                env=env,
                stdout=log,
                stderr=log,
            )
            startup.update(pid=server.pid, ready=False)
            startup_path.write_text(json.dumps(startup, indent=2))
            ready = False
            for _ in range(40):
                if server.poll() is not None:
                    startup.update(
                        elapsed_seconds=time.monotonic() - startup_started,
                        native_exit_observed=server.returncode,
                    )
                    startup_path.write_text(json.dumps(startup, indent=2))
                    raise RuntimeError(
                        "Isolated Jupyter exited; inspect the private server.log."
                    )
                try:
                    request = Request(
                        f"http://127.0.0.1:{port}/api/status",
                        headers={"Authorization": f"token {token}"},
                    )
                    with urlopen(request, timeout=1) as response:
                        ready = response.status == 200
                    if ready:
                        break
                except (URLError, TimeoutError):
                    time.sleep(0.5)
            startup.update(
                ready=ready, elapsed_seconds=time.monotonic() - startup_started
            )
            startup_path.write_text(json.dumps(startup, indent=2))
            if not ready:
                raise RuntimeError("Isolated Jupyter did not become ready.")
            subprocess.run(
                [
                    args.node,
                    str(
                        Path(__file__).with_name("analysis_panel_jupyter.mjs")
                        if args.scenario == "analysis"
                        else Path(__file__).with_name("chemistry_pending_jupyter.mjs")
                        if args.scenario == "chemistry-pending"
                        else Path(__file__).with_name(
                            "chemistry_preparation_jupyter.mjs"
                        )
                        if args.scenario == "chemistry-preparation"
                        else Path(__file__).with_name("chemistry_panel_jupyter.mjs")
                        if args.scenario == "chemistry"
                        else Path(__file__).with_name("periodic_panel_jupyter.mjs")
                        if args.scenario in {"periodic", "periodic-general"}
                        else Path(__file__).with_name("fit_panel_jupyter.mjs")
                        if args.scenario == "fit"
                        else Path(__file__).with_name("fit_external_panel_jupyter.mjs")
                        if args.scenario == "fit-external"
                        else Path(__file__).with_name("center_error_jupyter.mjs")
                        if args.scenario == "center-errors"
                        else Path(__file__).with_name("axes_panel_jupyter.mjs")
                        if args.scenario == "axes"
                        else Path(__file__).with_name("rotate_panel_jupyter.mjs")
                        if args.scenario == "rotate"
                        else Path(__file__).with_name("center_panel_jupyter.mjs")
                        if args.scenario == "center"
                        else Path(__file__).with_name("geometry_panel_jupyter.mjs")
                        if args.scenario == "geometry"
                        else Path(__file__).with_name("result_panel_jupyter.mjs")
                        if args.scenario == "results"
                        else Path(__file__).with_suffix(".mjs")
                    ),
                ],
                env=env,
                check=True,
                timeout=240,
            )
    finally:
        if server is not None:
            try:
                shutdown = Request(
                    f"http://127.0.0.1:{port}/api/shutdown",
                    method="POST",
                    headers={"Authorization": f"token {token}"},
                )
                with urlopen(shutdown, timeout=10):
                    pass
                server.wait(timeout=15)
            except (URLError, TimeoutError, subprocess.TimeoutExpired):
                server.terminate()
                try:
                    server.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait(timeout=5)
        for credential in (output / "settings.json", config):
            credential.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
