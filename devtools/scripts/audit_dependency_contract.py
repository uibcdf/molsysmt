"""Audit every declared copy or alternate provider of public dependencies.

``pyproject.toml`` owns runtime names and constraints. The route inventory in
``devtools/dependency_contract.toml`` owns only where those constraints must be
checked. This command never rewrites a packaging or environment file.
"""

from __future__ import annotations

import argparse
import ast
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

import yaml
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = Path("devtools/dependency_contract.toml")
PIN_LINE = re.compile(
    r"git\+https://github\.com/uibcdf/(?P<name>[A-Za-z0-9_.-]+)@(?P<sha>[0-9a-f]{40})"
)
SPEC_NAME = re.compile(r"^\s*(?P<name>[A-Za-z0-9_.-]+)(?:\s|[<>=!~]|$)")


@dataclass(frozen=True)
class Finding:
    """A contract mismatch with its owning file and actionable explanation."""

    path: str
    message: str


def _load_toml(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _project_requirements(root: Path) -> tuple[dict[str, Requirement], Requirement]:
    project = _load_toml(root / "pyproject.toml")["project"]
    requirements = {
        canonicalize_name(parsed.name): parsed
        for parsed in (Requirement(item) for item in project["dependencies"])
    }
    if len(requirements) != len(project["dependencies"]):
        raise ValueError("pyproject.toml declares the same runtime dependency twice")
    return requirements, Requirement(f"python{project['requires-python']}")


def _name(raw: str) -> str:
    match = SPEC_NAME.match(raw)
    if match is None:
        raise ValueError(f"cannot identify a dependency name in {raw!r}")
    return canonicalize_name(match.group("name"))


def _requirement(raw: str, aliases: dict[str, str]) -> tuple[str, Requirement]:
    parsed = Requirement(raw.strip())
    name = aliases.get(canonicalize_name(parsed.name), canonicalize_name(parsed.name))
    return name, parsed


def _recipe_items(path: Path) -> list[str]:
    """Read the bounded run block without pretending a Jinja recipe is plain YAML."""
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line == "requirements:")
        run = next(i for i in range(start + 1, len(lines)) if lines[i] == "  run:")
    except StopIteration as exc:
        raise ValueError("cannot find the requirements.run block") from exc

    items = []
    for line in lines[run + 1 :]:
        if line and not line.startswith(" "):
            break
        if re.match(r"^  (?:build|host|run):", line):
            break
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not stripped.startswith("- "):
            raise ValueError(f"unsupported requirements.run entry: {stripped}")
        item = stripped[2:].split("#", 1)[0].strip()
        if not item or "{{" in item or "${{" in item:
            raise ValueError(f"unresolved requirements.run entry: {stripped}")
        items.append(item)
    if not items:
        raise ValueError("requirements.run is empty")
    return items


def _environment_items(path: Path) -> list[str]:
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    dependencies = content.get("dependencies") if isinstance(content, dict) else None
    if not isinstance(dependencies, list):
        raise ValueError("environment has no dependencies list")
    items = []
    for dependency in dependencies:
        if isinstance(dependency, str):
            items.append(dependency)
        elif isinstance(dependency, dict) and set(dependency) == {"pip"}:
            if not isinstance(dependency["pip"], list) or not all(
                isinstance(item, str) for item in dependency["pip"]
            ):
                raise ValueError("pip dependencies must be a list of strings")
            items.extend(dependency["pip"])
        else:
            raise ValueError(f"unsupported environment dependency: {dependency!r}")
    return items


def _observed_requirements(
    items: list[str],
    names: set[str],
    aliases: dict[str, str],
    *,
    parse_python: bool = False,
) -> tuple[dict[str, Requirement], list[Requirement]]:
    observed: dict[str, Requirement] = {}
    python: list[Requirement] = []
    for item in items:
        name = aliases.get(_name(item), _name(item))
        if name == "python" and not parse_python:
            continue
        if name != "python" and name not in names:
            continue
        parsed_name, parsed = _requirement(item, aliases)
        if parsed_name == "python":
            python.append(parsed)
        elif parsed_name in observed:
            raise ValueError(f"duplicate runtime dependency: {parsed_name}")
        else:
            observed[parsed_name] = parsed
    return observed, python


def _compare_requirements(
    path: str,
    expected: dict[str, Requirement],
    observed: dict[str, Requirement],
    supplied: set[str],
) -> list[Finding]:
    findings = []
    for name, requirement in expected.items():
        actual = observed.get(name)
        if name in supplied:
            if actual is not None:
                findings.append(
                    Finding(path, f"{name} is both listed and source-supplied")
                )
            continue
        if actual is None:
            findings.append(Finding(path, f"missing {requirement}"))
        elif actual.specifier != requirement.specifier:
            findings.append(
                Finding(
                    path,
                    f"{name} declares {actual.specifier or '(unbounded)'}; "
                    f"pyproject.toml requires {requirement.specifier or '(unbounded)'}",
                )
            )
    return findings


