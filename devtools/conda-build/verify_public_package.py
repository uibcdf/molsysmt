"""Verify one exact public Conda file without changing registry state."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

OWNER = "uibcdf"
MAX_RESPONSE_BYTES = 16 * 1024 * 1024
VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
NAME = re.compile(r"[a-z0-9][a-z0-9-]*\Z")
SUBDIR = re.compile(r"[a-z0-9][a-z0-9-]*\Z")
FILENAME = re.compile(r"[A-Za-z0-9_.+\-]+\.(?:conda|tar\.bz2)\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class VerificationPending(Exception):
    """The public label or index has not exposed the expected file yet."""


class VerificationError(Exception):
    """The public record contradicts the expected immutable coordinate."""


def validate_coordinate(
    package: str, version: str, subdir: str, filename: str, sha256: str
) -> None:
    """Reject unsafe or inconsistent coordinates before making network requests."""
    if not NAME.fullmatch(package) or not VERSION.fullmatch(version):
        raise VerificationError("package or version is not canonical")
    if not SUBDIR.fullmatch(subdir) or not FILENAME.fullmatch(filename):
        raise VerificationError("subdir or filename is not a single Conda coordinate")
    if not filename.startswith(f"{package}-{version}-") or not SHA256.fullmatch(sha256):
        raise VerificationError(
            "filename or SHA-256 does not match the expected coordinate"
        )


def fetch_json(url: str) -> dict:
    """Fetch a bounded, anonymous public JSON document."""
    request = Request(url, headers={"User-Agent": "uibcdf-conda-public-verifier/1"})
    with urlopen(request, timeout=20) as response:
        payload = response.read(MAX_RESPONSE_BYTES + 1)
    if len(payload) > MAX_RESPONSE_BYTES:
        raise VerificationError("public registry response exceeds the size limit")
    document = json.loads(payload)
    if not isinstance(document, dict):
        raise VerificationError("public registry response is not a JSON object")
    return document


def verify_snapshot(
    release: dict,
    repodata: dict,
    package: str,
    version: str,
    subdir: str,
    filename: str,
    sha256: str,
) -> str:
    """Check both Anaconda's public label and the solver-visible index."""
    basename = f"{subdir}/{filename}"
    distributions = release.get("distributions")
    if not isinstance(distributions, list):
        raise VerificationError("release metadata has no distributions list")
    matches = [
        entry
        for entry in distributions
        if isinstance(entry, dict) and entry.get("basename") == basename
    ]
    if not matches:
        raise VerificationPending(f"{basename} is not in the public release metadata")
    if len(matches) != 1:
        raise VerificationError(f"duplicate public release records for {basename}")
    distribution = matches[0]
    if distribution.get("sha256") != sha256:
        raise VerificationError(f"public release SHA-256 differs for {basename}")
    if (
        not isinstance(distribution.get("labels"), list)
        or "main" not in distribution["labels"]
    ):
        raise VerificationPending(f"{basename} does not yet have the main label")
    attrs = distribution.get("attrs")
    if not isinstance(attrs, dict) or attrs.get("subdir") != subdir:
        raise VerificationError(f"public release subdir differs for {basename}")

    info = repodata.get("info")
    if not isinstance(info, dict) or info.get("subdir") != subdir:
        raise VerificationError(f"public repodata is not for {subdir}")
    section = "packages.conda" if filename.endswith(".conda") else "packages"
    records = repodata.get(section)
    if records is None:
        raise VerificationPending(f"public repodata has no {section} mapping yet")
    if not isinstance(records, dict):
        raise VerificationError(f"public repodata has an invalid {section} mapping")
    record = records.get(filename)
    if record is None:
        raise VerificationPending(f"{basename} is not yet solver-visible")
    if not isinstance(record, dict) or record.get("sha256") != sha256:
        raise VerificationError(f"solver-visible SHA-256 differs for {basename}")
    if record.get("name") != package or record.get("version") != version:
        raise VerificationError(
            f"solver-visible package identity differs for {basename}"
        )
    return f"https://conda.anaconda.org/{OWNER}/{basename}"


def verify_public(
    package: str,
    version: str,
    subdir: str,
    filename: str,
    sha256: str,
    attempts: int = 6,
    interval: float = 15,
) -> str:
    """Retry bounded index propagation; never mutate or download a package."""
    validate_coordinate(package, version, subdir, filename, sha256)
    if attempts < 1 or interval < 0:
        raise VerificationError("attempts must be positive and interval non-negative")
    release_url = (
        f"https://api.anaconda.org/release/{OWNER}/{quote(package)}/{quote(version)}"
    )
    index_url = f"https://conda.anaconda.org/{OWNER}/{quote(subdir)}/repodata.json"
    for attempt in range(1, attempts + 1):
        try:
            release = fetch_json(release_url)
            repodata = fetch_json(index_url)
            return verify_snapshot(
                release, repodata, package, version, subdir, filename, sha256
            )
        except HTTPError as error:
            if error.code not in (404, 429) and error.code < 500:
                raise VerificationError(
                    f"public registry rejected the query: HTTP {error.code}"
                ) from error
            pending = f"public registry returned HTTP {error.code}"
        except URLError as error:
            pending = f"public registry request failed: {error.reason}"
        except VerificationPending as error:
            pending = str(error)
        if attempt == attempts:
            raise VerificationError(
                f"not verified after {attempts} attempts: {pending}"
            )
        time.sleep(interval)
    raise AssertionError("unreachable retry state")


def main(argv: list[str] | None = None) -> int:
    """Run the read-only public verification CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--subdir", required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--attempts", type=int, default=6)
    parser.add_argument("--interval", type=float, default=15)
    args = parser.parse_args(argv)
    try:
        url = verify_public(
            args.package,
            args.version,
            args.subdir,
            args.filename,
            args.sha256,
            args.attempts,
            args.interval,
        )
    except (VerificationError, ValueError, json.JSONDecodeError) as error:
        print(f"public Conda verification failed: {error}", file=sys.stderr)
        return 1
    print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
