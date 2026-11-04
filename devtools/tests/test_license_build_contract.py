"""Protect compatible build inputs and actual distribution license evidence."""

from __future__ import annotations

import io
import re
import tarfile
import tomllib
from pathlib import Path
from zipfile import ZipFile

import pytest
import yaml
from packaging.requirements import Requirement
from packaging.version import Version

from devtools.scripts.validate_license_metadata import (
    BUNDLED_NOTICES,
    validate_license_metadata,
)

ROOT = Path(__file__).resolve().parents[2]
BUILD_INPUTS = [
    "devtools/conda-build/meta.yaml",
    "devtools/rattler-build/recipe.yaml",
    *[
        f"devtools/conda-envs/{name}_env.yaml"
        for name in ("build", "setup", "development", "test", "docs")
    ],
]


def build_tool_requirements(relative):
    """Read actual environment dependencies or Conda host requirements."""
    text = (ROOT / relative).read_text()
    if relative == "devtools/conda-build/meta.yaml":
        # The classic recipe has Jinja outside its plain-YAML host block.
        section = re.search(r"(?ms)^  host:\n(.*?)^  run:\n", text)
        assert section is not None, "the classic recipe needs its real host block"
        host = section.group(1)
        values = yaml.safe_load("dependencies:\n" + host)["dependencies"]
    else:
        data = yaml.safe_load(text)
        values = (
            data["requirements"]["host"]
            if "requirements" in data
            else data["dependencies"]
        )
    return [
        Requirement(value)
        for value in values
        if isinstance(value, str)
        and re.match(r"setuptools(?=\s|[<>=!~]|$)", value, re.I)
    ]


def test_setuptools_minimum_supports_the_declared_pep639_fields():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text())
    requirement = next(
        Requirement(raw)
        for raw in config["build-system"]["requires"]
        if Requirement(raw).name == "setuptools"
    )
    lower = [
        Version(spec.version) for spec in requirement.specifier if spec.operator == ">="
    ]
    assert lower and max(lower) >= Version("77.0.0"), (
        "PEP 639 fields require an explicit Setuptools >=77 floor"
    )
    assert config["project"]["license"] == "MIT"
    assert config["project"]["license-files"] == ["LICENSE"]
    for relative in BUILD_INPUTS:
        requirements = build_tool_requirements(relative)
        assert len(requirements) == 1, relative
        assert requirements[0].specifier == requirement.specifier, relative


@pytest.mark.parametrize("relative", BUILD_INPUTS[:2] + [BUILD_INPUTS[2]])
def test_build_tool_pin_outside_its_actual_host_or_dependencies_does_not_count(
    relative, tmp_path, monkeypatch
):
    path = tmp_path / relative
    path.parent.mkdir(parents=True)
    if "conda-envs" in relative:
        text = "dependencies:\n- pip\nunrelated:\n- setuptools >=77.0.3\n"
    else:
        text = (
            "requirements:\n  build:\n  - setuptools >=77.0.3\n"
            "  host:\n  - pip\n  run:\n  - setuptools >=77.0.3\n"
        )
    path.write_text(text)
    monkeypatch.setitem(build_tool_requirements.__globals__, "ROOT", tmp_path)
    assert build_tool_requirements(relative) == []


@pytest.fixture
def source(tmp_path):
    root = tmp_path / "source"
    root.mkdir()
    (root / "pyproject.toml").write_text(
        '[project]\nname="molsysmt"\nlicense="MIT"\nlicense-files=["LICENSE"]\n'
    )
    (root / "LICENSE").write_bytes(b"project copyright and MIT terms\n")
    for name in BUNDLED_NOTICES:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"unchanged third-party notice\n")
    return root


def make_archive(
    source,
    kind,
    *,
    expression="MIT",
    version="2.4",
    declare=True,
    corrupt=None,
    omit=None,
):
    parent = "molsysmt-1.0.0.dist-info" if kind == "wheel" else "molsysmt-1.0.0"
    metadata = f"Metadata-Version: {version}\nName: molsysmt\nLicense-Expression: {expression}\n"
    if declare:
        metadata += "License-File: LICENSE\n"
    license_path = (
        f"{parent}/licenses/LICENSE" if kind == "wheel" else f"{parent}/LICENSE"
    )
    notice_path = (
        BUNDLED_NOTICES[0] if kind == "wheel" else f"{parent}/{BUNDLED_NOTICES[0]}"
    )
    entries = {
        f"{parent}/METADATA"
        if kind == "wheel"
        else f"{parent}/PKG-INFO": metadata.encode(),
        license_path: (source / "LICENSE").read_bytes(),
        notice_path: (source / BUNDLED_NOTICES[0]).read_bytes(),
    }
    target = license_path if corrupt == "project" or omit == "project" else notice_path
    if corrupt:
        entries[target] = b"substituted notice"
    if omit:
        del entries[target]
    path = source.parent / ("test.whl" if kind == "wheel" else "test.tar.gz")
    if kind == "wheel":
        with ZipFile(path, "w") as archive:
            for name, payload in entries.items():
                archive.writestr(name, payload)
    else:
        with tarfile.open(path, "w:gz") as archive:
            for name, payload in entries.items():
                info = tarfile.TarInfo(name)
                info.size = len(payload)
                archive.addfile(info, io.BytesIO(payload))
    return path


@pytest.mark.parametrize("kind", ["wheel", "sdist"])
@pytest.mark.parametrize("version", ["2.4", "2.5"])
def test_matching_metadata_and_original_notices_pass(source, kind, version):
    assert (
        validate_license_metadata(make_archive(source, kind, version=version), source)
        == []
    )


@pytest.mark.parametrize("kind", ["wheel", "sdist"])
@pytest.mark.parametrize(
    "change",
    [
        dict(expression="Apache-2.0"),
        dict(version="2.3"),
        dict(declare=False),
        dict(corrupt="project"),
        dict(corrupt="third_party"),
        dict(omit="project"),
        dict(omit="third_party"),
    ],
)
def test_metadata_labels_cannot_replace_matching_declarations_and_notice_bytes(
    source, kind, change
):
    assert validate_license_metadata(make_archive(source, kind, **change), source)
