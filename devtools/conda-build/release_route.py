"""Selecting a fail-closed Conda route for one exact release version.

A staged release never rebuilds the tested coordinate. Its publication uses the
separate exact-file promotion workflow. A direct release is allowed only when
Anaconda confirms that the version does not exist under any label.
"""

from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

PACKAGE = Path(__file__).resolve().parents[2].name
PLAN = Path(__file__).with_name("release_plan.toml")
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")


def read_plan(path: Path = PLAN) -> dict:
    """Load the committed route decision and reject incomplete plans."""
    plan = tomllib.loads(path.read_text(encoding="utf-8"))
    if not VERSION.fullmatch(str(plan.get("version", ""))):
        raise ValueError("release plan needs a canonical X.Y.Z version")
    if plan.get("route") not in {"direct", "staged"}:
        raise ValueError("release plan route must be direct or staged")
    if not isinstance(plan.get("reason"), str) or not plan["reason"].strip():
        raise ValueError("release plan needs a reviewed reason")
    return plan


def assert_version_unoccupied(version: str) -> None:
    """Allow a direct build only after an explicit absent-version response."""
    url = f"https://api.anaconda.org/release/uibcdf/{PACKAGE}/{quote(version, safe='')}"
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": f"{PACKAGE}-release-route",
        },
    )
    try:
        with urlopen(request, timeout=20) as response:
            json.load(response)
    except HTTPError as error:
        if error.code == 404:
            return
        raise ValueError(f"Anaconda preflight failed with HTTP {error.code}") from error
    raise ValueError(
        f"{PACKAGE} {version} already exists under an Anaconda label; "
        "a direct upload could overwrite or collide with validated bytes"
    )


def select_route(version: str, event: str, path: Path = PLAN) -> str:
    """Match dispatch or Release to the versioned decision."""
    if not VERSION.fullmatch(version):
        raise ValueError("release version must be canonical X.Y.Z")
    plan = read_plan(path)
    if plan["version"] != version:
        raise ValueError(f"release plan is for {plan['version']}, not {version}")
    route = plan["route"]
    if event == "workflow_dispatch":
        if route != "staged":
            raise ValueError("manual candidate dispatch requires a staged plan")
    elif event == "release":
        if route == "direct":
            assert_version_unoccupied(version)
    else:
        raise ValueError(f"unsupported release event: {event}")
    return route


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True)
    parser.add_argument(
        "--event", choices=("workflow_dispatch", "release"), required=True
    )
    parser.add_argument("--github-output", type=Path, required=True)
    args = parser.parse_args()
    route = select_route(args.version, args.event)
    with args.github_output.open("a", encoding="utf-8") as stream:
        stream.write(f"route={route}\n")
    print(f"{PACKAGE} {args.version}: {route} Conda route")


if __name__ == "__main__":
    main()
