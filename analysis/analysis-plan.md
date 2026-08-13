# Analysis plan

This document separates primary tests from exploratory and sensitivity analyses. It also records changes required to correct weaknesses in the earlier working specification.

## General rules

- Preserve raw participant-level files unchanged.
- Validate schemas, value ranges, uniqueness, missingness, and paired structure before analysis.
- Apply the survey attention check before any survey-derived calculation: retain responses where J2 = 2.
- Report analysis-specific sample sizes.
- Use two-sided tests unless a direction was explicitly specified before seeing the data and a one-sided test was documented. The current pipeline uses two-sided tests.
- Report effect sizes or paired differences with p-values where defensible.
- Treat p-values as graded evidence, not a binary measure of substantive importance.
- Do not interpret non-significance as equivalence or absence of effect.

## Study 1: deployment usability

### Primary outcomes

- Completion proportion with Wilson 95% confidence interval.
- Completion time among successful attempts: mean, SD, median, and range.
- Assistance points by attempt.
- SUS: all-attempt and completer-only mean, SD, median, and range.

### Decision rule

The prespecified operational target was at least 80% completion. The intended completion-time target was approximately 30 minutes. SUS = 68 is displayed only as a common descriptive benchmark; it is not treated as a sharp validated pass/fail threshold for this artifact.

### Excluded claim

No statistical comparison with conventional manual deployment is performed because no manual-deployment observations were collected.

## Survey scales

### Scoring

Scale scores are respondent-level means of available items after the attention check. J1 is reverse scored for quality-control inspection but is not part of the six focal scales.

### Reliability

Cronbach's alpha is reported for perceived usefulness, perceived ease of use, perceived trust, perceived risk, continuance intention, and perceived memory. Alpha is descriptive in this small sample. The perceived-risk composite is not used for substantive claims if alpha remains below .70.

## H2: differences across workflow stages

### Primary test

Cochran's Q tests whether the seven related binary delegation indicators have equal marginal proportions among complete cases.

### Follow-up comparisons

All 21 paired stage contrasts use exact McNemar tests. Holm adjustment controls family-wise error. The follow-ups describe which stages differ; they do not replace the omnibus test.

### Effect presentation

Report each stage's proportion and Wilson 95% confidence interval, ordered by workflow position rather than by magnitude.

## H3a: delegation before and after first failure

### Event definition

The index event is a user's first event coded as failed or partially successful within a workflow stage. Count events in the same stage during the 14 days before and 14 days after the index date. Exclude the index date from both windows. Retain user-stage units with at least one pre-index event.

### Primary unit of inference

For each user, average pre- and post-index daily rates across eligible stages. Compare the paired user-level rates using the exact two-sided Wilcoxon signed-rank test. Report n, W, exact p, mean and median rates, median paired change, and matched-pairs rank-biserial correlation.

### Sensitivity analysis

Repeat the comparison at the user-stage level. Because multiple stages from the same user are dependent, label this result as descriptive sensitivity evidence and do not treat its p-value as independent-person inference.

### Interpretation

The design supports a temporal association. It does not isolate algorithm aversion from regression to the mean, task completion, changing opportunities, seasonality, or other time-varying factors.

## H3b: memory accumulation and continuance

### Variables

- Timeline length in lines.
- Number of recorded memory updates.
- Continuance intention: mean of F1-F3.

### Primary analysis

Merge by pseudonymous link code after applying the attention check. Compute Spearman's rho, exact or asymptotic two-sided p as provided by SciPy, and bootstrap percentile confidence intervals with a fixed seed. Report linked n for each association.

### Interpretation

Results are correlational. Days used, general engagement, initial enthusiasm, and user-specific workflow intensity may confound the association.

## H4: single-agent versus multi-agent pilot

### Outcome construction

Output quality is the mean of eight ratings: four dimensions from each of two blind raters. Also report agreement between the two raters' overall scores using an absolute-agreement intraclass correlation coefficient when estimable.

### Task-specific paired analysis

Within each task, pair observations by participant. For total time, intervention count, intervention time, and quality:

- report condition means and SDs;
- report the median paired difference, multi minus single;
- run the exact two-sided Wilcoxon signed-rank test;
- report matched-pairs rank-biserial correlation, signed so positive values favor the multi-agent condition after orienting lower-is-better metrics.

### Interpretation

With n = 4 pairs, the minimum attainable exact two-sided p-value for four non-zero differences in the same direction is .125. The analysis therefore emphasizes direction, magnitude, individual trajectories, and uncertainty. It does not label H4 statistically supported and does not infer non-inferiority from a non-significant quality comparison.

## Deviations from the earlier working specification

1. H3a now uses the user rather than user-stage as the primary inferential unit because repeated stages within a person are dependent.
2. The experiment uses exact Wilcoxon inference and matched-pairs rank-biserial correlation. The earlier normal-approximation effect-size calculation did not handle zeros and tied ranks correctly.
3. The deployment comparison against an assumed two-hour manual baseline is removed because no baseline group was observed.
4. SUS = 68 is retained as a visual reference rather than a deterministic validation cutoff.
5. Experimental non-significance is not described as quality non-inferiority.
6. H4 is classified as exploratory because the pilot's attainable p-values and precision are incompatible with confirmatory superiority claims.

