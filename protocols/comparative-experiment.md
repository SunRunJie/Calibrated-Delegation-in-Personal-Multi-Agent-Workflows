# Comparative experiment: single-agent versus multi-agent workflows

## Objective

Compare elapsed time, human intervention, and blind-rated output quality under single-agent and multi-agent configurations across tasks that differ in decomposability and verification demands.

## Design

- Within-participant design.
- Each participant completes tasks A, B, and C once under each condition.
- Counterbalance condition and task order across participants.
- Give identical materials and time limits in both conditions.
- Blind output raters to condition and participant identity.

## Conditions

### Single-agent

One general-purpose agent, no persistent project memory, and no explicit orchestration-verification role separation.

### Multi-agent

The studied orchestration-execution-verification configuration with access to the configured memory layer.

Record the actual model, tool version, prompt/configuration version, and date for every run. The original data file does not contain these fields; future replications should add them because model changes can alter the treatment.

## Tasks

### Task A — information retrieval and organization

**Topic:** Applications of generative AI in university teaching

Produce an 800-1,200 word structured note with:

1. current applications in university teaching;
2. research or practice evidence supporting or challenging AI-assisted teaching, with sources;
3. major controversies.

Emphasis: relevance, source accuracy, and structural completeness.

### Task B — data analysis

Given an approximately 50-row simulated survey CSV containing an identifier, gender, use frequency, satisfaction, and related fields:

1. handle missing and anomalous values and state the rules;
2. report appropriate frequencies, means, and standard deviations;
3. state three evidence-linked patterns.

Produce a data note with processing rules, statistics, and three conclusions.

### Task C — integrative writing

Given three short source excerpts about how AI assistants affect personal productivity and everyday life, write an approximately 800-word review with a clearly derived theme, coherent structure, and explicit argument.

## Procedure

1. Obtain consent and explain that the system configurations, not the participant, are being evaluated.
2. Assign a counterbalanced sequence.
3. Limit each task-condition run to 30 minutes.
4. Record total elapsed time, intervention count, and intervention time using the same operational definitions in both conditions.
5. Save each output under a blinded code such as `P1-A2` before rating.
6. Two raters independently score each output.

## Blind-rating rubric

Use a five-point scale for each dimension.

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Relevance | Much content is unrelated | Mostly relevant with some irrelevant material | Focused throughout |
| Accuracy | Material factual or computational errors | Minor errors without changing the overall result | Key information correct and sources verifiable |
| Structure | Disorganized | Basic structure with uneven transitions | Clear hierarchy and coherent reasoning |
| Completeness | Several requirements missing | Main requirements covered with minor omissions | All specified requirements covered |

The output quality score is the mean of eight ratings: four dimensions from each of two raters. Report inter-rater agreement. Do not replace independent scores with a consensus score without preserving the original ratings and documenting adjudication.

## Analysis

Pair by participant within task. Report means, SDs, median paired differences, exact two-sided Wilcoxon tests, and matched-pairs rank-biserial correlations. With four pairs, the minimum exact two-sided p-value when all non-zero differences share a direction is .125; interpret the study as a pilot.

No non-inferiority margin was specified. A non-significant quality difference does not establish equivalence or non-inferiority.

## Reproducibility gaps

The named Task B simulated CSV and Task C source packet are not present in the current repository. The existing run-level results can be reanalyzed, but the experimental stimuli cannot yet be independently reproduced. Add the exact materials, their provenance, and their hashes before treating the experiment as fully reproducible.

