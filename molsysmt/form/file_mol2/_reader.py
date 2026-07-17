"""Read one Tripos MOL2 record while retaining source bond tokens."""

from depdigest import dep_digest


def _format_error(path, reason):
    from molsysmt._private.smonitor import FormatError

    raise FormatError(
        reason=f'Invalid MOL2 file {path!r}: {reason}',
        caller='molsysmt.form.file_mol2',
    )


def _source_metadata(path):
    with open(path, encoding='utf-8') as stream:
        lines = stream.readlines()

    molecule_markers = [
        index
        for index, line in enumerate(lines)
        if line.strip().upper() == '@<TRIPOS>MOLECULE'
    ]
    if len(molecule_markers) != 1:
        _format_error(
            path,
            'exactly one @<TRIPOS>MOLECULE record is required; '
            f'found {len(molecule_markers)}.',
        )

    marker = molecule_markers[0]
    header = []
    for line in lines[marker + 1:]:
        stripped = line.strip()
        if stripped.startswith('@<TRIPOS>'):
            break
        if stripped:
            header.append(stripped)
    if len(header) < 4:
        _format_error(path, 'the MOLECULE header is incomplete.')

    bond_markers = [
        index
        for index, line in enumerate(lines)
        if line.strip().upper() == '@<TRIPOS>BOND'
    ]
    if len(bond_markers) > 1:
        _format_error(path, 'more than one BOND section was found.')

    raw_bonds = []
    if bond_markers:
        for line_number, line in enumerate(
            lines[bond_markers[0] + 1:], start=bond_markers[0] + 2
        ):
            stripped = line.strip()
            if stripped.startswith('@<TRIPOS>'):
                break
            if not stripped or stripped.startswith('#'):
                continue
            fields = stripped.split()
            if len(fields) < 4:
                _format_error(path, f'incomplete bond record at line {line_number}.')
            token = fields[3].lower()
            if token not in {'1', '2', '3', '4', 'ar', 'am'}:
                _format_error(
                    path,
                    f'unsupported bond token {token!r} at line {line_number}; '
                    'MolSysMT will not invent its chemistry.',
                )
            raw_bonds.append(
                {
                    'bond_id': fields[0],
                    'atom1_id': fields[1],
                    'atom2_id': fields[2],
                    'token': token,
                    'line_number': line_number,
                }
            )

    try:
        declared_n_bonds = int(header[1].split()[1])
    except (IndexError, ValueError):
        _format_error(path, 'the atom/bond counts line is malformed.')
    if declared_n_bonds != len(raw_bonds):
        _format_error(
            path,
            f'the header declares {declared_n_bonds} bonds but '
            f'{len(raw_bonds)} records were read.',
        )

    return {
        'molecule_name': header[0],
        'molecule_type': header[2],
        'charge_type': header[3].upper(),
        'has_crysin': any(
            line.strip().upper() == '@<TRIPOS>CRYSIN' for line in lines
        ),
        'bonds': raw_bonds,
    }


@dep_digest('parmed')
def read_mol2(path):
    """Return a ParmEd structure and validated source-level MOL2 metadata."""

    from parmed.formats.mol2 import Mol2File

    metadata = _source_metadata(path)
    try:
        structure = Mol2File.parse(path, structure=True)
    except Exception as error:
        _format_error(path, f'ParmEd could not parse it: {error}')
    return structure, metadata
