# Continuous Integration

- GitHub Actions is used for all testing and documentation workflows.
- Documentation is deployed to GitHub Pages using:
  <https://github.com/uibcdf/action-sphinx-docs-to-gh-pages>
- Push and pull request checks run the fast tier on Ubuntu with Python 3.13.
- Full matrix checks run weekly (scheduled) and on manual dispatch:
  Ubuntu and macOS with Python 3.10 through 3.13.
- Docs-only changes are skipped via workflow `paths-ignore`.
- Explicit CI skip is supported with `[skip ci]` in commit or PR metadata.
