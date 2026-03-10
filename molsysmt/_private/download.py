from __future__ import annotations

import os
import random
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from smonitor.integrations import context_extra

from molsysmt._private.smonitor import DownloadWarning, warn


def download_with_retries(url, output_filename, resource, provider, caller, retries=5, timeout=30, backoff_base=2.0):
    """Downloading a remote resource with retry-aware diagnostics."""

    headers = {"User-Agent": "MolSysMT/1.0 (+https://uibcdf.org) Python-urllib"}
    last_err = None

    for attempt in range(retries):
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=timeout) as resp, open(output_filename, "wb") as fh:
                while True:
                    chunk = resp.read(1024 * 64)
                    if not chunk:
                        break
                    fh.write(chunk)
            return output_filename

        except HTTPError as err:
            last_err = err
            if err.code == 429 or (500 <= err.code < 600):
                _cleanup_partial(output_filename)
                wait = (backoff_base ** attempt) + random.uniform(0, 0.5)
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

            _cleanup_partial(output_filename)
            raise RuntimeError(f"Failed to download {resource} (HTTP {err.code}). URL: {url}") from err

        except URLError as err:
            last_err = err
            _cleanup_partial(output_filename)
            wait = (backoff_base ** attempt) + random.uniform(0, 0.5)
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
            _cleanup_partial(output_filename)
            raise RuntimeError(f"Unexpected error while downloading {resource}: {err}") from err

    raise RuntimeError(
        f"Could not download {resource} after {retries} attempts. Last error: {last_err}"
    )


def _emit_retry_warning(*, caller, resource, provider, attempt, retries, reason, url, wait):
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


def _cleanup_partial(output_filename):
    if os.path.exists(output_filename):
        try:
            os.remove(output_filename)
        except OSError:
            pass
