# This should be a native class of Sabueso

from copy import deepcopy


class TitleSection():

    def __init__(self):

        self.header = None
        self.obslte = None
        self.title = None
        self.split = None
        self.caveat = None
        self.compnd = None
        self.source = None
        self.keywds = None
        self.expdta = None
        self.nummdl = None
        self.mdltyp = None
        self.author = None
        self.revdat = None
        self.sprsde = None
        self.jrnl = None
        self.remarks = None


class PrimaryStructureSection():

    def __init__(self):

        self.dbref = None
        self.dbref1_dbref2 = None
        self.seqadv = None
        self.seqres = None
        self.modres = None


class HeterogenSection():

    def __init__(self):

        self.het = None
        self.hetnam = None
        self.hetsyn = None
        self.formul = None


class SecondaryStructureSection():

    def __init__(self):

        self.helix = None
        self.sheet = None


class ConnectivityAnnotationSection():

    def __init__(self):

        self.ssbond = None
        self.link = None
        self.cispep = None


class MiscellaneousFeaturesSection():

    def __init__(self):

        self.site = None


class CrystallographicAndCoordinateTransformationSection():

    def __init__(self):

        self.cryst1 = None
        self.origx = None
        self.scale = None
        self.mtrix = None


class CoordinateSection():

    def __init__(self):

        self.model = None


class ConnectivitySection():

    def __init__(self):

        self.conect = None


class BookkeepingSection():

    def __init__(self):

        self.master = None
        self.end = None


class HeaderRecord():

    def __init__(self):

        self.classification = None
        self.depDate = None
        self.idCode = None


class ObslteRecord():

    def __init__(self):

        self.classification = None
        self.depDate = None
        self.idCode = None
        self.rIdCode = None


class TitleRecord():

    def __init__(self):

        self.title = None


class SplitRecord():

    def __init__(self):

        self.idCode = None


class CaveatRecord():

    def __init__(self):

        self.idCode = None
        self.comment = None


class CompndRecord():

    def __init__(self):

        self.mol_id = None
        self.molecule = None
        self.chain = None
        self.fragment = None
        self.synonym = None
        self.ec = None
        self.engineered = None
        self.mutation = None
        self.other_details = None


class SourceRecord():

    def __init__(self):

        self.mol_id = None
        self.syntetic = None
        self.fragment = None
        self.organism_scientific = None
        self.organism_common = None
        self.organism_taxid = None
        self.strain = None
        self.variant = None
        self.cell_line = None
        self.atcc = None
        self.organ = None
        self.tissue = None
        self.cell = None
        self.organelle = None
        self.secretion = None
        self.cellular_location = None
        self.plasmid = None
        self.gene = None
        self.expression_system = None
        self.expression_system_common = None
        self.expression_system_taxid = None
        self.expression_system_strain = None
        self.expression_system_variant = None
        self.expression_system_cell_line = None
        self.expression_system_atcc_number = None
        self.expression_system_organ = None
        self.expression_system_tissue = None
        self.expression_system_cell = None
        self.expression_system_organelle = None
        self.expression_system_cellular_location = None
        self.expression_system_vector_type = None
        self.expression_system_vector = None
        self.expression_system_plasmid = None
        self.expression_system_gene = None
        self.other_details = None


class KeywdsRecord():

    def __init__(self):

        self.keywds = None


class ExpdtaRecord():

    def __init__(self):

        self.technique = None


class NummdlRecord():

    def __init__(self):

        self.modelNumber = None


class MdltypRecord():

    def __init__(self):

        self.comment = None


class AuthorRecord():

    def __init__(self):

        self.authorList = None


class RevdatRecord():

    def __init__(self):

        self.modNum = None
        self.modDate = None
        self.modId = None
        self.modType = None
        self.record = None


class SprsdeRecord():

    def __init__(self):

        self.sprsdeDate = None
        self.idCode = None
        self.sIdCode = None


