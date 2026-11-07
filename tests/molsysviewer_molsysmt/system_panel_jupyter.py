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
            "center",
            "center-errors",
            "fit",
            "periodic",
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
    if args.scenario in {"geometry", "center", "center-errors", "fit", "periodic"}:
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
    if args.scenario == "periodic":
        initial = (
            initial.removesuffix("view\n")
            + "import itertools\nimport json\nimport numpy as np\n_periodic_box=np.array([[3.,0,0],[0.7,4.,0],[0.2,0.6,5.]])\n_periodic_boxes=np.repeat(_periodic_box[None],3,axis=0)\n_periodic_before=source_coordinates+[8.,7.,6.]\nview.addons.molsysmt.basic.set(coordinates=msm.pyunitwizard.quantity(_periodic_before,'nm'),box=msm.pyunitwizard.quantity(_periodic_boxes,'nm'))\n_periodic_revision=view.addons.molsysmt.get_sync_status()['target_revision']\n_origin=np.array([0.2,-0.4,0.7])\n_periodic_component=_periodic_before.copy()\nfor frame in [2,0]:\n    center=_periodic_before[frame].mean(axis=0)\n    fractional=(center-_origin)@np.linalg.inv(_periodic_box)\n    target=_origin+(fractional-np.floor(fractional+0.5))@_periodic_box\n    _periodic_component[frame]+=target-center\n_shifts=np.array(list(itertools.product(range(-2,3),repeat=3)))\ndef _nearest_lattice(vectors):\n    seed=np.rint(vectors@np.linalg.inv(_periodic_box))\n    candidates=vectors[:,None]-(seed[:,None]+_shifts[None])@_periodic_box\n    return candidates[np.arange(len(vectors)),np.argmin(np.sum(candidates*candidates,axis=-1),axis=1)]\n_periodic_source=_periodic_component.copy()\n_periodic_source[0]=np.array([10.,10.,10.])+_nearest_lattice(_periodic_component[0]-[10.,10.,10.])\nassert np.max(np.abs(_periodic_source[0]-_periodic_component[0]))>1\n_periodic_result=_periodic_source.copy()\nfor frame in [1,2]:\n    _periodic_result[frame]=_periodic_result[frame-1]+_nearest_lattice(_periodic_source[frame]-_periodic_result[frame-1])\n"
        )
        initial += f"Path({str(output / 'periodic-expected.json')!r}).write_text(json.dumps({{'before_angstrom':(_periodic_before*10).tolist(),'component_angstrom':(_periodic_component*10).tolist(),'source_angstrom':(_periodic_source*10).tolist(),'result_angstrom':(_periodic_result*10).tolist()}}))\nview\n"
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
                        if args.scenario == "periodic"
                        else Path(__file__).with_name("fit_panel_jupyter.mjs")
                        if args.scenario == "fit"
                        else Path(__file__).with_name("center_error_jupyter.mjs")
                        if args.scenario == "center-errors"
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
