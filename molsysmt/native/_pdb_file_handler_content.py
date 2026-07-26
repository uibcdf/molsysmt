"""Normalizing PDB records behind :class:`PDBFileHandler`."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PDBAtomRecord:
    """Holding one ATOM or HETATM record without MolSysMT semantics."""

    record_name: str
    serial: int
    raw_serial: str
    atom_name: str
    alternate_location: str
    group_name: str
    chain_id: str
    group_id: str
    insertion_code: str
    chain_segment: int
    coordinates: tuple
    occupancy: float | None
    b_factor: float | None
    element_symbol: str | None
    formal_charge: int | None

    @property
    def site_key(self):
        """Returning the PDB identity of the canonical atom site."""

        return (
            self.chain_segment,
            self.chain_id,
            self.group_id,
            self.insertion_code,
            self.group_name,
            self.atom_name,
        )


@dataclass
class PDBModel:
    """Holding one ordered PDB model."""

    structure_id: str
    atoms: list = field(default_factory=list)


@dataclass(frozen=True)
class PDBLinkRecord:
    """Holding the two symbolic endpoints of a LINK record."""

    endpoint1: tuple
    endpoint2: tuple


@dataclass(frozen=True)
class PDBSSBondRecord:
    """Holding the two residue endpoints of an SSBOND record."""

    endpoint1: tuple
    endpoint2: tuple


@dataclass(frozen=True)
class PDBConectRecord:
    """Holding serial-number endpoints from one CONECT record."""

    source_serial: int
    target_serials: tuple


@dataclass(frozen=True)
class PDBContentIssue:
    """Describing content that cannot be interpreted without ambiguity."""

    attribute: str
    kind: str
    reason: str
    atom_site_keys: tuple = ()


@dataclass
class PDBContent:
    """Holding the normalized, form-neutral content owned by a PDB handler."""

    models: list = field(default_factory=list)
    links: list = field(default_factory=list)
    ssbonds: list = field(default_factory=list)
    conect: list = field(default_factory=list)
    cryst1: tuple | None = None
    bioassemblies: dict = field(default_factory=dict)
    issues: list = field(default_factory=list)


def _parse_float(field):
    value = field.strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _parse_formal_charge(field):
    value = field.strip()
    if not value:
        return None, None
    if len(value) == 2 and value[0].isdigit() and value[1] in "+-":
        magnitude = int(value[0])
        return magnitude if value[1] == "+" else -magnitude, None
    return None, PDBContentIssue(
        attribute="formal_charge",
        kind="malformed_record",
        reason=f"PDB formal-charge field {value!r} is not a magnitude followed by a sign.",
    )


def _parse_atom(line, chain_segment, parse_serial):
    formal_charge, issue = _parse_formal_charge(line[78:80])
    try:
        coordinates = (
            float(line[30:38]),
            float(line[38:46]),
            float(line[46:54]),
        )
    except ValueError:
        return None, PDBContentIssue(
            attribute="coordinates",
            kind="malformed_record",
            reason="A PDB coordinate field is not numeric.",
        )

    atom = PDBAtomRecord(
        record_name=line[0:6].strip(),
        serial=parse_serial(line[6:11]),
        raw_serial=line[6:11].strip(),
        atom_name=line[12:16].strip(),
        alternate_location=line[16].strip(),
        group_name=line[17:20].strip(),
        chain_id=line[21].strip() or " ",
        group_id=line[22:26].strip(),
        insertion_code=line[26].strip(),
        chain_segment=chain_segment,
        coordinates=coordinates,
        occupancy=_parse_float(line[54:60]),
        b_factor=_parse_float(line[60:66]),
        element_symbol=line[76:78].strip() or None,
        formal_charge=formal_charge,
    )
    if issue is not None:
        issue = PDBContentIssue(
            attribute=issue.attribute,
            kind=issue.kind,
            reason=issue.reason,
            atom_site_keys=(atom.site_key,),
        )
    return atom, issue


def _link_endpoint(line, atom_slice, alt_index, group_slice, chain_index,
                   group_id_slice, insertion_index):
    return (
        line[chain_index].strip() or " ",
        line[group_id_slice].strip(),
        line[insertion_index].strip(),
        line[group_slice].strip(),
        line[atom_slice].strip(),
        line[alt_index].strip(),
    )


def _parse_bioassemblies(lines, issues):
    assemblies = {}
    assembly_ids = []
    active_chain_ids = []

    for line in lines:
        if not line.startswith("REMARK 350"):
            continue
        payload = line[10:].strip()
        if payload.startswith("BIOMOLECULE:"):
            assembly_ids = [
                value.strip()
                for value in payload.split(":", 1)[1].split(",")
                if value.strip()
            ]
            for assembly_id in assembly_ids:
                assemblies.setdefault(assembly_id, {"operations": {}})
            continue
        if (
            payload.startswith("APPLY THE FOLLOWING TO CHAINS:")
            or payload.startswith("AND CHAINS:")
        ):
            active_chain_ids = [
                value.strip()
                for value in payload.split(":", 1)[1].split(",")
                if value.strip()
            ]
            continue
        if "BIOMT" not in payload or not assembly_ids:
            continue

        fields = payload.split()
        if len(fields) != 6 or not fields[0].startswith("BIOMT"):
            issues.append(PDBContentIssue(
                attribute="bioassembly",
                kind="malformed_record",
                reason="A REMARK 350 BIOMT record is incomplete.",
            ))
            continue
        try:
            row = int(fields[0][-1]) - 1
            operation_id = fields[1]
            values = [float(value) for value in fields[2:]]
        except (ValueError, IndexError):
            issues.append(PDBContentIssue(
                attribute="bioassembly",
                kind="malformed_record",
                reason="A REMARK 350 BIOMT record contains invalid numeric fields.",
            ))
            continue
        if row not in {0, 1, 2}:
            continue
        for assembly_id in assembly_ids:
            operation = assemblies[assembly_id]["operations"].setdefault(
                operation_id,
                {
                    "chain_ids": tuple(active_chain_ids),
                    "rotation": [None, None, None],
                    "translation": [None, None, None],
                },
            )
            operation["rotation"][row] = values[:3]
            operation["translation"][row] = values[3]

    output = {}
    for assembly_id, assembly in assemblies.items():
        complete = []
        for operation in assembly["operations"].values():
            if (
                all(row is not None for row in operation["rotation"])
                and all(value is not None for value in operation["translation"])
            ):
                complete.append(operation)
            else:
                issues.append(PDBContentIssue(
                    attribute="bioassembly",
                    kind="malformed_record",
                    reason=f"Bioassembly {assembly_id!r} contains an incomplete BIOMT operation.",
                ))
        if complete:
            output[assembly_id] = complete
    return output


def parse_pdb_content(lines, parse_serial):
    """Parsing normalized content for the owning PDB handler."""

    normalized_lines = [line.rstrip("\r\n").ljust(80) for line in lines]
    content = PDBContent()
    current_model = None
    explicit_models = False
    chain_segment = 0

    def ensure_model():
        nonlocal current_model
        if current_model is None:
            current_model = PDBModel(structure_id="1")
        return current_model

    def finish_model():
        nonlocal current_model, chain_segment
        if current_model is not None and current_model.atoms:
            content.models.append(current_model)
        current_model = None
        chain_segment = 0

    for line in normalized_lines:
        record = line[0:6].strip()
        if record == "MODEL":
            finish_model()
            explicit_models = True
            current_model = PDBModel(structure_id=line[10:14].strip())
            continue
        if record == "ENDMDL":
            finish_model()
            continue
        if record in {"ATOM", "HETATM"}:
            atom, issue = _parse_atom(line, chain_segment, parse_serial)
            if atom is not None:
                ensure_model().atoms.append(atom)
            if issue is not None:
                content.issues.append(issue)
            continue
        if record == "TER":
            if current_model is not None and current_model.atoms:
                chain_segment += 1
            continue
        if record == "CRYST1":
            values = tuple(_parse_float(line[start:stop]) for start, stop in (
                (6, 15), (15, 24), (24, 33), (33, 40), (40, 47), (47, 54)
            ))
            if all(value is not None for value in values):
                content.cryst1 = values
            else:
                content.issues.append(PDBContentIssue(
                    attribute="box",
                    kind="malformed_record",
                    reason="The PDB CRYST1 record contains invalid numeric fields.",
                ))
            continue
        if record == "LINK":
            content.links.append(PDBLinkRecord(
                endpoint1=_link_endpoint(line, slice(12, 16), 16, slice(17, 20),
                                         21, slice(22, 26), 26),
                endpoint2=_link_endpoint(line, slice(42, 46), 46, slice(47, 50),
                                         51, slice(52, 56), 56),
            ))
            continue
        if record == "SSBOND":
            content.ssbonds.append(PDBSSBondRecord(
                endpoint1=(
                    line[15].strip() or " ",
                    line[17:21].strip(),
                    line[21].strip(),
                ),
                endpoint2=(
                    line[29].strip() or " ",
                    line[31:35].strip(),
                    line[35].strip(),
                ),
            ))
            continue
        if record == "CONECT":
            source = parse_serial(line[6:11])
            targets = tuple(
                parse_serial(line[start:start + 5])
                for start in (11, 16, 21, 26)
                if line[start:start + 5].strip()
            )
            content.conect.append(PDBConectRecord(source, targets))

    finish_model()
    if explicit_models:
        for index, model in enumerate(content.models, start=1):
            if not model.structure_id:
                model.structure_id = str(index)
    content.bioassemblies = _parse_bioassemblies(normalized_lines, content.issues)
    return content
