---
summary: Receive the failed macOS Python 3.12 full-matrix environment.
issue: uibcdf/molsysmt#671
status: open
opened: 2026-11-09
closed:
severity: medium
verification: upstream
area: [ci, environment]
guard:
normative:
blocked_by: []
supersedes: []
---

Full run 42689572908 fails before import/science/tests on macOS Python 3.12.
Native setup logs show libmamba download error 28 for AmberTools/statsmodels:
less than 30 bytes/s for sixty seconds. Cleanup subsequently reports ENOENT for
the absent micromamba-shell path. The original includes no scientific
certificate or JUnit for this cell. This is observed provisioning failure,
not a numerical/test-timeout diagnosis or an upstream setup-action claim.

Retain the original complete GH Run Receptor capture under
uibcdf/molsysviewer#315. Recover through the next agreed corrected-source
matrix, separately from #670's fixture correction; investigate repeated download
failure if observed. Do not omit science, convert the cell to a passing skip,
raise scientific deadlines or dispatch duplicate matrices. No workflow change
is currently justified by the one observed network failure.
