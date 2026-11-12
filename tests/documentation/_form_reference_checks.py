"""Shared source and rendered-reference checks for reviewed native tutorials."""

import ast
import importlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
PAGES = Path("docs/content/user/tools/form/class/molsysmt")
_OPERATIONS = {
    "MolSys": {
        "__init__",
        "extract",
        "copy",
        "add",
        "merge",
        "append_structures",
        "add_bonds",
        "remove_bonds",
        "get_topological_attributes",
        "get_structural_attributes",
        "get_mechanical_attributes",
        "set",
        "iterators",
        "has_attribute",
        "is_form",
    },
    "Topology": {
        "__init__",
        "extract",
        "copy",
        "add",
        "merge",
        "append_structures",
        "get_topological_attributes",
        "get_structural_attributes",
        "set",
        "iterators",
        "has_attribute",
        "is_form",
    },
    "Structures": {
        "__init__",
        "extract",
        "copy",
        "add",
        "merge",
        "append_structures",
        "get_topological_attributes",
        "get_structural_attributes",
        "set",
        "iterators",
        "has_attribute",
        "is_form",
    },
}


def _assert_native_form_reference_contract(name):
    page = ROOT / PAGES / f"molsysmt_{name}.ipynb"
    notebook = json.loads(page.read_text())
    source = "\n".join("".join(cell["source"]) for cell in notebook["cells"])
    adapter = importlib.import_module(f"molsysmt.form.molsysmt_{name}")
    directory = Path(f"molsysmt/form/molsysmt_{name}")
    expected = {directory / f"{item}.py" for item in _OPERATIONS[name]}
    expected.update(
        directory / f"{value if isinstance(value, str) else value.__name__}.py"
        for value in adapter._convert_to.values()
    )
    conversions = "".join(notebook["cells"][4]["source"])
    assert set(re.findall(r"^\| `([^`]+)` \|", conversions, re.M)) == set(
        adapter._convert_to
    )
    assert re.findall(
        r"\*\*(\d+) registered direct conversion routes\*\*", conversions
    ) == [str(len(adapter._convert_to))]
    links = re.findall(r"\]\((https://github.com/uibcdf/molsysmt/blob/[^)]+)\)", source)
    observed = set()
    for url in links:
        parsed = urlsplit(url)
        parts = parsed.path.split("/")
        assert re.fullmatch(r"[a-f0-9]{40}", parts[4])
        path = Path(*parts[5:])
        assert path in expected and (ROOT / path).is_file()
        line = re.fullmatch(r"L([1-9][0-9]*)", parsed.fragment)
        assert line is not None
        lineno = int(line[1])
        assert lineno <= len((ROOT / path).read_text().splitlines())
        if lineno > 1:
            definitions = [
                node
                for node in ast.parse((ROOT / path).read_text()).body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.lineno == lineno
            ]
            assert len(definitions) == 1 and definitions[0].name == path.stem
            module = importlib.import_module(".".join(path.with_suffix("").parts))
            assert callable(getattr(module, definitions[0].name))
        observed.add(path)
    assert observed == expected
    assert not re.search(
        rf"\{{(?:func|mod)\}}`~?molsysmt\.form\.molsysmt_{name}", source
    )
    return {
        "name": name,
        "page": page,
        "links": links,
        "source_files": expected,
        "operations": len(_OPERATIONS[name]) - 1,
        "converters": len(adapter._convert_to),
    }


def _assert_rendered_native_form_references(html_root, name):
    from bs4 import BeautifulSoup

    contract = _assert_native_form_reference_contract(name)
    html_root = Path(html_root).resolve()
    page = (
        html_root / "content/user/tools/form/class/molsysmt" / f"molsysmt_{name}.html"
    )
    soup = BeautifulSoup(page.read_text(), "html.parser")
    article = soup.select_one("article.bd-article")
    assert article is not None
    hrefs = [node["href"] for node in article.find_all("a", href=True)]
    expected = set(contract["links"])
    assert expected and expected <= set(hrefs), expected - set(hrefs)
    assert sum(href in expected for href in hrefs) == len(contract["links"])
    assert all(
        node.find_parent("a") is not None for node in article.select("code.xref")
    )
    tables = article.find_all("table")
    assert len(tables[1].find_all("a", href=True)) == contract["operations"]
    assert len(tables[2].find_all("a", href=True)) == contract["converters"]
    local = set()
    for href in hrefs:
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc:
            continue
        target = (page.parent / unquote(parsed.path)).resolve() if parsed.path else page
        if target.is_dir():
            target /= "index.html"
        assert target.is_relative_to(html_root) and target.is_file(), href
        if parsed.fragment:
            target_soup = (
                soup
                if target == page
                else BeautifulSoup(target.read_text(), "html.parser")
            )
            fragment = unquote(parsed.fragment)
            assert target_soup.find(id=fragment) or target_soup.find(
                "a", attrs={"name": fragment}
            ), href
        local.add((str(target.relative_to(html_root)), parsed.fragment))
    return {
        "name": name,
        "expected_reference_occurrences": len(contract["links"]),
        "unique_source_destinations": len(expected),
        "operations": contract["operations"],
        "converters": contract["converters"],
        "local_destinations": len(local),
        "no_unlinked_python_roles": True,
    }
