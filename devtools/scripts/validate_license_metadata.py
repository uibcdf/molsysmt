"""Check MolSysMT archive license metadata and retained notice bytes without installing."""

from __future__ import annotations

import argparse
import tarfile
import tomllib
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
BUNDLED_NOTICES = ("molsysmt/interactions/cation_pi/PROLIF_LICENSE.txt",)


def validate_license_metadata(archive: Path, root: Path = ROOT) -> list[str]:
    """Compare archive declarations and notice bytes with their source authority."""
    root = root.resolve()
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    notices = {}
    for pattern in project["license-files"]:
        matches = [path for path in root.glob(pattern) if path.is_file()]
        if not matches:
            raise ValueError(f"source license pattern has no files: {pattern}")
        for path in matches:
            if not path.resolve().is_relative_to(root):
                raise ValueError("source license file leaves the source tree")
            notices[path.relative_to(root).as_posix()] = path.read_bytes()

    if archive.name.endswith(".whl"):
        context = ZipFile(archive)
    elif archive.name.endswith(".tar.gz"):
        context = tarfile.open(archive, "r:gz")
    else:
        raise ValueError("expected a wheel or gzip source distribution")
    with context as opened:
        wheel = isinstance(opened, ZipFile)
        names = (
            opened.namelist()
            if wheel
            else [member.name for member in opened if member.isfile()]
        )
        metadata = [
            name
            for name in names
            if (wheel and name.endswith(".dist-info/METADATA"))
            or (
                not wheel
                and len(PurePosixPath(name).parts) == 2
                and name.endswith("/PKG-INFO")
            )
        ]
        if len(metadata) != 1:
            return ["expected exactly one distribution metadata record"]

        def read(name):
            if wheel:
                return opened.read(name)
            stream = opened.extractfile(name)
            if stream is None:
                raise ValueError(f"not a regular archive file: {name}")
            with stream:
                return stream.read()

        record = BytesParser().parsebytes(read(metadata[0]))
        problems = []
        if record.get("Name", "").lower() != project["name"].lower():
            problems.append("distribution name differs from source")
        try:
            major, minor = map(int, record.get("Metadata-Version", "").split("."))
            compatible = major == 2 and minor >= 4
        except ValueError:
            compatible = False
        if not compatible:
            problems.append("expected PEP 639 core metadata 2.4 or a later 2.x minor")
        if record.get_all("License-Expression", []) != [project["license"]]:
            problems.append("License-Expression differs from source")
        if sorted(record.get_all("License-File", [])) != sorted(notices):
            problems.append("License-File declarations differ from source files")
        parent = PurePosixPath(metadata[0]).parent
        license_root = parent / "licenses" if wheel else parent
        expected = {str(license_root / name): data for name, data in notices.items()}
        package_root = PurePosixPath() if wheel else parent
        expected.update(
            {
                str(package_root / name): (root / name).read_bytes()
                for name in BUNDLED_NOTICES
            }
        )
        for name, data in expected.items():
            if names.count(name) != 1:
                problems.append(f"expected exactly one notice: {name}")
            elif read(name) != data:
                problems.append(f"notice bytes differ from source: {name}")
        return problems


def main() -> int:
    """Validate explicitly named artifacts without importing their package code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", nargs="+", type=Path)
    parser.add_argument("--source", type=Path, default=ROOT)
    args = parser.parse_args()
    failed = False
    for path in args.archives:
        problems = validate_license_metadata(path, args.source)
        failed |= bool(problems)
        print(f"{path.name}: {'FAIL' if problems else 'PASS'}")
        for problem in problems:
            print(f"  {problem}")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
