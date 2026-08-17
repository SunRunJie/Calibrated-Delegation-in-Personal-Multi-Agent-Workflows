# Zenodo archival record

This repository uses `CITATION.cff` as the authoritative metadata source for GitHub and Zenodo. Do not add a `.zenodo.json` file unless Zenodo-specific fields are needed: when both files are present, Zenodo ignores `CITATION.cff` during GitHub release archiving.

## Published identifiers

- Version 1.0.0 DOI: [`10.5281/zenodo.21976763`](https://doi.org/10.5281/zenodo.21976763)
- Project concept DOI: [`10.5281/zenodo.21976762`](https://doi.org/10.5281/zenodo.21976762)
- Publication date: 17 August 2026
- Record type: Software
- Access: Open

The version DOI identifies the exact `v1.0.0` archive. The concept DOI resolves to the project's latest archived version and should be used for a version-independent project link.

## Preferred citation

Sun, R. (2026). *Calibrated Delegation in Personal Multi-Agent Workflows: Deployment, Task Boundaries, and Continued Use* (Version 1.0.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.21976763

## Future versions

For each substantive public release, update the version and release date in `CITATION.cff`, create a new semantic-version GitHub tag, and publish a GitHub release. Zenodo will assign a new version DOI while retaining the same concept DOI. Do not alter an existing release tag after it has been archived.

## Official guidance

- [Enable a GitHub repository in Zenodo](https://help.zenodo.org/docs/github/enable-repository/)
- [Archive a GitHub release](https://help.zenodo.org/docs/github/archive-software/github-upload/)
- [Describe software for Zenodo](https://help.zenodo.org/docs/github/describe-software/)
