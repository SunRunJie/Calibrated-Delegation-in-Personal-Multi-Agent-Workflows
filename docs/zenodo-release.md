# Zenodo archival release

This repository uses `CITATION.cff` as the authoritative metadata source for GitHub and Zenodo. Do not add a `.zenodo.json` file unless Zenodo-specific fields are needed: when both files are present, Zenodo ignores `CITATION.cff` during GitHub release archiving.

## One-time connection

1. Sign in to [Zenodo](https://zenodo.org/) with the GitHub account that owns this repository.
2. Open the profile menu, choose **GitHub**, and authorize the connection if prompted.
3. Select **Sync now**.
4. Find `SunRunJie/Calibrated-Delegation-in-Personal-Multi-Agent-Workflows` and enable it.

## Archive version 1.0.0

1. Confirm that `CITATION.cff`, the README, licenses, public analysis code, aggregate results, figures, and documentation are committed on `main`.
2. On GitHub, open **Releases** and choose **Draft a new release**.
3. Create the tag `v1.0.0` from `main` and use `Calibrated Delegation v1.0.0` as the release title.
4. Summarize the research materials included in the release and state that participant-level data are excluded under the original consent terms.
5. Publish the GitHub release. Zenodo will ingest the release automatically after the repository has been enabled.
6. Open the resulting Zenodo record and check the title, author, affiliation, description, version, license, and files before using the DOI publicly.

## Return the DOI to the repository

After Zenodo publishes the record:

- add the version DOI to `CITATION.cff` using the `doi` field;
- replace the repository URL in the preferred citation on the project page with `https://doi.org/...`;
- replace the project page's **DOI pending** status with the DOI link;
- add the Zenodo DOI badge to the README;
- commit and publish these metadata updates without changing the archived `v1.0.0` tag.

Use the version DOI when citing version 1.0.0. Zenodo also provides a concept DOI that resolves to the latest archived version; use it for a version-independent project link.

## Official guidance

- [Enable a GitHub repository in Zenodo](https://help.zenodo.org/docs/github/enable-repository/)
- [Archive a GitHub release](https://help.zenodo.org/docs/github/archive-software/github-upload/)
- [Describe software for Zenodo](https://help.zenodo.org/docs/github/describe-software/)
