"""Executable contract for the Four Paths course structure."""

from devtools.scripts import validate_course


def test_common_core_identity_and_numbering_are_fully_consolidated():
    assert validate_course.SECTIONS["Common_Core"] == ("core", range(1, 21))
    assert validate_course.main() == 0
