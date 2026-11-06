"""Legacy list resolver sharing the public resource registry."""

from molsysmt._private.engines import arg_digest_engine
from molsysmt.molecular_mechanics.forcefields import (
    forcefields as forcefields,
)
from molsysmt.molecular_mechanics.forcefields import (
    implicit_solvent_models,
    switcher,
    water_models,
)


def digest_forcefield(forcefield, engine, implicit_solvent=None, water_model=None):

    from molsysmt._private.smonitor import ArgumentChoiceError

    forcefields_out = []

    if type(forcefield) not in [list, tuple]:
        forcefield = [forcefield]

    engine = arg_digest_engine(engine)

    for ff in forcefield:
        try:
            if implicit_solvent is not None:
                if implicit_solvent in implicit_solvent_models:
                    aux = switcher[engine][ff][implicit_solvent]
                    forcefields_out.extend(aux)
                else:
                    raise ArgumentChoiceError(
                        argument="implicit_solvent",
                        value=implicit_solvent,
                        choices=list(implicit_solvent_models.keys()),
                        caller="molsysmt._private.forcefield.digest_forcefield",
                    )
            elif water_model is not None:
                if water_model in water_models:
                    aux = switcher[engine][ff][water_model]
                    forcefields_out.extend(aux)
                else:
                    raise ArgumentChoiceError(
                        argument="water_model",
                        value=water_model,
                        choices=list(water_models.keys()),
                        caller="molsysmt._private.forcefield.digest_forcefield",
                    )
            else:
                aux = switcher[engine][ff]["vacuum"]
                forcefields_out.extend(aux)
        except Exception:
            raise NotImplementedError(
                "{} with implicit solvent {} or water model {} and {} needs to be implemented in MolSysMT".format(
                    ff, implicit_solvent, water_model, engine
                )
            )

    forcefields_out = list(set(forcefields_out))

    return forcefields_out