class JrnlRecord():

    def __init__(self):

        self.auth = None
        self.titl = None
        self.edit = None
        self.ref = None
        self.publ = None
        self.refn = None
        self.pmid = None
        self.doi = None


class RemarkRecord():

    def __init__(self):

        self.remarkNum = None
        self.message = None


class DbrefRecord():

    def __init__(self):

        self.idCode = None
        self.chainId = None
        self.seqBegin = None
        self.insertBegin = None
        self.seqEnd = None
        self.insertEnd = None
        self.database = None
        self.dbAccession = None
        self.dbIdCode = None
        self.dbSeqBegin = None
        self.dbInsBegin = None
        self.dbSeqEnd = None
        self.dbInsEnd = None


class Dbref1Dbref2Record():

    def __init__(self):

        self.idCode = None
        self.chainId = None
        self.seqBegin = None
        self.insertBegin = None
        self.seqEnd = None
        self.insertEnd = None
        self.database = None
        self.dbAccession = None
        self.dbIdCode = None
        self.dbSeqBegin = None
        self.dbSeqEnd = None


class SeqadvRecord():

    def __init__(self):

        self.idCode = None
        self.resName = None
        self.chainId = None
        self.seqNum = None
        self.iCode = None
        self.database = None
        self.dbAccession = None
        self.dbRes = None
        self.dbSeq = None
        self.conflict = None


class SeqresRecord():

    def __init__(self):

        self.chainId = None
        self.numRes = None
        self.resName = []


class ModresRecord():

    def __init__(self):

        self.idCode = None
        self.resName = None
        self.chainId = None
        self.seqNum = None
        self.iCode = None
        self.stdRes = None
        self.comment = None


class HetRecord():

    def __init__(self):

        self.hetId = None
        self.chainId = None
        self.seqNum = None
        self.iCode = None
        self.numHetAtoms = None
        self.text = None


class HetnamRecord():

    def __init__(self):

        self.hetId = None
        self.text = None


class HetsynRecord():

    def __init__(self):

        self.hetId = None
        self.hetSynonyms = []


class FormulRecord():

    def __init__(self):

        self.compNum = None
        self.hetId = None
        self.asterisk = False
        self.text = ''


class HelixRecord():

    def __init__(self):

        self.serNum = None
        self.helixId = None
        self.initResName = None
        self.initChainId = None
        self.initSeqNum = None
        self.initICode = None
        self.endResName = None
        self.endChainId = None
        self.endSeqNum = None
        self.endICode = None
        self.helixClass = None
        self.comment = None
        self.length = None


class SheetRecord():

    def __init__(self):

        self.strand = None
        self.sheetId = None
        self.numStrands = None
        self.initResName = None
        self.initChainId = None
        self.initSeqNum = None
        self.initICode = None
        self.endResName = None
        self.endChainId = None
        self.endSeqNum = None
        self.endICode = None
        self.sense = None
        self.curAtom = None
        self.curResName = None
        self.curChainId = None
        self.curResSeq = None
        self.curICode = None
        self.prevAtom = None
        self.prevResName = None
        self.prevChainId = None
        self.prevResSeq = None
        self.prevICode = None


class SsbondRecord():

    def __init__(self):

        self.serNum = None
        self.resName1 = None
        self.chainId1 = None
        self.seqNum1 = None
        self.iCode1 = None
        self.resName2 = None
        self.chainId2 = None
        self.seqNum2 = None
        self.iCode2 = None
        self.sym1 = None
        self.sym2 = None
        self.length = None


class LinkRecord():

    def __init__(self):

        self.name1 = None
        self.altLoc1 = None
        self.resName1 = None
        self.chainId1 = None
        self.resSeq1 = None
        self.iCode1 = None
        self.name2 = None
        self.altLoc2 = None
        self.resName2 = None
        self.chainId2 = None
        self.resSeq2 = None
        self.iCode2 = None
        self.sym1 = None
        self.sym2 = None
        self.length = None


