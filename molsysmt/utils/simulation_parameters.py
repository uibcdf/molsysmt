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
        'implicit_solvent': 'implicitSolvent',
        'implicit_solvent_salt_conc': 'implicitSolventSaltConc',
        'implicit_solvent_kappa': 'implicitSolventKappa',
        'solute_dielectric': 'soluteDielectric',
        'solvent_dielectric': 'solventDielectric',
        'use_dispersion_correction': 'useDispersionCorrection',
        'ewald_error_tolerance': 'ewaldErrorTolerance',
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

        #'implicit_solvent_salt_conc': 0.0 * unit.mole/unit.liter (default),

        #'implicit_solvent_kappa': None or 0.0/unit.nanometers (default)

        #'solute_dielectric': 1.0 (default)

        #'solvent_dielectric': 78.5 (default)

        'constraints':{
            None: None,
            'h_bonds': app.HBonds,
            'all_bonds': app.AllBonds,
            'h_angles': app.HAngles,
            }
        }


parameters_keywords_leap={
        }

parameters_values_leap={

        }



def digest(engine, **kwargs):

    output={}

    if engine=='OpenMM':

        if kwargs['non_bonded_method']=='no_cutoff':
            if kwargs['non_bonded_cutoff'] is None:
                from simtk.unit import nanometers
                kwargs['non_bonded_cutoff']=1.0*nanometers # I have to check this. The value should be None

        for parameter, value in kwargs.items():
            try:
                if parameter in parameters_values_openmm:
                    output[parameters_keywords_openmm[parameter]]=parameters_values_openmm[parameter][value]
                else:
                    output[parameters_keywords_openmm[parameter]]=value
            except:
                raise NotImplementedError("{} parameter not implemented in molsysmt.utils.simulation_parameters".format(parameter))

    elif engine=='LEaP':

        for parameter, value in kwargs.items():
            if parameter in parameters_values_leap:
                output[parameters_keywords_leap[parameter]]=parameters_values_leap[parameter][value]
            else:
                output[parameters_keywords_leap[parameter]]=value

    else:

        raise NotImplementedError

    return output
