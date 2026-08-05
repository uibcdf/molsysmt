import sys
from importlib.resources import files

def path(package, file):
    return files(package).joinpath(file)


class SystemsDict(dict):
    """Subclass of dict holding pre-packaged demo systems and category metadata."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = {}
        self.info = {}


systems = SystemsDict()

# -----------------------------------------------------------------------------
# Dipeptides & Small Peptides
# -----------------------------------------------------------------------------

systems['alanine dipeptide'] = {}
systems['alanine dipeptide']['alanine_dipeptide.h5msm'] = path('molsysmt.data.h5msm', 'alanine_dipeptide.h5msm')

systems['proline dipeptide'] = {}
systems['proline dipeptide']['proline_dipeptide.h5msm'] = path('molsysmt.data.h5msm', 'proline_dipeptide.h5msm')

systems['valine dipeptide'] = {}
systems['valine dipeptide']['valine_dipeptide.h5msm'] = path('molsysmt.data.h5msm', 'valine_dipeptide.h5msm')

systems['lysine dipeptide'] = {}
systems['lysine dipeptide']['lysine_dipeptide.h5msm'] = path('molsysmt.data.h5msm', 'lysine_dipeptide.h5msm')

systems['pentalanine'] = {}
systems['pentalanine']['pentalanine.inpcrd'] = path('molsysmt.data.inpcrd', 'pentalanine.inpcrd')
systems['pentalanine']['pentalanine.prmtop'] = path('molsysmt.data.prmtop', 'pentalanine.prmtop')
systems['pentalanine']['traj_pentalanine.h5'] = path('molsysmt.data.h5', 'traj_pentalanine.h5')
systems['pentalanine']['traj_pentalanine.h5msm'] = path('molsysmt.data.h5msm', 'traj_pentalanine.h5msm')

systems['Met-enkephalin'] = {}
systems['Met-enkephalin']['met_enkephalin.pdb'] = path('molsysmt.data.pdb', 'met_enkephalin.pdb')
systems['Met-enkephalin']['met_enkephalin.h5msm'] = path('molsysmt.data.h5msm', 'met_enkephalin.h5msm')


# -----------------------------------------------------------------------------
# Small & Globular Proteins
# -----------------------------------------------------------------------------

systems['Trp-Cage'] = {}
systems['Trp-Cage']['1l2y.pdb'] = path('molsysmt.data.pdb', '1l2y.pdb')
systems['Trp-Cage']['1l2y.bcif.gz'] = path('molsysmt.data.bcif_gz', '1l2y.bcif.gz')
systems['Trp-Cage']['1l2y.h5msm'] = path('molsysmt.data.h5msm', '1l2y.h5msm')

systems['chicken villin HP35'] = {}
systems['chicken villin HP35']['1vii.pdb'] = path('molsysmt.data.pdb', '1vii.pdb')
systems['chicken villin HP35']['1vii.bcif.gz'] = path('molsysmt.data.bcif_gz', '1vii.bcif.gz')
systems['chicken villin HP35']['1vii.bcif'] = path('molsysmt.data.bcif', '1vii.bcif')
systems['chicken villin HP35']['chicken_villin_HP35.h5msm'] = path('molsysmt.data.h5msm', 'chicken_villin_HP35.h5msm')
systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'] = path('molsysmt.data.h5msm', 'chicken_villin_HP35_solvated.h5msm')
systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd'] = path('molsysmt.data.dcd', 'traj_chicken_villin_HP35_solvated.dcd')
systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5'] = path('molsysmt.data.h5', 'traj_chicken_villin_HP35_solvated.h5')
systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5msm'] = path('molsysmt.data.h5msm', 'traj_chicken_villin_HP35_solvated.h5msm')

systems['T4 lysozyme L99A'] = {}
systems['T4 lysozyme L99A']['181l.pdb'] = path('molsysmt.data.pdb', '181l.pdb')
systems['T4 lysozyme L99A']['181l.bcif.gz'] = path('molsysmt.data.bcif_gz', '181l.bcif.gz')
systems['T4 lysozyme L99A']['181l.h5msm'] = path('molsysmt.data.h5msm', '181l.h5msm')
systems['T4 lysozyme L99A']['1l17.pdb'] = path('molsysmt.data.pdb', '1l17.pdb')
systems['T4 lysozyme L99A']['1l17.h5msm'] = path('molsysmt.data.h5msm', '1l17.h5msm')
systems['T4 lysozyme L99A']['t4_lysozyme_L99A.h5msm'] = path('molsysmt.data.h5msm', 't4_lysozyme_L99A.h5msm')

systems['TcTIM'] = {}
systems['TcTIM']['1tcd.pdb'] = path('molsysmt.data.pdb', '1tcd.pdb')
systems['TcTIM']['1tcd.bcif.gz'] = path('molsysmt.data.bcif_gz', '1tcd.bcif.gz')
systems['TcTIM']['1tcd.h5msm'] = path('molsysmt.data.h5msm', '1tcd.h5msm')

systems['Hexokinase 2'] = {}
systems['Hexokinase 2']['2nzt.bcif.gz'] = path('molsysmt.data.bcif_gz', '2nzt.bcif.gz')
systems['Hexokinase 2']['2nzt.h5msm'] = path('molsysmt.data.h5msm', '2nzt.h5msm')


# -----------------------------------------------------------------------------
# Complexes & Large Assemblies
# -----------------------------------------------------------------------------

systems['Barnase-Barstar'] = {}
systems['Barnase-Barstar']['barnase_barstar.h5msm'] = path('molsysmt.data.h5msm', 'barnase_barstar.h5msm')
systems['Barnase-Barstar']['1brs.bcif'] = path('molsysmt.data.bcif', '1brs.bcif')
systems['Barnase-Barstar']['1brs.bcif.gz'] = path('molsysmt.data.bcif_gz', '1brs.bcif.gz')
systems['Barnase-Barstar']['1brs.h5msm'] = path('molsysmt.data.h5msm', '1brs.h5msm')

systems['1YCR'] = {}
systems['1YCR']['1ycr.pdb'] = path('molsysmt.data.pdb', '1ycr.pdb')
systems['1YCR']['1ycr.bcif.gz'] = path('molsysmt.data.bcif_gz', '1ycr.bcif.gz')

systems['1ATP'] = {}
systems['1ATP']['1atp.pdb'] = path('molsysmt.data.pdb', '1atp.pdb')
systems['1ATP']['1atp.bcif.gz'] = path('molsysmt.data.bcif_gz', '1atp.bcif.gz')

systems['1CEN'] = {}
systems['1CEN']['1cen.pdb'] = path('molsysmt.data.pdb', '1cen.pdb')
systems['1CEN']['1cen.bcif.gz'] = path('molsysmt.data.bcif_gz', '1cen.bcif.gz')

systems['2HGR'] = {}
systems['2HGR']['2hgr.pdb'] = path('molsysmt.data.pdb', '2hgr.pdb')

systems['4V4Z'] = {}
systems['4V4Z']['4v4z.bcif.gz'] = path('molsysmt.data.bcif_gz', '4v4z.bcif.gz')
systems['4V4Z']['4v4z_openmm.pdb'] = path('molsysmt.data.pdb', '4v4z_openmm.pdb')


# -----------------------------------------------------------------------------
# Small Molecules & Ligands
# -----------------------------------------------------------------------------

systems['benzamidine'] = {}
systems['benzamidine']['benzamidine.pdb'] = path('molsysmt.data.pdb', 'benzamidine.pdb')

systems['caffeine'] = {}
systems['caffeine']['caffeine.mol2'] = path('molsysmt.data.mol2', 'caffeine.mol2')


# -----------------------------------------------------------------------------
# Lipids & Membranes
# -----------------------------------------------------------------------------

systems['POPC'] = {}
systems['POPC']['popc.crd'] = path('molsysmt.data.crd', 'popc.crd')
systems['POPC']['popc.psf'] = path('molsysmt.data.psf', 'popc.psf')

systems['POPC membrane'] = {}
systems['POPC membrane']['popc_membrane.psf'] = path('molsysmt.data.psf', 'popc_membrane.psf')
systems['POPC membrane']['popc_membrane.dcd'] = path('molsysmt.data.dcd', 'popc_membrane.dcd')


# -----------------------------------------------------------------------------
# Toy Models & Test Systems
# -----------------------------------------------------------------------------

systems['two LJ particles'] = {}
systems['two LJ particles']['traj_two_lj_particles.trjpk'] = path('molsysmt.data.trjpk', 'traj_two_lj_particles.trjpk')

systems['particles 4'] = {}
systems['particles 4']['traj_particles_4.xyznpy'] = path('molsysmt.data.xyznpy', 'traj_particles_4.xyznpy')

systems['nglview'] = {}
systems['nglview']['ala3.pdb'] = path('molsysmt.data.pdb', 'ala3.pdb')
systems['nglview']['md_1u19.gro'] = path('molsysmt.data.gro', 'md_1u19.gro')
systems['nglview']['md_1u19.pdb'] = path('molsysmt.data.pdb', 'md_1u19.pdb')
systems['nglview']['md_1u19.traj'] = path('molsysmt.data.traj', 'md_1u19.traj')
systems['nglview']['md_1u19.trr'] = path('molsysmt.data.trr', 'md_1u19.trr')
systems['nglview']['md_1u19.xtc'] = path('molsysmt.data.xtc', 'md_1u19.xtc')


# -----------------------------------------------------------------------------
# System Metadata & Categories Dictionary
# -----------------------------------------------------------------------------

systems.info = {
    'alanine dipeptide': {
        'category': 'Dipeptides & Small Peptides',
        'description': 'Alanine dipeptide (ACE-ALA-NME) benchmark system in H5MSM format.'
    },
    'proline dipeptide': {
        'category': 'Dipeptides & Small Peptides',
        'description': 'Proline dipeptide in H5MSM format.'
    },
    'valine dipeptide': {
        'category': 'Dipeptides & Small Peptides',
        'description': 'Valine dipeptide in H5MSM format.'
    },
    'lysine dipeptide': {
        'category': 'Dipeptides & Small Peptides',
        'description': 'Lysine dipeptide in H5MSM format.'
    },
    'pentalanine': {
        'category': 'Dipeptides & Small Peptides',
        'description': 'Pentalanine peptide in Amber prmtop/inpcrd and trajectory formats.'
    },
    'Met-enkephalin': {
        'category': 'Dipeptides & Small Peptides',
        'description': 'Pentapeptide neurotransmitter Met-enkephalin (PDB and H5MSM).'
    },
    'Trp-Cage': {
        'category': 'Small & Globular Proteins',
        'description': '20-residue synthetic mini-protein Trp-Cage TC5b (PDB 1L2Y).'
    },
    'chicken villin HP35': {
        'category': 'Small & Globular Proteins',
        'description': 'Villin headpiece subdomain HP35 (PDB 1VII), solvated structure and DCD trajectory.'
    },
    'T4 lysozyme L99A': {
        'category': 'Small & Globular Proteins',
        'description': 'T4 Lysozyme L99A mutant cavity system (PDB 181L, 1L17).'
    },
    'TcTIM': {
        'category': 'Small & Globular Proteins',
        'description': 'Trypanosoma cruzi Triosephosphate Isomerase (PDB 1TCD).'
    },
    'Hexokinase 2': {
        'category': 'Small & Globular Proteins',
        'description': 'Human Hexokinase 2 enzyme (PDB 2NZT).'
    },
    'Barnase-Barstar': {
        'category': 'Complexes & Assemblies',
        'description': 'Ribonuclease Barnase bound to inhibitor Barstar (PDB 1BRS).'
    },
    '1YCR': {
        'category': 'Complexes & Assemblies',
        'description': 'MDM2 bound to p53 transactivation domain peptide (PDB 1YCR).'
    },
    '1ATP': {
        'category': 'Complexes & Assemblies',
        'description': 'cAMP-dependent protein kinase catalytic subunit complex (PDB 1ATP).'
    },
    '1CEN': {
        'category': 'Complexes & Assemblies',
        'description': 'Centromere protein B DNA-binding domain (PDB 1CEN).'
    },
    '2HGR': {
        'category': 'Complexes & Assemblies',
        'description': 'Ribosome structural benchmark dataset (PDB 2HGR).'
    },
    '4V4Z': {
        'category': 'Complexes & Assemblies',
        'description': 'Thermus thermophilus 70S ribosome assembly (PDB 4V4Z, 149,640 atoms).'
    },
    'benzamidine': {
        'category': 'Small Molecules & Ligands',
        'description': 'Benzamidine aromatic ligand (PDB format).'
    },
    'caffeine': {
        'category': 'Small Molecules & Ligands',
        'description': 'Caffeine small molecule (MOL2 format).'
    },
    'POPC': {
        'category': 'Lipids & Membranes',
        'description': 'Single POPC lipid molecule (CHARMM PSF/CRD).'
    },
    'POPC membrane': {
        'category': 'Lipids & Membranes',
        'description': 'Hydrated POPC lipid bilayer membrane simulation trajectory (CHARMM PSF and DCD).'
    },
    'two LJ particles': {
        'category': 'Toy & Synthetic Models',
        'description': 'Two Lennard-Jones particles toy trajectory.'
    },
    'particles 4': {
        'category': 'Toy & Synthetic Models',
        'description': '4-particle spatial trajectory in XYZ NumPy format.'
    },
    'nglview': {
        'category': 'Toy & Synthetic Models',
        'description': 'Test files for NGLView and MDTraj integration (ala3, md_1u19 GRO/XTC/TRR).'
    }
}

# Group system names by category
categories = {}
for name, data in systems.info.items():
    cat = data['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(name)

systems.categories = categories
