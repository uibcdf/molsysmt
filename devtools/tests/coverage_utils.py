from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Optional


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=False)


def file_rows(data: dict, package_root: str = "molsysmt", subpackage: Optional[str] = None) -> list[dict]:
    rows = []
    subpackage_parts = tuple(subpackage.split(".")) if subpackage else None

    for path, info in data.get("files", {}).items():
        parts = Path(path).parts
        if package_root not in parts:
            continue

        pkg_parts = parts[parts.index(package_root):]
        dot_parts = []
        for p in pkg_parts:
            if p.endswith(".py"):
                dot_parts.append(p[:-3])
            else:
                dot_parts.append(p)
        package_dot = ".".join(dot_parts)

        if subpackage_parts:
            if tuple(package_dot.split(".")[:len(subpackage_parts)]) != subpackage_parts:
                continue

        summary = info.get("summary", {})
        rows.append({
            "path": path,
            "parts": parts,
            "package_dot": package_dot,
            "percent": float(summary.get("percent_covered", 0.0)),
            "statements": int(summary.get("num_statements", 0)),
            "missing": int(summary.get("missing_lines", 0)),
            "covered": int(summary.get("covered_lines", 0)),
        })
    return rows


def package_key(path_str: str, root: str = "molsysmt", depth: int = 1) -> str | None:
    parts = Path(path_str).parts
    if root not in parts:
        return None
    idx = parts.index(root)
    subparts = list(parts[idx: idx + 1 + max(depth, 0)])
    if subparts and subparts[-1].endswith(".py"):
        subparts = subparts[:-1]
    if not subparts:
        return None
    return ".".join(subparts)


def aggregate_by_package(rows: list[dict], root: str = "molsysmt", depth: int = 1) -> list[dict]:
    stats: Dict[str, Dict[str, int]] = defaultdict(lambda: {"statements": 0, "missing": 0, "covered": 0, "files": 0})
    for row in rows:
        key = package_key(row["path"], root=root, depth=depth)
        if key is None:
            continue
        stats[key]["statements"] += row["statements"]
        stats[key]["missing"] += row["missing"]
        stats[key]["covered"] += row["covered"]
        stats[key]["files"] += 1

    out = []
    for key, values in stats.items():
        stmts = values["statements"]
        miss = values["missing"]
        covered = values["covered"]
        files = values["files"]
        percent = 100.0 * (stmts - miss) / stmts if stmts else 0.0
        out.append({
            "package": key,
            "percent": percent,
            "statements": stmts,
            "missing": miss,
            "covered": covered,
            "files": files,
        })
    return out


def sort_packages(packages: list[dict], mode: str = "coverage") -> list[dict]:
    packages = list(packages)
    if mode == "name":
        packages.sort(key=lambda x: x["package"])
    else:
        packages.sort(key=lambda x: (x["percent"], -x["statements"], x["package"]))
    return packages


def grade(percent: float) -> str:
    if percent >= 95:
        return "excellent"
    if percent >= 85:
        return "good"
    if percent >= 70:
        return "fair"
    return "weak"


def bar(percent: float, width: int = 20) -> str:
    filled = round(percent / 100.0 * width)
    return "█" * filled + "·" * (width - filled)


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        out.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(out)


def global_summary(rows: list[dict]) -> dict:
    statements = sum(r["statements"] for r in rows)
    missing = sum(r["missing"] for r in rows)
    covered = sum(r["covered"] for r in rows)
    percent = 100.0 * (statements - missing) / statements if statements else 0.0
    return {
        "percent": percent,
        "statements": statements,
        "missing": missing,
        "covered": covered,
        "files": len(rows),
    }
