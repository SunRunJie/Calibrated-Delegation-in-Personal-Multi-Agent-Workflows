# Research blueprint

## Project title

**Calibrated Delegation in Personal Multi-Agent Workflows: Deployment, Task Boundaries, and Continued Use**

## Research problem

Personal multi-agent systems can perform multi-step work, call tools, divide responsibilities, and retain user-specific context. Their practical value nevertheless depends on two conditions that benchmark studies often hold constant: whether a non-technical user can deploy the system and whether that user can learn which parts of a real workflow should be delegated. The study treats deployment and task-level reliance as empirical phenomena rather than implementation details.

The empirical setting is the April 2026 *Personal AI Chief of Staff* workshop at the School of Information Management, Nanjing University. Participants used a document-guided installation artifact to configure a personal agent system with an orchestration layer, an execution layer, a verification loop, and file-based memory. Post-workshop use created a field setting in which delegation, withdrawal, failure, and memory accumulation could be observed.

## Research questions

### RQ1 — Deployment

Can a document-guided self-bootstrapping protocol enable non-technical users to deploy a usable personal multi-agent configuration with limited assistance?

### RQ2 — Task-level delegation

How do users allocate and withdraw delegation across stages of a real knowledge-work workflow, and how are these decisions associated with experienced failures and accumulated memory?

### RQ3 — Comparative workflow performance

What observable differences arise between single-agent and multi-agent configurations in time, human intervention, and externally rated output quality across tasks with different structures?

## Theoretical positioning

The study connects five research conversations.

1. **Multi-agent orchestration.** Role-based coordination, tool use, iterative evaluation, and memory provide the technical basis for the artifact. The empirical question is not whether these mechanisms can be implemented, but when users benefit from them in ordinary workflows.
2. **Trust calibration and appropriate reliance.** Users must align reliance with system capability. Delegation and withdrawal are treated as behavioral expressions of that calibration process.
3. **Task-technology fit.** Delegation is expected to vary by workflow stage because task requirements differ in structure, verifiability, and demand for contextual judgment.
4. **Transaction costs and relationship-specific investment.** Explaining instructions, checking outputs, and switching tools create interaction costs. Accumulated memory may increase personalization while also increasing switching costs.
5. **Information-systems continuance.** Continued use is distinct from initial adoption. Post-deployment experience, confirmation, trust, and accumulated user-specific context may shape continuance intention.

## DDA mechanism model

The Deploy-Delegate-Accumulate (DDA) model organizes the project-specific mechanism.

### Deploy

The Self-Bootstrapping Deployment Protocol (SBDP) encodes setup knowledge in a document that an agent can execute with the user. It shifts part of the setup burden from code and environment configuration to guided interaction. In this study, that shift is evaluated through observed completion, elapsed time, assistance requests, failure points, and SUS responses.

### Delegate

Delegation occurs at the workflow-stage level. A user weighs perceived capability and task-technology fit, trust based on prior performance, the cost of communicating and checking, and the consequences of error. A failed or partially successful event may move the delegation boundary inward for the affected stage.

### Accumulate

File-based memory records user preferences, priorities, decisions, people, and session history. Accumulation may improve personalization and reduce repeated explanation. It may also produce relationship-specific investment and switching costs. The present data identify association, not the relative causal contribution of these mechanisms.

## Propositions and empirical hypotheses

### P1 / H1 — Feasible document-guided deployment

The protocol is operationally feasible if at least four of five non-technical users complete deployment with limited assistance and completed deployments cluster near the intended 30-minute target. SUS is reported descriptively for all attempts and for completers. The study has no observed manual-deployment control group and therefore does not test a comparative time advantage.

### P2 / H2 — Stage-specific delegation

Delegation rates differ across the seven workflow stages. Retrieval, organization, and generation were expected to be delegated more often than problem definition and judgment/decision.

### P3 / H3a — Failure-linked recalibration

