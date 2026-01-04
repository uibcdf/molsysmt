# papers.yml format

Top-level keys:
- `repo` (required): central repository in `org/repo` format.
- `papers` (required): list of paper entries.

Paper entry (required unless noted):
- `id` (string): unique within this file.
- `title` (string)
- `authors` (list[string])
- `year` (int)
- `venue` (string): journal/conference/preprint server.
- `status` (string): idea | in_preparation | submitted | accepted | published | archived
- `path` (string): repo-relative path in the central papers repo.
- `primary` (bool)
- `related_repos` (list[string]) in org/repo format
- `doi` (string, optional)
- `url` (string, optional)
- `tags` (list[string], optional)  <-- supported by validator
- `notes` (string, optional)

Template:
```yaml
repo: uibcdf/molsyssuite-papers

papers:
  - id: <tool-or-ecosystem>-<shortslug>-20YY
    title: "<Paper title>"
    authors:
      - "<Author One>"
      - "<Author Two>"
    year: 20YY
    venue: "TBD"
    status: "in_preparation"  # idea | in_preparation | submitted | accepted | published | archived
    path: "<tool>/20YY-<paper-directory>"
    primary: true
    related_repos:
      - "uibcdf/<tool-repo>"
    doi: null
    url: null
    tags:
      - "<tool-name>"
      - "<topic-tag>"
    notes: "<Optional short note>"
```
