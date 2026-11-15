"""Receive the real footer through Sphinx at the site root and a nested page."""

import shutil
from html.parser import HTMLParser
from io import StringIO
from pathlib import Path
from urllib.parse import urlsplit

import pytest


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.href = None
        self.text = ""
        self.links = []

    def handle_starttag(self, tag, attributes):
        if tag == "a":
            self.href = dict(attributes).get("href")
            self.text = ""

    def handle_data(self, data):
        if self.href is not None:
            self.text += data

    def handle_endtag(self, tag):
        if tag == "a":
            self.links.append((self.href, self.text))
            self.href = None


def test_actual_footer_resolves_authors_from_root_and_nested_pages(tmp_path):
    pytest.importorskip("pydata_sphinx_theme")
    from sphinx.application import Sphinx

    source = tmp_path / "source"
    templates = source / "_templates"
    templates.mkdir(parents=True)
    root = Path(__file__).resolve().parents[2]
    shutil.copy2(root / "docs/_templates/copyright.html", templates / "copyright.html")
    (source / "content/about").mkdir(parents=True)
    (source / "nested").mkdir()
    (source / "conf.py").write_text(
        "project = 'Footer receiving'\n"
        "html_theme = 'pydata_sphinx_theme'\n"
        "templates_path = ['_templates']\n"
    )
    (source / "index.rst").write_text(
        "Receiving\n=========\n\n.. toctree::\n\n   nested/lesson\n   content/about/who\n"
    )
    (source / "nested/lesson.rst").write_text("Lesson\n======\n")
    (source / "content/about/who.rst").write_text("Authors\n=======\n")
    output = tmp_path / "html"
    warnings = StringIO()
    app = Sphinx(
        str(source),
        str(source),
        str(output),
        str(tmp_path / "doctrees"),
        "html",
        status=StringIO(),
        warning=warnings,
        warningiserror=True,
        freshenv=True,
    )
    app.build(force_all=True)
    assert app.statuscode == 0, warnings.getvalue()
    for name in ("index.html", "nested/lesson.html"):
        page = output / name
        parser = Links()
        parser.feed(page.read_text())
        links = [href for href, text in parser.links if "and contributors" in text]
        assert len(links) == 1
        url = urlsplit(links[0])
        assert not url.scheme and not url.netloc and not url.path.startswith("/")
        target = (page.parent / url.path).resolve()
        assert target.is_relative_to(output.resolve())
        assert target == (output / "content/about/who.html").resolve()
        assert target.is_file()
