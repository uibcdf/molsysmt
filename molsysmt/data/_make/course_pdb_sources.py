"""Restore byte-pinned course PDB inputs from local originals or RCSB.

Run from any directory. Network access requires --download; normal test and
course execution use the committed resources and never call this generator.
"""

import argparse
import hashlib
import json
import tempfile
import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "pdb"


def restore(destination, manifest, source_directory=None, download=False):
    """Restore only verified bytes, preserving any existing mismatched file."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    for name, record in manifest["files"].items():
        target = destination / name
        if target.exists():
            data = target.read_bytes()
        elif source_directory is not None:
            data = (Path(source_directory) / name).read_bytes()
        elif download:
            with urllib.request.urlopen(record["url"], timeout=60) as response:
                data = response.read()
        else:
            raise FileNotFoundError(
                f"Missing {name}: supply --source-directory or explicitly --download"
            )
        if (
            len(data) != record["bytes"]
            or hashlib.sha256(data).hexdigest() != record["sha256"]
        ):
            raise ValueError(f"Archive bytes changed for {name}; refusing replacement")
        if not target.exists():
            with tempfile.NamedTemporaryFile(dir=destination, delete=False) as handle:
                temporary = Path(handle.name)
                handle.write(data)
            try:
                temporary.replace(target)
            finally:
                temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-directory", type=Path)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    restore(
        DATA,
        json.loads((DATA / "course_sources.json").read_text()),
        source_directory=args.source_directory,
        download=args.download,
    )
