"""Construct chemical reference templates from explicitly selected CCD resources."""

from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.chemical_reference import DIGEST_OPTIONS


@signal(tags=["api", "physchem", "preparation"])
@arg_digest(**DIGEST_OPTIONS)
@dep_digest("rdkit", when={"method": "ccd_canonical_descriptor"})
def get_chemical_template(
    component_id,
    source,
    method="ccd_canonical_descriptor",
    hydrogen_policy="stored_counts",
    descriptor_program="CACTVS",
    max_matches=4096,
    skip_digestion=False,
):
    """Constructing a coordinate-free chemical template from one CCD reference.

    Parameters
    ----------
    component_id : str
        CCD component identifier, interpreted case-insensitively. This is a
        reference label, not a MolSysMT component index or state selection.
    source : str, pathlib.Path or bytes
        Required source authority. 'rcsb' explicitly downloads one component.
        A path selects a local component/catalogue CIF, optionally gzip-compressed,
        or a directory containing one matching component file. Bytes supply an
        exact caller definition. Offline misses never trigger online fallback.
    method : {'ccd_canonical_descriptor', 'ccd_tables'}, default='ccd_canonical_descriptor'
        Canonical-descriptor interpretation uses optional RDKit to validate CCD
        graph/charge/aromatic/H declarations and transfer consensus chemistry
        from the selected canonical SMILES. ccd_tables projects declarations
        without RDKit and keeps unsupported or missing fields unknown.
    hydrogen_policy : {'stored_counts', 'explicit_atoms'}, default='stored_counts'
        Store H as heavy-atom counts or retain indexed CCD H atoms. Count
        projection refuses isotopic, isolated or nonordinary H that cannot be
        represented without information loss. No H coordinates are generated.
    descriptor_program : str, default='CACTVS'
        Exact source program for SMILES_CANONICAL. Missing/ambiguous descriptors
        remain explicit; another program is never substituted automatically.
    max_matches : int, default=4096
        Maximum complete descriptor/CCD graph correspondences. Exceeding this
        bound raises rather than certifying a truncated assignment consensus.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion and validation.

    Returns
    -------
    dict
        Coordinate-free native MolSys under template, independent JSON-compatible
        template_provenance and a molsysmt.chemical_reference_template@1 report.
        It retains source bytes/digests, original atom/bond names and row axes,
        projection maps, chosen policy, actual software and detached attribution.
        The report is also archived in ChemicalStates preparation history.
        Formal charge remains in the native elementary-charge convention.

    Raises
    ------
    ArgumentError
        If identifiers, source types or policy arguments are invalid.
    ChemicalReferenceLookupError
        If the selected reference is missing, ambiguous, unavailable or changes
        during reading. Its reason and original operational cause are retained.
    FileContentError
        If required CCD structure is malformed, inconsistent or duplicated.
    StructuralInconsistencyError
        If H projection would lose declared reference information.
    LibraryNotFoundError
        If the explicitly selected canonical-descriptor method lacks RDKit.
    MemoryBudgetExceededError
        If reference input buffers or descriptor candidates exceed their
        respective share of the configured memory budget.
    UnsupportedHeavyOperationError
        If descriptor correspondence enumeration exceeds max_matches.

    Notes
    -----
    This factory supports CCD, not arbitrary chemical databases or pH prediction.
    It constructs a reference rather than modifying an observed system. Apply it
    with an explicit exhaustive map through assess_chemical_template and
    apply_chemical_template. Atom counts, source array order and ideal/model
    coordinates never establish correspondence to an observed component.

    Canonical interpretation explicitly chooses the named descriptor over CCD
    stereo flags and retains disagreements. Symmetric graph mappings must agree
    on transferred assignments. Unknown stereogenic configurations stay unknown;
    no blanket achirality, neutral charge or radical count is fabricated.
    An unassessed result remains useful evidence, not a complete-state certificate.

    Local catalogue scanning retains selected component bytes; the full resource
    hash and selected definition hash describe different byte universes. Input
    source bytes are not an executable plan or authentication token. Optional
    Ackredit capture credits executed software and consulted reference data.
    Physical lines and retained definitions each use an estimated buffer budget
    of one quarter of configure.max_ram_usage. This is an acquisition safeguard,
    not a bound on total process RSS or parser/native-object memory.

    See Also
    --------
    get_peptide_chemical_template : Construct explicitly declared peptide references.
    assess_chemical_template : Assess a reference and its explicit atom map.
    apply_chemical_template : Apply compatible assignments while preserving pose.

    Examples
    --------
    Reading a small caller-declared definition needs neither RDKit nor a network.
    Table projection preserves the explicitly unknown interpretation scope.

    >>> import molsysmt as msm
    >>> definition = b'''data_HEL
    ... _chem_comp.id HEL
    ... _chem_comp_atom.atom_id HE
    ... _chem_comp_atom.type_symbol He
    ... _chem_comp_atom.charge 0
    ... _chem_comp_atom.pdbx_aromatic_flag N
    ... _chem_comp_atom.pdbx_stereo_config N
    ... '''
    >>> result = msm.physchem.get_chemical_template(
    ...     'HEL', source=definition, method='ccd_tables')
    >>> result['template'].structures is None
    True
    >>> result['report']['status']
    'unassessed'
    >>> msm.get(result['template'], formal_charge=True)
    [0]

    .. admonition:: User guide

       See :ref:`Tutorial_Get_Chemical_Template` for explicit reference acquisition
       and its application limits.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.chemical_reference_template import construct

    return construct(
        component_id, source, method, hydrogen_policy, descriptor_program, max_matches
    )
