"""Render the course's existing key-takeaway blocks as standard admonitions."""

from docutils.parsers.rst.directives.admonitions import Admonition


class KeyTakeaway(Admonition):
    """Use a default title while retaining Docutils content and option handling."""

    required_arguments = 0
    optional_arguments = 1

    def run(self):
        self.arguments = self.arguments or ["Key takeaway"]
        return super().run()


def setup(app):
    app.add_directive("key-takeaway", KeyTakeaway)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
