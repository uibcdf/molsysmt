Getting a one-letter group code
===============================

The former amino-acid entry point was removed before 1.0. Use
:func:`molsysmt.element.group.get_1_letter_code_from_name` instead. Context-dependent
names require an explicit ``naming_scheme``. Historical parent-table values are
available through ``naming_scheme='legacy'``; there is no implicit legacy alias.

See :ref:`Tutorial_Group_Name_Code` for executable examples.
