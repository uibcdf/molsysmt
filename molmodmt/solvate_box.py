# =======================
# BUH
# =======================

from simtk import unit

"""
Solvate Box
==============

Methods and wrappers to create and solvate boxes

"""

def make_box(item, engine=None):
    pass

def solvate (item, box_geometry="truncated_octahedral", clearance=14.0*unit.angstroms, water='TIP3P',
             anion='Cl-', num_anions="neutralize", cation='Na+', num_cations="neutralize",
             forcefield='AMBER99SB-ILDN', engine="LEaP"):
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

    if num_anions=="neutralize" and num_cations=="neutralize":

        from .multitool import get as _get
        charge = _get(item, charge=True)

        num_anions = 0
        num_cations = 0

        if charge>0:
            num_cations=abs(charge)
        elif charge<0:
            num_anions=abs(charge)

    if engine=="LEaP":

        from .multitool import convert as _convert
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
        _convert(item, pdbfile_in)

        tleap = TLeap()
        tleap.load_parameters(*leaprc_parameters)
        tleap.load_unit(unit_name='MolecularSystem', file_path=pdbfile_in)
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

        tmp_item = _convert(pdbfile_out)

        remove(pdbfile_in, pdbfile_out)

        return tmp_item

