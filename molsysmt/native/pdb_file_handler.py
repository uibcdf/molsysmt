import numpy as np
from molsysmt import pyunitwizard as puw
import io

### Parser format 3.3
#https://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html

_dict_database_name = {
        'GB' : 'GenBank',
        'PDB' : 'Protein Data Bank',
        'UNP' : 'UNIPROT',
        'NORINE' : 'Norine',
        'UNIMES' : 'UNIMES',
        }

_dict_helix_class = {
        1 : 'Right-handed alpha',
        2 : 'Right-handed omega',
        3 : 'Right-handed pi',
        4 : 'Right-handed gamma',
        5 : 'Right-handed 3 - 10',
        6 : 'Left-handed alpha',
        7 : 'Left-handed omega',
        8 : 'Left-handed gamma',
        9 : '2 - 7 ribbon/helix',
        10 : 'Polyproline'
        }


def guess_format_version(file):

    return '3.3'


def parse_format33(file):

    from .pdb_atomic_coordinate_entry import PDBAtomicCoordinateEntry
    from .pdb_atomic_coordinate_entry import HeaderRecord, ObslteRecord, TitleRecord, SplitRecord,\
    CaveatRecord, CompndRecord, SourceRecord, KeywdsRecord, ExpdtaRecord, NummdlRecord,\
    MdltypRecord, AuthorRecord, RevdatRecord, SprsdeRecord, JrnlRecord, RemarkRecord, DbrefRecord,\
    Dbref1Dbref2Record, SeqadvRecord, SeqresRecord, ModresRecord, HetRecord, HetnamRecord,\
    HetsynRecord, FormulRecord, HelixRecord, SheetRecord, SsbondRecord, LinkRecord, CispepRecord,\
    SiteRecord, Cryst1Record, OrigxRecord, ScaleRecord, MtrixRecord, Model, AtomRecord,\
    HetatmRecord, MasterRecord

    if isinstance(file, io.IOBase):

        if file.closed:
            file = open(file.name, 'r')
            lines = file.readlines()
            file.close()
        else:
            file.seek(0)
            lines = file.readlines()
            file.seek(0)

    elif isinstance(file, str):

        file = open(file.name, 'r')
        lines = file.readlines()
        file.close()

    pdb = PDBAtomicCoordinateEntry()

    n_lines = len(lines)
    counter = 0

    while counter<n_lines:

        line = lines[counter]
        record = line[0:6]

        #print(counter, n_lines, record)

        ##### Title section

        ### HEADER
        if record=='HEADER':

            header = HeaderRecord()
            pdb.title.header = header

            header.classification = line[10:50].strip()
            header.depDate = line[50:59]
            header.idCode = line[62:66]

            counter += 1

        ### OBSLTE
        elif record=='OBSLTE':

            while record=='OBSLTE':

                if line[8:10].isspace():

                    obslte = ObslteRecord()
                    pdb.title.obslte = obslte

                    obslte.repDate = line[11:20]
                    obslte.idCode = line[21:25]

                position=31
                while not line[position:position+4].isspace():
                    obslte.rIdCode(line[position:position+4])
                    position+=5
                    if position>=75:
                        break

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### TITLE
        elif record=='TITLE ':

            while record=='TITLE ':

                if line[8:10]=='  ':
                    title = TitleRecord()
                    pdb.title.title = title
                    title.title = ''

                title.title += line[10:80].strip()

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### SPLIT
        elif record=='SPLIT ':

            while record=='SPLIT ':

                if line[8:10]=='  ':
                    split = SplitRecord()
                    pdb.title.split = split

                position=11
                while not line[position:position+4].isspace():
                    split.idCode.append(line[position:position+4])
                    position+=5
                    if position==81:
                        break

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### CAVEAT
        elif record=='CAVEAT':

            while record=='CAVEAT':

                if line[8:10]=='  ':
                    caveat = CaveatRecord()
                    pdb.title.caveat = caveat
                    caveat.idCode = line[11:15]

                caveat.comment+=line[10:80].rstrip()

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### COMPND
        elif record=='COMPND':

            pdb.title.compnd = []

            while record=='COMPND':

                aux = line[10:80].strip()

                if aux.startswith('MOL_ID:'): ### mol_id
                    compnd = CompndRecord()
                    pdb.title.compnd.append(compnd)
                    compnd.mol_id = int(aux[7:].strip()[:-1])
                elif aux.startswith('MOLECULE:'): ### molecule
                    compnd.molecule = aux[8:].strip()[:-1]
                elif aux.startswith('CHAIN:'): ### chain
                    compnd.chain = [ii.strip() for ii in aux[6:].strip()[:-1].split(',')]
                elif aux.startswith('FRAGMENT:'): ### FRAGMENT
                    compnd.fragment = aux[9:].strip()[:-1]
                elif aux.startswith('EC:'): ### EC
                    compnd.ec = aux[3:].strip()[:-1]
                elif aux.startswith('SYNONYM:'): ### SYNONYM
                    compnd.synonym += [ii.strip() for ii in aux[8:].strip()[:-1].split(',')]
                elif aux.startswith('ENGINEERED:'): ### ENGINEERED
                    compnd.engineered = aux[11:].strip()[:-1]
                elif aux.startswith('MUTATION:'): ### MUTATION
                    compnd.mutation = aux[9:].strip()[:-1]
                elif aux.startswith('OTHER_DETAILS:'): ### OTHER DETAILS
                    compnd.other_details = aux[14:].strip()[:-1]

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### SOURCE
        elif record=='SOURCE':

            pdb.title.source = []

            while record=='SOURCE':

                aux = line[10:80].strip()
                if aux.startswith('MOL_ID:'): ### MOL_ID
                    source = SourceRecord()
                    pdb.title.source.append(source)
                    source.mol_id = int(aux[7:].strip()[:-1])
                elif aux.startswith('SYNTHETIC:'): ### SYNTHETIC
                    source.synthetic = aux[10:].strip()[:-1]
                elif aux.startswith('FRAGMENT:'): ### FRAGMENT
                    source.fragment = aux[9:].strip()[:-1]
                elif aux.startswith('ORGANISM_SCIENTIFIC:'): ### ORGANISM_SCIENTIFIC
                    source.organism_scientific = aux[20:].strip()[:-1]
                elif aux.startswith('ORGANISM_COMMON:'): ### ORGANISM_COMMON
                    source.organism_common = aux[16:].strip()[:-1]
                elif aux.startswith('ORGANISM_TAXID:'): ### ORGANISM_TAXID
                    source.organism_taxid = aux[15:].strip()[:-1]
                elif aux.startswith('STRAIN:'): ### STRAIN
                    source.strain = aux[7:].strip()[:-1]
                elif aux.startswith('VARIANT:'): ### VARIANT
                    source.variant = aux[8:].strip()[:-1]
                elif aux.startswith('CELL_LINE:'): ### CELL_LINE
                    source.cell_line = aux[10:].strip()[:-1]
                elif aux.startswith('ATCC:'): ### ATCC
                    source.atcc = aux[5:].strip()[:-1]
                elif aux.startswith('ORGAN:'): ### ORGAN
                    source.organ = aux[6:].strip()[:-1]
                elif aux.startswith('TISSUE:'): ### TISSUE
                    source.tissue = aux[7:].strip()[:-1]
                elif aux.startswith('CELL:'): ### CELL
                    source.cell = aux[5:].strip()[:-1]
                elif aux.startswith('ORGANELLE:'): ### ORGANELLE
                    source.organelle = aux[10:].strip()[:-1]
                elif aux.startswith('SECRETION:'): ### SECRETION
                    source.secretion = aux[10:].strip()[:-1]
                elif aux.startswith('CELLULAR_LOCATION:'): ### CELLULAR_LOCATION
                    source.cellular_location = aux[18:].strip()[:-1]
                elif aux.startswith('PLASMID:'): ### PLASMID
                    source.plasmid = aux[8:].strip()[:-1]
                elif aux.startswith('GENE:'): ### GENE
                    source.gene = aux[5:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM:'): ### EXPRESSION_SYSTEM
                    source.expression_system = aux[18:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_COMMON:'): ### EXPRESSION_SYSTEM_COMMON
                    source.expression_system_common = aux[26:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_TAXID:'): ### EXPRESSION_SYSTEM_TAXID
                    source.expression_system_taxid = aux[25:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_STRAIN:'): ### EXPRESSION_SYSTEM_STRAIN
                    source.expression_system_strain = aux[26:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_VARIANT:'): ### EXPRESSION_SYSTEM_VARIANT
                    source.expression_system_variant = aux[27:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_CELL_LINE:'): ### EXPRESSION_SYSTEM_CELL_LINE
                    source.expression_system_cell_line = aux[28:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_ATCC_NUMBER:'): ### EXPRESSION_SYSTEM_ATCC_NUMBER
                    source.expression_system_atcc_number = aux[31:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_ORGAN:'): ### EXPRESSION_SYSTEM_ORGAN
                    source.expression_system_organ = aux[24:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_TISSUE:'): ### EXPRESSION_SYSTEM_TISSUE
                    source.expression_system_tissue = aux[25:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_CELL:'): ### EXPRESSION_SYSTEM_CELL
                    source.expression_system_cell = aux[23:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_ORGANELLE:'): ### EXPRESSION_SYSTEM_ORGANELLE
                    source.expression_system_organelle = aux[28:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_CELLULAR_LOCATION:'): ### EXPRESSION_SYSTEM_CELLULAR_LOCATION
                    source.expression_system_cellular_location = aux[36:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_VECTOR_TYPE:'): ### EXPRESSION_SYSTEM_VECTOR_TYPE
                    source.expression_system_vector_type = aux[30:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_VECTOR:'): ### EXPRESSION_SYSTEM_VECTOR
                    source.expression_system_vector = aux[25:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_PLASMID:'): ### EXPRESSION_SYSTEM_PLASMID
                    source.expression_system_plasmid = aux[26:].strip()[:-1]
                elif aux.startswith('EXPRESSION_SYSTEM_GENE:'): ### EXPRESSION_SYSTEM_GENE
                    source.expression_system_gene = aux[23:].strip()[:-1]
                elif aux.startswith('OTHER_DETAILS:'): ### OTHER DETAILS
                    source.other_details = aux[14:].strip()[:-1]

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### KEYWDS
        elif record=='KEYWDS':

            while record=='KEYWDS':

                if line[8:10]=='  ':
                    keywds = KeywdsRecord()
                    pdb.title.keywds = keywds
                    keywds.keywds = []

                keywds.keywds += [ii.strip() for ii in line[10:80].split(',')]

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### EXPDTA
        elif record=='EXPDTA':

            while record=='EXPDTA':

                if line[8:10]=='  ':
                    expdta = ExpdtaRecord()
                    pdb.title.expdta = expdta
                    expdta.technique = ''

                expdta.technique += line[10:80].strip()

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### NUMMDL
        elif record=='NUMMDL':

            nummdl = ExpdtaRecord()
            pdb.title.nummdl = nummdl
            nummdl.modelNumber = int(line[10:14])
            counter += 1

        ### MDLTYP
        elif record=='MDLTYP':

            while record=='MDLTYP':

                if line[8:10]=='  ':
                    mdltyp = MdltypRecord()
                    pdb.title.mdltyp = mdltyp
                    dmltyp.comment = ''

                dmltyp += line[10:80].strip()

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### AUTHOR
        elif record=='AUTHOR':

            while record=='AUTHOR':

                if line[8:10]=='  ':
                    author = AuthorRecord()
                    pdb.title.author = author
                    author.authorList = []

                author.authorList += [ii.strip() for ii in line[10:79].split(',')]

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### REVDAT
        elif record=='REVDAT':

            pdb.title.revdat = []

            while record=='REVDAT':

                if line[10:12]=='  ':
                    revdat = RevdatRecord()
                    pdb.title.revdat.append(revdat)
                    revdat.modNum = int(line[7:10])
                    revdat.modDate = line[13:22]
                    revdat.modId = line[23:27]
                    revdat.modType = int(line[31])
                    revdat.record = []

                position=39
                while not line[position:position+6].isspace():
                    revdat.record.append(line[position:position+6].strip())
                    position+=8
                    if position>=66:
                        break

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### SPRSDE
        elif record=='SPRSDE':

            while record=='SPRSDE':

                if line[8:10]=='  ':
                    sprsde = SprsdeRecord()
                    pdb.title.sprsde.append(superseded)
                    sprsde.sprsdeDate = line[11:20]
                    sprsde.idCode = line[21:25]

                position=31
                while not line[position:position+4].isspace():
                    modification.changes.append(line[position:position+4].strip())
                    position+=6
                    if position>=75:
                        break

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### JRNL
        elif record=='JRNL  ':

            jrnl=JrnlRecord()
            pdb.title.jrnl=jrnl

            while record=='JRNL  ':

                aux = line[12:16]
                if aux == 'AUTH': ### AUTH
                    if line[16:18]=='  ':
                        jrnl.authorList=[ii.strip() for ii in line[19:79].strip().split(',')]
                    else:
                        jrnl.authorList+=[ii.strip() for ii in line[19:79].strip().split(',')]
                elif aux.startswith('TITL'): ### TITL
                    if line[16:18]=='  ':
                        jrnl.title=line[19:79].strip()
                    else:
                        jrnl.title+=line[19:79].strip()
                elif aux.startswith('EDIT'): ### EDIT
                    if line[16:18]=='  ':
                        jrnl.edit=[ii.strip() for ii in line[19:79].strip().split(',')]
                    else:
                        jrnl.edit+=[ii.strip() for ii in line[19:79].strip().split(',')]
                elif aux.startswith('REF '): ### REF
                    if line[16:18]=='  ':
                        jrnl.ref=line[19:79].strip()
                    else:
                        jrnl.ref+=line[19:79].strip()
                elif aux.startswith('PUBL'): ### REF
                    if line[16:18]=='  ':
                        jrnl.pubr=line[19:79].strip()
                    else:
                        jrnl.pub+=line[19:79].strip()
                elif aux.startswith('REFN'): ### REFN
                    jrnl.refn = line[35:65].strip()
                elif aux.startswith('PMID'): ### PMID
                    jrnl.pmid = line[19:79].strip()
                elif aux.startswith('DOI '): ### DOI
                    jrnl.doi = line[19:79].strip()

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### REMARKS
        elif record=='REMARK':

            pdb.title.remarks = []
            mark_id = -1

            while record=='REMARK':

                if line[11:79].isspace() and int(line[7:10])!=mark_id:
                    remark = RemarkRecord()
                    pdb.title.remarks.append(remark)
                    remark.remarkNum = int(line[7:10])
                    mark_id = int(line[7:10])
                    remark.message = ''

                remark.message += line[11:79].strip()+'\n'

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ##### Primary Structure Section

        ### DBREF
        elif record=='DBREF ':

            pdb.primary_structure.dbref=[]

            while record=='DBREF ':

                db_ref=DbrefRecord()
                pdb.primary_structure.dbref.append(db_ref)

                db_ref.idCode = line[7:11]
                db_ref.chainId = line[12]
                db_ref.seqBegin = int(line[14:18])
                db_ref.insertBegin = line[18]
                db_ref.seqEnd = int(line[20:24])
                db_ref.insertEnd = line[24]
                db_ref.database = _dict_database_name[line[26:32].strip()]
                db_ref.dbAccession = line[33:41].strip()
                db_ref.dbIdCode = line[42:54].strip()
                db_ref.dbSeqBegin = int(line[55:60])
                db_ref.dbInsBegin = line[60]
                db_ref.dbSeqEnd = int(line[62:67])
                db_ref.dbInsEnd = line[67]

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### DBREF1/DBREF2
        elif record=='DBREF1':

            db_ref=Dbref1Dbref2Record()
            try:
                pdb.primary_structure.dbref1_dbref2.append(db_ref)
            except:
                pdb.primary_structure.dbref1_dbref2 = []
                pdb.primary_structure.dbref1_dbref2.append(db_ref)

            db_ref.idCode = line[7:11]
            db_ref.chainId = line[12]
            db_ref.seqBegin = int(line[14:18])
            db_ref.insertBegin = line[18]
            db_ref.seqEnd = int(line[20:24])
            db_ref.insertEnd = line[24]
            db_ref.database = _dict_database_name[line[26:32].strip()]
            db_ref.dbIdCode = line[47:67].strip()

            counter += 1
            line = lines[counter]
            record = line[0:6]

            if record!='DBREF2':
                raise ValueError('DBREF1 is not followed by DBREF2')

            if db_ref.chain_id != line[12]:
                raise ValueError('DBREF2 with different chain id')

            db_ref.dbAccession = line[18:40].strip()
            db_ref.dbSeqBegin = int(line[45:55])
            db_ref.dbSeqEnd = int(line[57:67])

            counter += 1
            line = lines[counter]
            record = line[0:6]

        ### SEQADV
        elif record=='SEQADV':

            pdb.primary_structure.seqadv = []

            while record=='SEQADV':

                seqadv=SeqadvRecord()
                pdb.primary_structure.seqadv.append(seqadv)

                seqadv.idCode = line[7:11]
                seqadv.resName = line[12:15]
                seqadv.chainId = line[16]
                seqadv.seqNum = int(line[18:22])
                seqadv.iCode = line[22]
                seqadv.database = _dict_database_name[line[24:28].strip()]
                seqadv.dbAccesion = line[29:38].strip()
                seqadv.dbRes = line[39:42].strip()
                seqadv.dbSeq = int(line[43:48])
                seqadv.conflict = line[49:70].strip()

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### SEQRES
        elif record=='SEQRES':

            pdb.primary_structure.seqres = []

            while record=='SEQRES':

                if int(line[7:10])==1:
                    seqres=SeqresRecord()
                    pdb.primary_structure.seqres.append(seqres)
                    seqres.chainId = line[11]
                    seqres.numRes = int(line[13:17])
                    seqres.resName = []

                position=19
                while not line[position:position+3].isspace():
                    seqres.resName.append(line[position:position+3].strip())
                    position+=4
                    if position>=70:
                        break

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### MODRES
        elif record=='MODRES':

            pdb.primary_structure.modres = []

            while record=='MODRES':

                modres=ModresRecord()
                pdb.primary_structure.modres.append(modres)

                modres.idCode = line[7:11]
                modres.resName = line[12:15]
                modres.chainId = line[16]
                modres.seqNum = int(line[18:22])
                modres.iCode = line[22]
                modres.stdRes = line[24:27]
                modres.comment = line[29:70]

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ##### Heterogen section

        ### HET
        elif record=='HET   ':

            pdb.heterogen.het = []

            while record=='HET   ':

                het=HetRecord()
                pdb.heterogen.het.append(het)

                het.hetId = line[7:10]
                het.chainId = line[12]
                het.seqNum = int(line[13:17])
                het.iCode = line[17]
                het.numHetAtoms = int(line[20:25])
                het.text = line[30:70]

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### HETNAM
        elif record=='HETNAM':

            pdb.heterogen.hetnam = []

            while record=='HETNAM':

                if line[8:10]=='  ':

                    hetnam=HetnamRecord()
                    pdb.heterogen.het.append(hetnam)

                    hetnam.hetId = line[11:14]
                    hetnam.text = ''

                hetnam.text += line[15:70].strip()

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### HETSYN
        elif record=='HETSYN':

            pdb.heterogen.hetsyn = []

            while record=='HETSYN':

                if line[8:10]=='  ':

                    hetsyn=HetsynRecord()
                    pdb.heterogen.hetsyn.append(hetsyn)

                    hetsyn.hetId = line[11:14]
                    hetsyn.hetSynonyms = []

                hetnam.hetSynonyms += [ii.strip() for ii in line[15:70].split(';')]

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### FORMUL
        elif record=='FORMUL':

            pdb.heterogen.formul = []

            while record=='FORMUL':

                if line[16:18]=='  ':

                    formul=FormulRecord()
                    pdb.heterogen.formul.append(formul)

                    formul.compNum = int(line[8:10])
                    formul.hetId = line[12:15]
                    formul.asterisk = line[18]
                    formul.text = ''

                formul.text += line[19:70].strip()

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ##### Secondary Structure section

        ### HELIX
        elif record=='HELIX ':

            pdb.secondary_structure.helix = []

            while record=='HELIX ':

                helix=HelixRecord()
                pdb.secondary_structure.helix.append(helix)

                helix.serNum = int(line[7:10])
                helix.helixId = line[11:14]
                helix.initResName = line[15:18]
                helix.initChainId = line[19]
                helix.initSeqNum = int(line[21:25])
                helix.initICode = line[25]
                helix.endResName = line[27:30]
                helix.endChainId = line[31]
                helix.endSeqNum = int(line[33:37])
                helix.endICode = line[37]
                helix.helixClass = _dict_helix_class[int(line[38:40])]
                helix.comment = line[40:70]
                helix.length = int(line[71:76])

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### SHEET
        elif record=='SHEET ':

            pdb.secondary_structure.sheet = []

            while record=='SHEET ':

                sheet=SheetRecord()
                pdb.secondary_structure.sheet.append(sheet)

                sheet.strand = int(line[7:10])
                sheet.sheetId = line[11:14]
                sheet.numStrands = int(line[14:16])
                sheet.initResName = line[17:20]
                sheet.initChainId = line[21]
                sheet.initSeqNum = int(line[22:26])
                sheet.initICode = line[26]
                sheet.endResName = line[28:31]
                sheet.endChainId = line[32]
                sheet.endSeqNum = int(line[33:37])
                sheet.endICode = line[37]
                sheet.sense = int(line[38:40])
                sheet.curAtom = line[41:45]
                sheet.curResName = line[45:48]
                sheet.curChainId = line[49]
                sheet.curResSeq = line[50:54]
                sheet.curICode = line[54]
                sheet.prevAtom = line[56:60]
                sheet.prevResName = line[60:63]
                sheet.prevChainId = line[64]
                sheet.prevResSeq = line[65:69]
                sheet.prevICode = line[69]

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ##### Connectivity annotation section

        ### SSBOND
        elif record=='SSBOND':

            pdb.connectivity_annotation.ssbond = []

            while record=='SSBOND':

                ssbond=SsbondRecord()
                pdb.connectivity_annotation.ssbond.append(ssbond)

                ssbond.serNum = int(line[7:10])
                ssbond.resName1 = line[11:14]
                ssbond.chainId1 = line[15]
                ssbond.seqNum1 = int(line[17:21])
                ssbond.iCode1 = line[21]
                ssbond.resName2 = line[25:28]
                ssbond.chainId2 = line[29]
                ssbond.seqNum2 = int(line[31:35])
                ssbond.iCode2 = line[35]
                ssbond.sym1 = line[59:65]
                ssbond.sym2 = line[66:72]
                ssbond.sym2 = float(line[73:78])

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### LINK
        elif record=='LINK  ':

            pdb.connectivity_annotation.link = []

            while record=='LINK  ':

                link=LinkRecord()
                pdb.connectivity_annotation.link.append(link)

                link.name1 = line[12:16]
                link.altLoc1 = line[16]
                link.resName1 = line[17:20]
                link.chainId1 = line[21]
                link.resSeq1 = int(line[22:26])
                link.iCode1 = line[26]
                link.name2 = line[42:46]
                link.altLoc2 = line[46]
                link.resName2 = line[47:50]
                link.chainId2 = line[51]
                link.resSeq2 = int(line[52:56])
                link.iCode2 = line[56]
                link.sym1 = line[59:65]
                link.sym2 = line[66:72]
                link.length = float(line[73:78])

                counter += 1
                line = lines[counter]
                record = line[0:6]


        ### CISPEP
        elif record=='CISPEP':

            pdb.connectivity_annotation.cispep = []

            while record=='CISPEP':

                cispep=LinkRecord()
                pdb.connectivity_annotation.cispep.append(cispep)

                cispep.serNum = int(line[7:10])
                cispep.pep1 = line[11:14]
                cispep.chainId1 = line[15]
                cispep.seqNum1 = int(line[17:21])
                cispep.iCode1 = line[22]
                cispep.pep2 = line[25:28]
                cispep.chainId2 = line[29]
                cispep.seqNum2 = int(line[31:35])
                cispep.iCode2 = line[35]
                cispep.modNum = int(line[43:46])
                cispep.measure = float(line[53:59])

                counter += 1
                line = lines[counter]
                record = line[0:6]


        ##### Miscellaneous features section

        ### SITE
        elif record=='SITE  ':

            pdb.miscellaneous_features.site = []

            while record=='SITE  ':

                site=SiteRecord()
                pdb.miscellaneous_features.site.append(site)

                site.seqNum = int(line[7:10])
                site.siteId = line[11:14]
                site.numRes = int(line[15:17])
                site.resName1 = line[18:21]
                site.chainId1 = line[22]
                site.seq1 = int(line[23:27])
                site.iCode1 = line[27]
                site.resName2 = line[29:32]
                site.chainId2 = line[33]
                site.seq2 = int(line[34:38])
                site.iCode2 = line[38]
                site.resName3 = line[40:43]
                site.chainId3 = line[44]
                site.seq3 = int(line[45:49])
                site.iCode3 = line[49]
                site.resName4 = line[51:54]
                site.chainId4 = line[55]
                site.seq4 = int(line[56:60])
                site.iCode4 = line[60]

                counter += 1
                line = lines[counter]
                record = line[0:6]


        ##### Crystallographic and coordinate transformation section

        ### CRYST1
        elif record=='CRYST1':

            cryst1=Cryst1Record()
            pdb.crystallographic_and_coordinate_transformation.cryst1 = cryst1

            cryst1.a = float(line[6:15])
            cryst1.b = float(line[15:24])
            cryst1.c = float(line[24:33])
            cryst1.alpha = float(line[33:40])
            cryst1.beta = float(line[40:47])
            cryst1.gamma = float(line[47:54])
            cryst1.gamma = line[55:66].strip()

            counter += 1
            line = lines[counter]
            record = line[0:6]

        ### ORIGx
        elif record=='ORIGX1':

            origx=OrigxRecord()
            pdb.crystallographic_and_coordinate_transformation.origx = origx

            origx.o11 = float(line[10:20])
            origx.o12 = float(line[20:30])
            origx.o13 = float(line[30:40])
            origx.t1 = float(line[45:55])

            counter += 1
            line = lines[counter]
            record = line[0:6]

            origx.o21 = float(line[10:20])
            origx.o22 = float(line[20:30])
            origx.o23 = float(line[30:40])
            origx.t2 = float(line[45:55])

            counter += 1
            line = lines[counter]
            record = line[0:6]

            origx.o31 = float(line[10:20])
            origx.o32 = float(line[20:30])
            origx.o33 = float(line[30:40])
            origx.t3 = float(line[45:55])

            counter += 1
            line = lines[counter]
            record = line[0:6]


        ### SCALE
        elif record=='SCALE1':

            scale=ScaleRecord()
            pdb.crystallographic_and_coordinate_transformation.scale = scale

            scale.s11 = float(line[10:20])
            scale.s12 = float(line[20:30])
            scale.s13 = float(line[30:40])
            scale.u1 = float(line[45:55])

            counter += 1
            line = lines[counter]
            record = line[0:6]

            scale.s21 = float(line[10:20])
            scale.s22 = float(line[20:30])
            scale.s23 = float(line[30:40])
            scale.u2 = float(line[45:55])

            counter += 1
            line = lines[counter]
            record = line[0:6]

            scale.s31 = float(line[10:20])
            scale.s32 = float(line[20:30])
            scale.s33 = float(line[30:40])
            scale.u3 = float(line[45:55])

            counter += 1
            line = lines[counter]
            record = line[0:6]


        ### MTRIX
        elif record=='MTRIX1':

            mtrix=MtrixRecord()
            pdb.crystallographic_and_coordinate_transformation.mtrix = mtrix

            mtrix.serial = int(line[7:10])

            mtrix.m11 = float(line[10:20])
            mtrix.m12 = float(line[20:30])
            mtrix.m13 = float(line[30:40])
            mtrix.v1 = float(line[45:55])

            counter += 1
            line = lines[counter]
            record = line[0:6]

            mtrix.m21 = float(line[10:20])
            mtrix.m22 = float(line[20:30])
            mtrix.m23 = float(line[30:40])
            mtrix.v2 = float(line[45:55])

            counter += 1
            line = lines[counter]
            record = line[0:6]

            mtrix.m31 = float(line[10:20])
            mtrix.m32 = float(line[20:30])
            mtrix.m33 = float(line[30:40])
            mtrix.v3 = float(line[45:55])

            mtrix.iGiven = line[59]

            counter += 1
            line = lines[counter]
            record = line[0:6]

        ### ATOM/HETATM
        elif record in ['ATOM  ', 'HETATM']:

            model = Model()
            model.record = []
            try:
                pdb.coordinate.model.append(model)
            except:
                pdb.coordinate.model=[]
                pdb.coordinate.model.append(model)

            prev_record = lines[counter-1][0:6]

            if prev_record == 'MODEL ':
                model.serial = int(lines[counter-1][10:14])
            else:
                model.serial = len(pdb.coordinate.model)

            while record in ['ATOM  ', 'HETATM', 'ANISOU', 'TER   ']:

                if record == 'ATOM  ':

                    record_element = AtomRecord()
                    model.record.append(record_element)

                    record_element.recordName = 'ATOM'
                    record_element.serial = int(line[6:11])
                    record_element.name = line[12:16].strip()
                    record_element.altLoc = line[16]
                    record_element.resName = line[17:20].strip()
                    record_element.chainId = line[21]
                    record_element.resSeq = line[22:26].strip()
                    record_element.iCode = line[26]
                    record_element.x = float(line[30:38])
                    record_element.y = float(line[38:46])
                    record_element.z = float(line[46:54])
                    record_element.occupancy = float(line[54:60])
                    record_element.tempFactor = float(line[60:66])
                    record_element.element = line[76:78].strip()
                    record_element.charge = line[78:80]

                elif record == 'HETATM':

                    record_element = AtomRecord()
                    model.record.append(record_element)

                    record_element.recordName = 'HETATOM'
                    record_element.serial = int(line[6:11])
                    record_element.name = line[12:16].strip()
                    record_element.altLoc = line[16]
                    record_element.resName = line[17:20].strip()
                    record_element.chainId = line[21]
                    record_element.resSeq = line[22:26].strip()
                    record_element.iCode = line[26]
                    record_element.x = float(line[30:38])
                    record_element.y = float(line[38:46])
                    record_element.z = float(line[46:54])
                    record_element.occupancy = float(line[54:60])
                    record_element.tempFactor = float(line[60:66])
                    record_element.element = line[76:78].strip()
                    record_element.charge = line[78:80]

                elif record == 'ANISOU':

                    record_element = AtomRecord()
                    model.record.append(record_element)

                    if record_element.serial!=int(line[6:11]):
                        raise ValueError("ANISOU record not referring previous atom record.")

                    record_element.anisou11 = int(line[28:35])
                    record_element.anisou22 = int(line[35:42])
                    record_element.anisou33 = int(line[42:49])
                    record_element.anisou12 = int(line[49:56])
                    record_element.anisou13 = int(line[56:63])
                    record_element.anisou23 = int(line[63:70])

                counter += 1
                line = lines[counter]
                record = line[0:6]


        ##### Connectivity section

        ### Conect
        elif record=='CONECT':

            pdb.connectivity.conect=[]

            previous_serial_atom_number = -1

            while record=='CONECT':

                if previous_serial_atom_number != int(line[6:11]):

                    conect = ConectRecord()
                    pdb.connectivity.conect.append(conect)
                    conect.bondedAtomsSerialNumbers=[]

                    conect.atomSerNum = int(line[6:11])
                    conect.bondedAtomsSerNum = []

                    position=11
                    while not line[position:position+5].isspace():
                        conect.bondedAtomsSerNum(int(line[position:position+5]))
                        position+=5
                        if position>=31:
                            break

                    previous_serial_atom_number = connect.atomSerNum

                else:

                    position=11
                    while not line[position:position+5].isspace():
                        conect.bondedAtomsSerNum(int(line[position:position+5]))
                        position+=5
                        if position>=31:
                            break

                counter += 1
                line = lines[counter]
                record = line[0:6]

        ### Bookkeeping
        elif record=='MASTER':

            master = MasterRecord()
            pdb.bookkeeping.master=master

            master.numRemark = int(line[10:15])
            master.numHet = int(line[20:25])
            master.numHelix = int(line[25:30])
            master.numSheet = int(line[30:35])
            master.numTurn = int(line[35:40])
            master.numSite = int(line[40:45])
            master.numXform = int(line[45:50])
            master.numCoord = int(line[50:55])
            master.numTer = int(line[55:60])
            master.numConect = int(line[60:65])
            master.numSeq = int(line[65:70])

            counter += 1
            line = lines[counter]
            record = line[0:6]


        else:

            counter += 1

        #    raise PDBRecordNotRecognized

    return pdb


class PDBFileHandler():

    def __init__(self, filename, io_mode='r', closed=False, skip_digestion=False):

        self.file = None
        self.format_version = None
        self.entry = None

        if io_mode=='w':

            self.file = None

        elif io_mode=='r':

            self.file = open(filename, "r")
            self.format_version = guess_format_version(self.file)

        else:

            raise NotImplementedError

        if closed:
            self.file.close()

    def close(self):

        self.file.close()

    def load(self):

        if self.format_version == '3.3':

            self.entry = parse_format33(self.file)

    def dump(self):

        pass

    def get_atoms_with_alternate_locations(self):

        output = {}

        for model in self.entry.coordinate.model:
            output[model.serial]=[]
            for record in model.record:
                if record.altLoc != ' ':
                    output[model.serial].append(deepcopy(record))

        return output

