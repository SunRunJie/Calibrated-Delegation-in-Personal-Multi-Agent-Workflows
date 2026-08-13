# Deployment usability protocol

## Objective

Evaluate whether the SBDP installation guide enables non-technical users to complete a personal multi-agent deployment with limited assistance. Record completion, elapsed time, assistance requests, failure points, and SUS responses.

## Sample

Recruit 3-5 students or colleagues who did not attend the workshop, have not seen the guide, are unfamiliar with agent deployment, and report no programming experience. Participants need access to a supported AI coding tool.

## Environment

1. Prepare a clean user environment with VS Code or another supported tool.
2. Open an empty working directory.
3. Place `artifact/sbdp_installation_guide.md` in the directory as the only instructional material.
4. Prepare a timer and observation record.

## Procedure

1. **Introduction:** “Please use only this document to complete the requested setup. You may ask for the time, but not for instructions. If you are blocked for more than ten minutes, I will record the point and you may stop.”
2. **Deployment:** record start and end time for every stage, all assistance requests, and observable problems. Do not provide instructions outside the artifact.
3. **Completion:** completion occurs only when the artifact reaches its final completion declaration. Otherwise code the attempt as not completed.
4. **SUS:** administer the ten-item scale immediately after the attempt.
5. **Optional debrief:** ask where the guide was difficult, ambiguous, or misleading. Use responses for artifact revision.

## Observation record

| Field | Definition |
|---|---|
| Participant ID | Non-identifying code, e.g. S1 |
| Tool | Copilot, Claude Code, Cursor, Codex, or other |
| Completion | Yes or no |
| Elapsed time | Minutes from reading the guide to completion or stopping |
| Assistance points | Number and location of requests for help |
| Failure point | Stage and reason for non-completion |
| SUS | Total score from 0 to 100 |

Record stage-level times for initial configuration questions, second-round bootstrap questions, entry-file creation, memory-directory creation, memory-file population, and completion declaration.

## Evaluation rule

The original operational target was at least 80% completion and approximately 30 minutes among successful attempts. Report SUS descriptively for all attempts and completers. SUS = 68 may be displayed as a common reference value, but should not be treated as a universal pass/fail boundary.

The study did not collect a manual-deployment control condition. Do not claim a statistically established time advantage relative to conventional setup.

