from molsysmt._private.exceptions import ArgumentError

def digest_molecular_mechanics(molecular_mechanics, caller=None):

    if isinstance(molecular_mechanics, dict):
        from molsysmt.form.molsysmt_MolecularMechanicsDict import is_molsysmt_MolecularMechanicsDict
        if is_molsysmt_MolecularMechanicsDict(molecular_mechanics):
            return molecular_mechanics

    raise ArgumentError('molecular_mechanics', value=molecular_mechanics, caller=caller, message=None)
