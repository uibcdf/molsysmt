# =======================
# BUH
# =======================


"""
Solvate Box
==============

Methods and wrappers to create and solvate boxes

"""

def make_box(item, engine=None):
    pass

def solvate (item, geometry=None, water=None, anion=None, num_anions="neutralize",
             cation=None, num_cations="neutralize", forcefield=None, engine="LEaP"):
    """solvate(item, geometry=None, water=None, engine=None)

    Methods and wrappers to create and solvate boxes

    Parameters
    ----------

    anion: 'Cl-', 'Br-', 'F-', and 'I-'
    num_anions: number of cations to add. integer or "neutralize"
    cation: "NA"  'Cs+', 'K+', 'Li+', 'Na+', and 'Rb+'
    num_cations: number of cations to add. integer or "neutralize"

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

    if engine=="LEaP":

        from .multitool import convert as _convert
        from yank.utils import TLeap
        from .utils.miscellanea import tmp_filename

        if water=="tip3p":
            leaprc_parameters = ['oldff/leaprc.ff99SBildn', 'leaprc.water.tip3p']
            #leaprc_parameters = ['oldff/leaprc.ff99SBildn', 'leaprc.gaff']

        elif water=="spc":
            leaprc_parameters = ['oldff/leaprc.ff99SBildn', 'leaprc.water.spce']

        pdbfile_in = tmp_filename(".pdb")
        _convert(item, pdbfile_in)

        tleap = TLeap()
        tleap.load_parameters(*leaprc_parameters)
        tleap.load_unit(unit_name='MolecularSystem', file_path=pdbfile_in)
        tleap.solvate(unit_name='MolecularSystem', box_geometry="truncated_octahedral",
                      solvent_model='TIP3PBOX', clearance=14.0)

        if anions is not None:
            if anion== "CL":
                anion = "Cl-"
            if num_anions == "neutralize":
                num_anions = 0
            tleap.add_ions(unit_name='MolecularSystem', ion=anion, num_ions=0,
                           replace_solvent=True)

        if cations is not None:
            if anion== "NA":
                anion = "Na+"
            if num_anions == "neutralize":
                num_anions = 0
            tleap.add_ions(unit_name='MolecularSystem', ion=anion, num_ions=0,
                           replace_solvent=True)

        pdbfile_out = tmp_filename(".pdb")
        tleap.save_unit(unit_name='MolecularSystem', output_path=pdbfile_out)

        tleap.script()
        tleap.run()

        tmp_item = _convert(pdbfile_out)

        remove(pdbfile_in, pdbfile_out)

        return tmp_item

