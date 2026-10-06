"""Checking the active HTML fix, rather than a CSS token in scene data."""

import importlib.util
import json
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


class HeadScripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.active = False
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.in_head = True
        if tag == "script":
            attributes = dict(attrs)
            self.active = (
                self.in_head
                and not attributes.get("type")
                and not attributes.get("src")
            )

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        if tag == "script":
            self.active = False

    def handle_data(self, data):
        if self.active:
            self.scripts.append(data)


def _check_header(html):
    parser = HeadScripts()
    parser.feed(html.split("</head>", 1)[0] + "</head>")
    for script in parser.scripts:
        script = re.sub(r"//[^\n]*", "", script).strip()
        if not script.startswith("if (window.self !== window.top)"):
            continue
        assignment = re.search(
            r'sheet.textContent\s*=\s*("(?:[^"\\]|\\.)*")\s*;', script
        )
        if assignment is None:
            continue
        css = json.loads(assignment[1])
        if re.search(r"html\s*\{\s*color-scheme:\s*light dark;\s*\}", css):
            assert 'document.createElement("style")' in script
            assert "document.head.appendChild(sheet);" in script
            assert "html, body { background: transparent !important; }" in css
            return
    raise AssertionError("No active embedded-background correction before the body")


def test_all_transparent_exports_install_embedded_scheme_before_body():
    paths = sorted((REPO / "docs/_static/views").glob("*.html"))
    checked = 0
    for path in paths:
        html = path.read_text()
        ui = re.search(
            r'<script id="molsysviewer-ui"[^>]*>(.*?)</script>', html, re.DOTALL
        )
        if ui:
            assert json.loads(ui[1])["background_mode"] == "transparent", path
            _check_header(html)
            checked += 1
    assert checked > 0


@pytest.mark.parametrize("mutation", ["body", "inert", "comment", "missing_css"])
def test_inert_or_misplaced_background_fixes_are_rejected(mutation):
    sample = (REPO / "docs/_static/views/tools_build_build_peptide_1.html").read_text()
    head, body = sample.split("</head>", 1)
    script = re.search(r"<script>.*?</script>", head, re.DOTALL)[0]
    head = head.replace(script, "")
    if mutation == "body":
        body = script + body
    elif mutation == "inert":
        head += script.replace("<script>", '<script type="application/json">')
    elif mutation == "comment":
        head += "<!--" + script + "-->"
    else:
        head += script.replace("color-scheme: light dark;", "")
    with pytest.raises(AssertionError):
        _check_header(head + "</head>" + body)


def test_header_migration_preserves_every_body_byte_and_is_idempotent():
    path = REPO / "docs/generate_static_views/refresh_transparent_headers.py"
    spec = importlib.util.spec_from_file_location("refresh_transparent_headers", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original = (
        REPO / "docs/_static/views/tools_build_build_peptide_1.html"
    ).read_bytes()
    head, separator, body = original.partition(b"</head>")
    script = re.search(rb"<script>.*?</script>", head, re.DOTALL)[0]
    legacy_script = script.replace(b"html { color-scheme: light dark; } ", b"")
    old = head.replace(script, legacy_script) + separator + body
    result = module.refresh_header(old, script)
    assert result.partition(b"</head>")[2] == body
    _check_header(result.decode())
    assert module.refresh_header(result, script) == result
