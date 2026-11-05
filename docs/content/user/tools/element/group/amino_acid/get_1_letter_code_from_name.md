(Tutorial_Get_1_letter_code_from_name)=
# Getting a one-letter group code

The public helper moved to
{func}`molsysmt.element.group.get_1_letter_code_from_name` before 1.0.
The former entry under `element.group.amino_acid` is removed.

Follow the {ref}`complete tutorial <Tutorial_Group_Name_Code>` for the standard
twenty amino acids, sequence ambiguity symbols, modified parents, context
refusal and native declarations. Use `naming_scheme='legacy'` explicitly when
you need the historical table. Names such as GLH and XLE require context;
the new helper does not reproduce the old implicit legacy interpretation.

See {ref}`user-foundations-group-naming-schemes` for the supported vocabularies,
their differences and bounded scientific coverage.
