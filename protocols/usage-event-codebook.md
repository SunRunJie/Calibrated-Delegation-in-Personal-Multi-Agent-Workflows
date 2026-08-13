# Usage-event coding manual

## Unit of analysis

One delegation event: a user gives an agent a task or a separable workflow stage and receives an outcome. A long conversation may contain several events if the user delegates distinct tasks. Several messages that pursue one objective form one event.

## Required fields

| Field | Definition |
|---|---|
| `event_id` | Unique non-identifying event code |
| `user_id` | Pseudonymous user code |
| `event_date` | Calendar date of the event |
| `seq` | Chronological sequence within user |
| `stage` | One of seven workflow stages |
| `outcome` | Successful, partially successful, withdrawn, or failed |
| `fail_reason` | Reason when outcome is not successful |
| `iterations` | Number of user-agent revision rounds |
| `error_exposure` | How an error became visible |
| `coderB_*` | Independent second-coder values for the reliability sample |
| `note` | Optional de-identified contextual note |

## Workflow stages

| Stage | Include | Exclude / boundary rule |
|---|---|---|
| Problem definition | Clarifying goals, requirements, constraints, or success criteria | Searching or drafting after the requirement is settled |
| Information retrieval | Searching, locating, or collecting sources and facts | Organizing already collected material |
| Information organization | Summarizing, classifying, structuring, or note-making | New interpretation or inference |
| Analysis and reasoning | Statistical analysis, comparison, diagnosis, explanation, or logical inference | Final value-laden choice |
| Content generation | Drafting prose, plans, code, or creative material | Direct changes to external systems |
| Operational execution | Sending, editing, running, scheduling, or changing external state | Merely recommending an action |
| Judgment and decision | Choosing, approving, prioritizing, or reaching a consequential conclusion | Preparatory analysis without the final choice |

If one request spans several stages, code separate events only when stage-level outcomes can be identified. Otherwise code the dominant stage and explain the decision in `note`.

## Outcome

| Value | Definition |
|---|---|
| Successful | Meets the user's stated requirement without material correction |
| Partially successful | Provides useful output but requires material correction or completion |
| Withdrawn | The user stops delegation and completes the work personally or with another tool |
| Failed | No usable output or a materially incorrect result |

## Failure reason

Use only when the outcome is partially successful, withdrawn, or failed.

- Insufficient capability
- Unreliable output
- No time saving
- Privacy concern
- Preference for personal completion
- Other, with a concise note

## Error exposure

- Agent detected and disclosed the error
- User detected and corrected it immediately
- User discovered it later
- Third party detected it
- Not detected / no error observed

## Reliability procedure

Independently double-code a randomly selected 20% of events before reconciliation. Compute Cohen's kappa separately for workflow stage, outcome, failure reason, and error exposure. The working target is kappa >= .70. If a dimension falls below the target, clarify definitions, recode the reliability sample independently, and document the revision; do not repeatedly recode merely to obtain a favorable statistic.

## H3a temporal construction

For each user and stage, identify the first failed or partially successful event. Count events in the same stage in the 14 days before and after that date, excluding the index date. The primary inferential unit is the user, aggregating eligible stages within user. See `docs/analysis_plan.md`.

