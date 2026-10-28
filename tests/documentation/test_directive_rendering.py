"""Include real-source directive rendering in normal pytest discovery."""

from devtools.tests.test_documentation_directive_rendering import (
    build as build,
)
from devtools.tests.test_documentation_directive_rendering import (
    test_all_standard_dropdowns_keep_contents_and_links as test_all_standard_dropdowns_keep_contents_and_links,
)
from devtools.tests.test_documentation_directive_rendering import (
    test_citation_panels_keep_text_doi_and_bibliography_download as test_citation_panels_keep_text_doi_and_bibliography_download,
)
from devtools.tests.test_documentation_directive_rendering import (
    test_dropdown_inventory_distinguishes_directives_from_code_examples as test_dropdown_inventory_distinguishes_directives_from_code_examples,
)
from devtools.tests.test_documentation_directive_rendering import (
    test_supported_forms_notice_keeps_body_and_live_portal_link as test_supported_forms_notice_keeps_body_and_live_portal_link,
)
from devtools.tests.test_documentation_directive_rendering import (
    test_topology_dropdowns_keep_tutorial_bodies_and_reference_lists as test_topology_dropdowns_keep_tutorial_bodies_and_reference_lists,
)
