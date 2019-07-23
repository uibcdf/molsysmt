.. currentmodule:: molmodmt

####################
Source Documentation
####################

Native item
-----------

Description of MolModMT's classes.

.. autosummary::
    :toctree: generated/

    MolMod


Items transformation
--------------------

Basic methods to deal with molecular models.

.. autosummary::
    :toctree: generated/

    load
    get_form
    info
    select
    convert
    extract
    merge
    view

Items manipulation
------------------

.. autosummary::
    :toctree: generated/

    set
    remove
    remove_solvent
    protonation.add_missing_hydrogens
    recenter
    fix_chains

Observables
-----------

Methods to get molecular models' attributes or simple observables.

.. autosummary::
    :toctree: generated/

    get
    distances
    contact_map
    neighbors_lists
    center_of_mass
    geometrical_center
    radius_of_gyration

Structural and Topological items comparison
-------------------------------------------

.. autosummary::
    :toctree: generated/

    rmsd
    least_rmsd_fit
    sequence_identity
    sequence_alignment
    structure_alignment 

Modeling
--------

Methods to molecular modeling.

.. autosummary::
    :toctree: generated/

    add_loop
