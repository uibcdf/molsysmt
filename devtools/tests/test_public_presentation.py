"""Protecting public capability claims and MolSysSuite positioning."""

import ast
import json
import re
import tomllib
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]


def _check_readme(text):
    symbols = json.loads(
        (REPO / "devtools/data/public_api_stability.json").read_text()
    )["symbols"]
    capabilities = text.split("## What is inside\n", 1)[1].split("\n## ", 1)[0]
    for bullet in re.split(r"\n(?=- )", capabilities.strip()):
        references = re.findall(r"`((?:msm|molsysmt)\.[\w.]+)`", bullet)
        # Natural-language names also count: omitting an API reference must not
        # make an experimental capability appear stable.
        for term, symbol in (
            (r"\bSASA\b", "molsysmt.physchem.get_sasa"),
            (r"\bRMSF\b", "molsysmt.structure.get_rmsf"),
            (r"secondary.structure", "molsysmt.structure.get_secondary_structure"),
            (r"native structure preparation", "molsysmt.build"),
        ):
            if re.search(term, bullet, re.IGNORECASE):
                references.append(symbol)
        for reference in references:
            reference = reference.replace("msm.", "molsysmt.", 1)
            relevant = [
                entry
                for name, entry in symbols.items()
                if name == reference or name.startswith(reference + ".")
            ]
            if any(entry["stability"] == "experimental" for entry in relevant):
                assert re.search(r"\bexperimental\b", bullet, re.IGNORECASE), bullet

    for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text):
        url = urlsplit(target)
        if not url.scheme and not url.netloc and url.path:
            assert (REPO / unquote(url.path)).is_file(), target


def test_readme_capability_claims_match_stability_and_links():
    _check_readme((REPO / "README.md").read_text())


@pytest.mark.parametrize(
    "label", ["Experimental native structure preparation", "Experimental analysis"]
)
def test_unqualified_experimental_claims_are_rejected(label):
    text = (REPO / "README.md").read_text()
    assert label in text
    replacement = label.replace("Experimental ", "")
    if label == "Experimental analysis":
        text = text.replace("experimental API contract", "API contract")
    with pytest.raises(AssertionError):
        _check_readme(text.replace(label, replacement))


def test_a_broken_readme_local_link_is_rejected():
    text = (REPO / "README.md").read_text()
    with pytest.raises(AssertionError, match="CONTRIBUTORS"):
        _check_readme(text + "\n[Contributors](CONTRIBUTORS.md)\n")


def _check_role(text):
    # Require the molecular-library role in the sentence naming the ecosystem;
    # a badge, an unrelated footer, or a mention of another suite member is not it.
    sentences = re.split(r"(?<=[.!?])\s+", " ".join(text.split()))
    assert any(
        "MolSysSuite" in sentence
        and re.search(r"\bcore\b", sentence, re.IGNORECASE)
        and re.search(r"\blibrary\b", sentence, re.IGNORECASE)
        and re.search(r"\bmolecular(?:-system| systems)?\b", sentence, re.IGNORECASE)
        for sentence in sentences
    ), text


def test_public_surfaces_state_the_core_molecular_library_role():
    readme = (REPO / "README.md").read_text()
    opening = readme.split("---\n", 1)[1].split("## Why MolSysMT?", 1)[0]
    notebook = json.loads((REPO / "docs/index.ipynb").read_text())
    landing = "".join(notebook["cells"][1]["source"]).split("## Install it", 1)[0]
    metadata = tomllib.loads((REPO / "pyproject.toml").read_text())
    citation = yaml.safe_load((REPO / "CITATION.cff").read_text())
    for text in (
        opening,
        landing,
        metadata["project"]["description"],
        citation["abstract"],
    ):
        _check_role(text)


def test_a_suite_badge_or_unrelated_footer_does_not_supply_the_role():
    with pytest.raises(AssertionError):
        _check_role("MolSysMT is a molecular library. MolSysSuite has core tools.")


def test_the_native_hero_selects_native_engines_and_bundled_input():
    code = re.search(
        r"```python\n(.*?)```", (REPO / "README.md").read_text(), re.DOTALL
    )[1]
    tree = ast.parse(code)
    build_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Attribute)
        and node.func.value.attr == "build"
    ]
    assert len(build_calls) == 3
    assert all(
        any(
            keyword.arg == "engine"
            and isinstance(keyword.value, ast.Constant)
            and keyword.value.value == "MolSysMT"
            for keyword in call.keywords
        )
        for call in build_calls
    )
    assert "msm.systems[" in code
