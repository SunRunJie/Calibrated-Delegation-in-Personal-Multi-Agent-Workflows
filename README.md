# Calibrated Delegation

**Deployment, task boundaries, and continued use in personal multi-agent workflows**

This repository contains an empirical information-systems study of how non-technical users deploy personal multi-agent systems, decide which workflow stages to delegate, revise those decisions after unsuccessful outcomes, and develop continuance intentions as personal memory accumulates. All public-facing materials are in English.

**Research site:** [Explore the interactive project page](https://sunrunjie.github.io/Calibrated-Delegation-in-Personal-Multi-Agent-Workflows/) · **Paper:** [`docs/research-report.md`](docs/research-report.md) · **Artifact:** [`artifact/sbdp-installation-guide.md`](artifact/sbdp-installation-guide.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21976763.svg)](https://doi.org/10.5281/zenodo.21976763)

## Research design

| Study component | Analytical sample | Purpose |
| --- | ---: | --- |
| Deployment usability | 5 attempts; 4 completions | Evaluate document-guided deployment |
| Post-workshop survey | 29 valid of 30 responses | Measure perceptions and delegation boundaries |
| Usage-event coding | 327 events from 13 users | Examine outcomes and failure-linked recalibration |
| Memory linkage | 13 linked records | Examine association with continuance intention |
| Comparative pilot | 4 participants x 3 tasks x 2 conditions | Compare single- and multi-agent workflows |

## Repository structure

```text
docs/          Complete English research report, theory, and study design
protocols/     Ethics materials, instruments, codebooks, and study protocols
data/          Data-access documentation and Git-ignored restricted inputs
analysis/      Statistical analysis plan and figure-generation code
results/       Non-disclosive aggregate result tables
figures/       Research figures and figure documentation
artifact/      Self-Bootstrapping Deployment Protocol
```

The complete English manuscript is available at [`docs/research-report.md`](docs/research-report.md).

## Reproduce the figures

Python 3.12 or later is recommended.

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python analysis/generate_figures.py
```

Authorized local users must place the five restricted CSV files in `data/restricted/` using the filenames documented there. These files are ignored by Git. Running the script validates the principal statistical results and regenerates the original set of 33 figures as English PNG files.

## Evidence boundaries

- Survey, usage-event, and memory results are observational and do not establish causal effects.
- H3a uses users, rather than repeated user-stage records, as the primary inferential unit.
- The comparative experiment has four paired participants per task and is exploratory.
- A non-significant quality difference is not evidence of equivalence or non-inferiority.
- Perceived risk has low internal consistency in this sample and is not interpreted as a reliable composite.
- The deployment study has no manual-configuration control group.

## Data access

The original consent terms do not permit external distribution of participant-level data. The GitHub version therefore contains research instruments, analysis code, non-disclosive aggregate results, and figures, but not row-level survey responses, dated event logs, linked memory records, or participant-level experimental runs.

## License

Code is available under the MIT License. Written research materials are available under CC BY 4.0. Participant-level data are excluded from the license and from the public repository.

## Archival release

Version 1.0.0 is preserved on Zenodo under the version DOI [`10.5281/zenodo.21976763`](https://doi.org/10.5281/zenodo.21976763). The concept DOI [`10.5281/zenodo.21976762`](https://doi.org/10.5281/zenodo.21976762) resolves to the continuing project record. See [`docs/zenodo-release.md`](docs/zenodo-release.md) for versioning notes. Citation metadata are maintained in [`CITATION.cff`](CITATION.cff).

## Author

**Runjie Sun**<br />
School of Information Management, Nanjing University<br />
[251820093@smail.nju.edu.cn](mailto:251820093@smail.nju.edu.cn)

Research interests represented in this project include human–AI interaction, information systems, personal multi-agent workflows, task-level delegation, trust calibration, and design-science evaluation.
