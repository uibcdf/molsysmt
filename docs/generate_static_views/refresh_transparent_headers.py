"""Refreshing exported transparent headers without recomputing stored scenes.

Use this bounded migration for uibcdf/molsysmt#199. Normal scene generation
continues to use the other scripts in this directory and MolSysViewer's exporter.
The template must come from a current public ``view.export.html`` operation.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path


def refresh_header(data, script):
    """Insert the provider's embedded-background script before the body."""
    head, separator, body = data.partition(b"</head>")
    if not separator or b"</body>" not in body:
        raise ValueError("Expected a complete exported HTML document")
    if re.search(rb'"background_mode"\s*:\s*"transparent"', body) is None:
        raise ValueError("Only transparent MolSysViewer exports may be refreshed")
    if re.search(rb'sheet.textContent\s*=\s*"html \{ color-scheme: light dark;', head):
        return data
    # Replace the old embedded-background script, retaining all other head data.
    old = re.findall(rb"<script>.*?</script>", head, re.DOTALL)
    if len(old) != 1 or b"document.head.appendChild(sheet)" not in old[0]:
        raise ValueError("Expected exactly one legacy embedded-background script")
    return head.replace(old[0], script) + separator + body


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    args = parser.parse_args()
    head = args.template.read_bytes().partition(b"</head>")[0]
    scripts = re.findall(rb"<script>(.*?)</script>", head, re.DOTALL)
    if len(scripts) != 1 or b"color-scheme: light dark" not in scripts[0]:
        raise ValueError("Template lacks the provider's transparent-background fix")
    script = b"<script>" + scripts[0] + b"</script>"
    repo = Path(__file__).resolve().parents[2]
    records = []
    for path in sorted((repo / "docs/_static/views").glob("*.html")):
        before = path.read_bytes()
        if re.search(rb'"background_mode"\s*:\s*"transparent"', before) is None:
            continue
        after = refresh_header(before, script)
        body = before.partition(b"</head>")[2]
        assert after.partition(b"</head>")[2] == body
        if before != after:
            path.write_bytes(after)
        records.append(
            {
                "path": str(path.relative_to(repo)),
                "changed": before != after,
                "before_sha256": hashlib.sha256(before).hexdigest(),
                "after_sha256": hashlib.sha256(after).hexdigest(),
                "unchanged_body_sha256": hashlib.sha256(body).hexdigest(),
            }
        )
    args.evidence.write_text(
        json.dumps(
            {
                "template_sha256": hashlib.sha256(
                    args.template.read_bytes()
                ).hexdigest(),
                "exported_script_sha256": hashlib.sha256(script).hexdigest(),
                "views": records,
            },
            indent=2,
        )
        + "\n"
    )
    print(
        f"Refreshed {sum(r['changed'] for r in records)}/{len(records)} transparent exports"
    )


if __name__ == "__main__":
    main()
