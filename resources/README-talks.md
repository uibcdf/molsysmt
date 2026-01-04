# talks.yml format

Top-level keys:
- `repo` (required): central repository in `org/repo` format.
- `talks` (required): list of talk entries.

Talk entry (required unless noted):
- `id` (string): unique within this file.
- `title` (string)
- `authors` (list[string])
- `role` (string): e.g. primary focus | core tool presented | brief mention
- `event` (mapping): name, location, date (YYYY-MM-DD), duration_min (int)
- `path` (string): repo-relative path in the central talks repo.
- `artifacts` (mapping, optional): where binaries live (e.g. dropbox/drive/github).
- `tags` (list[string])
- `status` (string): draft | idea | planned | ready | delivered | archived
- `notes` (string, optional)

Template:
```yaml
repo: uibcdf/molsyssuite-talks

talks:
  - id: 20YY-<slug-unique>
    title: "<Talk title>"
    authors:
      - "<Author One>"
      - "<Author Two>"
    role: "primary focus"  # primary focus | core tool presented | brief mention
    event:
      name: "<Conference / Seminar / Workshop>"
      location: "<City, Country (or Online)>"
      date: "20YY-MM-DD"
      duration_min: 25
    path: "talks/20YY-<talk-directory>"
    artifacts:
      slides: "github"     # github | dropbox | drive | zenodo | TBD
      videos: "dropbox"
    tags:
      - "<tool-name>"
      - "<topic-tag>"
    status: "draft"        # draft | idea | planned | ready | delivered | archived
    notes: "<Optional short note>"
```
