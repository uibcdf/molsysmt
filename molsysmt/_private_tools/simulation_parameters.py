
def digest_simulation_parameters(engine, **kwargs):

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

