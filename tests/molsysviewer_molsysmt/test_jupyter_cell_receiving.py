"""Check protocol decoding against Jupyter Server's independent serializers."""

import base64
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(
    NODE is None, reason="Node is required for browser-receiver guards"
)


def test_node_execution_association_and_bounded_diagnostics(tmp_path):
    result = subprocess.run(
        [
            NODE,
            "--test",
            "--test-reporter=tap",
            str(HERE / "jupyter_cell_receiving.test.mjs"),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    (tmp_path / "node-controls.tap").write_text(result.stdout, encoding="utf-8")
    assert result.returncode == 0, result.stdout + result.stderr
    assert re.search(r"^# tests 13$", result.stdout, re.M), result.stdout
    assert re.search(r"^# pass 13$", result.stdout, re.M), result.stdout
    assert re.search(r"^# fail 0$", result.stdout, re.M), result.stdout


@pytest.mark.parametrize("transport", ["json", "legacy", "v1"])
def test_decode_official_jupyter_error_packets_without_widget_buffers(transport):
    serializers = pytest.importorskip("jupyter_server.services.kernels.connection.base")
    message = {
        "header": {"msg_id": "original", "msg_type": "error"},
        "parent_header": {"msg_id": "owned-execution"},
        "metadata": {},
        "content": {
            "ename": "AssertionError",
            "evalue": "original failure",
            "traceback": ["original line"],
        },
        "channel": "iopub",
    }
    if transport == "json":
        wire = json.dumps(message).encode()
    elif transport == "legacy":
        wire = serializers.serialize_binary_message(
            {**message, "buffers": [b"x" * (2 * 1024**2)]}
        )
    else:
        wire = serializers.serialize_msg_to_ws_v1(
            [
                json.dumps(message[name]).encode()
                for name in ["header", "parent_header", "metadata", "content"]
            ]
            + [b"x" * (2 * 1024**2)],
            "iopub",
        )
    program = (
        "import {readFileSync} from 'node:fs';\n"
        f"import {{decodeKernelMessage}} from {json.dumps((HERE / 'jupyter_cell_receiving.mjs').as_uri())};\n"
        "const input=Buffer.from(readFileSync(0,'utf8'),'base64');\n"
        f"const decoded=decodeKernelMessage({'input.toString()' if transport == 'json' else 'input'});\n"
        "console.log(JSON.stringify(decoded));\n"
    )
    result = subprocess.run(
        [NODE, "--input-type=module", "-e", program],
        input=base64.b64encode(wire).decode(),
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
    decoded = json.loads(result.stdout)
    for name in ["header", "parent_header", "metadata", "content", "channel"]:
        assert decoded[name] == message[name]
    assert "buffers" not in decoded
