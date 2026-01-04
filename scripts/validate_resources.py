#!/usr/bin/env python3

"""
Validate MolSysSuite-style resources YAML files:
- resources/talks.yml
- resources/papers.yml
- resources/tutorials.yml

This validator is intentionally lightweight (no external schema engine) and aims to
catch common issues early (missing keys, wrong types, invalid enums, duplicate ids).

Usage:
  python scripts/validate_resources.py
  python scripts/validate_resources.py --repo-root /path/to/repo
  python scripts/validate_resources.py --strict
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import yaml  # type: ignore
except Exception:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml OR conda install -c conda-forge pyyaml")
    raise

ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")  # org/repo

TALK_STATUS = {"draft", "idea", "planned", "ready", "delivered", "archived"}
PAPER_STATUS = {"idea", "in_preparation", "submitted", "accepted", "published", "archived"}
TUTORIAL_STATUS = {"idea", "planned", "draft", "ready", "archived"}

TUTORIAL_LEVEL = {"beginner", "intermediate", "advanced"}
TUTORIAL_FORMAT = {"notebook", "markdown", "workshop"}


@dataclass
class ValidationError:
    file: Path
    message: str


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_str(x: Any) -> bool:
    return isinstance(x, str)


def is_int(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def is_bool(x: Any) -> bool:
    return isinstance(x, bool)


def is_list(x: Any) -> bool:
    return isinstance(x, list)


def is_dict(x: Any) -> bool:
    return isinstance(x, dict)


def require_keys(obj: Dict[str, Any], keys: List[str], ctx: str, errors: List[ValidationError], file: Path):
    for k in keys:
        if k not in obj:
            errors.append(ValidationError(file, f"{ctx}: missing required key '{k}'"))


def validate_repo_field(repo: Any, file: Path, errors: List[ValidationError], ctx: str):
    if not is_str(repo) or not REPO_RE.match(repo):
        errors.append(ValidationError(file, f"{ctx}: 'repo' must be 'org/repo' string (got {repo!r})"))


def validate_tags(tags: Any, file: Path, errors: List[ValidationError], ctx: str):
    if tags is None:
        return
    if not is_list(tags) or not all(is_str(t) for t in tags):
        errors.append(ValidationError(file, f"{ctx}: 'tags' must be a list of strings"))


def validate_path_field(path_value: Any, file: Path, errors: List[ValidationError], ctx: str):
    if not is_str(path_value) or path_value.strip() == "":
        errors.append(ValidationError(file, f"{ctx}: 'path' must be a non-empty string"))
        return
    if "://" in path_value:
        errors.append(ValidationError(file, f"{ctx}: 'path' should be a repo-relative path, not a URL"))


def validate_unique_ids(items: List[Dict[str, Any]], file: Path, errors: List[ValidationError], kind: str):
    seen = set()
    for i, it in enumerate(items):
        _id = it.get("id")
        if not is_str(_id):
            continue
        if _id in seen:
            errors.append(ValidationError(file, f"{kind}[{i}]: duplicate id '{_id}'"))
        seen.add(_id)


def validate_talks(data: Any, file: Path, errors: List[ValidationError]):
    ctx0 = "talks.yml"
    if not is_dict(data):
        errors.append(ValidationError(file, f"{ctx0}: top-level YAML must be a mapping"))
        return

    validate_repo_field(data.get("repo"), file, errors, ctx0)

    talks = data.get("talks")
    if not is_list(talks):
        errors.append(ValidationError(file, f"{ctx0}: 'talks' must be a list"))
        return

    validate_unique_ids(talks, file, errors, "talks")

    for i, t in enumerate(talks):
        ctx = f"talks[{i}]"
        if not is_dict(t):
            errors.append(ValidationError(file, f"{ctx}: must be a mapping"))
            continue

        require_keys(
            t,
            ["id", "title", "authors", "role", "event", "path", "tags", "status"],
            ctx,
            errors,
            file,
        )

        if "id" in t and not is_str(t["id"]):
            errors.append(ValidationError(file, f"{ctx}: 'id' must be a string"))
        if "title" in t and not is_str(t["title"]):
            errors.append(ValidationError(file, f"{ctx}: 'title' must be a string"))

        authors = t.get("authors")
        if not is_list(authors) or not all(is_str(a) for a in authors):
            errors.append(ValidationError(file, f"{ctx}: 'authors' must be a list of strings"))

        if "role" in t and not is_str(t["role"]):
            errors.append(ValidationError(file, f"{ctx}: 'role' must be a string"))

        event = t.get("event")
        if not is_dict(event):
            errors.append(ValidationError(file, f"{ctx}: 'event' must be a mapping"))
        else:
            require_keys(event, ["name", "location", "date", "duration_min"], f"{ctx}.event", errors, file)
            if "name" in event and not is_str(event["name"]):
                errors.append(ValidationError(file, f"{ctx}.event: 'name' must be a string"))
            if "location" in event and not is_str(event["location"]):
                errors.append(ValidationError(file, f"{ctx}.event: 'location' must be a string"))
            if "date" in event:
                d = event["date"]
                if not is_str(d) or not ISO_DATE_RE.match(d):
                    errors.append(ValidationError(file, f"{ctx}.event: 'date' must be YYYY-MM-DD (got {d!r})"))
            if "duration_min" in event and not is_int(event["duration_min"]):
                errors.append(ValidationError(file, f"{ctx}.event: 'duration_min' must be an integer"))

        validate_path_field(t.get("path"), file, errors, ctx)
        validate_tags(t.get("tags"), file, errors, ctx)

        status = t.get("status")
        if not is_str(status) or status not in TALK_STATUS:
            errors.append(ValidationError(file, f"{ctx}: 'status' must be one of {sorted(TALK_STATUS)} (got {status!r})"))

        artifacts = t.get("artifacts")
        if artifacts is not None:
            if not is_dict(artifacts):
                errors.append(ValidationError(file, f"{ctx}: 'artifacts' must be a mapping if present"))
            else:
                for k, v in artifacts.items():
                    if not is_str(k) or not is_str(v):
                        errors.append(ValidationError(file, f"{ctx}.artifacts: keys and values must be strings"))

        if "notes" in t and t["notes"] is not None and not is_str(t["notes"]):
            errors.append(ValidationError(file, f"{ctx}: 'notes' must be a string if present"))


def validate_papers(data: Any, file: Path, errors: List[ValidationError]):
    ctx0 = "papers.yml"
    if not is_dict(data):
        errors.append(ValidationError(file, f"{ctx0}: top-level YAML must be a mapping"))
        return

    validate_repo_field(data.get("repo"), file, errors, ctx0)

    papers = data.get("papers")
    if not is_list(papers):
        errors.append(ValidationError(file, f"{ctx0}: 'papers' must be a list"))
        return

    validate_unique_ids(papers, file, errors, "papers")

    for i, p in enumerate(papers):
        ctx = f"papers[{i}]"
        if not is_dict(p):
            errors.append(ValidationError(file, f"{ctx}: must be a mapping"))
            continue

        require_keys(
            p,
            ["id", "title", "authors", "year", "venue", "status", "path", "primary", "related_repos"],
            ctx,
            errors,
            file,
        )

        if "id" in p and not is_str(p["id"]):
            errors.append(ValidationError(file, f"{ctx}: 'id' must be a string"))
        if "title" in p and not is_str(p["title"]):
            errors.append(ValidationError(file, f"{ctx}: 'title' must be a string"))

        authors = p.get("authors")
        if not is_list(authors) or not all(is_str(a) for a in authors):
            errors.append(ValidationError(file, f"{ctx}: 'authors' must be a list of strings"))

        if "year" in p and not is_int(p["year"]):
            errors.append(ValidationError(file, f"{ctx}: 'year' must be an integer"))
        if "venue" in p and not is_str(p["venue"]):
            errors.append(ValidationError(file, f"{ctx}: 'venue' must be a string"))

        status = p.get("status")
        if not is_str(status) or status not in PAPER_STATUS:
            errors.append(ValidationError(file, f"{ctx}: 'status' must be one of {sorted(PAPER_STATUS)} (got {status!r})"))

        validate_path_field(p.get("path"), file, errors, ctx)

        primary = p.get("primary")
        if not is_bool(primary):
            errors.append(ValidationError(file, f"{ctx}: 'primary' must be boolean"))

        related = p.get("related_repos")
        if not is_list(related) or not all(is_str(r) and REPO_RE.match(r) for r in related):
            errors.append(ValidationError(file, f"{ctx}: 'related_repos' must be a list of 'org/repo' strings"))

        # Optional fields
        if "doi" in p and p["doi"] is not None and not is_str(p["doi"]):
            errors.append(ValidationError(file, f"{ctx}: 'doi' must be a string if present"))
        if "url" in p and p["url"] is not None and not is_str(p["url"]):
            errors.append(ValidationError(file, f"{ctx}: 'url' must be a string if present"))
        if "notes" in p and p["notes"] is not None and not is_str(p["notes"]):
            errors.append(ValidationError(file, f"{ctx}: 'notes' must be a string if present"))

        # NEW: allow optional tags in papers.yml
        if "tags" in p:
            validate_tags(p.get("tags"), file, errors, ctx)


def validate_tutorials(data: Any, file: Path, errors: List[ValidationError]):
    ctx0 = "tutorials.yml"
    if not is_dict(data):
        errors.append(ValidationError(file, f"{ctx0}: top-level YAML must be a mapping"))
        return

    validate_repo_field(data.get("repo"), file, errors, ctx0)

    tutorials = data.get("tutorials")
    if not is_list(tutorials):
        errors.append(ValidationError(file, f"{ctx0}: 'tutorials' must be a list"))
        return

    validate_unique_ids(tutorials, file, errors, "tutorials")

    for i, t in enumerate(tutorials):
        ctx = f"tutorials[{i}]"
        if not is_dict(t):
            errors.append(ValidationError(file, f"{ctx}: must be a mapping"))
            continue

        require_keys(
            t,
            ["id", "title", "level", "format", "est_time_min", "path", "status", "tags"],
            ctx,
            errors,
            file,
        )

        if "id" in t and not is_str(t["id"]):
            errors.append(ValidationError(file, f"{ctx}: 'id' must be a string"))
        if "title" in t and not is_str(t["title"]):
            errors.append(ValidationError(file, f"{ctx}: 'title' must be a string"))

        level = t.get("level")
        if not is_str(level) or level not in TUTORIAL_LEVEL:
            errors.append(ValidationError(file, f"{ctx}: 'level' must be one of {sorted(TUTORIAL_LEVEL)} (got {level!r})"))

        fmt = t.get("format")
        if not is_str(fmt) or fmt not in TUTORIAL_FORMAT:
            errors.append(ValidationError(file, f"{ctx}: 'format' must be one of {sorted(TUTORIAL_FORMAT)} (got {fmt!r})"))

        if "est_time_min" in t and not is_int(t["est_time_min"]):
            errors.append(ValidationError(file, f"{ctx}: 'est_time_min' must be an integer"))

        validate_path_field(t.get("path"), file, errors, ctx)

        status = t.get("status")
        if not is_str(status) or status not in TUTORIAL_STATUS:
            errors.append(ValidationError(file, f"{ctx}: 'status' must be one of {sorted(TUTORIAL_STATUS)} (got {status!r})"))

        validate_tags(t.get("tags"), file, errors, ctx)

        if "notes" in t and t["notes"] is not None and not is_str(t["notes"]):
            errors.append(ValidationError(file, f"{ctx}: 'notes' must be a string if present"))

        # NEW: allow optional prerequisites list[str]
        if "prerequisites" in t and t["prerequisites"] is not None:
            prereq = t["prerequisites"]
            if not is_list(prereq) or not all(is_str(x) for x in prereq):
                errors.append(ValidationError(file, f"{ctx}: 'prerequisites' must be a list of strings if present"))


def validate_file(path: Path) -> Tuple[bool, List[ValidationError]]:
    errors: List[ValidationError] = []
    try:
        data = load_yaml(path)
    except Exception as e:
        return False, [ValidationError(path, f"Failed to parse YAML: {e}")]

    if path.name == "talks.yml":
        validate_talks(data, path, errors)
    elif path.name == "papers.yml":
        validate_papers(data, path, errors)
    elif path.name == "tutorials.yml":
        validate_tutorials(data, path, errors)
    else:
        errors.append(ValidationError(path, "Unknown resources file (expected talks.yml, papers.yml, tutorials.yml)"))

    return (len(errors) == 0), errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=str, default=".", help="Path to the repository root")
    ap.add_argument("--strict", action="store_true", help="Fail if any resources file is missing")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    resources_dir = repo_root / "resources"

    if not resources_dir.exists():
        print(f"ERROR: resources/ directory not found in {repo_root}")
        return 2

    targets = [resources_dir / "talks.yml", resources_dir / "papers.yml", resources_dir / "tutorials.yml"]

    ok_all = True
    any_found = False

    for f in targets:
        if not f.exists():
            if args.strict:
                print(f"ERROR: missing file: {f}")
                ok_all = False
            else:
                print(f"WARNING: missing file: {f} (skipping)")
            continue

        any_found = True
        ok, errs = validate_file(f)
        if ok:
            print(f"OK: {f.relative_to(repo_root)}")
        else:
            ok_all = False
            print(f"FAIL: {f.relative_to(repo_root)}")
            for e in errs:
                print(f"  - {e.message}")

    if args.strict and not any_found:
        print("ERROR: strict mode enabled but no resources files found.")
        return 2

    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
