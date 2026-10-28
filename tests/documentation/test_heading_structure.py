"""Include published semantic heading guarantees in normal pytest discovery."""

from devtools.tests.test_documentation_heading_structure import (
    build as build,
)
from devtools.tests.test_documentation_heading_structure import (
    test_documentation_ci_options_reject_real_sphinx_warning as test_documentation_ci_options_reject_real_sphinx_warning,
)
from devtools.tests.test_documentation_heading_structure import (
    test_heading_inventory_distinguishes_sections_and_examples as test_heading_inventory_distinguishes_sections_and_examples,
)
from devtools.tests.test_documentation_heading_structure import (
    test_home_has_one_semantic_title_and_preserved_section_names as test_home_has_one_semantic_title_and_preserved_section_names,
)
from devtools.tests.test_documentation_heading_structure import (
    test_home_render_keeps_brand_and_one_document_title as test_home_render_keeps_brand_and_one_document_title,
)
from devtools.tests.test_documentation_heading_structure import (
    test_published_markdown_has_continuous_heading_levels as test_published_markdown_has_continuous_heading_levels,
)
from devtools.tests.test_documentation_heading_structure import (
    test_published_markdown_labels_are_unambiguous as test_published_markdown_labels_are_unambiguous,
)
