from simtk.openmm import app


parameters_keywords_openmm={
        'non_bonded_method': 'nonbondedMethod',
        'non_bonded_cutoff': 'nonbondedCutoff',
        'constraints': 'constraints',
        'rigid_water': 'rigidWater',
        'remove_cm_motion': 'removeCMMotion',
        'hydrogen_mass': 'hydrogenMass',
        'residue_templates': 'residueTemplates',
        'ignore_external_bonds': 'ignoreExternalBonds',
        'switch_distance': 'switchDistance',
        'flexible_constraints': 'flexibleConstraints',
        'implicit_solvent': 'implicitSolvent'
        }

parameters_values_openmm={

        'non_bonded_method':{
            'no_cutoff': app.NoCutoff,
            'cutoff_non_periodic': app.CutoffNonPeriodic,
            'cutoff_periodic': app.CutoffPeriodic,
            'Ewald': app.Ewald,
            'PME': app.PME,
            'LJPME': app.LJPME
            },

        #'non_bonded_cutoff': distance quantity

        'constraints':{
            None: None,
            'h_bonds': app.HBonds,
            'all_bonds': app.AllBonds,
            'h_angles': app.HAngles
            },

        #'rigid_water': boolean

        #'remove_cm_motion': boolean

        #'hydrogen_mass': None or Quantity

        #'residue_templates': dict

        #'ignore_external_bonds': boolean

        #'switch_distance': float or Quantity

        #'flexible_constraints': boolean

        'implicit_solvent':{
            None: None,
            'HCT': app.HCT,
            'OBC1': app.OBC1,
            'OBC2': app.OBC2,
            'GBn': app.GBn,
            'GBn2': app.GBn2,
            },

        #'implicit_solvent_kappa': 0.0/unit.nanometers (default)

        #'solute_dielectric': 1.0 (default)

        #'solvent_dielectric': 78.5 (default)

        'constraints':{
            None: None,
            'h_bonds': app.HBonds,
            'all_bonds': app.AllBonds,
            'h_angles': app.HAngles,
            }
        }

def digest(engine, **kwargs):

    output={}

    if engine=='openmm':

        if kwargs['non_bonded_method']=='no_cutoff':
            if kwargs['non_bonded_cutoff'] is None:
                from simtk.unit import nanometers
                kwargs['non_bonded_cutoff']=1.0*nanometers

        for parameter, value in kwargs.items():
            if parameter in parameters_values_openmm:
                output[parameters_keywords_openmm[parameter]]=parameters_values_openmm[parameter][value]
            else:
                output[parameters_keywords_openmm[parameter]]=value

    else:

        raise NotImplementedError

    return output
