from molsysmt._private.digestion import digest

@digest()
def add_missing_hydrogens(molecular_system, pH=7.4, forcefield='AMBER99SB-ILDN', engine='OpenMM'):

    """
    To be written soon...

    The missing hydrogens of a molecular model are added. This method does not remove any hydrogen
    already present.
    Regarding the protonation states of the aminoacids the documentation corresponding to the
    chosen engine should be checked for further details.
    - OpenMM: The protonation state is determined according the frequency of the variant at the specified pH, and the participation of Cysteines in disulfide bonds or Histidines in hydrogen bonds. This engine needs the specification of a forcefield. See the `OpenMM User Manual <http://docs.openmm.org/7.0.0/userguide/application.html#adding-hydrogens>`_ or the `OpenMM Api Guide <http://docs.openmm.org/development/api-python/generated/simtk.openmm.app.modeller.Modeller.html#simtk.openmm.app.modeller.Modeller.addHydrogens>`_.
    - PDBFixer: The protonation state is determined according to the frequency of the variant at the specified pH. See the `PDBFixer Manual <http://htmlpreview.github.io/?https://raw.github.com/pandegroup/pdbfixer/master/Manual.html>`_.
    Parameters
    ----------
    item: Molecular model in accepted form.
        Molecular model in any of the accepted forms by MolSysMT.
    pH: float, default: 7.4
        The pH based on which to determine the aminoacids protonation states.
    forcefield: str, default: 'AMBER99SB-ILDN'
        Name of the forcefield to be used by OpenMM ([check the list of names accepted here]())
    engine: str ('OpenMM' or 'PDBFixer'), default: 'OpenMM'
        Name of the engine used to add the missing hydrogens. The following options are available:
            - 'OpenMM': The method openmm.app.modeller.Modeller.addHydrogens is included in the
              workflow. See the `OpenMM User Manual
              <http://docs.openmm.org/7.0.0/userguide/application.html#adding-hydrogens>`_ or the
              `OpenMM Api Guide
              <http://docs.openmm.org/development/api-python/generated/simtk.openmm.app.modeller.Modeller.html#simtk.openmm.app.modeller.Modeller.addHydrogens>`_.
            - 'PDBFixer': The method pdbfixer.PDBFixer.addMissingHydrogens() is included in the workflow. See the `PDBFixer Manual <http://htmlpreview.github.io/?https://raw.github.com/pandegroup/pdbfixer/master/Manual.html>`_.
    Returns
    -------
    item : Molecular model in the same form as input `item`.
        A new molecular model with the missing hydrogens
        added is returned. The form will be the same as the input model.
    Examples
    --------
    See Also
    --------
    Notes
    -----
    """

    from molsysmt.basic import convert, get_form

    output_molecular_system = None
    form_in = get_form(molecular_system)
    form_out = form_in

    if engine=="OpenMM":

        temp_molecular_system = convert(molecular_system, to_form="openmm.Modeller")
        log_residues_changed = temp_molecular_system.addHydrogens(pH=pH)

    elif engine=='PDBFixer':

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer")
        temp_molecular_system.addMissingHydrogens(pH=pH)

    else:

        raise NotImplementedError

    output_molecular_system = convert(temp_molecular_system, to_form=form_out)

    return output_molecular_system

