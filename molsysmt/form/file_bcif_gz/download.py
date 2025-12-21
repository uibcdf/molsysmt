import os
import time
import random
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from molsysmt._private.files_and_directories import temp_filename
from molsysmt._private.warnings import warn, DownloadWarning

def download(pdb_id=None, output_filename=None, tempfile=False, wwPDB_Partner='RCSB PDB',
             retries=5, timeout=30, backoff_base=2.0):
    """
    Download <pdb_id>.bcif.gz from the specified wwPDB partner, handling rate limiting (HTTP 429)
    and transient network errors with retries and exponential backoff + jitter.

    Parameters
    ----------
    pdb_id : str
        4-character PDB ID (case-insensitive).
    tempfile : bool, default True
        If True, create a temporary filename via MolSysMT's temp_filename(). If False and
        output_filename is None, the output will be "<pdb_id>.bcif.gz" in the current directory.
    wwPDB_Partner : str, default 'RCSB PDB'
        wwPDB partner source. Currently only 'RCSB PDB' is supported.
    output_filename : str or None, default None
        If provided, write to this path. Otherwise it is computed from `tempfile`/`pdb_id`.
    retries : int, default 5
        Maximum number of attempts before failing.
    timeout : int or float, default 30
        Per-request timeout (seconds).
    backoff_base : float, default 2.0
        Exponential backoff base. Retry wait ~ (backoff_base ** attempt) + jitter.

    Returns
    -------
    str
        Path to the downloaded file.

    Raises
    ------
    NotImplementedError
        If the partner is not supported.
    RuntimeError
        If retries are exhausted or a non-recoverable HTTP error occurs (e.g., 404).
    """

    if pdb_id.startswith('pdb_id:'):
        pdb_id = pdb_id.split(':')[-1]
    elif pdb_id.startswith('pdb_'):
        pdb_id = pdb_id[-4:]

    if wwPDB_Partner != 'RCSB PDB':
        raise NotImplementedError("Only 'RCSB PDB' is supported at the moment.")

    # Determine output filename
    if output_filename is None:
        if tempfile:
            output_filename = temp_filename(extension="bcif.gz")
        else:
            output_filename = f"{pdb_id}.bcif.gz"

    url = f"https://models.rcsb.org/{pdb_id}.bcif.gz"

    # Polite User-Agent; some servers prefer/require it
    headers = {"User-Agent": "MolSysMT/1.0 (+https://uibcdf.org) Python-urllib"}

    last_err = None
    for attempt in range(retries):
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=timeout) as resp, open(output_filename, "wb") as fh:
                # Stream to file in chunks to avoid loading the entire response in memory
                while True:
                    chunk = resp.read(1024 * 64)
                    if not chunk:
                        break
                    fh.write(chunk)
            return output_filename  # success

        except HTTPError as e:
            last_err = e
            # Retry on rate limiting (429) or server errors (5xx)
            if e.code == 429 or (500 <= e.code < 600):
                # Clean up any partial file
                if os.path.exists(output_filename):
                    try:
                        os.remove(output_filename)
                    except OSError:
                        pass
                # Exponential backoff with small jitter
                wait = (backoff_base ** attempt) + random.uniform(0, 0.5)
                warn(
                    f"Download of {pdb_id}.bcif.gz was rate-limited or the server failed "
                    f"(HTTP {e.code}). Retrying in {wait:.1f}s…",
                    DownloadWarning,
                )
                time.sleep(wait)
                continue
            else:
                # Non-recoverable HTTP error (e.g., 400/404)
                if os.path.exists(output_filename):
                    try:
                        os.remove(output_filename)
                    except OSError:
                        pass
                raise RuntimeError(
                    f"Failed to download {pdb_id}.bcif.gz (HTTP {e.code}). URL: {url}"
                ) from e

        except URLError as e:
            # Transient network error: retry with backoff
            last_err = e
            if os.path.exists(output_filename):
                try:
                    os.remove(output_filename)
                except OSError:
                    pass
            wait = (backoff_base ** attempt) + random.uniform(0, 0.5)
            warn(
                f"Network issue while downloading {pdb_id}.bcif.gz "
                f"({getattr(e, 'reason', e)}). Retrying in {wait:.1f}s…",
                DownloadWarning,
            )
            time.sleep(wait)
            continue

        except Exception as e:
            # Unexpected error: abort cleanly
            if os.path.exists(output_filename):
                try:
                    os.remove(output_filename)
                except OSError:
                    pass
            raise RuntimeError(
                f"Unexpected error while downloading {pdb_id}.bcif.gz: {e}"
            ) from e

    # Retries exhausted
    raise RuntimeError(
        f"Could not download {pdb_id}.bcif.gz after {retries} attempts. Last error: {last_err}"
    )

#    from molsysmt._private.files_and_directories import temp_filename
#    from urllib.request import urlretrieve
#
#    output = None
#
#    if tempfile:
#        output_filename=temp_filename(extension="bcif.gz")
#
#    if wwPDB_Partner=='RCSB PDB':
#
#        filename = pdb_id+'.bcif.gz'
#        fullurl = 'https://models.rcsb.org/'+filename
#
#        if output_filename is None:
#            output_filename = filename
#
#        urlretrieve(fullurl, output_filename)
#
#        output = output_filename
#
#    else:
#
#        raise NotImplementedError()
#
#    return output