def _controlled_names(path: Path) -> set[str]:
    names = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = PIN_LINE.fullmatch(line)
        if match is None:
            raise ValueError(f"invalid controlled source pin: {line}")
        name = canonicalize_name(match.group("name"))
        if name in names:
            raise ValueError(f"duplicate controlled source pin: {name}")
        names.add(name)
    if not names:
        raise ValueError("controlled source manifest has no pins")
    return names


def _registry_findings(root: Path, project: set[str]) -> list[Finding]:
    """Compare hard/soft form classification with public runtime metadata."""
    path = "molsysmt/_depdigest.py"
    tree = ast.parse((root / path).read_text(encoding="utf-8"))
    declaration = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "LIBRARIES"
                for target in node.targets
            )
        ),
        None,
    )
    if declaration is None:
        raise ValueError("the DepDigest LIBRARIES registry is missing")
    libraries = ast.literal_eval(declaration.value)
    findings = []
    for metadata in libraries.values():
        name = canonicalize_name(metadata["pypi"])
        kind = metadata["type"]
        if kind == "hard" and name not in project:
            findings.append(
                Finding(
                    path, f"hard form dependency {name} is absent from pyproject.toml"
                )
            )
        elif kind == "soft" and name in project:
            findings.append(
                Finding(
                    path,
                    f"soft form dependency {name} is an unconditional runtime requirement",
                )
            )
        elif kind not in {"hard", "soft"}:
            findings.append(
                Finding(path, f"unknown dependency classification {kind!r}")
            )
    return findings


def _workflow_jobs(path: Path) -> dict:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    jobs = payload.get("jobs") if isinstance(payload, dict) else None
    if not isinstance(jobs, dict):
        raise ValueError("workflow has no jobs mapping")
    return jobs


def _job_runs(job: dict) -> str:
    return "\n".join(
        step["run"]
        for step in job.get("steps", [])
        if isinstance(step, dict) and isinstance(step.get("run"), str)
    )