After a user's first failed or partially successful event within a stage, the user's delegation frequency to that stage is expected to decline in a symmetric 14-day window. The primary analysis aggregates stage-level rates within each user before testing the paired user-level change. A user-stage analysis is retained as a sensitivity specification and is not treated as independent-person inference.

### P3 / H3b — Memory and continuance

Two indicators of memory accumulation—timeline length and update frequency—are expected to correlate positively with continued-use intention. This is an observational linked-sample analysis. Personalization, tenure, overall engagement, and switching cost remain plausible alternative explanations.

### P4 / H4 — Task-contingent multi-agent advantage

For decomposable, multi-stage, verifiable tasks, the multi-agent condition is expected to reduce time and human intervention without an evident loss of rated output quality. For a single-stage, judgment-heavy writing task, little advantage is expected. Because the pilot has four paired observations per task and no preregistered non-inferiority margin, the analysis is exploratory and cannot establish superiority or non-inferiority.

## Artifact design

The evaluated configuration has three layers.

- **Deployment layer:** the SBDP installation guide gathers configuration information, creates files, initializes memory, and conducts a bootstrap interview.
- **Collaboration layer:** an orchestrator decomposes and integrates work, executor agents perform bounded tasks, and a verifier checks outputs against instructions and returns discrepancies.
- **Memory layer:** frequently loaded profile files, an append-only timeline, and indexed cold memory preserve user-specific context in human-readable files.

Five original design principles organize the artifact: identity, memory, growth, collaboration, and verification. Their empirical status differs. Deployment and workflow behavior are observed directly; the psychological mechanisms attached to identity and memory require stronger measurement and causal designs before they can be treated as established.

## Study design

The project uses design science research with convergent mixed evidence.

| Study | Evidence | Main role | Principal limitation |
|---|---|---|---|
| 1. Deployment usability | Completion, time, assistance, SUS | Artifact evaluation | Five attempts; no manual baseline |
| 2a. Survey | Perceptions, use, delegation selections | Cross-sectional description and reliability | Single workshop; self-report |
| 2b. Usage-event coding | Stage, outcome, failures, iterations | Behavioral description over time | Platform heterogeneity; observational |
| 2c. Memory linkage | File indicators linked by pseudonymous code | Association with continuance | Small linked sample; confounding |
| 3. Comparative experiment | Paired single/multi runs and blind ratings | Directional workflow comparison | Four participants; underpowered |

## Contribution claims within evidence boundaries

### Conceptual contribution

The DDA model links deployment, task-level delegation, and accumulated memory in one process account. Its value is as a falsifiable organizing model. The current study provides an initial empirical probe, not definitive validation.

### Empirical contribution

The study records delegation at workflow-stage resolution and combines survey selections with event coding, failure-linked temporal comparison, and a pilot multi-agent experiment. This moves analysis below system-level adoption while retaining the temporal dimension of continued use.

### Design contribution

The SBDP artifact makes deployment observable through completion, time, assistance, and failure points. It offers a reproducible design object whose limitations can be inspected and revised.

### Method contribution

The repository integrates artifact evaluation, field behavior, linked indicators, and a controlled pilot. The contribution lies in traceability across these evidence types, not in sample scale.

## Interpretation boundaries

- No result from the survey, event logs, or memory linkage supports a causal claim.
- A temporal decline following failure is consistent with recalibration and algorithm aversion but does not uniquely identify either mechanism.
- A correlation between memory and continuance does not show that memory caused continued use.
- A non-significant quality comparison does not demonstrate equivalence or non-inferiority.
- The small, single-institution convenience samples restrict statistical precision and external validity.
- The system and model environment is time-specific. Agent capabilities and deployment affordances may change rapidly.

## Research integrity

Participation was voluntary and governed by informed consent. Identifiable information was excluded from analysis outputs. Original consent prohibited external distribution of participant-level data, so the public release contains aggregate results only unless renewed permission and institutional review authorize broader disclosure. The researcher remains responsible for research design, data provenance, analytical decisions, and conclusions.
