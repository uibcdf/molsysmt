"""Receive explicit adjacent form/lifecycle articles in actual compiled HTML."""

import json
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest
from bs4 import BeautifulSoup

from tests.documentation._form_reference_checks import (
    _EXTERNAL_CLASS_OPERATIONS,
    _FILE_OPERATIONS,
    _OPERATIONS,
    _STRING_OPERATIONS,
    ROOT,
    _assert_native_form_reference_contract,
)

PAGES = (
    "user/tools/form/class/molsysmt/molsysmt_H5MSMFileHandler.ipynb",
    "user/tools/form/class/molsysmt/molsysmt_PDBFileHandler.ipynb",
    "user/tools/form/close.ipynb",
    "user/tools/form/get_attributes.ipynb",
    "user/tools/form/has_attribute.ipynb",
    "user/tools/form/is_file.ipynb",
    "user/tools/form/is_item.ipynb",
    "user/tools/form/is_string.ipynb",
    "user/tools/form/file/file_pdb_gz.ipynb",
    "user/tools/basic/copy.ipynb",
    "user/tools/basic/extract.ipynb",
    "user/cookbook/form_teleportation.ipynb",
    "user/foundations/governance/public_api_and_lifecycle.md",
    "course/Common_Core/18_Extracting_and_Removing_Elements.ipynb",
)


def test_every_form_tutorial_has_an_explicit_receiving_owner():
    reviewed = {
        _assert_native_form_reference_contract(name)["page"]
        for name in (
            *_OPERATIONS,
            *_FILE_OPERATIONS,
            *_STRING_OPERATIONS,
            *_EXTERNAL_CLASS_OPERATIONS,
        )
    }
    auxiliary = {
        ROOT / "docs/content" / name
        for name in PAGES
        if name.startswith("user/tools/form/")
    }
    assert not reviewed & auxiliary
    actual = set((ROOT / "docs/content/user/tools/form").rglob("*.ipynb"))
    assert reviewed | auxiliary == actual


@pytest.mark.parametrize("name", PAGES)
def test_reviewed_auxiliary_article_delivers_intended_references(name):
    directory = os.environ.get("MOLSYSMT_FORM_REFERENCE_HTML")
    assert directory, "Select the actual received HTML directory explicitly."
    html = Path(directory).resolve()
    source = ROOT / "docs/content" / name
    if source.suffix == ".ipynb":
        notebook = json.loads(source.read_text())
        text = "\n".join(
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "markdown"
        )
    else:
        text = source.read_text()
    page = html / "content" / Path(name).with_suffix(".html")
    soup = BeautifulSoup(page.read_text(), "html.parser")
    article = soup.select_one("article.bd-article")
    assert article is not None
    intended = re.findall(r"\{(?:func|class|mod|meth)\}`([^`]+)`", text)
    roles = article.select("code.xref")
    assert len(roles) == len(intended) and all(
        node.find_parent("a") is not None for node in roles
    )
    hrefs = [node["href"] for node in article.find_all("a", href=True)]
    section_roles = re.findall(r"\{ref\}`([^`]+)`", text)
    section_nodes = article.select("span.std-ref")
    assert len(section_nodes) == len(section_roles) and all(
        node.find_parent("a") is not None for node in section_nodes
    )
    explicit = re.findall(
        r"\]\((https://github.com/uibcdf/molsysmt/blob/[^)]+)\)", text
    )
    for href in explicit:
        assert href in hrefs
        parts = urlsplit(href).path.split("/")
        assert (ROOT / Path(*parts[5:])).is_file(), href
    assert intended or explicit or section_roles
    for href in hrefs:
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc:
            continue
        target = (page.parent / unquote(parsed.path)).resolve() if parsed.path else page
        if target.is_dir():
            target /= "index.html"
        assert target.is_relative_to(html) and target.is_file(), href
        if parsed.fragment:
            dom = (
                soup
                if target == page
                else BeautifulSoup(target.read_text(), "html.parser")
            )
            assert dom.find(id=unquote(parsed.fragment)) or dom.find(
                "a", attrs={"name": unquote(parsed.fragment)}
            ), href
