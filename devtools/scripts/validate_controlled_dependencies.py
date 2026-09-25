"""Reject controlled CI installs below MolSysMT's declared runtime floors."""

from __future__ import annotations

import importlib.metadata
import re
import tomllib
from collections.abc import Callable
from pathlib import Path

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[2]
PINS = ROOT / "devtools" / "controlled_sources.txt"
PIN_PATTERN = re.compile(
    r"git\+https://github\.com/uibcdf/(?P<name>[A-Za-z0-9_.-]+)@(?P<sha>[0-9a-f]{40})"
)


def controlled_names(text: str) -> list[str]:
    """Read the exact source-pin names without trusting unrecognized lines."""
    names: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = PIN_PATTERN.fullmatch(line)
        if match is None:
            raise ValueError(f"invalid controlled source pin: {line}")
        name = canonicalize_name(match.group("name"))
        if name in names:
            raise ValueError(f"duplicate controlled source pin: {name}")
        names.append(name)
    return names


def find_violations(
    dependencies: list[str], names: list[str], version_for: Callable[[str], str]
) -> list[str]:
    """Compare installed source versions with the package's runtime contract."""
    requirements: dict[str, Requirement] = {}
    for item in dependencies:
        requirement = Requirement(item)
        requirements[canonicalize_name(requirement.name)] = requirement
    violations: list[str] = []
    for name in names:
        requirement = requirements.get(name)
        if requirement is None or not requirement.specifier:
            violations.append(f"{name}: no bounded runtime requirement")
            continue
        try:
            installed = version_for(name)
        except importlib.metadata.PackageNotFoundError:
            violations.append(f"{name}: controlled source is not installed")
            continue
        if not requirement.specifier.contains(installed, prereleases=True):
            violations.append(f"{name}: installed {installed} violates {requirement}")
    return violations


def main() -> int:
    """Validate the controlled source environment before scientific tests run."""
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    names = controlled_names(PINS.read_text(encoding="utf-8"))
    violations = find_violations(
        pyproject["project"]["dependencies"], names, importlib.metadata.version
    )
    if violations:
        for violation in violations:
            print(f"[CONTROLLED_DEPENDENCY] {violation}")
        return 1
    print(
        f"Controlled source dependencies satisfy runtime metadata: {', '.join(names)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
