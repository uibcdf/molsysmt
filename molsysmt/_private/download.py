from __future__ import annotations

import os
import random
import time
from tempfile import TemporaryDirectory
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from smonitor.integrations import context_extra

from molsysmt._private.smonitor import DownloadWarning, warn


def download_with_retries(
    url,
    output_filename,
    resource,
    provider,
    caller,
    retries=5,
    timeout=30,
    backoff_base=2.0,
):
    """Downloading into owned staging and publishing only a complete response."""

    headers = {"User-Agent": "MolSysMT/1.0 (+https://uibcdf.org) Python-urllib"}
    last_err = None

    for attempt in range(retries):
        try:
            req = Request(url, headers=headers)
            destination_directory = os.path.dirname(os.path.abspath(output_filename))
            with TemporaryDirectory(
                prefix=".molsysmt-download-", dir=destination_directory
            ) as scratch:
                staged_filename = os.path.join(scratch, "payload")
                with (
                    urlopen(req, timeout=timeout) as resp,
                    open(staged_filename, "wb") as fh,
                ):
                    while True:
                        chunk = resp.read(1024 * 64)
                        if not chunk:
                            break
                        fh.write(chunk)
                os.replace(staged_filename, output_filename)
            return output_filename

        except HTTPError as err:
            last_err = err
            if err.code == 429 or (500 <= err.code < 600):
                wait = (backoff_base**attempt) + random.uniform(0, 0.5)
                _emit_retry_warning(
                    caller=caller,
                    resource=resource,
                    provider=provider,
                    attempt=attempt + 1,
                    retries=retries,
                    reason=f"HTTP {err.code}",
                    url=url,
                    wait=wait,
                )
                time.sleep(wait)
                continue

            raise RuntimeError(
                f"Failed to download {resource} (HTTP {err.code}). URL: {url}"
            ) from err

        except URLError as err:
            last_err = err
            wait = (backoff_base**attempt) + random.uniform(0, 0.5)
            reason = str(getattr(err, "reason", err))
            _emit_retry_warning(
                caller=caller,
                resource=resource,
                provider=provider,
                attempt=attempt + 1,
                retries=retries,
                reason=reason,
                url=url,
                wait=wait,
            )
            time.sleep(wait)
            continue

        except Exception as err:
            raise RuntimeError(
                f"Unexpected error while downloading {resource}: {err}"
            ) from err

    raise RuntimeError(
        f"Could not download {resource} after {retries} attempts. Last error: {last_err}"
    )


def _emit_retry_warning(
    *, caller, resource, provider, attempt, retries, reason, url, wait
):
    warn(
        f"Download of {resource} failed ({reason}). Retrying in {wait:.1f}s…",
        DownloadWarning,
        extra=context_extra(
            caller=caller,
            resource=resource,
            provider=provider,
            operation="download",
            extra={
                "attempt": attempt,
                "retries": retries,
                "reason": reason,
                "url": url,
            },
        ),
    )
