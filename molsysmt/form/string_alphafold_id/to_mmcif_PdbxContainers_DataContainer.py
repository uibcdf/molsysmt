from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError, FormatError

@arg_digest(form='string:alphafold_id')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from mmcif.io.BinaryCifReader import BinaryCifReader
    import urllib.request
    from urllib.request import urlretrieve
    import json
    import time
    from os import remove
    from os.path import exists
    from molsysmt._private.files_and_directories import temp_filename
    from smonitor.integrations import context_extra, emit_from_catalog
    from molsysmt._private.smonitor import CATALOG

    uniprot_id = item.split('-')[-2]

    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    request = urllib.request.Request(api_url, headers={"accept": "application/json"})

    # Retry with exponential backoff: AlphaFold API occasionally returns HTTP 500.
    _retries = 3
    _delay = 2.0
    for _attempt in range(_retries):
        try:
            with urllib.request.urlopen(request) as response:
                response_data = response.read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 500 and _attempt < _retries - 1:
                time.sleep(_delay)
                _delay *= 2
            else:
                raise

    aux_json = json.loads(response_data)
    fullbcifurl = aux_json[0]['bcifUrl']

    binary_cif_reader = BinaryCifReader()
    tmp_filename = temp_filename(extension="bcif")
    try:
        urlretrieve(fullbcifurl, tmp_filename)
        containers = binary_cif_reader.deserialize(tmp_filename)
    finally:
        if exists(tmp_filename):
            remove(tmp_filename)

    if len(containers)>1:
        emit_from_catalog(
            CATALOG['warnings']['MultiContainerWarning'],
            extra=context_extra(
                caller='molsysmt.form.string_alphafold_id.to_mmcif_PdbxContainers_DataContainer',
                operation='download',
                provider='AlphaFold DB',
                extra={'format': 'BCIF'},
            ),
        )
    if len(containers)==0:
        raise FormatError("AlphaFold ID has no DataContainer", caller="molsysmt.form.string_alphafold_id.to_mmcif_PdbxContainers_DataContainer")

    tmp_item = containers[0]

    return tmp_item
