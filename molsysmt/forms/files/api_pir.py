# =======================
# PIR File Format
# =======================

"""
PIR File Format
===============

This format was introduced for the Protein Information Resource (PIR), a project of the National
Biomedical Research Foundation (NBRF).

The Protein Information Resource. Nucleic Acids Res. 2000 Jan 1; 28(1): 41–44.
doi: 10.1093/nar/28.1.41 https://doi.org/10.1093/nar/28.1.41
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC102418/

Modeller use PIR as alignment native file.
https://salilab.org/modeller/9v7/manual/node445.html

Other source information:
    http://emboss.sourceforge.net/docs/themes/seqformats/NbrfFormat.html
    https://biopython.org/DIST/docs/api/Bio.SeqIO.PirIO-module.html
    https://salilab.org/modeller/manual/node496.html

- This is EBI format, diferent from modeller, is the default.


"""


from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'pir': form_name,
    'PIR': form_name
    }

info=["",""]

def rewrite_to_style(filename, style=None):

    if style == 'modeller':
        fff = open(filename,"r")
        content = fff.readlines()
        fff.close()

        fff = open(filename,"w")
        fff.writelines(content[0])
        fff.write("sequence:::::::::")
        fff.writelines(content[1:])
        fff.close()

        pass
    else:
        pass

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import get_form
    return get_form(item)

