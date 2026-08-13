# Post-workshop survey

## Administration

- Anonymous administration; all substantive items required.
- Place the informed-consent statement on the first page.
- An optional four-digit self-generated random link code may connect survey responses to de-identified log and memory indicators.
- Unless stated otherwise, seven-point agreement scale: 1 = strongly disagree, 2 = disagree, 3 = somewhat disagree, 4 = neutral, 5 = somewhat agree, 6 = agree, 7 = strongly agree.
- J1 is reverse scored as `8 - response` for quality-control inspection.
- J2 is an instructed-response attention check. Responses other than 2 are excluded from survey-derived analysis.

## A. Current use

**A1. Are you still using the personal AI chief-of-staff system configured during the workshop?**

1. Every day
2. Several times per week
3. Occasionally
4. I have stopped using it

**A2. How long does a typical session last?**

1. Less than 10 minutes
2. 10-30 minutes
3. 30-60 minutes
4. More than one hour

**A3. What are your main use contexts? Select all that apply.**

- Academic tasks
- Personal administration
- Emotional reflection
- Information research
- Writing
- Other: ______

## B. Perceived usefulness (adapted from Davis, 1989)

- **B1.** Using my personal AI chief of staff improves my task efficiency.
- **B2.** Using it improves the quality of my work output.
- **B3.** It is useful for my academic work and everyday affairs.
- **B4.** Overall, it helps me organize and handle tasks more efficiently.

## C. Perceived ease of use (adapted from Davis, 1989)

- **C1.** I found the deployment process straightforward.
- **C2.** Day-to-day use requires little learning effort.
- **C3.** I can make the system understand my needs without difficulty.
- **C4.** Overall, using the system requires little effort.

## D. Perceived trust (adapted from Lee and See, 2004)

- **D1.** I trust the analysis and recommendations provided by the system.
- **D2.** Before delegating a task, I believe the system can perform it competently.
- **D3.** I consider its judgments generally reliable.
- **D4.** Even when an error occurs, I believe it can be detected and corrected.

## E. Perceived risk

- **E1.** Delegating personal matters to AI makes me worry about privacy breaches.
- **E2.** I worry that AI output may contain incorrect information.
- **E3.** The consequences of an AI error could be difficult for me to bear.

## F. Continuance intention (adapted from Bhattacherjee, 2001)

- **F1.** I intend to continue using my personal AI chief of staff.
- **F2.** If circumstances allow, I would like to use it more frequently.
- **F3.** I would recommend it to people I know.

## G. Delegated workflow stages

**G1. At which stages do you delegate work to the system? Select all that apply.**

- **G1_1:** Problem definition — clarifying what I want
- **G1_2:** Information retrieval — searching and gathering materials
- **G1_3:** Information organization — summarizing, structuring, and note-making
- **G1_4:** Analysis and reasoning — data analysis and logical inference
- **G1_5:** Content generation — writing, copy, and initial plans
- **G1_6:** Operational execution — sending email, editing files, running programs, or other actions
- **G1_7:** Judgment and decision — choosing among options or reaching conclusions

## H. Reasons for withdrawing delegation

**H1. Which reasons describe tasks that you first delegated and later took back? Select all that apply.**

- **H1_1:** Insufficient capability — it could not do the task or performed it poorly
- **H1_2:** Unreliable output — inconsistent quality or excessive rework
- **H1_3:** No time saving — explaining and checking took longer than doing the task personally
- **H1_4:** Privacy concern — the task involved sensitive personal or institutional information
- **H1_5:** Preference for personal completion — I wanted to do this task myself
- Other: ______

## I. Perceived memory

- **I1.** My personal AI chief of staff remembers me, so I do not need to explain everything again in each conversation.
- **I2.** It understands my preferences and circumstances, producing responses that fit me better than a general-purpose AI tool.
- **I3.** If I switched to a new AI tool, I would lose accumulated memory and shared understanding.

## J. Quality control

- **J1.** *Reverse scored:* Delegating tasks to AI often makes the work more troublesome.
- **J2.** *Instructed response:* Please select “somewhat disagree” for this item.

## Variable schema

| Variable | Meaning | Values |
|---|---|---|
| `link_id` | Self-generated pseudonymous link code | Text |
| `A1` | Use status | 1-4 |
| `A2` | Typical session length | 1-4 |
| `A3_1`-`A3_6` | Use contexts in listed order | 0/1 |
| `B1`-`B4` | Perceived usefulness | 1-7 |
| `C1`-`C4` | Perceived ease of use | 1-7 |
| `D1`-`D4` | Perceived trust | 1-7 |
| `E1`-`E3` | Perceived risk | 1-7 |
| `F1`-`F3` | Continuance intention | 1-7 |
| `G1_1`-`G1_7` | Delegated stages | 0/1 |
| `H1_1`-`H1_5` | Withdrawal reasons | 0/1 |
| `I1`-`I3` | Perceived memory | 1-7 |
| `J1` | Reverse-scored quality-control item | 1-7 |
| `J2` | Instructed-response attention check | 1-7; expected 2 |

Reliability is reported for each multi-item construct. In the collected sample, perceived risk has low internal consistency and is not interpreted as a reliable composite.

