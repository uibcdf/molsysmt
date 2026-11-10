"""Receive the native prefix of the continuous real-host scientific session."""

from tests.molsysviewer_molsysmt.continuous_session_fixture import ContinuousSession


def test_native_composition_edit_and_correspondence_prefix(tmp_path):
    session = ContinuousSession(tmp_path)
    try:
        view = session.start()
        view.addons.molsysmt.basic.remove(selection=session.removed, in_place=True)
        session.after_remove()
        assert [r["phase"] for r in session.checks] == [
            "composed",
            "removed_and_copied",
        ]
    finally:
        session.close()