class CispepRecord():

    def __init__(self):

        self.serNum = None
        self.pep1 = None
        self.chainId1 = None
        self.seqNum1 = None
        self.iCode1 = None
        self.pep2 = None
        self.chainId2 = None
        self.seqNum2 = None
        self.iCode2 = None
        self.modNum = None
        self.measure = None


class SiteRecord():

    def __init__(self):

        self.seqNum = None
        self.siteId = None
        self.numRes = None
        self.resName1 = None
        self.chainId1 = None
        self.seq1 = None
        self.iCode1 = None
        self.resName2 = None
        self.chainId2 = None
        self.seq2 = None
        self.iCode2 = None
        self.resName3 = None
        self.chainId3 = None
        self.seq3 = None
        self.iCode3 = None
        self.resName4 = None
        self.chainId4 = None
        self.seq4 = None
        self.iCode4 = None


class Cryst1Record():

    def __init__(self):

        self.a = None
        self.b = None
        self.c = None
        self.alpha = None
        self.beta = None
        self.gamma = None
        self.sGroup = None
        self.z = None


class OrigxRecord():

    def __init__(self):

        self.o11 = None
        self.o12 = None
        self.o13 = None
        self.o21 = None
        self.o22 = None
        self.o23 = None
        self.o31 = None
        self.o32 = None
        self.o33 = None
        self.t1 = None
        self.t2 = None
        self.t3 = None


class ScaleRecord():

    def __init__(self):

        self.s11 = None
        self.s12 = None
        self.s13 = None
        self.s21 = None
        self.s22 = None
        self.s23 = None
        self.s31 = None
        self.s32 = None
        self.s33 = None
        self.u1 = None
        self.u2 = None
        self.u3 = None


class MtrixRecord():

    def __init__(self):

        self.serial = None
        self.m11 = None
        self.m12 = None
        self.m13 = None
        self.m21 = None
        self.m22 = None
        self.m23 = None
        self.m31 = None
        self.m32 = None
        self.m33 = None
        self.v1 = None
        self.v2 = None
        self.v3 = None
        self.iGiven = None


class Model():

    def __init__(self):

        self.serial = None
        self.record = None


class AtomRecord():

    def __init__(self):

        self.recordName = None
        self.serial = None
        self.name = None
        self.altLoc = None
        self.resName = None
        self.chainId = None
        self.resSeq = None
        self.iCode = None
        self.x = None
        self.y = None
        self.z = None
        self.occupancy = None
        self.tempFactor = None
        self.element = None
        self.charge = None
        self.anisou11 = None
        self.anisou22 = None
        self.anisou33 = None
        self.anisou12 = None
        self.anisou13 = None
        self.anisou23 = None

    def to_string(self, output='short_string'):

        if output=='short_string':

            string = self.name+'-'+str(self.serial)

        elif output=='long_string':

            string = self.name+'-'+str(self.serial)+'/'+self.resName+'-'+self.resSeq+'/'+self.chainId

        return string


class HetatmRecord(AtomRecord):

    def __init__(self):

        super().__init__()


class ConectRecord():

    def __init__(self):

        self.atomSerNum = None
        self.bondedAtomsSerNum = None


class MasterRecord():

    def __init__(self):

        self.numRemark = None
        self.numHet = None
        self.numHelix = None
        self.numSheet = None
        self.numTurn = None
        self.numSite = None
        self.numXform = None
        self.numCoord = None
        self.numTer = None
        self.numConect = None
        self.numSeq = None


class PDBAtomicCoordinateEntry():

    def __init__(self):

        self.version = None

        self.title = TitleSection()
        self.primary_structure = PrimaryStructureSection()
        self.heterogen = HeterogenSection()
        self.secondary_structure = SecondaryStructureSection()
        self.connectivity_annotation = ConnectivityAnnotationSection()
        self.miscellaneour_features = MiscellaneousFeaturesSection()
        self.crystallographic_and_coordinate_transformation = CrystallographicAndCoordinateTransformationSection()
        self.coordinate = CoordinateSection()
        self.connectivity = ConnectivitySection()
        self.bookkeeping = BookkeepingSection()

    def _heal(self):

        pass

