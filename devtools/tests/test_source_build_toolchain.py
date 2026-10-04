"""Checking that source-build jobs execute the declared compiler selection."""

import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]
WORKFLOWS = ["ci-smoke.yaml", "ci-full.yaml", "ci-weekly.yaml", "test_import.yaml"]


@pytest.mark.parametrize("filename", WORKFLOWS)
def test_source_build_selects_pinned_minimal_rust(filename, tmp_path):
    """Execute provisioning/build commands with recording tools, without downloads."""
    pin = tomllib.loads((REPO / "rust-toolchain.toml").read_text())["toolchain"][
        "channel"
    ]
    workflow = yaml.safe_load((REPO / ".github" / "workflows" / filename).read_text())
    jobs = [
        job
        for job in workflow["jobs"].values()
        if any(
            "pip install" in step.get("run", "")
            and ("install --editable ." in step["run"] or "install ." in step["run"])
            for step in job.get("steps", [])
        )
    ]
    assert len(jobs) == 1
    steps = jobs[0]["steps"]
    build_index = next(
        i for i, step in enumerate(steps) if step.get("name") == "Install package"
    )
    provision_index = next(
        i
        for i, step in enumerate(steps)
        if step.get("name") == "Select the pinned minimal Rust toolchain"
    )
    assert provision_index < build_index

    record = tmp_path / "commands.jsonl"
    binaries = tmp_path / "bin"
    binaries.mkdir()
    script = (
        f"#!{sys.executable}\n"
        "import json, os, sys\n"
        "from pathlib import Path\n"
        "with open(os.environ['MSM_TOOLCHAIN_RECORD'], 'a') as stream:\n"
        "    stream.write(json.dumps([Path(sys.argv[0]).name, sys.argv[1:], "
        "os.environ.get('RUSTUP_TOOLCHAIN')]) + '\\n')\n"
    )
    for name in ("rustup", "rustc", "python"):
        executable = binaries / name
        executable.write_text(script)
        executable.chmod(0o755)
    environment = dict(os.environ)
    environment.pop("RUSTUP_TOOLCHAIN", None)
    environment.update(
        PATH=f"{binaries}{os.pathsep}{os.environ['PATH']}",
        MSM_TOOLCHAIN_RECORD=str(record),
    )
    for index in (provision_index, build_index):
        step = steps[index]
        subprocess.run(
            ["bash", "-euc", step["run"]],
            env={**environment, **jobs[0].get("env", {}), **step.get("env", {})},
            cwd=tmp_path,
            check=True,
            capture_output=True,
            text=True,
        )
    commands = [json.loads(line) for line in record.read_text().splitlines()]
    assert commands[0][:2] == [
        "rustup",
        ["toolchain", "install", pin, "--profile", "minimal"],
    ]
    assert commands[1][:2] == ["rustc", [f"+{pin}", "--version"]]
    builds = [
        command
        for command in commands[2:]
        if command[0] == "python"
        and command[1][:3] == ["-m", "pip", "install"]
        and "." in command[1]
    ]
    assert len(builds) == 1
    assert builds[0][2] == pin  # Suppress implicit development-component requests.
