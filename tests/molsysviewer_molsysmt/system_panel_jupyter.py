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
        choices=("system", "results", "geometry", "center", "center-errors"),
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
    if args.scenario in {"geometry", "center", "center-errors"}:
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
    # Keep a native stack if initialization stalls. The shell event closes the
    # diagnostic after the actual display hook, without warming that hook first.
    initial = (
        "import faulthandler as _source_faults\n"
        f"_source_trace = open({str(output / 'kernel-initialization-trace.log')!r}, 'w')\n"
        "_source_faults.dump_traceback_later(45, repeat=True, file=_source_trace)\n"
        "def _source_initialized(_result):\n"
        "    _source_faults.cancel_dump_traceback_later()\n"
        "    _source_trace.close()\n"
        "    get_ipython().events.unregister('post_run_cell', _source_initialized)\n"
        "get_ipython().events.register('post_run_cell', _source_initialized)\n"
        + initial
    )
    (output / "notebooks/system.ipynb").write_text(
        json.dumps(_notebook([initial, final]))
    )
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
    try:
        with (output / "server.log").open("w") as log:
            server = subprocess.Popen(
                [sys.executable, "-m", "jupyterlab", "--no-browser"],
                env=env,
                stdout=log,
                stderr=log,
            )
            ready = False
            for _ in range(40):
                if server.poll() is not None:
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
            if not ready:
                raise RuntimeError("Isolated Jupyter did not become ready.")
            subprocess.run(
                [
                    args.node,
                    str(
                        Path(__file__).with_name("center_error_jupyter.mjs")
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
