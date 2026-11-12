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
SPEC_NAME = re.compile(r"^\s*(?P<name>[A-Za-z0-9_.-]+)(?:\s|[<>=!~;\[]|$)")


@dataclass(frozen=True)
class Finding:
    """A contract mismatch with its owning file and actionable explanation."""

    path: str
    message: str


def _load_toml(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _project_requirements(
    root: Path, runtime_extras: list[str]
) -> tuple[dict[str, Requirement], dict[str, Requirement], Requirement]:
    project = _load_toml(root / "pyproject.toml")["project"]
    requirements = {
        canonicalize_name(parsed.name): parsed
        for parsed in (Requirement(item) for item in project["dependencies"])
    }
    if len(requirements) != len(project["dependencies"]):
        raise ValueError("pyproject.toml declares the same runtime dependency twice")
    if (
        not isinstance(runtime_extras, list)
        or not all(isinstance(name, str) for name in runtime_extras)
        or len(set(runtime_extras)) != len(runtime_extras)
    ):
        raise ValueError("runtime extras must be a list of unique public extra names")
    optional = {}
    for extra in runtime_extras:
        if extra not in project.get("optional-dependencies", {}):
            raise ValueError(f"unknown public runtime extra: {extra}")
        for raw in project["optional-dependencies"][extra]:
            requirement = Requirement(raw)
            name = canonicalize_name(requirement.name)
            if name in requirements:
                raise ValueError(
                    f"runtime optional dependency {name} is also unconditional"
                )
            if name in optional and optional[name] != requirement:
                raise ValueError(
                    f"conflicting runtime optional requirements for {name}"
                )
            optional[name] = requirement
    return requirements, optional, Requirement(f"python{project['requires-python']}")


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


def _environment_routes(path: Path) -> tuple[list[str], list[str], list[str]]:
    """Keep Conda and pip acquisition distinct while reading an environment."""
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    dependencies = content.get("dependencies") if isinstance(content, dict) else None
    if not isinstance(dependencies, list):
        raise ValueError("environment has no dependencies list")
    channels = content.get("channels", [])
    if not isinstance(channels, list) or not all(
        isinstance(channel, str) and channel.strip() for channel in channels
    ):
        raise ValueError("environment channels must be a list of nonempty strings")
    conda = []
    pip = []
    for dependency in dependencies:
        if isinstance(dependency, str):
            conda.append(dependency)
        elif isinstance(dependency, dict) and set(dependency) == {"pip"}:
            if not isinstance(dependency["pip"], list) or not all(
                isinstance(item, str) for item in dependency["pip"]
            ):
                raise ValueError("pip dependencies must be a list of strings")
            pip.extend(dependency["pip"])
        else:
            raise ValueError(f"unsupported environment dependency: {dependency!r}")
    return conda, pip, channels


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


def _constraint_text(requirement: Requirement) -> str:
    text = str(requirement.specifier) or "(unbounded)"
    if requirement.extras:
        text = f"[{','.join(sorted(requirement.extras))}]{text}"
    if requirement.url is not None:
        text = f"@ {requirement.url}"
    if requirement.marker is not None:
        text += f"; {requirement.marker}"
    return text


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
        elif (
            actual.specifier != requirement.specifier
            or actual.marker != requirement.marker
            or actual.extras != requirement.extras
            or actual.url != requirement.url
        ):
            findings.append(
                Finding(
                    path,
                    f"{name} declares {_constraint_text(actual)}; "
                    f"pyproject.toml requires {_constraint_text(requirement)}",
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


def _registry_libraries(root: Path) -> dict:
    """Read provider metadata without importing MolSysMT or optional engines."""
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
    if not isinstance(libraries, dict):
        raise ValueError("the DepDigest LIBRARIES registry must be a mapping")
    return libraries


def _registry_findings(libraries: dict, project: set[str]) -> list[Finding]:
    """Compare hard/soft form classification with public runtime metadata."""
    path = "molsysmt/_depdigest.py"
    findings = []
    for library, metadata in libraries.items():
        kind = metadata["type"]
        if kind not in {"hard", "soft"}:
            findings.append(
                Finding(path, f"unknown dependency classification {kind!r}")
            )
            continue
        distribution = metadata.get("pypi", library)
        if distribution is None:
            if kind != "hard":
                continue
            distribution = metadata.get("conda")
            if not isinstance(distribution, str) or not distribution.strip():
                findings.append(
                    Finding(
                        path,
                        f"hard form dependency {library} has no public Python distribution route",
                    )
                )
                continue
            try:
                route = Requirement(distribution)
            except ValueError:
                route = None
            channel = metadata.get("channel")
            if (
                route is None
                or route.specifier
                or route.extras
                or route.marker
                or route.url
                or not isinstance(channel, str)
                or not channel.strip()
            ):
                findings.append(
                    Finding(
                        path, f"invalid hard Conda distribution route for {library}"
                    )
                )
                continue
        if not isinstance(distribution, str) or not distribution.strip():
            findings.append(
                Finding(path, f"invalid Python distribution route for {library}")
            )
            continue
        name = canonicalize_name(distribution)
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
    return findings


def _provider_requirements(
    root: Path, libraries: dict, public_python_names: set[str]
) -> tuple[dict[str, Requirement], dict[str, str]]:
    """Read non-installer provider constraints and derive their Conda aliases."""
    tools = _load_toml(root / "pyproject.toml").get("tool", {})
    if not isinstance(tools, dict):
        raise ValueError("tool must be a table")
    owner = tools.get("molsysmt", {})
    if not isinstance(owner, dict):
        raise ValueError("tool.molsysmt must be a table")
    declarations = owner.get("provider-requirements", {})
    if not isinstance(declarations, dict):
        raise ValueError(
            "provider-requirements must be a table of capability requirements"
        )
    requirements = {}
    names = set()
    aliases = {}
    for library, raw in declarations.items():
        metadata = libraries.get(library)
        if metadata is None:
            raise ValueError(f"unknown provider-requirements capability {library}")
        if metadata.get("type") != "soft" or metadata.get("pypi", library) is not None:
            raise ValueError(
                f"provider-requirements capability {library} is not Conda-only"
            )
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError(f"invalid provider requirement for {library}")
        name, requirement = _requirement(raw, {})
        if (
            not requirement.specifier
            or requirement.marker
            or requirement.extras
            or requirement.url
        ):
            raise ValueError(
                f"provider requirement for {library} must declare only version constraints"
            )
        if name in names:
            raise ValueError(f"duplicate provider requirement distribution: {name}")
        names.add(name)
        package = metadata.get("conda")
        if not isinstance(package, str) or not package.strip():
            raise ValueError(f"invalid Conda package route for {library}")
        package_name, parsed = _requirement(package, {})
        if parsed.specifier or parsed.marker or parsed.extras or parsed.url:
            raise ValueError(f"invalid Conda package route for {library}")
        channel = metadata.get("channel")
        if not isinstance(channel, str) or not channel.strip():
            raise ValueError(f"invalid Conda channel for {library}")
        if package_name in aliases:
            raise ValueError(f"duplicate provider Conda package: {package_name}")
        if {name, package_name} & public_python_names:
            raise ValueError(
                f"Conda-only provider {library} has a public pip requirement"
            )
        aliases[package_name] = name
        requirements[library] = requirement
    return requirements, aliases


def _conda_provider_findings(
    path: str,
    required: list[str],
    libraries: dict,
    conda: list[str],
    pip: list[str],
    channels: list[str],
    public_python_names: set[str],
    provider_requirements: dict[str, Requirement],
) -> list[Finding]:
    """Check declared Conda-only acquisition, without asserting provider ABI support."""
    if not isinstance(required, list) or not all(
        isinstance(name, str) and name.strip() for name in required
    ):
        raise ValueError(
            "conda_provider_required must be a list of registry capability names"
        )
    if len(set(required)) != len(required):
        raise ValueError("conda_provider_required declares a capability more than once")
    selected = set(required)
    observed_names = {_name(raw) for raw in [*conda, *pip]}
    for library, metadata in libraries.items():
        if metadata.get("type") != "soft" or metadata.get("pypi", library) is not None:
            continue
        names = {canonicalize_name(library.split(".")[0])}
        package = metadata.get("conda")
        if isinstance(package, str) and package.strip():
            names.add(_name(package))
        if library in provider_requirements:
            names.add(canonicalize_name(provider_requirements[library].name))
        if names & observed_names:
            selected.add(library)
    findings = []
    for library in sorted(selected):
        metadata = libraries.get(library)
        if metadata is None:
            findings.append(
                Finding(path, f"unknown Conda provider capability {library}")
            )
            continue
        if metadata.get("type") != "soft" or metadata.get("pypi", library) is not None:
            findings.append(
                Finding(path, f"{library} is not a soft Conda-only provider")
            )
            continue
        package = metadata.get("conda")
        if not isinstance(package, str) or not package.strip():
            findings.append(Finding(path, f"invalid Conda package route for {library}"))
            continue
        try:
            package_name, expected = _requirement(package, {})
        except ValueError:
            findings.append(Finding(path, f"invalid Conda package route for {library}"))
            continue
        if expected.specifier or expected.extras or expected.marker or expected.url:
            findings.append(Finding(path, f"invalid Conda package route for {library}"))
            continue
        channel = metadata.get("channel")
        if not isinstance(channel, str) or not channel.strip():
            findings.append(Finding(path, f"invalid Conda channel for {library}"))
            continue
        if channel not in channels:
            findings.append(
                Finding(path, f"missing declared channel {channel} for {library}")
            )
        standalone_names = {canonicalize_name(library.split(".")[0])}
        requirement = provider_requirements.get(library)
        if requirement is not None:
            standalone_names.add(canonicalize_name(requirement.name))
        names = standalone_names | {package_name}
        for name in sorted(names & public_python_names):
            findings.append(
                Finding(
                    path,
                    f"Conda-only provider {library} has a public pip requirement {name}",
                )
            )
        for standalone in sorted((standalone_names - {package_name}) & observed_names):
            findings.append(
                Finding(
                    path,
                    f"standalone dependency {standalone} overrides Conda provider {library}",
                )
            )
        if any(_name(raw) == package_name for raw in pip):
            findings.append(
                Finding(
                    path, f"pip override for Conda provider {library}: {package_name}"
                )
            )
        provider_items = [raw for raw in conda if _name(raw) == package_name]
        if not provider_items:
            findings.append(
                Finding(path, f"missing Conda provider {library}: {package_name}")
            )
            continue
        if len(provider_items) > 1:
            findings.append(
                Finding(path, f"duplicate Conda provider {library}: {package_name}")
            )
            continue
        _, actual = _requirement(provider_items[0], {})
        if requirement is None and (
            actual.specifier or actual.extras or actual.marker or actual.url
        ):
            findings.append(
                Finding(
                    path,
                    f"unqualified constraint for Conda provider {library}: "
                    f"{actual}; registry declares acquisition through {package_name} "
                    "without a universal version floor",
                )
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
    project, optional, python = _project_requirements(root, config["runtime_extras"])
    libraries = _registry_libraries(root)
    project_metadata = _load_toml(root / "pyproject.toml")["project"]
    public_python_names = {
        canonicalize_name(Requirement(raw).name)
        for declarations in [
            project_metadata["dependencies"],
            *project_metadata.get("optional-dependencies", {}).values(),
        ]
        for raw in declarations
    }
    providers, provider_aliases = _provider_requirements(
        root, libraries, public_python_names
    )
    optional.update(
        {
            canonicalize_name(requirement.name): requirement
            for requirement in providers.values()
        }
    )
    runtime_names = set(project) | set(optional)
    conda_names = {
        canonicalize_name(conda): canonicalize_name(public)
        for public, conda in config["conda_names"].items()
    }
    if len(conda_names) != len(config["conda_names"]):
        raise ValueError("duplicate Conda name overrides")
    if provider_aliases.keys() & conda_names.keys() or (
        set(provider_aliases.values()) & set(conda_names.values())
    ):
        raise ValueError("provider Conda aliases must be derived from DepDigest only")
    conda_names.update(provider_aliases)
    if not set(conda_names.values()) <= runtime_names:
        raise ValueError("a Conda name override does not name a public dependency")
    if any(
        alias in runtime_names and alias != name for alias, name in conda_names.items()
    ):
        raise ValueError("a Conda name override shadows a different public dependency")
    findings: list[Finding] = []
    findings.extend(_registry_findings(libraries, set(project)))
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
            unknown_fields = set(entry) - {
                "path",
                "source_supplied",
                "optional_required",
                "conda_provider_required",
            }
            if unknown_fields:
                raise ValueError(
                    f"unknown environment inventory fields: {sorted(unknown_fields)}"
                )
            optional_names = entry.get("optional_required", [])
            if not isinstance(optional_names, list) or not all(
                isinstance(name, str) for name in optional_names
            ):
                raise ValueError(
                    "optional_required must be a list of public dependency names"
                )
            required_optional = {canonicalize_name(name) for name in optional_names}
            if len(required_optional) != len(optional_names):
                raise ValueError(
                    "optional_required declares a dependency more than once"
                )
            for name in sorted(required_optional - set(optional)):
                findings.append(
                    Finding(
                        path,
                        f"required optional dependency {name} is not in runtime extras",
                    )
                )
            conda, pip, channels = _environment_routes(root / path)
            findings.extend(
                _conda_provider_findings(
                    path,
                    entry.get("conda_provider_required", []),
                    libraries,
                    conda,
                    pip,
                    channels,
                    public_python_names,
                    providers,
                )
            )
            items = [*conda, *pip]
            observed, _ = _observed_requirements(items, runtime_names, conda_names)
            findings.extend(_compare_requirements(path, project, observed, supplied))
            selected_optional = {
                name: requirement
                for name, requirement in optional.items()
                if name in observed
                or name in required_optional
                or any(
                    canonicalize_name(providers[capability].name) == name
                    for capability in entry.get("conda_provider_required", [])
                    if capability in providers
                )
            }
            findings.extend(
                _compare_requirements(path, selected_optional, observed, set())
            )
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
