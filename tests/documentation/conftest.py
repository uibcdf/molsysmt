"""Shared rendering controls for executable documentation examples."""

import io

import pytest


@pytest.fixture
def headless_plotting(monkeypatch):
    """Retain real notebook display calls and their rendered figure evidence."""
    pytest.importorskip("matplotlib")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg

    previous_backend = plt.get_backend()
    plt.switch_backend("Agg")
    original_show = plt.show
    rendered = []

    def render_show(*args, **kwargs):
        assert isinstance(plt.gcf().canvas, FigureCanvasAgg)
        image = io.BytesIO()
        plt.gcf().savefig(image, format="png")
        data = image.getvalue()
        assert data.startswith(b"\x89PNG\r\n\x1a\n")
        rendered.append(data)
        return original_show(*args, **kwargs)

    monkeypatch.setattr(plt, "show", render_show)
    with plt.ioff():
        try:
            yield rendered
        finally:
            plt.close("all")
            plt.switch_backend(previous_backend)