def audit(root: Path) -> list[Finding]:
    """Return all static dependency-route mismatches in a repository tree."""
    root = root.resolve()
    config = _load_toml(root / CONTRACT)
    if config.get("schema") != 1:
        raise ValueError("unsupported dependency-contract schema")
    project, python = _project_requirements(root)
    conda_names = {
        canonicalize_name(conda): canonicalize_name(public)
        for public, conda in config["conda_names"].items()
    }
    if not set(conda_names.values()) <= set(project):
        raise ValueError("a Conda name override does not name a public dependency")
    findings: list[Finding] = []
    findings.extend(_registry_findings(root, set(project)))
    configured_recipes = set(config["recipes"].values())
    actual_recipes = {
        str(path.relative_to(root))
        for path in (root / "devtools").rglob("*.yaml")
        if path.name in {"meta.yaml", "recipe.yaml"}
    }
    for path in sorted(actual_recipes - configured_recipes):
        findings.append(Finding(path, "Conda recipe is not classified by the audit"))
    for path in sorted(configured_recipes - actual_recipes):
        findings.append(Finding(path, "inventoried Conda recipe does not exist"))
    for path in config["recipes"].values():
        try:
            items = _recipe_items(root / path)
            observed, python_items = _observed_requirements(
                items, set(project), conda_names, parse_python=True
            )
            findings.extend(_compare_requirements(path, project, observed, set()))
            for item in items:
                name = conda_names.get(_name(item), _name(item))
                if name not in project and name != "python":
                    findings.append(
                        Finding(path, f"undeclared Conda runtime dependency: {name}")
                    )
            if not any(item.specifier == python.specifier for item in python_items):
                findings.append(
                    Finding(
                        path, f"no Python runtime constraint matches {python.specifier}"
                    )
                )
        except (OSError, ValueError) as exc:
            findings.append(Finding(path, str(exc)))

    controlled_path = config["controlled_sources"]
    try:
        controlled = _controlled_names(root / controlled_path)
    except (OSError, ValueError) as exc:
        findings.append(Finding(controlled_path, str(exc)))
        controlled = set()
    for name in sorted(controlled - set(project)):
        findings.append(
            Finding(controlled_path, f"{name} is not a public runtime dependency")
        )

    configured = set()
    environments = {}
    for entry in config["environments"]:
        path = entry["path"]
        if path in configured:
            findings.append(
                Finding(path, "environment appears more than once in inventory")
            )
        configured.add(path)
        supplied = {canonicalize_name(name) for name in entry["source_supplied"]}
        for name in sorted(supplied - controlled - {"molsysviewer"}):
            findings.append(Finding(path, f"{name} has no audited source provider"))
        try:
            items = _environment_items(root / path)
            observed, _ = _observed_requirements(items, set(project), conda_names)
            findings.extend(_compare_requirements(path, project, observed, supplied))
            environments[path] = supplied
        except (OSError, ValueError) as exc:
            findings.append(Finding(path, str(exc)))
    for entry in config["excluded_environments"]:
        path = entry["path"]
        if path in configured or not entry.get("reason", "").strip():
            findings.append(
                Finding(path, "duplicate or unexplained environment exclusion")
            )
        configured.add(path)
    actual = {
        str(path.relative_to(root))
        for pattern in ("*.yaml", "*.yml")
        for path in (root / "devtools/conda-envs").glob(pattern)
    }
    for path in sorted(actual - configured):
        findings.append(Finding(path, "environment is not classified by the audit"))
    for path in sorted(configured - actual):
        findings.append(Finding(path, "inventoried environment does not exist"))

    required_workflows = set(config["workflow_sources"]["controlled"])
    routine = config["routine_viewer_source"]
    routine_workflows = set(routine["workflows"])
    if not re.fullmatch(r"[0-9a-f]{40}", routine["sha"]):
        raise ValueError("routine Viewer source must be a full commit SHA")
    discovered_workflows = set()
    discovered_routine = set()
    for path in sorted((root / ".github/workflows").glob("*.y*ml")):
        relative = str(path.relative_to(root))
        try:
            jobs = _workflow_jobs(path)
        except (OSError, ValueError) as exc:
            findings.append(Finding(relative, str(exc)))
            continue
        all_runs = "\n".join(
            _job_runs(job) for job in jobs.values() if isinstance(job, dict)
        )
        viewer_shas = set(
            re.findall(
                r"git\+https://github\.com/uibcdf/molsysviewer@([0-9a-f]{40})",
                all_runs,
            )
        )
        if viewer_shas:
            discovered_routine.add(relative)
        if relative in routine_workflows and viewer_shas != {routine["sha"]}:
            findings.append(
                Finding(relative, f"routine Viewer source must be {routine['sha']}")
            )
        if f"-r {controlled_path}" in all_runs:
            discovered_workflows.add(relative)
        for name in controlled:
            if re.search(
                rf"git\+https://github\.com/uibcdf/{re.escape(name)}@[0-9a-f]{{40}}",
                all_runs,
            ):
                findings.append(
                    Finding(
                        relative,
                        f"{name} repeats a controlled SHA outside the manifest",
                    )
                )
        for job in jobs.values():
            if not isinstance(job, dict):
                continue
            steps = job.get("steps", [])
            for step in steps:
                if not isinstance(step, dict):
                    continue
                checkout = (
                    step.get("with", {}).get("repository")
                    if isinstance(step.get("with"), dict)
                    else None
                )
                if isinstance(checkout, str) and checkout.startswith("uibcdf/"):
                    name = canonicalize_name(checkout.split("/", 1)[1])
                    if name in controlled:
                        findings.append(
                            Finding(
                                relative,
                                f"{name} is checked out outside the controlled manifest",
                            )
                        )
                env_path = (
                    step.get("with", {}).get("environment-file")
                    if isinstance(step.get("with"), dict)
                    else None
                )
                if env_path not in environments:
                    continue
                supplied = environments[env_path]
                runs = _job_runs(job)
                if supplied & controlled and f"-r {controlled_path}" not in runs:
                    findings.append(
                        Finding(
                            relative,
                            f"job using {env_path} omits controlled source install",
                        )
                    )
                if (
                    supplied & controlled
                    and "validate_controlled_dependencies.py" not in runs
                ):
                    findings.append(
                        Finding(
                            relative,
                            f"job using {env_path} omits controlled version check",
                        )
                    )
                viewer_direct = "git+https://github.com/uibcdf/molsysviewer@" in runs
                viewer_wheel = (
                    "controlled-wheelhouse/*.whl" in runs
                    and "git+https://github.com/uibcdf/molsysviewer@" in all_runs
                )
                if "molsysviewer" in supplied and not (viewer_direct or viewer_wheel):
                    findings.append(
                        Finding(
                            relative,
                            f"job using {env_path} omits Viewer source install",
                        )
                    )
    for path in sorted(required_workflows - discovered_workflows):
        findings.append(
            Finding(path, "workflow does not consume the controlled source manifest")
        )
    for path in sorted(discovered_workflows - required_workflows):
        findings.append(
            Finding(path, "unclassified consumer of controlled source manifest")
        )
    for path in sorted(discovered_routine - routine_workflows):
        findings.append(Finding(path, "unclassified literal Viewer source SHA"))
    for path in sorted(routine_workflows - discovered_routine):
        findings.append(Finding(path, "routine Viewer source SHA is missing"))
    return findings


def main() -> int:
    """Print a bounded, read-only verdict for local development and CI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        findings = audit(args.root)
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(f"Dependency contract audit: FAIL (invalid inventory: {exc})")
        return 1
    if findings:
        for finding in findings:
            print(f"[DEPENDENCY_CONTRACT] {finding.path}: {finding.message}")
        print(f"Dependency contract audit: FAIL ({len(findings)} mismatches)")
        return 1
    print(
        "Dependency contract audit: PASS (public requirements and declared routes agree)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
