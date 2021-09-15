#https://www.wwpdb.org/documentation/file-format-content/format32/v3.2.html

def line_is_ATOM_record(line):

    return line.startswith('ATOM  ')

def line_is_HETATM_record(line):

    return line.startswith('HETATM')

def get_fields_from_ATOM_record(record):

    fields={}
    fields['ATOM  '] = record[0:6]
    fields['serial'] = int(record[6:11])
    fields['name'] = record[12:16]
    fields['altLoc'] = record[16]
    fields['resName'] = record[17:20]
    fields['chainID'] = record[21]
    fields['resSeq'] = int(record[22:26])
    fields['iCode'] = record[26]
    fields['x'] = float(record[30:38])
    fields['y'] = float(record[38:46])
    fields['z'] = float(record[46:54])
    fields['occupancy'] = float(record[54:60])
    fields['tempFactor'] = float(record[60:66])
    fields['element'] = record[76:78]
    fields['charge'] = float(record[78:80])

def get_fields_from_HETATM_record(record):

    fields={}
    fields['HETATM'] = record[0:6]
    fields['serial'] = int(record[6:11])
    fields['name'] = record[12:16]
    fields['altLoc'] = record[16]
    fields['resName'] = record[17:20]
    fields['chainID'] = record[21]
    fields['resSeq'] = int(record[22:26])
    fields['iCode'] = record[26]
    fields['x'] = float(record[30:38])
    fields['y'] = float(record[38:46])
    fields['z'] = float(record[46:54])
    fields['occupancy'] = float(record[54:60])
    fields['tempFactor'] = float(record[60:66])
    fields['element'] = record[76:78]
    fields['charge'] = float(record[78:80])

