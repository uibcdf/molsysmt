# tutorials.yml format

Top-level keys:
- `repo` (required): central repository in `org/repo` format.
- `tutorials` (required): list of tutorial entries.

Tutorial entry (required unless noted):
- `id` (string): unique within this file.
- `title` (string)
- `level` (string): beginner | intermediate | advanced
- `format` (string): notebook | markdown | workshop
- `est_time_min` (int)
- `path` (string): repo-relative path in the central tutorials repo.
- `status` (string): idea | planned | draft | ready | archived
- `tags` (list[string])
- `prerequisites` (list[string], optional)  <-- supported by validator
- `notes` (string, optional)

Template:
```yaml
repo: uibcdf/molsyssuite-tutorials

tutorials:
  - id: <tool>-<shortslug>
    title: "<Tutorial title>"
    level: "beginner"       # beginner | intermediate | advanced
    format: "notebook"      # notebook | markdown | workshop
    est_time_min: 30
    path: "tutorials/<tool>/<tutorial-directory>"
    status: "planned"       # idea | planned | draft | ready | archived
    tags:
      - "<tool-name>"
      - "<topic-tag>"
    prerequisites:
      - "<Optional prereq>"
    notes: "<Optional short note>"
```
