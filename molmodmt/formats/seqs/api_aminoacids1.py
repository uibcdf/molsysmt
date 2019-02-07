from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].replace('api_','')+':seq'

is_form={
    'aminoacids1:seq' : form_name
}

### Corresponde al formato IUPAC extended protein que aparece en Biopython

def to_aminoacids3_seq(item):
    from Bio.SeqUtils import seq3
    tmp_seq=seq3(item.replace('aminoacids1:',''))
    tmp_item=tmp_seq
    del(seq3,tmp_seq)
    return tmp_item

def to_biopython_Seq(item):
    from Bio.Seq import Seq as _bio_Seq
    from Bio.Alphabet.IUPAC import ExtendedIUPACProtein
    tmp_item=_bio_Seq(item.replace('aminoacids1:',''),ExtendedIUPACProtein())
    del(_bio_Seq)
    return tmp_item

def to_biopython_SeqRecord(item):
    from molmodmt.formats.classes.api_biopython_Seq import to_biopython_SeqRecord as _Seq_to_SeqRecord
    tmp_item=to_biopython_Seq(item)
    tmp_item=_Seq_to_SeqRecord(tmp_item)
    del(_Seq_to_SeqRecord)
    return tmp_item

def to_fasta(item, output_file):
    from molmodmt.formats.classes.api_biopython_SeqRecord import to_fasta as  _SeqRecord_to_fasta
    tmp_item=to_biopython_SeqRecord(item)
    return _SeqRecord_to_fasta(tmp_item,output_file)

def get_shape(item):
    raise NotImplementedError

def select_with_mdtraj(item, selection):
    raise NotImplementedError

def extract_atoms_list(item, atoms_list):
    raise NotImplementedError
