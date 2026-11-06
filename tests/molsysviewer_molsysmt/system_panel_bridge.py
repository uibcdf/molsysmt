"""Persistent real native authority for the local browser panel receiving gate."""

import json
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    sys.path.insert(0, str(ROOT))

    import molsysviewer as msv
    from molsysviewer.widget import MolSysViewerWidget

    import molsysmt as msm

    class ReceivingWidget(MolSysViewerWidget):
        def send(self, content, buffers=None):
            if buffers:
                raise RuntimeError(
                    "The JSON browser probe must not silently drop binary buffers."
                )
            messages.append(content)

    messages = []
    with msv.demo["1TCD"] as source:
        with msv.MolSysView(transport=ReceivingWidget()) as view:
            view.load(source.molsys)
            payload = next(
                m
                for m in view.build_popup_scene_snapshot("canvas")
                if m.get("op") == "load_molsys_payload"
            )
            view._ready = True
            messages.clear()
            view._sync_addons_runtime()
            print(
                json.dumps(
                    {
                        "id": 0,
                        "result": {
                            "payload": payload,
                            "messages": messages,
                            "n_atoms": view.molsys.get_n_atoms(),
                            "native_source": msm.__file__,
                        },
                    }
                ),
                flush=True,
            )
            for line in sys.stdin:
                request = json.loads(line)
                messages.clear()
                try:
                    for event in request.get("events", []):
                        view._handle_frontend_event(event)
                    if request.get("external_edit"):
                        view.addons.molsysmt.basic.remove(
                            selection=[0], in_place=True, update_view=False
                        )
                    print(
                        json.dumps(
                            {
                                "id": request["id"],
                                "result": {
                                    "messages": messages,
                                    "n_atoms": view.molsys.get_n_atoms(),
                                    "status": view.addons.molsysmt.get_sync_status(),
                                },
                            }
                        ),
                        flush=True,
                    )
                except Exception:
                    print(
                        json.dumps(
                            {"id": request["id"], "error": traceback.format_exc()}
                        ),
                        flush=True,
                    )


if __name__ == "__main__":
    main()
