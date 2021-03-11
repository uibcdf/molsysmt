from molsysmt._private_tools.exceptions import *

def has_hydrogens(molecular_system):

    from molsysmt.multitool import get

    n_hydrogens = get(molecular_system, target='atom', selection='atom_type=="H"', n_atoms=True)

    return n_hydrogens

def add_missing_hydrogens(molecular_system, pH=7.4, forcefield='AMBER99SB-ILDN', engine='OpenMM', verbose=False):

    """add_missing_hydrogens(item, pH=7.4, forcefield='AMBER99SB-ILDN', engine='OpenMM', verbose=False)

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
    verbose: bool, default: False
        The method prints out useful information if verbose=`True`.

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


    from molsysmt.multitool import convert, get_form
    from molsysmt._private_tools._digestion import digest_engine

    form = get_form(molecular_system)
    engine = digest_engine(engine)

    if engine=="OpenMM":

        tmp_item = convert(molecular_system, to_form="openmm.Modeller")
        log_residues_changed = tmp_item.addHydrogens(pH=pH)

        if verbose:
            print('Missing hydrogens added.')
            ii = 0
            for residue in item.topology.residues():
                if log_residues_changed[ii] is not None:
                    print('{}-{} to {}-{}'.format(residue.name, residue.index,
                                                   log_residues_changed[ii], residue.index))
                ii+=1

    elif engine=='PDBFixer':

        tmp_item = convert(molecular_system, to_form="pdbfixer.PDBFixer")
        tmp_item.addMissingHydrogens(pH=pH)

        if verbose:
            print('Missing hydrogens added (PDBFixer gives no details).')

    else:

        raise NotImplementedError

    tmp_item = convert(tmp_item, to_form=form)

    return tmp_item

