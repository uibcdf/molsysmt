#!/usr/bin/env python
"""Installing and validating a built MolSysMT Rust wheel."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import types
from importlib import metadata
from pathlib import Path


def find_single_wheel(path: Path) -> Path:
    """Returning the single wheel represented by a path."""

    path = path.resolve()
    wheels = sorted(path.glob("*.whl")) if path.is_dir() else [path]
    if len(wheels) != 1 or not wheels[0].is_file():
        raise RuntimeError(
            f"expected exactly one wheel at {path}, found {len(wheels)}"
        )
    return wheels[0]


def is_editable_direct_url(content: str | None) -> bool:
    """Returning whether direct-url metadata declares an editable install."""

    if not content:
        return False
    try:
        payload = json.loads(content)
    except json.JSONDecodeError as error:
        raise RuntimeError("invalid direct_url.json metadata") from error
    return bool(payload.get("dir_info", {}).get("editable", False))


def _extension_path(distribution: metadata.Distribution) -> Path:
    files = distribution.files or ()
    candidates = [
        distribution.locate_file(item).resolve()
        for item in files
        if item.parent.as_posix() == "molsysmt"
        and item.name.startswith("_rust.")
        and item.suffix in {".so", ".pyd", ".dylib"}
    ]
    if len(candidates) != 1:
        raise RuntimeError(
            "expected exactly one installed molsysmt._rust extension, "
            f"found {len(candidates)}"
        )
    return candidates[0]


def _load_private_extension(extension_path: Path):
    package = types.ModuleType("molsysmt")
    package.__path__ = [str(extension_path.parent)]
    package.__package__ = "molsysmt"
    package.__spec__ = importlib.util.spec_from_loader(
        "molsysmt",
        loader=None,
        is_package=True,
    )
    sys.modules["molsysmt"] = package

    spec = importlib.util.spec_from_file_location(
        "molsysmt._rust",
        extension_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load extension from {extension_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["molsysmt._rust"] = module
    spec.loader.exec_module(module)
    return module


def validate_installed_extension() -> dict[str, object]:
    """Validating the installed private extension without importing MolSysMT."""

    import numpy as np

    distribution = metadata.distribution("molsysmt")
    if is_editable_direct_url(distribution.read_text("direct_url.json")):
        raise RuntimeError("installed MolSysMT distribution is editable")

    extension_path = _extension_path(distribution)
    prefix = Path(sys.prefix).resolve()
    if not extension_path.is_relative_to(prefix):
        raise RuntimeError(
            f"extension resolves outside the environment: {extension_path}"
        )

    rust = _load_private_extension(extension_path)
    public_exports = [name for name in dir(rust) if not name.startswith("_")]
    if len(public_exports) != 97:
        raise RuntimeError(
            f"expected 97 Rust exports, found {len(public_exports)}"
        )

    box = np.diag([10.0, 10.0, 10.0])
    wrapped = rust.wrap_to_mic_vector_single_structure(
        np.array([7.5, 0.0, 0.0]),
        box,
    )
    minimum_image = float(np.linalg.norm(wrapped))
    if minimum_image != 2.5:
        raise RuntimeError(
            f"minimum-image smoke returned {minimum_image}, expected 2.5"
        )

    return {
        "extension": str(extension_path),
        "exports": len(public_exports),
        "minimum_image": minimum_image,
    }


def main() -> int:
    """Installing one wheel and running its binary contract."""

    parser = argparse.ArgumentParser()
    parser.add_argument("wheel_or_directory", type=Path)
    args = parser.parse_args()

    wheel = find_single_wheel(args.wheel_or_directory)
    subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("validate_rust_wheel.py")),
            str(wheel),
        ],
        check=True,
    )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--force-reinstall",
            "--no-deps",
            str(wheel),
        ],
        check=True,
    )
    result = validate_installed_extension()
    print(
        "MolSysMT installed Rust wheel validation passed: "
        f"{wheel.name} | exports={result['exports']} | "
        f"minimum_image={result['minimum_image']} | "
        f"extension={result['extension']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
