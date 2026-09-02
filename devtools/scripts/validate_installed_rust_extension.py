#!/usr/bin/env python
"""Validating an already installed MolSysMT Rust extension."""

from validate_installed_rust_wheel import validate_installed_extension


def main() -> int:
    """Running the installed private-extension contract."""

    result = validate_installed_extension()
    print(
        "MolSysMT installed Rust extension validation passed: "
        f"exports={result['exports']} | minimum_image={result['minimum_image']} | "
        f"extension={result['extension']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
