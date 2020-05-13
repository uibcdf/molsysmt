# =======================
# Creando cajas solvatadas
# =======================

from simtk import unit
from os import remove

"""
Solvate Box
==============

Methods and wrappers to create and solvate boxes

"""

def solvate (item, box_geometry="truncated_octahedral", clearance=14.0*unit.angstroms, water='TIP3P',
             anion='Cl-', num_anions="neutralize", cation='Na+', num_cations="neutralize",
             add_hydrogens=False, forcefield='AMBER99SB-ILDN', engine="LEaP", to_form= None, verbose=False):
    """solvate(item, geometry=None, water=None, engine=None)

    Methods and wrappers to create and solvate boxes

    Parameters
    ----------

    anion: 'Cl-', 'Br-', 'F-', and 'I-'
    num_anions: number of cations to add. integer or "neutralize"
    cation: "NA"  'Cs+', 'K+', 'Li+', 'Na+', and 'Rb+'
    num_cations: number of cations to add. integer or "neutralize"
    box_geometry: "cubic" or "truncated_octahedral" (Default: "truncated_octahedral")

    Returns
    -------
    item : bla bla
        bla bla

    Examples
    --------

    See Also
    --------

    Notes
    -----
    """

    from .multitool import duplicate, convert, get
    from .utils.forms import digest_forms
    from copy import deepcopy

    tmp_item = duplicate(item)
    form_in, form_out = digest_forms(item)

    if num_anions=="neutralize" and num_cations=="neutralize":

        from .multitool import get
        charge = get(tmp_item, target="system", net_charge=True)

        num_anions = 0
        num_cations = 0

        if charge>0:
            num_cations=abs(charge)
        elif charge<0:
            num_anions=abs(charge)

        if verbose:
            print("Adding {} {} and {} {} to neutralize the box.".format(num_cations, cation,
                                                                         num_anions, anion))

    if add_hydrogens==True:

        from .remove_atoms import remove_hydrogens
        print("Hydrogens were removed. The engine building the box will protonate the system.")
        tmp_item = remove_hydrogens(tmp_item)

    if engine=="LEaP":

        from .multitool import convert as _convert
        from .multitool import get_form as _get_form
        from yank.utils import TLeap
        from .utils.miscellanea import tmp_filename
        from .utils.forcefields import switcher as ff_switcher

        leaprc_parameters = []
        leaprc_parameters.append(ff_switcher['LEaP']['AMBER99SB-ILDN'])
        #leaprc_parameters.append(ff_switcher['LEaP']['GAFF'])
        leaprc_parameters.append(ff_switcher['LEaP'][water])

        solvent_model=None
        if water=='SPC':
            solvent_model='SPCBOX'
        elif water=='TIP3P':
            solvent_model='TIP3PBOX'
        elif water =='TIP4P':
            solvent_model='TIP4PBOX'


        pdbfile_in = tmp_filename(".pdb")
        convert(tmp_item, to_form=pdbfile_in)

        tleap = TLeap()
        tleap.load_parameters(*leaprc_parameters)
        tleap.load_unit(unit_name='MolecularSystem', filepath=pdbfile_in)
        tleap.solvate(unit_name='MolecularSystem', solvent_model=solvent_model,
                      clearance=clearance, box_geometry=box_geometry)

        if abs(num_anions):
            tleap.add_ions(unit_name='MolecularSystem', ion=anion, num_ions=num_anions,
                           replace_solvent=True)

        if abs(num_cations):
            tleap.add_ions(unit_name='MolecularSystem', ion=cation, num_ions=num_cations,
                           replace_solvent=True)

        pdbfile_out = tmp_filename(".pdb")
        tleap.save_unit(unit_name='MolecularSystem', output_path=pdbfile_out)

        tleap.run()

        tmp_item = convert(pdbfile_out, to_form=form_in)

        remove(pdbfile_in)
        remove(pdbfile_out)

        return tmp_item

