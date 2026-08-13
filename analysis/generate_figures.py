# -*- coding: utf-8 -*-
"""Validate the principal results and generate the 33 English PNG figures.

Restricted inputs are read from ``data/restricted``. Figures are written to
``figures``.
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle
from matplotlib.colors import Normalize
from scipy import stats, interpolate
import warnings
import logging
import re
warnings.filterwarnings("ignore")
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ------------------------------------------------------------------

# ------------------------------------------------------------------
plt.rcParams["font.family"] = ["Times New Roman", "SimSun"]
plt.rcParams["font.serif"] = ["Times New Roman", "SimSun"]
plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["savefig.facecolor"] = "white"
plt.rcParams["axes.edgecolor"] = "#3D6680"
plt.rcParams["axes.linewidth"] = 0.9
plt.rcParams["axes.labelcolor"] = "#3D6680"
plt.rcParams["xtick.color"] = "#3D6680"
plt.rcParams["ytick.color"] = "#3D6680"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

# ------------------------------------------------------------------

# ------------------------------------------------------------------
# Project research palette. Group 1 is used first;
# Group 2 supplies additional categorical colors only when needed.
INK = "#3D6680"
GRAY = "#6769A1"
LGRAY = "#B6B6B6"
GRIDC = "#B6B6B6"
BLUE = "#8DC5E8"
ORANGE = "#D2868B"
GREEN = "#349237"
RED = "#D72828"
PURPLE = "#6769A1"
CYAN = "#3183BA"
BROWN = "#A39571"
GOLD = "#D85B75"
LIGHTB = "#8DC5E8"
LIGHTG = "#B6B6B6"
LIGHTO = "#D2868B"

OUT_C = {"\u6210\u529f": GREEN, "\u90e8\u5206\u6210\u529f": GOLD, "\u64a4\u56de": PURPLE, "\u5931\u8d25": RED}
STAGES = ["\u9700\u6c42\u754c\u5b9a", "\u4fe1\u606f\u68c0\u7d22", "\u4fe1\u606f\u6574\u7406", "\u5206\u6790\u63a8\u7406", "\u5185\u5bb9\u751f\u6210", "\u6267\u884c\u64cd\u4f5c", "\u5224\u65ad\u51b3\u7b56"]
OUTCOMES = ["\u6210\u529f", "\u90e8\u5206\u6210\u529f", "\u64a4\u56de", "\u5931\u8d25"]
REASONS = ["\u80fd\u529b\u4e0d\u8db3", "\u8f93\u51fa\u4e0d\u53ef\u9760", "\u4e0d\u7701\u65f6\u95f4", "\u9690\u79c1\u987e\u8651", "\u60c5\u611f\u9700\u6c42", "\u5176\u4ed6"]
EXPOSURES = ["\u5f53\u573a\u53d1\u73b0\u5e76\u7ea0\u6b63", "\u4e8b\u540e\u53d1\u73b0", "\u672a\u53d1\u73b0"]
G1 = [f"G1_{i}" for i in range(1, 8)]
H1 = [f"H1_{i}" for i in range(1, 6)]
SCALE_COLS = {"\u611f\u77e5\u6709\u7528\u6027": ["B1", "B2", "B3", "B4"],
              "\u611f\u77e5\u6613\u7528\u6027": ["C1", "C2", "C3", "C4"],
              "\u611f\u77e5\u4fe1\u4efb": ["D1", "D2", "D3", "D4"],
              "\u611f\u77e5\u98ce\u9669": ["E1", "E2", "E3"],
              "\u6301\u7eed\u4f7f\u7528\u610f\u5411": ["F1", "F2", "F3"],
              "\u8bb0\u5fc6\u611f\u77e5": ["I1", "I2", "I3"]}
STAGE_LEVEL_C = {"\u9700\u6c42\u754c\u5b9a": RED, "\u4fe1\u606f\u68c0\u7d22": BLUE, "\u4fe1\u606f\u6574\u7406": BLUE, "\u5206\u6790\u63a8\u7406": PURPLE,
                 "\u5185\u5bb9\u751f\u6210": BLUE, "\u6267\u884c\u64cd\u4f5c": PURPLE, "\u5224\u65ad\u51b3\u7b56": RED}

PALETTE_GROUP_1 = [BLUE, INK, RED, GREEN, ORANGE]
PALETTE_GROUP_2 = [PURPLE, LGRAY, BROWN, CYAN, GOLD]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "restricted")
OUT = os.path.join(ROOT, "figures")
Q_CSV = os.path.join(DATA, "survey-responses.csv")
L_CSV = os.path.join(DATA, "usage-event-coding.csv")
E_CSV = os.path.join(DATA, "comparative-experiment.csv")
M_CSV = os.path.join(DATA, "memory-indicators.csv")
SUS_CSV = os.path.join(DATA, "deployment-usability.csv")

OUTPUT_NAMES = {
    1: "01-deployment-cost-compression.png",
    2: "02-orchestrator-worker-checker-architecture.png",
    3: "03-theoretical-integration-framework.png",
    4: "04-dda-three-stage-model.png",
    5: "05-research-design-triangulation.png",
    6: "06-sbdp-six-stage-deployment-process.png",
    7: "07-deployment-usability-results.png",
    8: "08-sus-scores-and-usability-bands.png",
    9: "09-current-use-status.png",
    10: "10-delegation-rate-by-workflow-stage.png",
    11: "11-delegation-rate-profile.png",
    12: "12-three-attributes-of-the-delegation-boundary.png",
    13: "13-delegation-and-withdrawal-event-flow.png",
    14: "14-delegation-event-outcomes.png",
    15: "15-stage-by-outcome-heatmap.png",
    16: "16-failure-reason-distribution.png",
    17: "17-error-exposure-and-outcome.png",
    18: "18-iteration-count-distribution.png",
    19: "19-reasons-for-withdrawing-delegation.png",
    20: "20-weekly-delegation-events.png",
    21: "21-user-level-event-composition.png",
    22: "22-delegation-before-and-after-first-failure.png",
    23: "23-memory-accumulation-and-continuance.png",
    24: "24-survey-scale-reliability.png",
    25: "25-perceived-construct-radar.png",
    26: "26-total-time-comparison.png",
    27: "27-human-intervention-count.png",
    28: "28-human-intervention-time.png",
    29: "29-output-quality-comparison.png",
    30: "30-relative-multi-agent-gains.png",
    31: "31-paired-participant-trajectories.png",
    32: "32-effect-size-and-significance.png",
    33: "33-core-results-summary.png",
}

TRANSLATIONS = {
    "\u5b8c\u6210\u7387（4/5）": "Completion rate (4/5)",
    "\u9608\u503c ≥ 80%": "Target >= 80%",
    "（a）\u90e8\u7f72\u5b8c\u6210\u7387": "(a) Deployment completion",
    "68（\u53ef\u7528\u9608\u503c）": "68 (reference)",
    "SUS \u5f97\u5206": "SUS score",
    "（b）SUS \u7cfb\u7edf\u53ef\u7528\u6027\u5f97\u5206": "(b) System Usability Scale",
    "\u5206\u949f": "Minutes",
    "（c）\u72ec\u7acb\u90e8\u7f72\u8017\u65f6": "(c) Independent deployment time",
    "\u6b21\u6570": "Count",
    "（d）\u90e8\u7f72\u6c42\u52a9\u70b9": "(d) Assistance points",
    "\u7814\u7a761 \u81ea\u4e3e\u5f0f\u90e8\u7f72\u534f\u8bae（SBDP）\u53ef\u7528\u6027\u6d4b\u8bd5\u7ed3\u679c": "Study 1. SBDP deployment-usability results",
    "\u6ce8：S1—S3、S5 \u72ec\u7acb\u5b8c\u6210\u90e8\u7f72；S4 \u4e8e 42 min \u653e\u5f03。\u5b8c\u6210\u8005\u8017\u65f6 26—34 min（M=29.5），SUS 68—76（M=72.25）。\u6570\u636e\u6765\u6e90：03-\u5df2\u6536\u96c6\u6570\u636e/\u90e8\u7f72\u53ef\u7528\u6027\u6d4b\u8bd5.csv。": "Note: S1-S3 and S5 completed deployment; S4 stopped at 42 min. Completers took 26-34 min (M=29.5) and scored 68-76 on SUS (M=72.25). Source: deployment-usability.csv.",
    "\u90e8\u7f72\u88ab\u8bd5\u7684 SUS \u5f97\u5206\u4e0e\u53ef\u7528\u6027\u5206\u7ea7": "SUS scores and descriptive usability bands",
    "\u6ce8：\u5b8c\u6210\u8005 SUS \u5747 ≥ 68，\u5904\u4e8e“\u53ef\u7528”\u533a\u95f4；\u672a\u5b8c\u6210\u8005 S4=42。\u6570\u636e\u6765\u6e90：03-\u5df2\u6536\u96c6\u6570\u636e/\u90e8\u7f72\u53ef\u7528\u6027\u6d4b\u8bd5.csv。": "Note: All completers scored at least 68; the non-completer, S4, scored 42. The 68 line is a descriptive reference, not a universal pass criterion.",
    "\u5dee": "Poor", "\u52c9\u5f3a\u53ef\u7528": "Marginal", "\u53ef\u7528": "Usable", "\u4f18\u79c0": "Excellent",
    "\u4e24\u8f6e\u4fe1\u606f\u6536\u96c6": "Two-round information collection", "\u521b\u5efa\u5165\u53e3\u6587\u4ef6": "Create entry file",
    "\u521b\u5efa\u8bb0\u5fc6\u76ee\u5f55": "Create memory directory", "\u5199\u5165\u8bb0\u5fc6\u6863\u6848": "Write memory profiles",
    "\u5b8c\u6210\u5ba3\u544a": "Confirm completion", "\u6301\u7eed\u4f7f\u7528": "Continued use",
    "\u914d\u7f6e\u53c2\u6570＋Bootstrap\u91c7\u8bbf": "Configuration + bootstrap interview", "VS Code＋Copilot \u73af\u5883": "VS Code + Copilot environment",
    "\u8bb0\u5fc6\u76ee\u5f55\u7ed3\u6784": "Memory directory structure", "profile/priorities \u7b49\u521d\u59cb\u5316": "Initialize profile and priorities",
    "\u96f6\u4ee3\u7801·\u53ef\u5ba1\u8ba1": "No-code and auditable", "\u65f6\u95f4\u8f74\u65e5\u5fd7\u79ef\u7d2f": "Timeline log accumulation",
    "\u7b2c\u4e00\u8f6e：\u90e8\u7f72\u53c2\u6570": "Round 1: deployment settings", "\u7b2c\u4e8c\u8f6e：Bootstrap \u91c7\u8bbf": "Round 2: bootstrap interview",
    "\u5408\u5e76\u6267\u884c": "Combined execution", "SBDP \u81ea\u4e3e\u5f0f\u90e8\u7f72\u534f\u8bae：\u516d\u9636\u6bb5\u6d41\u7a0b": "SBDP: six-stage deployment process",
    "\u628a\u4e13\u5bb6\u52b3\u52a8\u7f16\u7801\u4e3a\u667a\u80fd\u4f53\u53ef\u6267\u884c\u7684\u6587\u6863\u6d41\u7a0b，\u7528\u6237\u5168\u7a0b\u4e0d\u63a5\u89e6\u4ee3\u7801": "Encode expert setup knowledge as an agent-executable document workflow without requiring users to edit code",
    "\u6ce8：\u4f9d\u636e\u7814\u7a76\u62a5\u544a 3.2 \u4e0e 4.1 \u7684\u534f\u8bae\u7ed3\u6784\u7ed8\u5236。": "Note: Drawn from the protocol structure described in Sections 3.2 and 4.1.",
    "\u90e8\u7f72\u6210\u672c\u7684\u538b\u7f29：\u4e13\u5bb6\u914d\u7f6e → \u5f15\u5bfc\u5f0f\u5bf9\u8bdd": "Compressing deployment burden: expert configuration to guided dialogue",
    "\u4f20\u7edf\u624b\u52a8\u914d\u7f6e": "Conventional manual setup", "\u73af\u5883\u914d\u7f6e（\u6570\u5c0f\u65f6）": "Environment setup (hours)",
    "\u7406\u89e3\u4ee3\u7801 / API": "Understand code and APIs", "\u591a\u89d2\u8272\u7f16\u6392": "Configure multiple roles", "\u4f9d\u8d56\u4e13\u5bb6\u52b3\u52a8": "Depends on expert labor",
    "SBDP \u5f15\u5bfc\u5f0f\u5bf9\u8bdd": "SBDP guided dialogue", "\u7ea6 30 \u5206\u949f（\u5b9e\u6d4b M=29.5 min）": "About 30 minutes (observed M=29.5 min)",
    "\u96f6\u4ee3\u7801 · \u7eaf\u6587\u6863": "No code; document based", "\u667a\u80fd\u4f53\u81ea\u4e3b\u6267\u884c": "Agent-executed setup", "\u666e\u901a\u7528\u6237\u53ef\u72ec\u7acb\u5b8c\u6210": "Designed for independent completion",
    "\u6210\u672c\u538b\u7f29": "Burden shift", "\u90e8\u7f72\u7684\u8ba4\u77e5\u8d1f\u8377\u4ece\u6280\u672f\u57df\u8f6c\u79fb\u5230\u5bf9\u8bdd\u57df；\u5bf9\u8bdd\u662f\u666e\u901a\u7528\u6237\u5df2\u5177\u5907\u7684\u80fd\u529b": "Setup effort shifts from technical configuration toward guided interaction",
    "\u6ce8：\u4f9d\u636e\u7814\u7a76\u62a5\u544a 1.1 \u4e0e 4.1 \u7ed8\u5236；\u5b9e\u6d4b\u6570\u636e\u89c1 07-\u90e8\u7f72\u53ef\u7528\u6027\u6d4b\u8bd5\u7ed3\u679c。": "Note: Conceptual mechanism; observed deployment attempts are shown in Figure 7. No manual-control condition was observed.",
    "\u59d4\u6258\u7387": "Delegation rate", "\u4efb\u52a1\u6d41\u4e03\u73af\u8282\u59d4\u6258\u7387（N=29）": "Delegation rate across seven workflow stages (N=29)",
    "\u6ce8：Cochran's Q = 54.23，p < 0.001，\u4e03\u73af\u8282\u59d4\u6258\u7387\u5dee\u5f02\u663e\u8457；\u5206\u5e03\u5448“\u4e2d\u95f4\u9ad8、\u4e24\u7aef\u4f4e”\u5f62\u6001。\u6570\u636e\u6765\u6e90：\u95ee\u5377 G1_1—G1_7；\u5206\u6790：03-\u59d4\u6258\u8fb9\u754c\u4e0e\u5047\u8bbe\u68c0\u9a8c.py。": "Note: Cochran's Q(6)=54.23, p<.001. Delegation was concentrated in intermediate workflow stages. Source: survey G1_1-G1_7.",
    "\u4efb\u52a1\u6d41\u4e03\u73af\u8282\u59d4\u6258\u7387\u7684\u5206\u5e03\u5f62\u6001": "Delegation profile across seven workflow stages",
    "\u6ce8：\u4e2d\u95f4\u73af\u8282（\u68c0\u7d22/\u6574\u7406/\u751f\u6210）\u59d4\u6258\u7387\u9ad8\u4e8e\u4e24\u7aef\u73af\u8282（\u9700\u6c42\u754c\u5b9a/\u5224\u65ad\u51b3\u7b56）。\u6570\u636e\u6765\u6e90：\u95ee\u5377 G1_1—G1_7（N=29）。": "Note: Retrieval, organization, and generation were delegated more often than problem definition and final judgment. Source: valid survey responses (N=29).",
    "\u9700\u6c42\u754c\u5b9a": "Problem\ndefinition", "\u4fe1\u606f\u68c0\u7d22": "Information\nretrieval", "\u4fe1\u606f\u6574\u7406": "Information\norganization",
    "\u5206\u6790\u63a8\u7406": "Analysis and\nreasoning", "\u5185\u5bb9\u751f\u6210": "Content\ngeneration", "\u6267\u884c\u64cd\u4f5c": "Operational\nexecution", "\u5224\u65ad\u51b3\u7b56": "Judgment and\ndecision",
    "\u4e8b\u4ef6\u5e8f\u53f7（\u6309\u65f6\u95f4\u5148\u540e）": "Event sequence (chronological)", "\u59d4\u6258—\u6536\u56de\u4e8b\u4ef6\u6d41（327 \u6761\u59d4\u6258\u4e8b\u4ef6）": "Delegation and withdrawal event flow (327 events)",
    "\u6ce8：\u6bcf\u4e2a\u70b9\u4ee3\u8868\u4e00\u6b21\u59d4\u6258\u4e8b\u4ef6，\u989c\u8272\u8868\u793a\u7ed3\u679c；× \u6807\u8bb0\u5931\u8d25\u4e8b\u4ef6。\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868；\u53cc\u7f16\u7801 Cohen's κ=0.879—0.971。": "Note: Each point is one delegation event; color indicates outcome and x marks failure. Double-coding kappa=.879-.971.",
    "\u6210\u529f": "Successful", "\u90e8\u5206\u6210\u529f": "Partially successful", "\u64a4\u56de": "Withdrawn", "\u5931\u8d25": "Failed",
    "\u59d4\u6258\u4e8b\u4ef6\u603b\u6570": "Delegation events", "\u6210\u529f\u4e8b\u4ef6\u5360\u7edd\u5bf9\u4e3b\u4f53；\n\u5931\u8d25\u4e8b\u4ef6\u4f4e\u9891\u4f46\u5f71\u54cd\u5927": "Successful events predominate;\nfailures are less frequent",
    "\u59d4\u6258\u4e8b\u4ef6\u7684\u7ed3\u679c\u6784\u6210": "Outcome composition of delegation events", "\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868（327 \u6761\u59d4\u6258\u4e8b\u4ef6）。": "Source: 327 coded delegation events.",
    "\u59d4\u6258\u7ed3\u679c": "Delegation outcome", "\u4efb\u52a1\u6d41\u73af\u8282": "Workflow stage", "\u73af\u8282\u5185\u5360\u6bd4（%）": "Share within stage (%)",
    "\u4efb\u52a1\u6d41\u73af\u8282 × \u59d4\u6258\u7ed3\u679c\u6784\u6210": "Workflow stage by delegation outcome", "\u6ce8：\u5355\u5143\u683c\u4e3a\u5404\u73af\u8282\u5185\u8be5\u7ed3\u679c\u7684\u5360\u6bd4。\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868（327 \u6761\u59d4\u6258\u4e8b\u4ef6）。": "Note: Cells show outcome shares within each workflow stage. Source: 327 coded delegation events.",
    "\u4e8b\u4ef6\u6570": "Events", "\u59d4\u6258\u5931\u8d25/\u64a4\u56de\u7684\u539f\u56e0\u5206\u5e03": "Reasons for failed or withdrawn delegation",
    "\u6ce8：\u4ec5\u7edf\u8ba1\u7ed3\u679c\u975e“\u6210\u529f”\u4e14\u586b\u5199\u4e86\u539f\u56e0\u7684\u4e8b\u4ef6。\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868（fail_reason，κ=0.933）。": "Note: Includes non-success events with a coded reason. Failure-reason kappa=.933.",
    "\u80fd\u529b\u4e0d\u8db3": "Insufficient capability", "\u8f93\u51fa\u4e0d\u53ef\u9760": "Unreliable output", "\u4e0d\u7701\u65f6\u95f4": "No time saving", "\u9690\u79c1\u987e\u8651": "Privacy concern", "\u60c5\u611f\u9700\u6c42": "Personal preference", "\u5176\u4ed6": "Other",
    "\u4e8b\u4ef6\u6570（\u975e\u6210\u529f\u4e8b\u4ef6）": "Events (non-success)", "\u9519\u8bef\u66b4\u9732\u65b9\u5f0f\u4e0e\u59d4\u6258\u7ed3\u679c": "Error exposure and delegation outcome",
    "\u6ce8：\u53ef\u5f53\u573a\u53d1\u73b0\u5e76\u7ea0\u6b63\u7684\u5931\u8d25\u4e0d\u89e6\u53d1\u7b97\u6cd5\u538c\u6076；\u4e8b\u540e\u53d1\u73b0\u7684\u5931\u8d25\u66f4\u6613\u5bfc\u81f4\u6536\u56de。\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868（error_exposure，κ=0.879）。": "Note: Descriptive association only; the observational data do not establish that exposure timing caused withdrawal. Error-exposure kappa=.879.",
    "\u5f53\u573a\u53d1\u73b0\u5e76\u7ea0\u6b63": "Detected and corrected immediately", "\u4e8b\u540e\u53d1\u73b0": "Detected later", "\u672a\u53d1\u73b0": "Not detected",
    "\u8fed\u4ee3\u8f6e\u6570": "Iteration count", "\u5355\u6b21\u59d4\u6258\u7684\u8fed\u4ee3\u8f6e\u6570\u5206\u5e03": "Iteration count per delegation event",
    "\u9009\u62e9\u6bd4\u4f8b（\u591a\u9009）": "Selection rate (multiple response)", "\u6536\u56de\u59d4\u6258\u7684\u539f\u56e0\u5206\u5e03（N=29）": "Reasons for withdrawing delegation (N=29)",
    "\u6ce8：\u4e03\u70b9\u95ee\u5377\u4e8c\u503c\u9898“\u662f\u5426\u56e0\u8be5\u539f\u56e0\u6536\u56de\u8fc7\u59d4\u6258”，\u7edf\u8ba1\u9009\u62e9\u6bd4\u4f8b。\u6570\u636e\u6765\u6e90：\u95ee\u5377 H1_1—H1_5；\u5206\u6790：01-\u95ee\u5377\u5206\u6790.py。": "Note: Multiple responses permitted. Source: survey items H1_1-H1_5 (N=29).",
    "\u6b21/\u5929": "Events/day", "\u8be5\u73af\u8282\u59d4\u6258\u9891\u7387（\u6b21/\u5929）": "Delegation rate in affected stage (events/day)",
    "\u9996\u6b21\u5931\u8d25\u524d\u540e 14 \u5929\u8be5\u73af\u8282\u59d4\u6258\u9891\u7387（H3a）": "Delegation rate 14 days before and after first failure (H3a)",
    "\u6ce8：\u4ee5\u9996\u6b21\u5931\u8d25\u65e5\u4e3a\u754c，\u6bd4\u8f83\u524d\u540e\u5404 14 \u5929\u5185\u8be5\u73af\u8282\u7684\u59d4\u6258\u9891\u7387（\u914d\u5bf9 Wilcoxon \u7b26\u53f7\u79e9\u68c0\u9a8c）。\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868；\u5206\u6790：03-\u59d4\u6258\u8fb9\u754c\u4e0e\u5047\u8bbe\u68c0\u9a8c.py。": "Note: User-stage sensitivity view. The primary user-aggregated analysis gives W=1.5, exact p=.0015, n=12; the temporal association is not causal.",
    "\u9996\u6b21\u5931\u8d25\u524d 14 \u5929": "14 days before first failure", "\u9996\u6b21\u5931\u8d25\u540e 14 \u5929": "14 days after first failure",
    "\u65f6\u95f4\u8f74\u65e5\u5fd7\u884c\u6570（\u8bb0\u5fc6\u79ef\u7d2f\u91cf）": "Timeline length (memory accumulation)", "\u6301\u7eed\u4f7f\u7528\u610f\u5411（F1—F3 \u5747\u503c）": "Continuance intention (mean of F1-F3)",
    "\u8bb0\u5fc6\u79ef\u7d2f\u4e0e\u6301\u7eed\u4f7f\u7528\u610f\u5411\u7684\u5173\u7cfb（H3b）": "Memory accumulation and continuance intention (H3b)",
    "\u6ce8：Spearman ρ = 0.850，p < 0.001（\u65f6\u95f4\u8f74\u884c\u6570）；ρ = 0.781，p = 0.002（\u66f4\u65b0\u9891\u6b21）。\u6570\u636e\u6765\u6e90：\u8bb0\u5fc6\u6307\u6807\u8868 × \u95ee\u5377 F \u91cf\u8868（link_id \u533f\u540d\u5173\u8054）。": "Note: Timeline length rho=.850, p<.001; update frequency rho=.781, p=.002; linked n=13. Associations are not causal.",
    "\u65f6\u95f4\u8f74\u65e5\u5fd7\u884c\u6570": "Timeline length", "\u8bb0\u5fc6\u66f4\u65b0\u9891\u6b21": "Memory-update frequency", "\u6837\u672c（N=13）": "Linked sample (N=13)",
    "\u6301\u7eed\u4f7f\u7528\u610f\u5411": "Continuance intention", "\u611f\u77e5\u6709\u7528\u6027": "Perceived usefulness", "\u611f\u77e5\u6613\u7528\u6027": "Perceived ease of use",
    "\u611f\u77e5\u4fe1\u4efb": "Perceived trust", "\u611f\u77e5\u98ce\u9669": "Perceived risk", "\u8bb0\u5fc6\u611f\u77e5": "Perceived memory",
    "0.70（\u5e38\u7528\u9608\u503c）": "0.70 (common reference)", "\u611f\u77e5\u98ce\u9669 α=0.403（\u91cf\u8868\u5185\u6db5\u8f83\u5bbd）": "Perceived risk alpha=.403 (do not interpret as a composite)",
    "\u95ee\u5377\u516d\u91cf\u8868\u4fe1\u5ea6（N=29）": "Reliability of six survey scales (N=29)",
    "\u6ce8：\u9664\u611f\u77e5\u98ce\u9669（α=0.403，\u91cf\u8868\u5185\u6db5\u8f83\u5bbd）\u5916，\u5404\u91cf\u8868 α \u5747\u9ad8\u4e8e 0.70。\u6570\u636e\u6765\u6e90：\u95ee\u5377 B/C/D/E/F/I；\u5206\u6790：01-\u95ee\u5377\u5206\u6790.py。": "Note: Perceived risk has alpha=.403 and is not interpreted as a coherent composite; other scales exceed .70. Source: valid survey responses.",
    "\u516d\u6784\u5ff5\u611f\u77e5\u5747\u503c（\u4e03\u70b9\u91cf\u8868，N=29）": "Mean levels of six perceived constructs (seven-point scales, N=29)",
    "\u6ce8：\u6570\u503c\u4e3a\u5404\u91cf\u8868\u9898\u76ee\u5f97\u5206\u7684\u5747\u503c。\u6570\u636e\u6765\u6e90：\u95ee\u5377 B/C/D/E/F/I；\u5206\u6790：01-\u95ee\u5377\u5206\u6790.py。": "Note: Values are respondent-level construct means. Perceived risk is shown descriptively despite low reliability.",
    "\u6bcf\u5929\u90fd\u5728\u7528": "Daily", "\u6bcf\u5468\u51e0\u6b21": "Several times a week", "\u5076\u5c14\u4f7f\u7528": "Occasionally", "\u5df2\u505c\u6b62\u4f7f\u7528": "Stopped using",
    "\u6709\u6548\u6837\u672c": "Valid sample", "\u7ea6 38% \u5df2\u505c\u6b62\u4f7f\u7528": "About 38% stopped using", "\u5de5\u4f5c\u574a\u6210\u5458\u5f53\u524d\u4f7f\u7528\u72b6\u6001（A1）": "Current use status among workshop participants (A1)",
    "\u6570\u636e\u6765\u6e90：\u95ee\u5377 A1（N=29，\u5254\u9664\u6d4b\u8c0e\u9879\u672a\u901a\u8fc7\u8005）。": "Source: survey A1 (N=29 after attention-check exclusion).",
    "\u7edf\u8ba1\u5468（2026 \u5e74）": "Study week (2026)", "\u59d4\u6258\u4e8b\u4ef6\u6570": "Delegation events", "\u59d4\u6258\u4e8b\u4ef6\u6309\u5468\u7684\u73af\u8282\u6784\u6210\u4e0e\u4f7f\u7528\u70ed\u5ea6": "Weekly delegation events by workflow stage",
    "\u6ce8：\u5de5\u4f5c\u574a\u540e\u9996\u6708\u4f7f\u7528\u6700\u6d3b\u8dc3，\u968f\u540e\u56de\u843d\u81f3\u7a33\u5b9a\u6c34\u5e73。\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868（327 \u6761\u59d4\u6258\u4e8b\u4ef6）。": "Note: Event volume was highest in the first post-workshop month and later stabilized. Source: 327 coded events.",
    "\u5404\u7528\u6237\u7684\u59d4\u6258\u4e8b\u4ef6\u89c4\u6a21\u4e0e\u7ed3\u679c\u6784\u6210": "Delegation-event volume and outcome composition by user", "\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868（\u6309 user_id \u6c47\u603b）。": "Source: usage-event data aggregated by pseudonymous user ID.",
    "\u603b\u65f6\u957f（min）": "Total time (min)", "\u4eba\u5de5\u4ecb\u5165\u6b21\u6570": "Human interventions", "\u4eba\u5de5\u4ecb\u5165\u65f6\u957f（min）": "Human intervention time (min)",
    "\u4ea7\u51fa\u8d28\u91cf（\u76f2\u8bc4，5 \u5206\u5236）": "Blind-rated output quality (1-5)", "\u5355\u667a\u80fd\u4f53": "Single agent", "\u591a\u667a\u80fd\u4f53": "Multi-agent",
    "\u4efb\u52a1 A\n\u68c0\u7d22\u6574\u7406\u578b": "Task A\nRetrieval and organization", "\u4efb\u52a1 B\n\u5206\u6790\u578b": "Task B\nAnalysis", "\u4efb\u52a1 C\n\u5199\u4f5c\u7efc\u5408\u578b": "Task C\nIntegrative writing",
    "\u4e09\u7c7b\u4efb\u52a1\u7684\u603b\u65f6\u957f：\u5355\u667a\u80fd\u4f53 vs \u591a\u667a\u80fd\u4f53": "Total time by task: single agent vs multi-agent",
    "\u6ce8：n=4，\u914d\u5bf9 Wilcoxon \u7b26\u53f7\u79e9\u68c0\u9a8c（\u4efb\u52a1 A/B：p=0.125，\u672a\u8fbe p<0.05，\u65b9\u5411\u4e00\u81f4、\u6548\u5e94\u91cf r≈0.91）；\u4efb\u52a1 C：p=0.875。\u6570\u636e\u6765\u6e90：\u5b9e\u9a8c\u6570\u636e\u8bb0\u5f55\u8868；\u5206\u6790：04-\u5bf9\u6bd4\u5b9e\u9a8c\u5206\u6790.py。": "Note: Four paired participants per task. Exact Wilcoxon p=.125 for Tasks A/B and .875 for Task C. Results are exploratory.",
    "\u4eba\u5de5\u4ecb\u5165\u6b21\u6570：\u5355\u667a\u80fd\u4f53 vs \u591a\u667a\u80fd\u4f53": "Human intervention count: single agent vs multi-agent",
    "\u6ce8：n=4，\u914d\u5bf9 Wilcoxon \u7b26\u53f7\u79e9\u68c0\u9a8c（\u4efb\u52a1 A：p=0.125；\u4efb\u52a1 B：p=0.25；\u4efb\u52a1 C：p=0.625）。\u6570\u636e\u6765\u6e90：\u5b9e\u9a8c\u6570\u636e\u8bb0\u5f55\u8868；\u5206\u6790：04-\u5bf9\u6bd4\u5b9e\u9a8c\u5206\u6790.py。": "Note: Four paired participants per task. Exact Wilcoxon p=.125, .250, and .625 for Tasks A-C, respectively.",
    "\u4eba\u5de5\u4ecb\u5165\u65f6\u957f：\u5355\u667a\u80fd\u4f53 vs \u591a\u667a\u80fd\u4f53": "Human intervention time: single agent vs multi-agent",
    "\u6ce8：n=4，\u914d\u5bf9 Wilcoxon \u7b26\u53f7\u79e9\u68c0\u9a8c（\u4efb\u52a1 A/B：p=0.125；\u4efb\u52a1 C：p=0.50）。\u6570\u636e\u6765\u6e90：\u5b9e\u9a8c\u6570\u636e\u8bb0\u5f55\u8868；\u5206\u6790：04-\u5bf9\u6bd4\u5b9e\u9a8c\u5206\u6790.py。": "Note: Four paired participants per task. Exact Wilcoxon p=.125 for Tasks A/B and .375 for Task C.",
    "\u4ea7\u51fa\u8d28\u91cf（\u53cc\u4eba\u76f2\u8bc4）：\u5355\u667a\u80fd\u4f53 vs \u591a\u667a\u80fd\u4f53": "Blind-rated output quality: single agent vs multi-agent",
    "\u6ce8：\u4ea7\u51fa\u8d28\u91cf\u4e3a\u4e24\u4f4d\u76f2\u8bc4\u8005\u5bf9\u76f8\u5173\u6027/\u51c6\u786e\u6027/\u7ed3\u6784/\u5b8c\u6574\u6027\u7684\u5e73\u5747\u5206；n=4，\u914d\u5bf9 Wilcoxon \u7b26\u53f7\u79e9\u68c0\u9a8c（\u4efb\u52a1 B：p=0.125，\u591a\u667a\u80fd\u4f53\u66f4\u9ad8）。\u6570\u636e\u6765\u6e90：\u5b9e\u9a8c\u6570\u636e\u8bb0\u5f55\u8868；\u5206\u6790：04-\u5bf9\u6bd4\u5b9e\u9a8c\u5206\u6790.py。": "Note: Quality is the mean of two blinded raters across four criteria; n=4 pairs per task. Task B exact p=.125. No non-inferiority claim is made.",
    "\u76f8\u5bf9\u589e\u76ca（%，\u6b63=\u66f4\u7701\u65f6/\u66f4\u5c11\u4ecb\u5165）": "Relative gain (positive = less time/intervention)", "\u591a\u667a\u80fd\u4f53\u76f8\u5bf9\u5355\u667a\u80fd\u4f53\u7684\u589e\u76ca（%）": "Relative multi-agent gains (%)",
    "\u6ce8：\u589e\u76ca =（\u5355−\u591a）/\u5355 × 100%。\u4efb\u52a1 A/B（\u53ef\u5206\u89e3、\u591a\u73af\u8282、\u9700\u6838\u67e5）\u589e\u76ca\u660e\u663e，\u4efb\u52a1 C（\u5355\u73af\u8282、\u5f3a\u4e3b\u89c2）\u589e\u76ca\u6d88\u5931。\u6570\u636e\u6765\u6e90：\u5b9e\u9a8c\u6570\u636e\u8bb0\u5f55\u8868。": "Note: Gain=(single-multi)/single x 100%. Descriptive pilot estimates; n=4 paired participants per task.",
    "\u914d\u5bf9\u4e2a\u4f53\u8f68\u8ff9：\u6bcf\u4f4d\u88ab\u8bd5\u7684\u603b\u65f6\u957f（\u5355 → \u591a\u667a\u80fd\u4f53）": "Paired participant trajectories: total time from single to multi-agent",
    "\u6ce8：\u7eff\u7ebf=\u591a\u667a\u80fd\u4f53\u66f4\u5feb，\u7ea2\u7ebf=\u591a\u667a\u80fd\u4f53\u66f4\u6162；\u6bcf\u4f4d\u88ab\u8bd5\u4e00\u6761\u8fde\u7ebf。\u6570\u636e\u6765\u6e90：\u5b9e\u9a8c\u6570\u636e\u8bb0\u5f55\u8868（n=4）。": "Note: Green indicates lower time with multi-agent; red indicates higher time. Each line represents one participant (n=4).",
    "\u603b\u65f6\u957f(min)": "Total time (min)", "\u4ecb\u5165\u6b21\u6570": "Intervention count", "\u4ecb\u5165\u65f6\u957f(min)": "Intervention time (min)", "\u4ea7\u51fa\u8d28\u91cf": "Output quality",
    "p \u503c": "p-value", "\u6548\u5e94\u91cf r（Wilcoxon \u8fd1\u4f3c）": "Effect size r (legacy approximation)", "\u5bf9\u6bd4\u5b9e\u9a8c\u5404\u6307\u6807\u7684\u6548\u5e94\u91cf\u4e0e\u663e\u8457\u6027": "Pilot effect sizes and p-values",
    "\u6ce8：\u4efb\u52a1 A/B \u65f6\u95f4\u4e0e\u4ecb\u5165\u7c7b\u6307\u6807 r≈0.91、p>0.05（\u5c0f\u6837\u672c n=4），\u7ed3\u8bba\u4e3a\u65b9\u5411\u6027\u652f\u6301。\u6570\u636e\u6765\u6e90：04-\u5bf9\u6bd4\u5b9e\u9a8c\u5206\u6790.csv。": "Note: Legacy standardized-r display retained from the original figure. Exact paired results are reported in the analysis output; n=4 per task.",
    "DDA \u4e09\u9636\u6bb5\u6a21\u578b：\u90e8\u7f72 → \u59d4\u6258 → \u6c89\u6dc0": "DDA model: Deploy - Delegate - Accumulate", "\u628a“\u7cfb\u7edf\u7ea7\u6280\u672f\u91c7\u7eb3”\u63a8\u8fdb\u4e3a“\u4efb\u52a1\u7ea7\u59d4\u6258\u51b3\u7b56”": "From system-level adoption to task-level delegation decisions",
    "\u90e8\u7f72\nDeploy": "DEPLOY", "\u59d4\u6258\nDelegate": "DELEGATE", "\u6c89\u6dc0\nAccumulate": "ACCUMULATE",
    "\u4fe1\u4efb\u6269\u5927\u59d4\u6258\u8fb9\u754c、\n\u6301\u7eed\u4f7f\u7528": "", "\u964d\u4f4e\u8f6c\u6362\u6210\u672c": "Reduce repeated explanation",
    "\u6ce8：\u4f9d\u636e\u7814\u7a76\u62a5\u544a 2.6 \u7ed8\u5236；\u56db\u4e2a\u547d\u9898\u5206\u522b\u5bf9\u5e94\u5047\u8bbe H1—H4。": "Note: The DDA model organizes testable propositions; current evidence is an initial probe, not definitive validation.",
    "“\u7edf\u7b79—\u6267\u884c—\u6838\u67e5”\u4e09\u667a\u80fd\u4f53\u534f\u4f5c\u67b6\u6784": "Orchestrator-worker-checker multi-agent architecture", "orchestrator-workers × evaluator-optimizer：\u663e\u5f0f\u9a8c\u6536\u56de\u8def＋\u4e2a\u4eba\u8bb0\u5fc6\u5c42": "Explicit verification loop with a personal memory layer",
    "\u7528\u6237": "User", "\u7edf\u7b79\u8005\nOrchestrator": "Orchestrator", "\u6267\u884c\u8005\nWorker": "Worker", "\u6838\u67e5\u8005\nChecker": "Checker", "\u8bb0\u5fc6\u7cfb\u7edf Memory": "Memory system",
    "\u59d4\u6258\u9700\u6c42": "Delegation request", "\u4ea7\u51fa\u4ea4\u4ed8": "Delivered output", "① \u4efb\u52a1\u5206\u89e3": "1 Task decomposition", "② \u5206\u914d\u5b50\u4efb\u52a1": "2 Assign subtasks", "③ \u4ea7\u51fa\u9001\u68c0": "3 Submit output", "④ \u9a8c\u6536\u56de\u704c": "4 Verification feedback", "⑤ \u8bb0\u5fc6\u6c89\u6dc0": "5 Memory update",
    "\u6ce8：\u4f9d\u636e\u7814\u7a76\u62a5\u544a 1.1 \u4e0e 2.1 \u7ed8\u5236；①—⑤\u4e3a\u4e00\u6b21\u59d4\u6258\u7684\u534f\u4f5c\u987a\u5e8f。": "Note: Steps 1-5 show the collaboration sequence for one delegated task.",
    "\u7814\u7a76\u8bbe\u8ba1：\u4e09\u89d2\u6d4b\u91cf（\u4e09\u4e2a\u5b50\u7814\u7a76\u6536\u655b）": "Research design: triangulation across three studies", "\u5171\u540c\u7406\u8bba\u6846\u67b6（DDA \u6a21\u578b）\u4e0e\u5171\u540c\u4eba\u5de5\u5236\u54c1（\u6846\u67b6\u4e0e\u5411\u5bfc）": "Shared DDA framework and evaluated research artifact",
    "\u7814\u7a761\n\u5236\u54c1\u53ef\u7528\u6027": "Study 1\nArtifact usability", "\u7814\u7a762\n\u59d4\u6258\u884c\u4e3a\u4e0e\u6301\u7eed\u4f7f\u7528": "Study 2\nDelegation and continuance", "\u7814\u7a763\n\u5355 vs \u591a\u667a\u80fd\u4f53": "Study 3\nSingle vs multi-agent", "\u4e09\u89d2\u6d4b\u91cf\u7efc\u5408": "Triangulated synthesis",
    "\u6ce8：\u4f9d\u636e\u7814\u7a76\u62a5\u544a 3.1 \u7ed8\u5236；\u4e09\u4e2a\u5b50\u7814\u7a76\u4ece\u4e0d\u540c\u8bc1\u636e\u6e90\u6536\u655b\u5230\u5bf9\u7814\u7a76\u95ee\u9898\u7684\u56de\u7b54。": "Note: Three studies contribute distinct evidence; convergence does not remove each design's limitations.",
    "\u7406\u8bba\u6574\u5408：\u4efb\u52a1\u7ea7\u59d4\u6258\u51b3\u7b56\u7684\u673a\u5236\u89e3\u91ca": "Theoretical integration for task-level delegation decisions", "DDA \u4e09\u9636\u6bb5\u6a21\u578b": "DDA three-stage model",
    "\u56db\u7c7b\u7406\u8bba\u6574\u5408\u4e3a DDA \u6a21\u578b，\u5bf9\u5e94\u56db\u4e2a\u53ef\u8bc1\u4f2a\u547d\u9898 P1—P4": "Four theoretical lenses inform four falsifiable DDA propositions (P1-P4)",
    "\u6ce8：\u4f9d\u636e\u7814\u7a76\u62a5\u544a 2.4—2.6 \u7ed8\u5236。": "Note: Drawn from the theoretical framework in Sections 2.4-2.6.",
    "\u4efb\u52a1—\u6280\u672f\u5339\u914d TTF": "Task-technology fit", "\u54ea\u4e9b\u4efb\u52a1\u503c\u5f97\u59d4\u6258": "Which tasks fit delegation", "\u4ea4\u6613\u6210\u672c\u7406\u8bba": "Transaction cost theory", "\u59d4\u6258\u8fd8\u662f\u81ea\u5236（\u673a\u5236）": "Delegate or retain", "\u671f\u671b\u786e\u8ba4\u6a21\u578b ECT": "Expectation-confirmation", "\u6301\u7eed\u4f7f\u7528（\u65f6\u95f4\u7ef4\u5ea6）": "Continued use over time", "\u7b97\u6cd5\u538c\u6076": "Algorithm aversion", "\u59d4\u6258\u4e2d\u7684\u884c\u4e3a\u504f\u5dee": "Behavior following error",
    "\u59d4\u6258\u8fb9\u754c\u7684\u4f4d\u7f6e\u7531\u4e09\u7c7b\u4efb\u52a1\u7ed3\u6784\u5c5e\u6027\u5171\u540c\u51b3\u5b9a": "Three task attributes shape the delegation boundary", "\u59d4\u6258\u8fb9\u754c": "Delegation boundary", "\u4efb\u52a1\u7ea7\n“\u81ea\u5236—\u5916\u8d2d”\u51b3\u7b56": "Task-level\nmake-or-delegate decision",
    "\u8f93\u51fa\u53ef\u9a8c\u8bc1\u6027": "Output verifiability", "\u7ed3\u679c\u53ef\u5feb\u901f\u6838\u5bf9": "Output can be checked", "\u540e\u679c\u53ef\u9006\u6027": "Consequence reversibility", "\u9519\u8bef\u53ef\u91cd\u6765": "Errors can be reversed", "\u4ef7\u503c\u7f16\u7801\u7a0b\u5ea6": "Value-laden judgment", "\u627f\u8f7d\u76ee\u6807\u4e0e\u4ef7\u503c\u5224\u65ad\u7684\u591a\u5c11": "Extent of goals and values encoded",
    "\u53ef\u9a8c\u8bc1\u6027↑、\u53ef\u9006\u6027↑、\u4ef7\u503c\u7f16\u7801↓ → \u59d4\u6258\u7387↑（\u4e2d\u95f4\u73af\u8282）": "Higher verifiability and reversibility, with less value judgment, predict greater delegation",
    "\u6ce8：\u4f9d\u636e\u7814\u7a76\u62a5\u544a 4.2.1 \u4e0e 5.2 \u7ed8\u5236；\u4efb\u52a1\u7ed3\u6784\u5c5e\u6027\u76f8\u5bf9\u7a33\u5b9a，\u6545\u59d4\u6258\u8fb9\u754c\u77ed\u671f\u7a33\u5b9a。": "Note: Proposed task-attribute mechanism; the current study provides descriptive rather than causal evidence.",
    "\u7814\u7a76\u6838\u5fc3\u7ed3\u679c\u6c47\u603b": "Core research results", "\u7814\u7a76": "Study", "\u6307\u6807": "Measure", "\u7ed3\u679c": "Result", "\u68c0\u9a8c / \u5224\u5b9a": "Test / interpretation",
    "\u7814\u7a761 \u90e8\u7f72": "Study 1: Deployment", "\u5b8c\u6210\u7387": "Completion rate", "H1 \u9608\u503c ≥ 80%，\u8fbe\u6210": "Operational target met", "\u5e73\u5747\u90e8\u7f72\u8017\u65f6": "Mean deployment time", "\u5b8c\u6210\u8005\u53e3\u5f84": "Completers only", "SUS \u5747\u503c": "Mean SUS", "\u5747 ≥ 68 \u53ef\u7528\u9608\u503c": "Descriptive; 68 is a reference",
    "\u7814\u7a762 \u59d4\u6258": "Study 2: Delegation", "\u4e03\u73af\u8282\u59d4\u6258\u7387\u5dee\u5f02": "Delegation differs across stages", "p < 0.001，\u652f\u6301 H2": "p<.001; supports within-sample difference", "\u9996\u6b21\u5931\u8d25\u524d\u540e 14 \u5929\u59d4\u6258\u9891\u7387": "Rate before/after first failure", "0.135 → 0.060 \u6b21/\u5929": "0.122 -> 0.051 events/day", "W = 80，p < 0.001，\u652f\u6301 H3a": "User-level W=1.5, exact p=.0015", "\u65f6\u95f4\u8f74\u884c\u6570 × \u6301\u7eed\u4f7f\u7528\u610f\u5411": "Timeline length x continuance", "p < 0.001，\u652f\u6301 H3b": "p<.001; observational association", "\u66f4\u65b0\u9891\u6b21 × \u6301\u7eed\u4f7f\u7528\u610f\u5411": "Update frequency x continuance", "p = 0.002，\u652f\u6301 H3b": "p=.002; observational association",
    "\u7814\u7a763 \u5bf9\u6bd4": "Study 3: Comparison", "\u603b\u65f6\u957f（\u4efb\u52a1 A）": "Total time (Task A)", "r ≈ 0.91，\u65b9\u5411\u6027\u652f\u6301 H4": "Exact p=.125; exploratory", "\u4eba\u5de5\u4ecb\u5165\u6b21\u6570（\u4efb\u52a1 A）": "Interventions (Task A)", "14.5 → 7.0 \u6b21": "14.5 -> 7.0", "\u4ea7\u51fa\u8d28\u91cf（\u4efb\u52a1 B）": "Output quality (Task B)", "3.50 → 4.31 \u5206": "3.50 -> 4.31", "\u591a\u667a\u80fd\u4f53\u4e0d\u4f4e，\u8d28\u91cf\u4e0d\u964d": "Exact p=.125; no equivalence claim",
    "\u6ce8：\u7814\u7a763 \u56e0\u6bcf\u6761\u4ef6 n=4，Wilcoxon \u68c0\u9a8c\u672a\u8fbe p<0.05，\u62a5\u544a\u8868\u8ff0\u4e3a“\u65b9\u5411\u6027\u652f\u6301、\u6548\u5e94\u91cf r≈0.91”。": "Note: Study 3 has four paired participants per task and is interpreted as exploratory; non-significance is not equivalence.",
    "\u5b8c\u6210\u90e8\u7f72（4\u4eba）": "Completed (4)", "\u672a\u5b8c\u6210（1\u4eba）": "Not completed (1)", "（\u653e\u5f03）": "(stopped)", "\u9636\u6bb5": "Stage", "\u9ad8\u59d4\u6258\u73af\u8282（\u68c0\u7d22/\u6574\u7406/\u751f\u6210）": "Higher delegation: retrieval, organization, generation", "\u4e2d\u59d4\u6258\u73af\u8282（\u5206\u6790/\u6267\u884c）": "Moderate delegation: analysis, execution", "\u4f4e\u59d4\u6258\u73af\u8282（\u754c\u5b9a/\u51b3\u7b56）": "Lower delegation: definition, decision", "\u5931\u8d25\u4e8b\u4ef6": "Failed event", " \u6b21": " events", "\u7ebf\u6027\u62df\u5408（r = ": "Linear fit (r = ", " \u4eba": " users", "\u4efb\u52a1 ": "Task ", "\u5747\u503c ": "Mean ", ", \u9891\u7387 ": ", frequency ",
    "\u9700\u6c42·\u6838\u67e5·\u7ec8\u68c0": "Requirements, checking, final review", "\u4efb\u52a1\u5206\u89e3·\u7ed3\u679c\u7efc\u5408·\u9a8c\u6536\u56de\u704c": "Task decomposition, integration, verification feedback",
    "\u5355\u4e00\u804c\u8d23·\u5de5\u5177\u8c03\u7528": "Bounded role and tool use", "\u4ea7\u51fa\u6bd4\u5bf9·\u9a8c\u6536": "Output comparison and acceptance",
    "\u70ed\u8bb0\u5fc6 / \u51b7\u8bb0\u5fc6 / \u65f6\u95f4\u8f74\u65e5\u5fd7（\u53ef\u8bfb·\u53ef\u5ba1\u8ba1）": "Hot memory / cold memory / timeline (readable and auditable)",
    "\u90e8\u7f72—\u59d4\u6258—\u6c89\u6dc0（P1—P4）": "Deploy - Delegate - Accumulate (P1-P4)",
    "P1 \u90e8\u7f72\u89e6\u53d1\u59d4\u6258": "P1 Deployment enables delegation", "\u90e8\u7f72\u6210\u672c\u662f\u59d4\u6258\n\u884c\u4e3a\u7684\u9996\u8981\u95e8\u69db": "Deployment burden is an initial\nbarrier to delegation",
    "P2 \u59d4\u6258\u8fb9\u754c\u7684\u5f62\u6210": "P2 Delegation boundary formation", "\u80fd\u529b\u611f\u77e5×\u4fe1\u4efb×\u4ea4\u4e92\u6210\u672c\n\u4e09\u5143\u5224\u65ad；\u5931\u8d25\u7ecf\u7b97\u6cd5\u538c\u6076\n\u538b\u4f4e\u59d4\u6258\u7387": "Perceived capability, trust, and interaction cost\nshape allocation; failures may\nreduce later delegation",
    "P3 \u6c89\u6dc0\u7d2f\u79ef\u4fe1\u4efb": "P3 Accumulation and continuance", "\u8bb0\u5fc6\u5f62\u6210\u8def\u5f84\u4f9d\u8d56，\u6295\u5165\n\u8d8a\u6df1\u8d8a\u96be\u79bb\u5f00、\u8d8a\u613f\u6258\u4ed8": "Memory may improve fit and create\nrelationship-specific investment",
    "P4 \u67b6\u6784\u7684\u8fb9\u754c": "P4 Architectural boundary", "\u53ef\u5206\u89e3\u591a\u73af\u8282\u4efb\u52a1\u591a\u667a\u80fd\u4f53\n\u5360\u4f18；\u5355\u73af\u8282\u5f3a\u4e3b\u89c2\n\u4efb\u52a1\u65e0\u4f18\u52bf": "Multi-agent coordination may help on\ndecomposable tasks, but not necessarily\non judgment-heavy tasks",
    "SBDP\n\u81ea\u4e3e\u5f0f\u90e8\u7f72\u534f\u8bae": "SBDP\nDeployment protocol", "\u8bb0\u5fc6＝\n\u5173\u7cfb\u4e13\u7528\u6027\u6295\u8d44": "Memory as\nrelationship-specific investment",
    "\u90e8\u7f72\u53ef\u7528\u6027\u6d4b\u8bd5 · H1": "Deployment usability test - H1", "\u95ee\u5377＋\u8bbf\u8c08＋\u65e5\u5fd7 · H2、H3": "Survey, interview, and logs - H2/H3",
    "\u53d7\u63a7\u5bf9\u6bd4\u5b9e\u9a8c · H4": "Controlled comparison - H4", "\u6536\u655b\u56de\u7b54 RQ1—RQ3": "Joint evidence for RQ1-RQ3",
    "\u6267\u884c\u6743\u9650·\u5de5\u5177\u94fe·\u8eab\u4efd": "Permissions, tools, and identity", "\u504f\u597d·\u76ee\u6807·\u5173\u952e\u4eba\u7269": "Preferences, goals, and key people",
    "\u90e8\u7f72\u4e0e\u8ba4\u8bc6\u7528\u6237\u4e00\u6b21\u5b8c\u6210": "Deployment and user initialization in one process", "\u4efb\u52a1\u7ea7“\u81ea\u5236—\u5916\u8d2d”\u51b3\u7b56": "Task-level make-or-delegate decision",
    "\u603b\u65f6\u957f": "Total time", "\u4ecb\u5165\u65f6\u957f": "Intervention time", "\u6807\u8bb0：\u4efb\u52a1 ｜ \u989c\u8272：\u6307\u6807": "Marker: task | Color: measure",
}


def translate_visible_text(fig):
    # Matplotlib creates tick-label and table Text artists lazily on the first draw.
    fig.canvas.draw()
    def translated_text(value):
        translated = TRANSLATIONS.get(value, value)
        if translated == value:
            for source, target in sorted(TRANSLATIONS.items(), key=lambda item: len(item[0]), reverse=True):
                if source in translated:
                    translated = translated.replace(source, target)
        return translated

    for text_object in fig.findobj(match=matplotlib.text.Text):
        value = text_object.get_text()
        text_object.set_text(translated_text(value))
    for ax in fig.axes:
        x_labels = [translated_text(item.get_text()) for item in ax.get_xticklabels()]
        y_labels = [translated_text(item.get_text()) for item in ax.get_yticklabels()]
        if any(re.search(r"[\u4e00-\u9fff]", item.get_text()) for item in ax.get_xticklabels()):
            ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator(ax.get_xticks()))
            ax.xaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(x_labels))
        if any(re.search(r"[\u4e00-\u9fff]", item.get_text()) for item in ax.get_yticklabels()):
            ax.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(ax.get_yticks()))
            ax.yaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(y_labels))
        for table in ax.tables:
            for cell in table.get_celld().values():
                cell_text = cell.get_text()
                cell_text.set_text(translated_text(cell_text.get_text()))
    fig.canvas.draw()
    remaining = sorted({obj.get_text() for obj in fig.findobj(match=matplotlib.text.Text) if re.search(r"[\u4e00-\u9fff]", obj.get_text())})
    if remaining:
        raise ValueError(f"Untranslated visible text: {remaining}")
    fig.canvas.draw()

# ------------------------------------------------------------------

# ------------------------------------------------------------------
def load():
    q = pd.read_csv(Q_CSV, encoding="utf-8-sig")
    q = q[pd.to_numeric(q["J2"], errors="coerce") == 2].copy()      # N=29
    log = pd.read_csv(L_CSV, encoding="utf-8-sig")
    reverse_maps = {
        "stage": {value: key for key, value in TRANSLATIONS.items() if key in STAGES},
        "outcome": {value: key for key, value in TRANSLATIONS.items() if key in OUTCOMES},
        "fail_reason": {value: key for key, value in TRANSLATIONS.items() if key in REASONS},
        "error_exposure": {value: key for key, value in TRANSLATIONS.items() if key in EXPOSURES},
    }
    reverse_maps.update({
        "coderB_stage": reverse_maps["stage"],
        "coderB_outcome": reverse_maps["outcome"],
        "coderB_fail_reason": reverse_maps["fail_reason"],
        "coderB_error_exposure": reverse_maps["error_exposure"],
    })
    for column, mapping in reverse_maps.items():
        log[column] = log[column].replace(mapping)
    # Public English inputs may already contain stage labels without the line
    # breaks used in figure display text. Normalize them back to the internal
    # canonical keys before aggregation.
    english_stage_map = {
        TRANSLATIONS[stage].replace("\n", " "): stage for stage in STAGES
    }
    for column in ("stage", "coderB_stage"):
        log[column] = log[column].replace(english_stage_map)
    log["event_date"] = pd.to_datetime(log["event_date"], errors="coerce")
    exp = pd.read_csv(E_CSV, encoding="utf-8-sig")
    rcols = [c for c in exp.columns if c.startswith("r") and "_" in c]
    exp["quality_score"] = exp[rcols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    mem = pd.read_csv(M_CSV, encoding="utf-8-sig")
    sus = pd.read_csv(SUS_CSV, encoding="utf-8-sig")
    sus["completion"] = sus["completion"].replace({"Yes": "\u662f", "No": "\u5426"})
    return q, log, exp, mem, sus


def new_fig(w=10, h=6):
    return plt.figure(figsize=(w, h), facecolor="white")


def style(ax, grid="y", xticks=True):
    """\u5b66\u672f\u5750\u6807\u8f74：\u767d\u5e95、\u9ed1\u8272\u7ec6\u6846、\u5411\u5185\u523b\u5ea6、\u6d45\u7070\u7f51\u683c"""
    ax.set_facecolor("white")
    for s in ax.spines.values():
        s.set_color(INK)
        s.set_linewidth(0.9)
    ax.tick_params(colors=INK, labelsize=11, length=4, width=0.9)
    if grid == "y":
        ax.grid(axis="y", color=GRIDC, lw=0.7, alpha=0.55, ls=(0, (2, 3)))
        ax.set_axisbelow(True)
    elif grid == "both":
        ax.grid(axis="both", color=GRIDC, lw=0.7, alpha=0.55, ls=(0, (2, 3)))
        ax.set_axisbelow(True)
    if not xticks:
        ax.set_xticks([])


def set_title(ax, text, fs=14.5, pad=12, weight="bold"):
    """Set a left-aligned figure title."""
    ax.set_title(text, fontsize=fs, color=INK, pad=pad, loc="left", fontweight=weight)


def note(fig, text, x=0.015, y=0.012, fs=9):
    """\u56fe\u6ce8：\u5de6\u4e0b\u89d2\u7070\u8272\u5c0f\u5b57，\u5b66\u672f\u89c4\u8303"""
    fig.text(x, y, text, fontsize=fs, color=LGRAY, ha="left", va="bottom")


def bval(ax, xs, hs, color, width=0.6, edge=INK, lw=0.8, z=3, alpha=1.0, hatch=None, bottom=0):
    """\u5b9e\u5fc3\u67f1（\u9ed1\u63cf\u8fb9）"""
    ax.bar(xs, hs, width=width, bottom=bottom, color=color, edgecolor=edge,
           linewidth=lw, zorder=z, alpha=alpha, hatch=hatch)


def barh(ax, ys, hs, color, height=0.6, edge=INK, lw=0.8, z=3, alpha=1.0, left=0, hatch=None):
    ax.barh(ys, hs, height=height, left=left, color=color, edgecolor=edge,
            linewidth=lw, zorder=z, alpha=alpha, hatch=hatch)


def valtxt(ax, x, v, fs=11.5, dy=None, fmt="{:.2f}", color=INK, ha="center", weight="normal"):
    if dy is None:
        dy = abs(v) * 0.04 + 0.02
    ax.text(x, v + dy, fmt.format(v), ha=ha, va="bottom", fontsize=fs, color=color,
            fontweight=weight, zorder=6)


def box(ax, xy, w, h, text, fc="white", ec=INK, fs=12, lw=1.0, weight="normal",
        sub=None, sub_fs=10, z=2, align="center", tc=INK):
    """\u6d41\u7a0b/\u6982\u5ff5\u56fe\u65b9\u6846：\u767d\u5e95\u6216\u6d45\u8272\u586b\u5145 + \u9ed1\u8272\u7ec6\u8fb9\u6846"""
    x, y = xy
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, facecolor=fc, edgecolor=ec,
                           linewidth=lw, zorder=z))
    if sub:
        ax.text(x, y + h * 0.13, text, ha="center", va="center", fontsize=fs,
                color=tc, zorder=z + 1, fontweight=weight)
        ax.text(x, y - h * 0.16, sub, ha="center", va="center", fontsize=sub_fs,
                color=GRAY, zorder=z + 1)
    else:
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc,
                zorder=z + 1, fontweight=weight)


def arr(ax, p1, p2, color=INK, lw=1.5, style="-|>", ms=13, ls="-", shrinkA=1, shrinkB=1, z=2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms,
                                 linewidth=lw, color=color, linestyle=ls,
                                 shrinkA=shrinkA, shrinkB=shrinkB, zorder=z))


def save(fig, name, dpi=220, tight=True):
    translate_visible_text(fig)
    match = re.match(r"(\d{2})-", name)
    if not match:
        raise ValueError(f"Figure filename has no numeric prefix: {name}")
    output_name = OUTPUT_NAMES[int(match.group(1))]
    fig.savefig(os.path.join(OUT, output_name), dpi=max(dpi, 300), bbox_inches="tight" if tight else None,
                facecolor="white")
    plt.close(fig)
    print("  [OK]", output_name)


# ==================================================================

# ==================================================================
def fig_01_dashboard(sus):
    """07 \u90e8\u7f72\u53ef\u7528\u6027\u6d4b\u8bd5\u7ed3\u679c（\u56db\u5b50\u56fe）"""
    fig = new_fig(11.5, 8.0)
    comp = (sus["completion"] == "\u662f").sum()
    total = len(sus)

    ax = fig.add_axes([0.06, 0.57, 0.26, 0.33])
    style(ax, grid=False); ax.set_aspect("equal")
    ax.pie([comp, total - comp], startangle=90, counterclock=False,
           colors=[BLUE, LIGHTG],
           wedgeprops=dict(width=0.32, edgecolor=INK, linewidth=1.2))
    ax.text(0, 0.14, f"{comp / total * 100:.0f}%", ha="center", va="center",
            fontsize=26, color=INK, fontweight="bold")
    ax.text(0, -0.12, "\u5b8c\u6210\u7387（4/5）", ha="center", va="center", fontsize=11.5, color=INK)
    ax.text(0, -0.30, "\u9608\u503c ≥ 80%", ha="center", va="center", fontsize=10, color=GRAY)
    set_title(ax, "（a）\u90e8\u7f72\u5b8c\u6210\u7387", fs=13)

    ax = fig.add_axes([0.40, 0.57, 0.54, 0.33])
    style(ax)
    sus = sus.sort_values("sus_score")
    names = sus["subject"].tolist()
    colors = [BLUE if s == "\u662f" else RED for s in sus["completion"]]
    y = np.arange(len(names))
    barh(ax, y, sus["sus_score"], colors, height=0.55)
    for i, (sc, c) in enumerate(zip(sus["sus_score"], colors)):
        ax.text(sc + 1.5, i, f"{sc}", va="center", fontsize=11.5, color=INK)
    ax.axvline(68, color=RED, lw=1.2, ls="--")
    ax.text(68, len(names) + 0.3, "68（\u53ef\u7528\u9608\u503c）", fontsize=10, color=RED, ha="center")
    ax.set_yticks(y); ax.set_yticklabels(names)
    ax.set_ylim(-0.6, len(names) + 0.8)
    ax.set_xlim(0, 95)
    ax.set_xlabel("SUS \u5f97\u5206", fontsize=12)
    set_title(ax, "（b）SUS \u7cfb\u7edf\u53ef\u7528\u6027\u5f97\u5206", fs=13)

    ax = fig.add_axes([0.06, 0.045, 0.42, 0.42])
    style(ax)
    sus_t = sus.sort_values("time_min")
    x = np.arange(len(sus_t))
    bval(ax, x, sus_t["time_min"], BLUE, width=0.5)
    for xi, v, s in zip(x, sus_t["time_min"], sus_t["subject"]):
        tag = "（\u653e\u5f03）" if sus_t.loc[sus_t["subject"] == s, "completion"].iloc[0] == "\u5426" else ""
        ax.text(xi, v + 1.2, f"{v}{tag}", ha="center", fontsize=11, color=INK)
    ax.set_xticks(x); ax.set_xticklabels(sus_t["subject"])
    ax.set_ylim(0, 52)
    ax.set_ylabel("\u5206\u949f", fontsize=12)
    set_title(ax, "（c）\u72ec\u7acb\u90e8\u7f72\u8017\u65f6", fs=13)

    ax = fig.add_axes([0.53, 0.045, 0.41, 0.42])
    style(ax)
    sus_h = sus.sort_values("help_points")
    x = np.arange(len(sus_h))
    bval(ax, x, sus_h["help_points"], ORANGE, width=0.5)
    for xi, v in zip(x, sus_h["help_points"]):
        ax.text(xi, v + 0.25, f"{v}", ha="center", fontsize=11.5, color=INK)
    ax.set_xticks(x); ax.set_xticklabels(sus_h["subject"])
    ax.set_ylim(0, 5.6)
    ax.set_ylabel("\u6b21\u6570", fontsize=12)
    set_title(ax, "（d）\u90e8\u7f72\u6c42\u52a9\u70b9", fs=13)
    fig.suptitle("\u7814\u7a761 \u81ea\u4e3e\u5f0f\u90e8\u7f72\u534f\u8bae（SBDP）\u53ef\u7528\u6027\u6d4b\u8bd5\u7ed3\u679c", fontsize=15, y=0.99, x=0.06,
                 ha="left", fontweight="bold")
    note(fig, "\u6ce8：S1—S3、S5 \u72ec\u7acb\u5b8c\u6210\u90e8\u7f72；S4 \u4e8e 42 min \u653e\u5f03。\u5b8c\u6210\u8005\u8017\u65f6 26—34 min（M=29.5），"
              "SUS 68—76（M=72.25）。\u6570\u636e\u6765\u6e90：03-\u5df2\u6536\u96c6\u6570\u636e/\u90e8\u7f72\u53ef\u7528\u6027\u6d4b\u8bd5.csv。")
    save(fig, "07-\u90e8\u7f72\u53ef\u7528\u6027\u6d4b\u8bd5\u7ed3\u679c.png")


def fig_02_sus_grading(sus):
    """08 SUS \u5f97\u5206\u4e0e\u53ef\u7528\u6027\u5206\u7ea7"""
    fig = new_fig(10, 6.0)
    ax = fig.add_axes([0.13, 0.16, 0.80, 0.74])
    style(ax, grid="both")
    zones = [(0, 51, RED, "\u5dee"), (51, 68, ORANGE, "\u52c9\u5f3a\u53ef\u7528"),
             (68, 85, GOLD, "\u53ef\u7528"), (85, 101, GREEN, "\u4f18\u79c0")]
    for lo, hi, c, lab in zones:
        ax.axvspan(lo, hi, color=matplotlib.colors.to_rgba(c, 0.12), zorder=0)
        ax.text((lo + hi) / 2, -0.9, lab, ha="center", fontsize=11, color=INK)
    sus = sus.sort_values("sus_score")
    y = np.arange(len(sus))
    colors = [BLUE if s == "\u662f" else RED for s in sus["completion"]]
    ax.barh(y, sus["sus_score"], height=0.55, color=LIGHTB, edgecolor=INK, lw=0.8, zorder=2)
    for yi, (_, r), c in zip(y, sus.iterrows(), colors):
        ax.scatter(r["sus_score"], yi, s=52, color=c, edgecolors=INK, linewidths=1.0, zorder=4)
        ax.text(r["sus_score"] + 3, yi, f"{r['sus_score']}", va="center", fontsize=11.5, color=INK)
    ax.axvline(68, color=RED, lw=1.3, ls="--", zorder=5)
    ax.text(68, len(sus) + 0.25, "68（\u53ef\u7528\u9608\u503c）", fontsize=10, color=RED, ha="center")
    ax.set_yticks(y); ax.set_yticklabels(sus["subject"])
    ax.set_ylim(-1.2, len(sus) + 0.7)
    ax.set_xlim(0, 103)
    ax.set_xlabel("SUS \u5f97\u5206", fontsize=12)
    set_title(ax, "\u90e8\u7f72\u88ab\u8bd5\u7684 SUS \u5f97\u5206\u4e0e\u53ef\u7528\u6027\u5206\u7ea7", fs=15)
    handles = [mpatches.Patch(color=BLUE, label="\u5b8c\u6210\u90e8\u7f72（4\u4eba）"),
               mpatches.Patch(color=RED, label="\u672a\u5b8c\u6210（1\u4eba）")]
    ax.legend(handles=handles, loc="lower right", fontsize=10.5, frameon=True,
              edgecolor=INK, framealpha=1.0)
    note(fig, "\u6ce8：\u5b8c\u6210\u8005 SUS \u5747 ≥ 68，\u5904\u4e8e“\u53ef\u7528”\u533a\u95f4；\u672a\u5b8c\u6210\u8005 S4=42。"
              "\u6570\u636e\u6765\u6e90：03-\u5df2\u6536\u96c6\u6570\u636e/\u90e8\u7f72\u53ef\u7528\u6027\u6d4b\u8bd5.csv。")
    save(fig, "08-SUS\u5f97\u5206\u4e0e\u53ef\u7528\u6027\u5206\u7ea7.png")


def fig_03_sbdp_flow():
    """06 SBDP \u516d\u9636\u6bb5\u90e8\u7f72\u6d41\u7a0b"""
    fig = new_fig(12, 6.6)
    ax = fig.add_axes([0.02, 0.05, 0.96, 0.88]); ax.set_axis_off()
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    steps = ["\u4e24\u8f6e\u4fe1\u606f\u6536\u96c6", "\u521b\u5efa\u5165\u53e3\u6587\u4ef6", "\u521b\u5efa\u8bb0\u5fc6\u76ee\u5f55", "\u5199\u5165\u8bb0\u5fc6\u6863\u6848", "\u5b8c\u6210\u5ba3\u544a", "\u6301\u7eed\u4f7f\u7528"]
    subs = ["\u914d\u7f6e\u53c2\u6570＋Bootstrap\u91c7\u8bbf", "VS Code＋Copilot \u73af\u5883", "\u8bb0\u5fc6\u76ee\u5f55\u7ed3\u6784",
            "profile/priorities \u7b49\u521d\u59cb\u5316", "\u96f6\u4ee3\u7801·\u53ef\u5ba1\u8ba1", "\u65f6\u95f4\u8f74\u65e5\u5fd7\u79ef\u7d2f"]
    # Wrap long labels so each stage remains inside its box.
    steps = ["Two-round\ninformation collection", "Create\nentry file", "Create memory\ndirectory",
             "Write memory\nprofiles", "Confirm\ncompletion", "Continued\nuse"]
    subs = ["Configuration +\nbootstrap interview", "VS Code + Copilot\nenvironment", "Memory directory\nstructure",
            "Initialize profile\nand priorities", "No-code and\nauditable", "Timeline log\naccumulation"]
    fills = [LIGHTB, LIGHTB, LIGHTB, LIGHTB, LIGHTB, LIGHTB]
    xs = np.linspace(9, 91, 6)
    y0 = 56
    for i, (s, sub, x) in enumerate(zip(steps, subs, xs)):
        box(ax, (x, y0), 14, 24, s, fc=fills[i], fs=11.2, weight="bold", sub=sub, sub_fs=8.8)
        ax.text(x, y0 + 17.5, f"Stage {i + 1}", ha="center", fontsize=10.5, color=GRAY)
        if i < 5:
            arr(ax, (x + 7.1, y0), (xs[i + 1] - 7.1, y0), lw=1.6, ms=14)

    box(ax, (24, 18), 26, 15, "\u7b2c\u4e00\u8f6e：\u90e8\u7f72\u53c2\u6570", fc="white", fs=11.5, sub="\u6267\u884c\u6743\u9650·\u5de5\u5177\u94fe·\u8eab\u4efd", sub_fs=9.5)
    box(ax, (50, 18), 26, 15, "\u7b2c\u4e8c\u8f6e：Bootstrap \u91c7\u8bbf", fc="white", fs=11.5, sub="\u504f\u597d·\u76ee\u6807·\u5173\u952e\u4eba\u7269", sub_fs=9.5)
    box(ax, (76, 18), 26, 15, "\u5408\u5e76\u6267\u884c", fc="white", fs=11.5, sub="\u90e8\u7f72\u4e0e\u8ba4\u8bc6\u7528\u6237\u4e00\u6b21\u5b8c\u6210", sub_fs=9.5)
    for xx in (24, 50):
        arr(ax, (xx, 26), (xs[0], y0 - 11), lw=1.3, ls="--", ms=11, color=GRAY)
    ax.text(50, 96, "SBDP \u81ea\u4e3e\u5f0f\u90e8\u7f72\u534f\u8bae：\u516d\u9636\u6bb5\u6d41\u7a0b", ha="center", fontsize=16, fontweight="bold")
    ax.text(50, 90.5, "\u628a\u4e13\u5bb6\u52b3\u52a8\u7f16\u7801\u4e3a\u667a\u80fd\u4f53\u53ef\u6267\u884c\u7684\u6587\u6863\u6d41\u7a0b，\u7528\u6237\u5168\u7a0b\u4e0d\u63a5\u89e6\u4ee3\u7801",
            ha="center", fontsize=11, color=GRAY)
    note(fig, "\u6ce8：\u4f9d\u636e\u7814\u7a76\u62a5\u544a 3.2 \u4e0e 4.1 \u7684\u534f\u8bae\u7ed3\u6784\u7ed8\u5236。", x=0.03)
    save(fig, "06-SBDP\u516d\u9636\u6bb5\u90e8\u7f72\u6d41\u7a0b.png")


def fig_04_cost_compress(sus):
    """01 \u90e8\u7f72\u6210\u672c\u538b\u7f29（\u4e13\u5bb6\u914d\u7f6e vs \u5f15\u5bfc\u5f0f\u5bf9\u8bdd）"""
    fig = new_fig(11.5, 6.2)
    ax = fig.add_axes([0.02, 0.04, 0.96, 0.88]); ax.set_axis_off()
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.text(50, 97, "\u90e8\u7f72\u6210\u672c\u7684\u538b\u7f29：\u4e13\u5bb6\u914d\u7f6e → \u5f15\u5bfc\u5f0f\u5bf9\u8bdd", ha="center",
            fontsize=16, fontweight="bold")

    box(ax, (24, 74), 34, 14, "\u4f20\u7edf\u624b\u52a8\u914d\u7f6e", fc=LIGHTO, fs=14.5, weight="bold")
    items_l = ["\u73af\u5883\u914d\u7f6e（\u6570\u5c0f\u65f6）", "\u7406\u89e3\u4ee3\u7801 / API", "\u591a\u89d2\u8272\u7f16\u6392", "\u4f9d\u8d56\u4e13\u5bb6\u52b3\u52a8"]
    for i, t in enumerate(items_l):
        ax.text(24, 56 - i * 11, t, ha="center", fontsize=13.5, color=INK)

    box(ax, (76, 74), 34, 14, "SBDP \u5f15\u5bfc\u5f0f\u5bf9\u8bdd", fc=LIGHTB, fs=14.5, weight="bold")
    items_r = ["\u7ea6 30 \u5206\u949f（\u5b9e\u6d4b M=29.5 min）", "\u96f6\u4ee3\u7801 · \u7eaf\u6587\u6863", "\u667a\u80fd\u4f53\u81ea\u4e3b\u6267\u884c",
               "\u666e\u901a\u7528\u6237\u53ef\u72ec\u7acb\u5b8c\u6210"]
    for i, t in enumerate(items_r):
        ax.text(76, 56 - i * 11, t, ha="center", fontsize=13.5, color=INK)
    arr(ax, (43, 40), (57, 40), lw=2.8, ms=22)
    ax.text(50, 45, "\u6210\u672c\u538b\u7f29", ha="center", fontsize=13.5, fontweight="bold")
    ax.text(50, 6, "\u90e8\u7f72\u7684\u8ba4\u77e5\u8d1f\u8377\u4ece\u6280\u672f\u57df\u8f6c\u79fb\u5230\u5bf9\u8bdd\u57df；\u5bf9\u8bdd\u662f\u666e\u901a\u7528\u6237\u5df2\u5177\u5907\u7684\u80fd\u529b",
            ha="center", fontsize=13, color=GRAY)
    note(fig, "\u6ce8：\u4f9d\u636e\u7814\u7a76\u62a5\u544a 1.1 \u4e0e 4.1 \u7ed8\u5236；\u5b9e\u6d4b\u6570\u636e\u89c1 07-\u90e8\u7f72\u53ef\u7528\u6027\u6d4b\u8bd5\u7ed3\u679c。", x=0.03)
    save(fig, "01-\u90e8\u7f72\u6210\u672c\u538b\u7f29\u793a\u610f.png")


# ==================================================================

# ==================================================================
def _rates(q):
    return q[G1].apply(pd.to_numeric, errors="coerce").mean().values


def fig_05_boundary(q):
    """10 \u4efb\u52a1\u6d41\u4e03\u73af\u8282\u59d4\u6258\u7387（\u4e3b\u56fe）"""
    rates = _rates(q)
    fig = new_fig(11, 6.2)
    ax = fig.add_axes([0.08, 0.16, 0.86, 0.72])
    style(ax)
    x = np.arange(7)
    colors = [STAGE_LEVEL_C[s] for s in STAGES]
    bval(ax, x, rates, colors, width=0.55)
    for xi, v in zip(x, rates):
        valtxt(ax, xi, v, fs=12, fmt="{:.2f}")

    xs = np.linspace(0, 6, 300)
    spl = interpolate.make_interp_spline(x, rates, k=3, bc_type="natural")
    ys = np.clip(spl(xs), 0, 1)
    ax.plot(xs, ys, color=INK, lw=1.4, ls="--", zorder=4)
    ax.axhline(0.5, color=LGRAY, lw=0.8, ls=":")
    ax.text(6.05, 0.51, "0.50", fontsize=9.5, color=GRAY)
    ax.set_xticks(x); ax.set_xticklabels(STAGES, fontsize=12)
    ax.set_ylim(0, 1.12)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("\u59d4\u6258\u7387", fontsize=12.5)
    set_title(ax, "\u4efb\u52a1\u6d41\u4e03\u73af\u8282\u59d4\u6258\u7387（N=29）", fs=15)
    handles = [mpatches.Patch(color=BLUE, label="\u9ad8\u59d4\u6258\u73af\u8282（\u68c0\u7d22/\u6574\u7406/\u751f\u6210）"),
               mpatches.Patch(color=PURPLE, label="\u4e2d\u59d4\u6258\u73af\u8282（\u5206\u6790/\u6267\u884c）"),
               mpatches.Patch(color=RED, label="\u4f4e\u59d4\u6258\u73af\u8282（\u754c\u5b9a/\u51b3\u7b56）")]
    ax.legend(handles=handles, loc="upper right", fontsize=9.5, frameon=True, edgecolor=INK)
    note(fig, "\u6ce8：Cochran's Q = 54.23，p < 0.001，\u4e03\u73af\u8282\u59d4\u6258\u7387\u5dee\u5f02\u663e\u8457；\u5206\u5e03\u5448“\u4e2d\u95f4\u9ad8、\u4e24\u7aef\u4f4e”\u5f62\u6001。"
              "\u6570\u636e\u6765\u6e90：\u95ee\u5377 G1_1—G1_7；\u5206\u6790：03-\u59d4\u6258\u8fb9\u754c\u4e0e\u5047\u8bbe\u68c0\u9a8c.py。")
    save(fig, "10-\u4efb\u52a1\u6d41\u4e03\u73af\u8282\u59d4\u6258\u7387.png")


def fig_06_arch(q):
    """11 \u4e03\u73af\u8282\u59d4\u6258\u7387\u7684\u5206\u5e03\u5f62\u6001（\u9762\u79ef\u56fe）"""
    rates = _rates(q)
    fig = new_fig(11, 6.0)
    ax = fig.add_axes([0.08, 0.16, 0.86, 0.72])
    style(ax)
    xs = np.linspace(0, 6, 400)
    spl = interpolate.make_interp_spline(np.arange(7), rates, k=3, bc_type="natural")
    ys = np.clip(spl(xs), 0, 1)
    ax.fill_between(xs, 0, ys, color=LIGHTB, edgecolor="none", zorder=1)
    ax.plot(xs, ys, color=BLUE, lw=2.0, zorder=3)
    ax.scatter(np.arange(7), rates, s=55, color=BLUE, edgecolors=INK, linewidths=1.0, zorder=4)
    for xi, v in zip(np.arange(7), rates):
        ax.text(xi, v + 0.05, f"{v:.2f}", ha="center", fontsize=12, color=INK)
    ax.axhline(0.5, color=LGRAY, lw=0.8, ls=":")
    ax.set_xticks(np.arange(7)); ax.set_xticklabels(STAGES, fontsize=12)
    ax.set_ylim(0, 1.12)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("\u59d4\u6258\u7387", fontsize=12.5)
    set_title(ax, "\u4efb\u52a1\u6d41\u4e03\u73af\u8282\u59d4\u6258\u7387\u7684\u5206\u5e03\u5f62\u6001", fs=15)
    note(fig, "\u6ce8：\u4e2d\u95f4\u73af\u8282（\u68c0\u7d22/\u6574\u7406/\u751f\u6210）\u59d4\u6258\u7387\u9ad8\u4e8e\u4e24\u7aef\u73af\u8282（\u9700\u6c42\u754c\u5b9a/\u5224\u65ad\u51b3\u7b56）。"
              "\u6570\u636e\u6765\u6e90：\u95ee\u5377 G1_1—G1_7（N=29）。")
    save(fig, "11-\u4efb\u52a1\u6d41\u4e03\u73af\u8282\u59d4\u6258\u7387-\u9762\u79ef\u56fe.png")


def fig_07_event_flow(log):
    """13 \u59d4\u6258—\u6536\u56de\u4e8b\u4ef6\u6d41"""
    log = log.dropna(subset=["event_date"]).sort_values(["user_id", "seq"])
    users = list(log["user_id"].unique())
    n = len(users)
    fig = new_fig(12, max(6.0, 0.55 * n + 1.6))
    ax = fig.add_axes([0.07, 0.10, 0.82, 0.82])
    style(ax, grid="both")
    for i, uid in enumerate(users):
        g = log[log["user_id"] == uid]
        y = n - 1 - i
        ax.plot([g["seq"].min(), g["seq"].max()], [y, y], color=LIGHTG, lw=3.5, zorder=1)
        for _, r in g.iterrows():
            ax.scatter(r["seq"], y, s=38, color=OUT_C.get(r["outcome"], LGRAY),
                       edgecolors=INK, linewidths=0.5, zorder=3)
        fail = g[g["outcome"] == "\u5931\u8d25"]
        if not fail.empty:
            ax.scatter(fail["seq"], [y] * len(fail), marker="x", s=70, color=INK,
                       linewidths=1.8, zorder=5)
    ax.set_yticks(range(n)); ax.set_yticklabels([users[n - 1 - i] for i in range(n)], fontsize=11)
    ax.set_xlabel("\u4e8b\u4ef6\u5e8f\u53f7（\u6309\u65f6\u95f4\u5148\u540e）", fontsize=12)
    ax.set_xlim(0, log["seq"].max() + 2)
    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c,
                          markersize=9, label=l) for l, c in OUT_C.items()]
    handles.append(plt.Line2D([0], [0], marker="x", color=INK, markersize=9, lw=1.6,
                              label="\u5931\u8d25\u4e8b\u4ef6"))
    ax.legend(handles=handles, loc="lower right", fontsize=10, frameon=True,
              edgecolor=INK, ncol=2)
    set_title(ax, "\u59d4\u6258—\u6536\u56de\u4e8b\u4ef6\u6d41（327 \u6761\u59d4\u6258\u4e8b\u4ef6）", fs=15)
    note(fig, "\u6ce8：\u6bcf\u4e2a\u70b9\u4ee3\u8868\u4e00\u6b21\u59d4\u6258\u4e8b\u4ef6，\u989c\u8272\u8868\u793a\u7ed3\u679c；× \u6807\u8bb0\u5931\u8d25\u4e8b\u4ef6。"
              "\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868；\u53cc\u7f16\u7801 Cohen's κ=0.879—0.971。")
    save(fig, "13-\u59d4\u6258\u6536\u56de\u4e8b\u4ef6\u6d41.png")


def fig_08_outcome_donut(log):
    """14 \u59d4\u6258\u4e8b\u4ef6\u7ed3\u679c\u6784\u6210"""
    cnt = log["outcome"].value_counts().reindex(OUTCOMES).fillna(0).astype(int)
    fig = new_fig(9, 6.0)
    ax = fig.add_axes([0.06, 0.14, 0.58, 0.78]); style(ax, grid=False); ax.set_aspect("equal")
    wedges, _ = ax.pie(cnt.values, startangle=90, counterclock=False,
                       colors=[OUT_C[o] for o in OUTCOMES],
                       wedgeprops=dict(width=0.34, edgecolor=INK, linewidth=1.2))
    total = cnt.sum()
    ax.text(0, 0.10, f"{total}", ha="center", va="center", fontsize=28, fontweight="bold")
    ax.text(0, -0.16, "\u59d4\u6258\u4e8b\u4ef6\u603b\u6570", ha="center", va="center", fontsize=11.5)
    for w, v in zip(wedges, cnt.values):
        ang = np.deg2rad((w.theta1 + w.theta2) / 2)
        r = 0.84
        ax.text(r * np.cos(ang), r * np.sin(ang), f"{v / total * 100:.1f}%",
                ha="center", va="center", fontsize=12, color=INK)
    ax = fig.add_axes([0.66, 0.14, 0.30, 0.78]); ax.set_axis_off()
    for i, (o, c) in enumerate(OUT_C.items()):
        ax.add_patch(Rectangle((0.03, 0.80 - i * 0.2), 0.09, 0.09,
                               facecolor=c, edgecolor=INK, linewidth=0.8))
        ax.text(0.17, 0.845 - i * 0.2, f"{o}: {cnt[o]} events", fontsize=12.5, va="center")
    ax.text(0.0, 0.0, "\u6210\u529f\u4e8b\u4ef6\u5360\u7edd\u5bf9\u4e3b\u4f53；\n\u5931\u8d25\u4e8b\u4ef6\u4f4e\u9891\u4f46\u5f71\u54cd\u5927",
            fontsize=11.5, color=GRAY, va="bottom")
    set_title(ax, "\u59d4\u6258\u4e8b\u4ef6\u7684\u7ed3\u679c\u6784\u6210", fs=16, pad=4)
    note(fig, "\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868（327 \u6761\u59d4\u6258\u4e8b\u4ef6）。")
    save(fig, "14-\u59d4\u6258\u4e8b\u4ef6\u7ed3\u679c\u6784\u6210.png")


def fig_09_stage_outcome_heat(log):
    """15 \u73af\u8282 × \u7ed3\u679c \u70ed\u529b\u56fe"""
    ct = pd.crosstab(log["stage"], log["outcome"]).reindex(index=STAGES, columns=OUTCOMES).fillna(0)
    pct = ct.div(ct.sum(axis=1), axis=0) * 100
    fig = new_fig(10.5, 6.2)
    ax = fig.add_axes([0.15, 0.16, 0.66, 0.72])
    heat_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "official_group_1_heat", ["#8DC5E8", "#FFFFFF", "#D72828"]
    )
    im = ax.imshow(pct.values, cmap=heat_cmap, aspect="auto", vmin=0, vmax=100, zorder=1)
    ax.set_xticks(range(4)); ax.set_xticklabels(OUTCOMES, fontsize=12)
    ax.set_yticks(range(7)); ax.set_yticklabels(STAGES, fontsize=12)
    for i in range(7):
        for j in range(4):
            v = pct.values[i, j]
            ax.text(j, i, f"{v:.0f}%", ha="center", va="center", fontsize=11,
                    color="white" if (v > 70 or v < 25) else INK)
    ax.set_xlabel("\u59d4\u6258\u7ed3\u679c", fontsize=12)
    ax.set_ylabel("\u4efb\u52a1\u6d41\u73af\u8282", fontsize=12)
    cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.03)
    cb.ax.tick_params(labelsize=10)
    cb.set_label("\u73af\u8282\u5185\u5360\u6bd4（%）", fontsize=10)
    set_title(ax, "\u4efb\u52a1\u6d41\u73af\u8282 × \u59d4\u6258\u7ed3\u679c\u6784\u6210", fs=15)
    note(fig, "\u6ce8：\u5355\u5143\u683c\u4e3a\u5404\u73af\u8282\u5185\u8be5\u7ed3\u679c\u7684\u5360\u6bd4。\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868（327 \u6761\u59d4\u6258\u4e8b\u4ef6）。")
    save(fig, "15-\u73af\u8282\u4e0e\u7ed3\u679c\u70ed\u529b\u56fe.png")


def fig_10_fail_reason(log):
    """16 \u59d4\u6258\u5931\u8d25/\u64a4\u56de\u539f\u56e0\u5206\u5e03"""
    sub = log[log["fail_reason"].notna() & (log["fail_reason"] != "")]
    cnt = sub["fail_reason"].value_counts().reindex(REASONS).fillna(0).astype(int)
    fig = new_fig(10.5, 5.8)
    ax = fig.add_axes([0.20, 0.16, 0.72, 0.72])
    style(ax, grid="x")
    y = np.arange(len(REASONS))[::-1]
    cols = [BLUE, ORANGE, GREEN, RED, PURPLE, BROWN]
    barh(ax, y, cnt.values, cols, height=0.55)
    for yi, v, c in zip(y, cnt.values, cols):
        ax.text(v + 0.5, yi, f"{v}", va="center", fontsize=12, color=INK)
    ax.set_yticks(y); ax.set_yticklabels(REASONS, fontsize=12)
    ax.set_xlim(0, cnt.max() * 1.15)
    ax.set_xlabel("\u4e8b\u4ef6\u6570", fontsize=12)
    set_title(ax, "\u59d4\u6258\u5931\u8d25/\u64a4\u56de\u7684\u539f\u56e0\u5206\u5e03", fs=15)
    note(fig, "\u6ce8：\u4ec5\u7edf\u8ba1\u7ed3\u679c\u975e“\u6210\u529f”\u4e14\u586b\u5199\u4e86\u539f\u56e0\u7684\u4e8b\u4ef6。\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868（fail_reason，κ=0.933）。")
    save(fig, "16-\u5931\u8d25\u539f\u56e0\u5206\u5e03.png")


def fig_11_error_exposure(log):
    """17 \u9519\u8bef\u66b4\u9732\u65b9\u5f0f\u4e0e\u7ed3\u679c"""
    sub = log[(log["error_exposure"].notna()) & (log["error_exposure"] != "") & (log["outcome"] != "\u6210\u529f")]
    order = ["\u5f53\u573a\u53d1\u73b0\u5e76\u7ea0\u6b63", "\u4e8b\u540e\u53d1\u73b0"]
    ct = pd.crosstab(sub["error_exposure"], sub["outcome"]).reindex(index=order, columns=OUTCOMES[1:]).fillna(0)
    fig = new_fig(10, 5.6)
    ax = fig.add_axes([0.22, 0.16, 0.70, 0.72])
    style(ax, grid="x")
    y = np.arange(len(order))[::-1]
    left = np.zeros(len(order))
    for j, oc in enumerate(OUTCOMES[1:]):
        vals = ct[oc].values
        barh(ax, y, vals, OUT_C[oc], height=0.55, left=left)
        for row_index, (yi, v) in enumerate(zip(y, vals)):
            if v > 0:
                ax.text(left[row_index] + v / 2, yi, f"{v}", ha="center", va="center",
                        fontsize=11, color=INK, fontweight="bold")
        left += vals
    ax.set_yticks(y); ax.set_yticklabels(order, fontsize=12)
    ax.set_xlim(0, ct.sum(axis=1).max() * 1.3)
    ax.set_xlabel("\u4e8b\u4ef6\u6570（\u975e\u6210\u529f\u4e8b\u4ef6）", fontsize=12)
    handles = [mpatches.Patch(color=OUT_C[o], label=o) for o in OUTCOMES[1:]]
    ax.legend(handles=handles, loc="lower right", fontsize=10.5, frameon=True, edgecolor=INK)
    set_title(ax, "\u9519\u8bef\u66b4\u9732\u65b9\u5f0f\u4e0e\u59d4\u6258\u7ed3\u679c", fs=15)
    note(fig, "\u6ce8：\u53ef\u5f53\u573a\u53d1\u73b0\u5e76\u7ea0\u6b63\u7684\u5931\u8d25\u4e0d\u89e6\u53d1\u7b97\u6cd5\u538c\u6076；\u4e8b\u540e\u53d1\u73b0\u7684\u5931\u8d25\u66f4\u6613\u5bfc\u81f4\u6536\u56de。"
              "\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868（error_exposure，κ=0.879）。")
    save(fig, "17-\u9519\u8bef\u66b4\u9732\u65b9\u5f0f\u4e0e\u7ed3\u679c.png")


def fig_12_iterations(log):
    """18 \u5355\u6b21\u59d4\u6258\u8fed\u4ee3\u8f6e\u6570\u5206\u5e03"""
    it = log["iterations"].astype(float).dropna()
    fig = new_fig(9.5, 5.6)
    ax = fig.add_axes([0.11, 0.16, 0.80, 0.72])
    style(ax)
    bins = np.arange(0.5, it.max() + 1.6, 1)
    n, _, _ = ax.hist(it, bins=bins, color=BLUE, edgecolor=INK, linewidth=0.9, zorder=2)
    for p, nn in zip(ax.patches, n):
        if nn > 0:
            ax.text(p.get_x() + p.get_width() / 2, nn + 2, f"{int(nn)}", ha="center",
                    fontsize=12, color=INK)
    ax.axvline(it.mean(), color=RED, lw=1.3, ls="--")
    ax.set_xticks(np.arange(1, it.max() + 1))
    ax.set_xlabel("\u8fed\u4ee3\u8f6e\u6570", fontsize=12)
    ax.set_ylabel("\u4e8b\u4ef6\u6570", fontsize=12)
    ax.set_ylim(0, n.max() * 1.3)
    ax.text(it.mean() + 0.1, n.max() * 1.15, f"Mean {it.mean():.2f}", fontsize=12, color=RED)
    set_title(ax, "\u5355\u6b21\u59d4\u6258\u7684\u8fed\u4ee3\u8f6e\u6570\u5206\u5e03", fs=15)
    note(fig, "\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868（327 \u6761\u59d4\u6258\u4e8b\u4ef6）。")
    save(fig, "18-\u8fed\u4ee3\u6b21\u6570\u5206\u5e03.png")


def fig_13_withdraw_reasons(q):
    """19 \u6536\u56de\u59d4\u6258\u7684\u539f\u56e0\u5206\u5e03（\u95ee\u5377 H1）"""
    labs = ["\u80fd\u529b\u4e0d\u8db3", "\u8f93\u51fa\u4e0d\u53ef\u9760", "\u4e0d\u7701\u65f6\u95f4", "\u9690\u79c1\u987e\u8651", "\u60c5\u611f\u9700\u6c42"]
    vals = q[H1].apply(pd.to_numeric, errors="coerce").mean().values
    fig = new_fig(10, 5.8)
    ax = fig.add_axes([0.20, 0.16, 0.72, 0.72])
    style(ax, grid="x")
    y = np.arange(len(labs))[::-1]
    cols = [BLUE, ORANGE, GREEN, RED, PURPLE]
    barh(ax, y, vals, cols, height=0.55)
    for yi, v, c in zip(y, vals, cols):
        ax.text(v + 0.02, yi, f"{v:.2f}", va="center", fontsize=12, color=INK)
    ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=12)
    ax.set_xlim(0, 0.75)
    ax.set_xlabel("\u9009\u62e9\u6bd4\u4f8b（\u591a\u9009）", fontsize=12)
    set_title(ax, "\u6536\u56de\u59d4\u6258\u7684\u539f\u56e0\u5206\u5e03（N=29）", fs=15)
    note(fig, "\u6ce8：\u4e03\u70b9\u95ee\u5377\u4e8c\u503c\u9898“\u662f\u5426\u56e0\u8be5\u539f\u56e0\u6536\u56de\u8fc7\u59d4\u6258”，\u7edf\u8ba1\u9009\u62e9\u6bd4\u4f8b。"
              "\u6570\u636e\u6765\u6e90：\u95ee\u5377 H1_1—H1_5；\u5206\u6790：01-\u95ee\u5377\u5206\u6790.py。")
    save(fig, "19-\u6536\u56de\u539f\u56e0\u5206\u5e03.png")


def fig_14_h3a(log):
    """22 \u9996\u6b21\u5931\u8d25\u524d\u540e 14 \u5929\u59d4\u6258\u9891\u7387（H3a）"""
    lg = log.dropna(subset=["event_date"]).sort_values(["user_id", "seq"])
    WIN = pd.Timedelta(days=14)
    stage_rows = []
    for uid, g in lg.groupby("user_id"):
        for st, sub in g.groupby("stage"):
            fail = sub.loc[sub["outcome"].isin(["\u5931\u8d25", "\u90e8\u5206\u6210\u529f"]), "event_date"]
            if fail.empty:
                continue
            fd = fail.min()
            nb = int(((sub["event_date"] >= fd - WIN) & (sub["event_date"] < fd)).sum())
            na = int(((sub["event_date"] > fd) & (sub["event_date"] <= fd + WIN)).sum())
            if nb < 1:
                continue
            stage_rows.append((uid, nb / 14, na / 14))
    user_rates = pd.DataFrame(stage_rows, columns=["user_id", "before", "after"]).groupby("user_id")[["before", "after"]].mean()
    before = user_rates["before"]
    after = user_rates["after"]
    mb, ma = before.mean(), after.mean()
    w, p = stats.wilcoxon(before, after, method="exact")
    fig = new_fig(9, 5.8)
    ax = fig.add_axes([0.12, 0.18, 0.76, 0.70])
    style(ax)
    bval(ax, [0, 1], [mb, ma], [BLUE, RED], width=0.4)
    ax.text(0, mb + 0.006, f"{mb:.3f}", ha="center", fontsize=13, color=INK, fontweight="bold")
    ax.text(1, ma + 0.006, f"{ma:.3f}", ha="center", fontsize=13, color=INK, fontweight="bold")
    ax.text(0, mb - 0.018, "\u6b21/\u5929", ha="center", fontsize=11, color="white", fontweight="bold")
    ax.text(1, ma - 0.018, "\u6b21/\u5929", ha="center", fontsize=11, color="white", fontweight="bold")
    arr(ax, (0.28, mb + 0.02), (0.72, ma + 0.02), lw=1.6, ms=13)
    ax.text(0.5, max(mb, ma) + 0.024, f"W = {w:.1f}, exact p = {p:.4f}", ha="center",
            fontsize=12.5, color=INK, fontweight="bold")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["\u9996\u6b21\u5931\u8d25\u524d 14 \u5929", "\u9996\u6b21\u5931\u8d25\u540e 14 \u5929"], fontsize=12.5)
    ax.set_ylim(0, max(mb, ma) + 0.075)
    ax.set_ylabel("\u8be5\u73af\u8282\u59d4\u6258\u9891\u7387（\u6b21/\u5929）", fontsize=12)
    set_title(ax, "\u9996\u6b21\u5931\u8d25\u524d\u540e 14 \u5929\u8be5\u73af\u8282\u59d4\u6258\u9891\u7387（H3a）", fs=15)
    note(fig, "\u6ce8：\u4ee5\u9996\u6b21\u5931\u8d25\u65e5\u4e3a\u754c，\u6bd4\u8f83\u524d\u540e\u5404 14 \u5929\u5185\u8be5\u73af\u8282\u7684\u59d4\u6258\u9891\u7387（\u914d\u5bf9 Wilcoxon \u7b26\u53f7\u79e9\u68c0\u9a8c）。"
              "\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868；\u5206\u6790：03-\u59d4\u6258\u8fb9\u754c\u4e0e\u5047\u8bbe\u68c0\u9a8c.py。")
    save(fig, "22-\u9996\u6b21\u5931\u8d25\u524d\u540e\u59d4\u6258\u9891\u7387.png")


def fig_15_memory(q, mem):
    """23 \u8bb0\u5fc6\u79ef\u7d2f\u4e0e\u6301\u7eed\u4f7f\u7528\u610f\u5411（H3b）"""
    q2 = q.copy()
    q2["continuance"] = q2[["F1", "F2", "F3"]].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    m = mem.merge(q2[["link_id", "continuance"]], on="link_id", how="inner").dropna()
    x = m["timeline_lines"].astype(float)
    y = m["continuance"].astype(float)
    r, p = stats.spearmanr(x, y)
    lr = stats.linregress(x, y)
    fig = new_fig(9.5, 6.0)
    ax = fig.add_axes([0.11, 0.15, 0.78, 0.74])
    style(ax, grid="both")
    xs = np.linspace(x.min() - 5, x.max() + 5, 100)
    ax.plot(xs, lr.intercept + lr.slope * xs, color=RED, lw=1.5, ls="--", zorder=3,
            label=f"Linear fit (r = {lr.rvalue:.3f})")
    ax.scatter(x, y, s=55, color=BLUE, edgecolors=INK, linewidths=0.8, zorder=4,
               label="\u6837\u672c（N=13）")
    # Pseudonymous point labels are omitted because they add no analytical value
    # and collide in the dense center of this small linked sample.
    ax.set_xlabel("\u65f6\u95f4\u8f74\u65e5\u5fd7\u884c\u6570（\u8bb0\u5fc6\u79ef\u7d2f\u91cf）", fontsize=12)
    ax.set_ylabel("\u6301\u7eed\u4f7f\u7528\u610f\u5411（F1—F3 \u5747\u503c）", fontsize=12)
    ax.set_ylim(1, 7.4)
    ax.legend(loc="upper left", fontsize=10.5, frameon=True, edgecolor=INK)
    set_title(ax, "\u8bb0\u5fc6\u79ef\u7d2f\u4e0e\u6301\u7eed\u4f7f\u7528\u610f\u5411\u7684\u5173\u7cfb（H3b）", fs=15)
    note(fig, "\u6ce8：Spearman ρ = 0.850，p < 0.001（\u65f6\u95f4\u8f74\u884c\u6570）；ρ = 0.781，p = 0.002（\u66f4\u65b0\u9891\u6b21）。"
              "\u6570\u636e\u6765\u6e90：\u8bb0\u5fc6\u6307\u6807\u8868 × \u95ee\u5377 F \u91cf\u8868（link_id \u533f\u540d\u5173\u8054）。")
    save(fig, "23-\u8bb0\u5fc6\u79ef\u7d2f\u4e0e\u6301\u7eed\u4f7f\u7528\u610f\u5411.png")


def fig_16_alpha():
    """24 \u95ee\u5377\u91cf\u8868\u4fe1\u5ea6（Cronbach's α）"""
    items = ["\u611f\u77e5\u6709\u7528\u6027", "\u611f\u77e5\u6613\u7528\u6027", "\u611f\u77e5\u4fe1\u4efb", "\u611f\u77e5\u98ce\u9669", "\u6301\u7eed\u4f7f\u7528\u610f\u5411", "\u8bb0\u5fc6\u611f\u77e5"]
    alphas = [0.871, 0.778, 0.815, 0.403, 0.879, 0.814]
    fig = new_fig(11.5, 6.2)
    ax = fig.add_axes([0.10, 0.22, 0.84, 0.66])
    style(ax)
    x = np.arange(len(items))
    cols = [GREEN if a >= 0.70 else RED for a in alphas]
    bval(ax, x, alphas, cols, width=0.5)
    for xi, a, c in zip(x, alphas, cols):
        ax.text(xi, a + 0.03, f"{a:.3f}", ha="center", fontsize=12, color=INK)
    ax.axhline(0.70, color=INK, lw=1.2, ls="--")
    ax.text(5.4, 0.715, "0.70（\u5e38\u7528\u9608\u503c）", fontsize=10, color=INK, ha="right")
    ax.annotate("Perceived risk: alpha=.403\nnot interpreted as a composite", xy=(3, 0.403), xytext=(2.48, 0.58),
                ha="left", fontsize=10.5, color=RED, linespacing=1.25,
                bbox=dict(boxstyle="round,pad=0.22", facecolor="#FFFFFF", edgecolor="none", alpha=0.92),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
    ax.set_xticks(x); ax.set_xticklabels(items, fontsize=10.5, rotation=18, ha="right")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Cronbach's α", fontsize=12)
    set_title(ax, "\u95ee\u5377\u516d\u91cf\u8868\u4fe1\u5ea6（N=29）", fs=15)
    note(fig, "\u6ce8：\u9664\u611f\u77e5\u98ce\u9669（α=0.403，\u91cf\u8868\u5185\u6db5\u8f83\u5bbd）\u5916，\u5404\u91cf\u8868 α \u5747\u9ad8\u4e8e 0.70。"
              "\u6570\u636e\u6765\u6e90：\u95ee\u5377 B/C/D/E/F/I；\u5206\u6790：01-\u95ee\u5377\u5206\u6790.py。")
    save(fig, "24-\u95ee\u5377\u91cf\u8868\u4fe1\u5ea6.png")


def fig_17_radar(q):
    """25 \u611f\u77e5\u6784\u5ff5\u5747\u503c\u96f7\u8fbe\u56fe"""
    labs = ["\u611f\u77e5\u6709\u7528\u6027", "\u611f\u77e5\u6613\u7528\u6027", "\u611f\u77e5\u4fe1\u4efb", "\u611f\u77e5\u98ce\u9669", "\u6301\u7eed\u4f7f\u7528\u610f\u5411", "\u8bb0\u5fc6\u611f\u77e5"]
    cols = [SCALE_COLS[k] for k in labs]
    vals = [q[c].apply(pd.to_numeric, errors="coerce").mean().mean() for c in cols]
    N = len(labs)
    ang = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    ang += ang[:1]
    v = vals + vals[:1]
    fig = new_fig(8.5, 7.0)
    ax = fig.add_axes([0.12, 0.12, 0.76, 0.78], polar=True)
    ax.set_facecolor("white")
    ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
    ax.set_ylim(0, 7)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(labs, fontsize=12)
    ax.set_yticks([1, 2, 3, 4, 5, 6, 7])
    ax.set_yticklabels(["1", "2", "3", "4", "5", "6", "7"], fontsize=9, color=GRAY)
    ax.grid(color=GRIDC, linewidth=0.8)
    for sp in ax.spines.values():
        sp.set_color(INK); sp.set_linewidth(0.9)
    ax.plot(ang, v, lw=2.0, color=BLUE, zorder=3)
    ax.fill(ang, v, color=to_rgba_light(BLUE, 0.25), zorder=2)
    ax.scatter(ang[:-1], vals, s=40, color=BLUE, edgecolors=INK, linewidths=0.8, zorder=4)
    for a, vv in zip(ang[:-1], vals):
        ax.text(a, vv + 0.5, f"{vv:.2f}", ha="center", va="center", fontsize=11, color=INK)
    ax.set_title("\u516d\u6784\u5ff5\u611f\u77e5\u5747\u503c（\u4e03\u70b9\u91cf\u8868，N=29）", fontsize=15, pad=24, fontweight="bold")
    note(fig, "\u6ce8：\u6570\u503c\u4e3a\u5404\u91cf\u8868\u9898\u76ee\u5f97\u5206\u7684\u5747\u503c。\u6570\u636e\u6765\u6e90：\u95ee\u5377 B/C/D/E/F/I；\u5206\u6790：01-\u95ee\u5377\u5206\u6790.py。")
    save(fig, "25-\u611f\u77e5\u6784\u5ff5\u96f7\u8fbe\u56fe.png")


def to_rgba_light(hexc, alpha):
    from matplotlib.colors import to_rgba
    r, g, b = to_rgba(hexc)[:3]
    return (r, g, b, alpha)


def fig_18_usage_groups(q):
    """09 \u5de5\u4f5c\u574a\u6210\u5458\u5f53\u524d\u4f7f\u7528\u72b6\u6001"""
    cnt = q["A1"].value_counts().sort_index()
    labels = {1: "\u6bcf\u5929\u90fd\u5728\u7528", 2: "\u6bcf\u5468\u51e0\u6b21", 3: "\u5076\u5c14\u4f7f\u7528", 4: "\u5df2\u505c\u6b62\u4f7f\u7528"}
    vals = [int(cnt.get(k, 0)) for k in [1, 2, 3, 4]]
    colors = [GREEN, BLUE, GOLD, RED]
    fig = new_fig(9, 6.0)
    ax = fig.add_axes([0.06, 0.14, 0.56, 0.78]); style(ax, grid=False); ax.set_aspect("equal")
    wedges, _ = ax.pie(vals, startangle=90, counterclock=False, colors=colors,
                       wedgeprops=dict(width=0.36, edgecolor=INK, linewidth=1.2))
    ax.text(0, 0.10, f"{sum(vals)}", ha="center", va="center", fontsize=26, fontweight="bold")
    ax.text(0, -0.18, "\u6709\u6548\u6837\u672c", ha="center", va="center", fontsize=11.5)
    for w, v in zip(wedges, vals):
        ang = np.deg2rad((w.theta1 + w.theta2) / 2)
        r = 0.82
        ax.text(r * np.cos(ang), r * np.sin(ang), f"{v / sum(vals) * 100:.0f}%",
                ha="center", va="center", fontsize=12, color=INK)
    axr = fig.add_axes([0.64, 0.14, 0.32, 0.78]); axr.set_axis_off()
    for i, (k, c) in enumerate(zip([1, 2, 3, 4], colors)):
        axr.add_patch(Rectangle((0.04, 0.82 - i * 0.2), 0.08, 0.08,
                                facecolor=c, edgecolor=INK, linewidth=0.8))
        axr.text(0.17, 0.86 - i * 0.2, f"{labels[k]}: {vals[i]} users", fontsize=12.5, va="center")
    axr.text(0.08, 0.02, "\u7ea6 38% \u5df2\u505c\u6b62\u4f7f\u7528", fontsize=10, color=GRAY, va="bottom")
    set_title(ax, "\u5de5\u4f5c\u574a\u6210\u5458\u5f53\u524d\u4f7f\u7528\u72b6\u6001（A1）", fs=16, pad=4)
    note(fig, "\u6570\u636e\u6765\u6e90：\u95ee\u5377 A1（N=29，\u5254\u9664\u6d4b\u8c0e\u9879\u672a\u901a\u8fc7\u8005）。")
    save(fig, "09-\u4f7f\u7528\u72b6\u6001\u5206\u5e03.png")


def fig_19_weekly(log):
    """20 \u59d4\u6258\u4e8b\u4ef6\u6309\u5468\u7684\u73af\u8282\u6784\u6210"""
    lg = log.dropna(subset=["event_date"]).copy().set_index("event_date")
    wk = lg.groupby([pd.Grouper(freq="W"), "stage"]).size().unstack(fill_value=0)
    wk = wk.reindex(columns=STAGES).fillna(0)
    fig = new_fig(12, 6.0)
    ax = fig.add_axes([0.08, 0.18, 0.84, 0.72])
    style(ax)
    xx = np.arange(len(wk))
    bottom = np.zeros(len(wk))
    for i, st in enumerate(STAGES):
        vals = wk[st].values
        ax.fill_between(xx, bottom, bottom + vals, step="mid", color=STAGE_LEVEL_C[st],
                        alpha=0.55, lw=0.5, edgecolor="none", zorder=2)
        bottom += vals
    total = wk.sum(axis=1).values
    ax.plot(xx, total, color=INK, lw=1.5, zorder=4)
    ax.set_xticks(xx)
    ax.set_xticklabels([d.strftime("%m-%d") for d in wk.index], fontsize=9.5, rotation=40)
    ax.set_xlim(-0.5, len(wk) - 0.5)
    ax.set_xlabel("\u7edf\u8ba1\u5468（2026 \u5e74）", fontsize=12)
    ax.set_ylabel("\u59d4\u6258\u4e8b\u4ef6\u6570", fontsize=12)
    handles = [mpatches.Patch(color=STAGE_LEVEL_C[st], label=st, alpha=0.6) for st in STAGES]
    ax.legend(handles=handles, loc="upper left", fontsize=9, frameon=True, edgecolor=INK, ncol=4)
    set_title(ax, "\u59d4\u6258\u4e8b\u4ef6\u6309\u5468\u7684\u73af\u8282\u6784\u6210\u4e0e\u4f7f\u7528\u70ed\u5ea6", fs=15)
    note(fig, "\u6ce8：\u5de5\u4f5c\u574a\u540e\u9996\u6708\u4f7f\u7528\u6700\u6d3b\u8dc3，\u968f\u540e\u56de\u843d\u81f3\u7a33\u5b9a\u6c34\u5e73。\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868（327 \u6761\u59d4\u6258\u4e8b\u4ef6）。")
    save(fig, "20-\u59d4\u6258\u4e8b\u4ef6\u5468\u5ea6\u65f6\u95f4\u5e8f\u5217.png")


def fig_20_user_events(log):
    """21 \u5404\u7528\u6237\u59d4\u6258\u4e8b\u4ef6\u89c4\u6a21\u4e0e\u7ed3\u679c\u6784\u6210"""
    users = list(log["user_id"].unique())
    ct = pd.crosstab(log["user_id"], log["outcome"]).reindex(index=users, columns=OUTCOMES).fillna(0)
    fig = new_fig(10.5, max(6.0, 0.48 * len(users) + 1.6))
    ax = fig.add_axes([0.12, 0.14, 0.66, 0.76])
    style(ax, grid="x")
    y = np.arange(len(users))[::-1]
    left = np.zeros(len(users))
    for oc in OUTCOMES:
        vals = ct[oc].values
        barh(ax, y, vals, OUT_C[oc], height=0.62, left=left)
        left += vals
    for yi, tot in zip(y, ct.sum(axis=1).values):
        ax.text(tot + 0.8, yi, f"{int(tot)}", va="center", fontsize=11, color=GRAY)
    ax.set_yticks(y); ax.set_yticklabels(users, fontsize=11)
    ax.set_xlim(0, ct.sum(axis=1).max() * 1.15)
    ax.set_xlabel("\u59d4\u6258\u4e8b\u4ef6\u6570", fontsize=12)
    handles = [mpatches.Patch(color=OUT_C[o], label=o) for o in OUTCOMES]
    ax.legend(handles=handles, loc="lower right", fontsize=10.5, frameon=True, edgecolor=INK)
    set_title(ax, "\u5404\u7528\u6237\u7684\u59d4\u6258\u4e8b\u4ef6\u89c4\u6a21\u4e0e\u7ed3\u679c\u6784\u6210", fs=15)
    note(fig, "\u6570\u636e\u6765\u6e90：\u65e5\u5fd7\u7f16\u7801\u8868（\u6309 user_id \u6c47\u603b）。")
    save(fig, "21-\u5404\u7528\u6237\u59d4\u6258\u4e8b\u4ef6\u6784\u6210.png")


# ==================================================================

# ==================================================================
def _exp_stats(exp):
    tasks = ["A", "B", "C"]
    metrics = [("total_time_min", "\u603b\u65f6\u957f(min)"), ("intervention_count", "\u4ecb\u5165\u6b21\u6570"),
               ("intervention_time_min", "\u4ecb\u5165\u65f6\u957f(min)"), ("quality_score", "\u4ea7\u51fa\u8d28\u91cf")]
    rows = []
    for t in tasks:
        sub = exp[exp["task"] == t]
        s = sub[sub["condition"] == "single"]
        m = sub[sub["condition"] == "multi"]
        for col, lab in metrics:
            sv = s[col].astype(float).values
            mv = m[col].astype(float).values
            paired = pd.merge(s[["participant", col]], m[["participant", col]],
                              on="participant", suffixes=("_s", "_m")).dropna()
            sm, mm = paired[col + "_s"].values, paired[col + "_m"].values
            if len(sm) >= 2:
                w, p = stats.wilcoxon(sm, mm)
                n = len(sm)
                mu = n * (n + 1) / 4
                sigma = np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
                r = abs((w - mu) / sigma) / np.sqrt(n)
            else:
                w, p, r = np.nan, np.nan, np.nan
            rows.append(dict(task=t, metric=lab, col=col, sm=sv.mean(), sd=sv.std(ddof=1),
                             mm=mv.mean(), md=mv.std(ddof=1), w=w, p=p, r=r, n=len(sm)))
    return rows


def _grouped(exp, col, ylab, fname, title, ymax, val_off, delta_off, note_text):
    rows = _exp_stats(exp)
    fig = new_fig(9.5, 5.8)
    ax = fig.add_axes([0.11, 0.17, 0.78, 0.72])
    style(ax)
    x = np.arange(3)
    sm = [r["sm"] for r in rows if r["col"] == col]
    mm = [r["mm"] for r in rows if r["col"] == col]
    w = 0.32
    bval(ax, x - w / 2, sm, LIGHTG, width=w, hatch="//")
    bval(ax, x + w / 2, mm, BLUE, width=w)
    for xi, v in zip(x - w / 2, sm):
        valtxt(ax, xi, v, fs=11.5, dy=val_off, fmt="{:.1f}")
    for xi, v in zip(x + w / 2, mm):
        valtxt(ax, xi, v, fs=11.5, dy=val_off, fmt="{:.1f}")
    for xi, r in zip(x, rows):
        if r["col"] != col:
            continue
        d = r["mm"] - r["sm"]
        ax.text(xi, max(r["sm"], r["mm"]) + delta_off, f"Δ{d:+.1f}", ha="center",
                fontsize=11, color=RED, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(["\u4efb\u52a1 A\n\u68c0\u7d22\u6574\u7406\u578b", "\u4efb\u52a1 B\n\u5206\u6790\u578b", "\u4efb\u52a1 C\n\u5199\u4f5c\u7efc\u5408\u578b"],
                                         fontsize=11.5)
    ax.set_ylim(0, ymax)
    ax.set_ylabel(ylab, fontsize=12)
    handles = [mpatches.Patch(facecolor=LIGHTG, edgecolor=INK, hatch="//", label="\u5355\u667a\u80fd\u4f53"),
               mpatches.Patch(facecolor=BLUE, edgecolor=INK, label="\u591a\u667a\u80fd\u4f53")]
    ax.legend(handles=handles, loc="upper right", fontsize=10.5, frameon=True, edgecolor=INK)
    set_title(ax, title, fs=15)
    note(fig, note_text)
    save(fig, fname)


def fig_21_time(exp):
    _grouped(exp, "total_time_min", "\u603b\u65f6\u957f（min）", "26-\u603b\u65f6\u957f\u5bf9\u6bd4.png",
             "\u4e09\u7c7b\u4efb\u52a1\u7684\u603b\u65f6\u957f：\u5355\u667a\u80fd\u4f53 vs \u591a\u667a\u80fd\u4f53",
             42, 0.9, 1.9,
             "\u6ce8：n=4，\u914d\u5bf9 Wilcoxon \u7b26\u53f7\u79e9\u68c0\u9a8c（\u4efb\u52a1 A/B：p=0.125，\u672a\u8fbe p<0.05，\u65b9\u5411\u4e00\u81f4、\u6548\u5e94\u91cf r≈0.91）；"
             "\u4efb\u52a1 C：p=0.875。\u6570\u636e\u6765\u6e90：\u5b9e\u9a8c\u6570\u636e\u8bb0\u5f55\u8868；\u5206\u6790：04-\u5bf9\u6bd4\u5b9e\u9a8c\u5206\u6790.py。")


def fig_22_count(exp):
    _grouped(exp, "intervention_count", "\u4eba\u5de5\u4ecb\u5165\u6b21\u6570", "27-\u4eba\u5de5\u4ecb\u5165\u6b21\u6570\u5bf9\u6bd4.png",
             "\u4eba\u5de5\u4ecb\u5165\u6b21\u6570：\u5355\u667a\u80fd\u4f53 vs \u591a\u667a\u80fd\u4f53",
             20, 0.6, 1.4,
             "\u6ce8：n=4，\u914d\u5bf9 Wilcoxon \u7b26\u53f7\u79e9\u68c0\u9a8c（\u4efb\u52a1 A：p=0.125；\u4efb\u52a1 B：p=0.25；\u4efb\u52a1 C：p=0.625）。"
             "\u6570\u636e\u6765\u6e90：\u5b9e\u9a8c\u6570\u636e\u8bb0\u5f55\u8868；\u5206\u6790：04-\u5bf9\u6bd4\u5b9e\u9a8c\u5206\u6790.py。")


def fig_23_intervention(exp):
    _grouped(exp, "intervention_time_min", "\u4eba\u5de5\u4ecb\u5165\u65f6\u957f（min）", "28-\u4eba\u5de5\u4ecb\u5165\u65f6\u957f\u5bf9\u6bd4.png",
             "\u4eba\u5de5\u4ecb\u5165\u65f6\u957f：\u5355\u667a\u80fd\u4f53 vs \u591a\u667a\u80fd\u4f53",
             23, 0.6, 1.4,
             "\u6ce8：n=4，\u914d\u5bf9 Wilcoxon \u7b26\u53f7\u79e9\u68c0\u9a8c（\u4efb\u52a1 A/B：p=0.125；\u4efb\u52a1 C：p=0.50）。"
             "\u6570\u636e\u6765\u6e90：\u5b9e\u9a8c\u6570\u636e\u8bb0\u5f55\u8868；\u5206\u6790：04-\u5bf9\u6bd4\u5b9e\u9a8c\u5206\u6790.py。")


def fig_24_quality(exp):
    _grouped(exp, "quality_score", "\u4ea7\u51fa\u8d28\u91cf（\u76f2\u8bc4，5 \u5206\u5236）", "29-\u4ea7\u51fa\u8d28\u91cf\u5bf9\u6bd4.png",
             "\u4ea7\u51fa\u8d28\u91cf（\u53cc\u4eba\u76f2\u8bc4）：\u5355\u667a\u80fd\u4f53 vs \u591a\u667a\u80fd\u4f53",
             5.8, 0.12, 0.26,
             "\u6ce8：\u4ea7\u51fa\u8d28\u91cf\u4e3a\u4e24\u4f4d\u76f2\u8bc4\u8005\u5bf9\u76f8\u5173\u6027/\u51c6\u786e\u6027/\u7ed3\u6784/\u5b8c\u6574\u6027\u7684\u5e73\u5747\u5206；n=4，\u914d\u5bf9 Wilcoxon \u7b26\u53f7\u79e9\u68c0\u9a8c"
             "（\u4efb\u52a1 B：p=0.125，\u591a\u667a\u80fd\u4f53\u66f4\u9ad8）。\u6570\u636e\u6765\u6e90：\u5b9e\u9a8c\u6570\u636e\u8bb0\u5f55\u8868；\u5206\u6790：04-\u5bf9\u6bd4\u5b9e\u9a8c\u5206\u6790.py。")


def fig_25_gain(exp):
    """30 \u591a\u667a\u80fd\u4f53\u76f8\u5bf9\u589e\u76ca（%）"""
    rows = _exp_stats(exp)
    metrics = [("total_time_min", "\u603b\u65f6\u957f"), ("intervention_count", "\u4ecb\u5165\u6b21\u6570"),
               ("intervention_time_min", "\u4ecb\u5165\u65f6\u957f")]
    tasks = ["A", "B", "C"]
    M = np.zeros((3, 3))
    for i, (col, _) in enumerate(metrics):
        for j, t in enumerate(tasks):
            r = [x for x in rows if x["col"] == col and x["task"] == t][0]
            M[i, j] = (r["sm"] - r["mm"]) / r["sm"] * 100 if r["sm"] else 0
    fig = new_fig(9.5, 5.6)
    ax = fig.add_axes([0.13, 0.17, 0.66, 0.72])
    im = ax.imshow(M, cmap="RdBu_r", aspect="auto", vmin=-20, vmax=60, zorder=1)
    ax.set_xticks(range(3)); ax.set_xticklabels([f"Task {t}" for t in tasks], fontsize=12)
    ax.set_yticks(range(3)); ax.set_yticklabels([m[1] for m in metrics], fontsize=12)
    for i in range(3):
        for j in range(3):
            v = M[i, j]
            ax.text(j, i, f"{v:+.0f}%", ha="center", va="center", fontsize=12.5,
                    color="white" if abs(v) > 25 else INK, fontweight="bold")
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.04)
    cb.ax.tick_params(labelsize=10)
    cb.set_label("\u76f8\u5bf9\u589e\u76ca（%，\u6b63=\u66f4\u7701\u65f6/\u66f4\u5c11\u4ecb\u5165）", fontsize=10)
    set_title(ax, "\u591a\u667a\u80fd\u4f53\u76f8\u5bf9\u5355\u667a\u80fd\u4f53\u7684\u589e\u76ca（%）", fs=15)
    note(fig, "\u6ce8：\u589e\u76ca =（\u5355−\u591a）/\u5355 × 100%。\u4efb\u52a1 A/B（\u53ef\u5206\u89e3、\u591a\u73af\u8282、\u9700\u6838\u67e5）\u589e\u76ca\u660e\u663e，"
              "\u4efb\u52a1 C（\u5355\u73af\u8282、\u5f3a\u4e3b\u89c2）\u589e\u76ca\u6d88\u5931。\u6570\u636e\u6765\u6e90：\u5b9e\u9a8c\u6570\u636e\u8bb0\u5f55\u8868。")
    save(fig, "30-\u591a\u667a\u80fd\u4f53\u76f8\u5bf9\u589e\u76ca.png")


def fig_26_slope(exp):
    """31 \u914d\u5bf9\u4e2a\u4f53\u8f68\u8ff9：\u603b\u65f6\u957f\u5355→\u591a"""
    tasks = ["A", "B", "C"]
    fig = new_fig(12, 5.4)
    for k, t in enumerate(tasks):
        ax = fig.add_subplot(1, 3, k + 1)
        style(ax, grid=False)
        sub = exp[exp["task"] == t]
        s = sub[sub["condition"] == "single"].set_index("participant")["total_time_min"]
        m = sub[sub["condition"] == "multi"].set_index("participant")["total_time_min"]
        parts = [p for p in s.index if p in m.index]
        def spread(values, minimum_gap=1.25):
            order = sorted(range(len(values)), key=lambda index: values[index])
            placed = list(map(float, values))
            for previous, current in zip(order, order[1:]):
                placed[current] = max(placed[current], placed[previous] + minimum_gap)
            return placed

        single_values = [float(s[p]) for p in parts]
        multi_values = [float(m[p]) for p in parts]
        single_labels = spread(single_values)
        multi_labels = spread(multi_values)
        for participant_index, p in enumerate(parts):
            sv, mv = s[p], m[p]
            c = GREEN if mv < sv else RED
            ax.plot([0, 1], [sv, mv], color=c, lw=1.6, zorder=3)
            ax.scatter([0, 1], [sv, mv], s=42, color=c, edgecolors=INK, linewidths=0.7, zorder=4)
            ax.text(-0.04, single_labels[participant_index], f"{sv:.0f}", ha="right", va="center", fontsize=10)
            ax.text(1.04, multi_labels[participant_index], f"{mv:.0f}", ha="left", va="center", fontsize=10)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["\u5355\u667a\u80fd\u4f53", "\u591a\u667a\u80fd\u4f53"], fontsize=11.5)
        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(0, 40)
        ax.set_title(f"Task {t}", fontsize=13, fontweight="bold")
    fig.suptitle("\u914d\u5bf9\u4e2a\u4f53\u8f68\u8ff9：\u6bcf\u4f4d\u88ab\u8bd5\u7684\u603b\u65f6\u957f（\u5355 → \u591a\u667a\u80fd\u4f53）", fontsize=15, y=0.965, fontweight="bold")
    note(fig, "\u6ce8：\u7eff\u7ebf=\u591a\u667a\u80fd\u4f53\u66f4\u5feb，\u7ea2\u7ebf=\u591a\u667a\u80fd\u4f53\u66f4\u6162；\u6bcf\u4f4d\u88ab\u8bd5\u4e00\u6761\u8fde\u7ebf。\u6570\u636e\u6765\u6e90：\u5b9e\u9a8c\u6570\u636e\u8bb0\u5f55\u8868（n=4）。")
    save(fig, "31-\u914d\u5bf9\u4e2a\u4f53\u8f68\u8ff9.png")


def fig_27_effect(exp):
    """32 \u6548\u5e94\u91cf\u4e0e\u663e\u8457\u6027（\u6c14\u6ce1\u56fe）"""
    rows = _exp_stats(exp)
    fig = new_fig(10.5, 6.0)
    ax = fig.add_axes([0.10, 0.16, 0.62, 0.70])
    style(ax)
    colors = {"\u603b\u65f6\u957f(min)": BLUE, "\u4ecb\u5165\u6b21\u6570": PURPLE, "\u4ecb\u5165\u65f6\u957f(min)": ORANGE, "\u4ea7\u51fa\u8d28\u91cf": GREEN}
    markers = {"A": "o", "B": "s", "C": "^"}
    for r in rows:
        if not np.isfinite(r["p"]) or not np.isfinite(r["r"]):
            continue
        ax.scatter(r["p"], r["r"], s=60 + r["r"] * 420, color=colors[r["metric"]],
                   marker=markers[r["task"]], alpha=0.85, edgecolors=INK, linewidths=0.8, zorder=3)
    ax.axvspan(0, 0.05, color=LIGHTB, zorder=0)
    ax.text(0.025, 1.255, "p < .05", ha="center", va="top", fontsize=10, color=INK)
    ax.axhline(0.5, color=LGRAY, lw=0.8, ls=":")
    ax.text(0.98, 0.52, "r = 0.50", fontsize=10, color=GRAY, ha="right")
    ax.set_xlim(0, 1.02); ax.set_ylim(0, 1.30)
    ax.set_xlabel("p \u503c", fontsize=12)
    ax.set_ylabel("\u6548\u5e94\u91cf r（Wilcoxon \u8fd1\u4f3c）", fontsize=12)
    h1 = [plt.Line2D([0], [0], marker=m, color="w", markerfacecolor=LGRAY,
                     markersize=8, label=f"Task {t}") for t, m in markers.items()]
    h2 = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c,
                     markersize=8, label=l) for l, c in colors.items()]
    ax.legend(handles=h1 + h2, loc="center left", bbox_to_anchor=(1.04, 0.50),
              fontsize=10, frameon=True, edgecolor=INK, title="\u6807\u8bb0：\u4efb\u52a1 ｜ \u989c\u8272：\u6307\u6807",
              title_fontsize=9.5)
    set_title(ax, "\u5bf9\u6bd4\u5b9e\u9a8c\u5404\u6307\u6807\u7684\u6548\u5e94\u91cf\u4e0e\u663e\u8457\u6027", fs=15)
    note(fig, "\u6ce8：\u4efb\u52a1 A/B \u65f6\u95f4\u4e0e\u4ecb\u5165\u7c7b\u6307\u6807 r≈0.91、p>0.05（\u5c0f\u6837\u672c n=4），\u7ed3\u8bba\u4e3a\u65b9\u5411\u6027\u652f\u6301。"
              "\u6570\u636e\u6765\u6e90：04-\u5bf9\u6bd4\u5b9e\u9a8c\u5206\u6790.csv。")
    save(fig, "32-\u6548\u5e94\u91cf\u4e0e\u663e\u8457\u6027.png")


# ==================================================================

# ==================================================================
def fig_28_dda():
    """04 DDA \u4e09\u9636\u6bb5\u6a21\u578b"""
    fig = new_fig(16, 9.5)
    ax = fig.add_axes([0.02, 0.03, 0.96, 0.92]); ax.set_axis_off()
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.text(50, 97.5, "DDA \u4e09\u9636\u6bb5\u6a21\u578b：\u90e8\u7f72 → \u59d4\u6258 → \u6c89\u6dc0", ha="center",
            fontsize=32, fontweight="bold")
    ax.text(50, 92.5, "\u628a“\u7cfb\u7edf\u7ea7\u6280\u672f\u91c7\u7eb3”\u63a8\u8fdb\u4e3a“\u4efb\u52a1\u7ea7\u59d4\u6258\u51b3\u7b56”", ha="center",
            fontsize=22, color=GRAY)
    box(ax, (22, 62), 27, 30, "\u90e8\u7f72\nDeploy", fc=LIGHTB, fs=30, weight="bold",
        sub="SBDP\n\u81ea\u4e3e\u5f0f\u90e8\u7f72\u534f\u8bae", sub_fs=20)
    box(ax, (50, 62), 27, 30, "\u59d4\u6258\nDelegate", fc="white", fs=30, weight="bold",
        sub="\u4efb\u52a1\u7ea7\n“\u81ea\u5236—\u5916\u8d2d”\u51b3\u7b56", sub_fs=20)
    box(ax, (78, 62), 27, 30, "\u6c89\u6dc0\nAccumulate", fc=LIGHTG, fs=30, weight="bold",
        sub="\u8bb0\u5fc6＝\n\u5173\u7cfb\u4e13\u7528\u6027\u6295\u8d44", sub_fs=20)
    arr(ax, (37, 62), (43, 62), lw=3.2, ms=26)
    arr(ax, (63, 62), (69, 62), lw=3.2, ms=26)

    ax.add_patch(FancyArrowPatch((78, 77), (58, 77), arrowstyle="-|>", mutation_scale=26,
                                 linewidth=3.0, color=INK, connectionstyle="arc3,rad=0.25",
                                 shrinkA=1, shrinkB=1, zorder=2))
    ax.text(65, 83.5, "\u4fe1\u4efb\u6269\u5927\u59d4\u6258\u8fb9\u754c、\n\u6301\u7eed\u4f7f\u7528", fontsize=20, color=INK,
            ha="center", va="center", linespacing=1.6)
    ax.text(65, 87.0, "Experience updates delegation\nand continued use", fontsize=15.5, color=INK,
            ha="center", va="center", linespacing=1.25, zorder=4)

    ax.add_patch(FancyArrowPatch((22, 42), (78, 42), arrowstyle="-|>", mutation_scale=18,
                                 linewidth=2.6, color=GRAY, linestyle=(0, (4, 2)),
                                 shrinkA=1, shrinkB=1, zorder=2))
    ax.text(50, 36.5, "\u964d\u4f4e\u8f6c\u6362\u6210\u672c", ha="center", va="center", fontsize=20, color=GRAY)
    props = [("P1\nDeployment enables delegation", "Deployment burden is an initial\nbarrier to delegation", BLUE),
             ("P2\nDelegation boundary formation", "Perceived capability, trust, and interaction cost\nshape allocation; failures may\nreduce later delegation", PURPLE),
             ("P3\nAccumulation and continuance", "Memory may improve fit and create\nrelationship-specific investment", GREEN),
             ("P4\nArchitectural boundary", "Multi-agent coordination may help on\ndecomposable tasks, but not necessarily\non judgment-heavy tasks", ORANGE)]
    for i, (t, d, c) in enumerate(props):
        x = 13 + i * 25
        box(ax, (x, 14), 22, 26, t, fc="white", ec=c, fs=14.5, weight="bold", sub=d, sub_fs=11.5)
    note(fig, "\u6ce8：\u4f9d\u636e\u7814\u7a76\u62a5\u544a 2.6 \u7ed8\u5236；\u56db\u4e2a\u547d\u9898\u5206\u522b\u5bf9\u5e94\u5047\u8bbe H1—H4。", x=0.03, fs=14)
    save(fig, "04-DDA\u4e09\u9636\u6bb5\u6a21\u578b.png")


def fig_29_architecture():
    """02 Orchestrator-worker-checker architecture."""
    fig = new_fig(12.5, 7.8)
    ax = fig.add_axes([0.03, 0.04, 0.94, 0.90])
    ax.set_axis_off()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    ax.text(50, 97, "Orchestrator-worker-checker multi-agent architecture",
            ha="center", fontsize=17, fontweight="bold")
    ax.text(50, 92.5, "Explicit verification loop with an auditable personal-memory layer",
            ha="center", fontsize=11, color=GRAY)

    box(ax, (50, 83), 23, 11, "User", fc="white", fs=14, weight="bold",
        sub="Requirements, checking, and final review", sub_fs=9.2)
    box(ax, (50, 63), 30, 15, "Orchestrator", fc=LIGHTB, fs=15, weight="bold",
        sub="Task decomposition, integration, and acceptance", sub_fs=9.4)
    box(ax, (28, 37), 24, 14, "Worker", fc="white", fs=14, weight="bold",
        sub="Bounded role and tool use", sub_fs=9.4)
    box(ax, (72, 37), 24, 14, "Checker", fc=LIGHTG, fs=14, weight="bold",
        sub="Output comparison and verification", sub_fs=9.4)
    box(ax, (50, 13), 44, 11, "Personal memory", fc="white", fs=13.5, weight="bold",
        sub="Hot memory / cold memory / auditable timeline", sub_fs=9.4)

    arr(ax, (47, 77.4), (47, 70.7), lw=1.8, ms=14)
    ax.text(44.8, 74.1, "Delegation request", ha="right", va="center", fontsize=10.5, color=INK)
    arr(ax, (53, 70.7), (53, 77.4), lw=1.8, ms=14)
    ax.text(55.2, 74.1, "Delivered output", ha="left", va="center", fontsize=10.5, color=INK)

    arr(ax, (42, 55.5), (32.5, 44.2), lw=1.9, ms=15)
    ax.text(31.5, 51.4, "1  Task decomposition", ha="center", fontsize=10.5, color=INK)
    arr(ax, (58, 55.5), (67.5, 44.2), lw=1.9, ms=15)
    ax.text(68.5, 51.4, "2  Assign subtasks", ha="center", fontsize=10.5, color=INK)

    arr(ax, (40.2, 37), (59.8, 37), lw=1.9, ms=15)
    ax.text(50, 40.6, "3  Submit output", ha="center", fontsize=10.5, color=INK)

    ax.add_patch(FancyArrowPatch((81.5, 44), (65, 63), arrowstyle="-|>", mutation_scale=15,
                                 linewidth=1.8, color=INK, connectionstyle="arc3,rad=-0.28",
                                 shrinkA=1, shrinkB=1, zorder=3))
    ax.text(84.5, 55.5, "4  Verification feedback", ha="center", va="center",
            fontsize=10.5, color=INK, rotation=58)

    ax.plot([35, 17, 17, 28], [62, 62, 13, 13], color=PURPLE, lw=1.6,
            linestyle=(0, (4, 2)), zorder=2)
    ax.add_patch(FancyArrowPatch((17, 13), (28, 13), arrowstyle="-|>", mutation_scale=14,
                                 linewidth=1.6, color=PURPLE, linestyle=(0, (4, 2)),
                                 shrinkA=0, shrinkB=1, zorder=3))
    ax.text(13.7, 38, "5  Memory update", ha="center", va="center", fontsize=10.5,
            color=PURPLE, rotation=90)

    note(fig, "Note: Steps 1-5 show the collaboration sequence for one delegated task; memory remains readable and auditable.", x=0.03)
    save(fig, "02-\u7edf\u7b79\u6267\u884c\u6838\u67e5\u67b6\u6784.png")


def fig_30_triangulation():
    """05 \u7814\u7a76\u8bbe\u8ba1\u7684\u4e09\u89d2\u6d4b\u91cf"""
    fig = new_fig(11.5, 7.0)
    ax = fig.add_axes([0.02, 0.04, 0.96, 0.90]); ax.set_axis_off()
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.text(50, 97, "\u7814\u7a76\u8bbe\u8ba1：\u4e09\u89d2\u6d4b\u91cf（\u4e09\u4e2a\u5b50\u7814\u7a76\u6536\u655b）", ha="center",
            fontsize=17, fontweight="bold")
    ax.text(50, 92.5, "\u5171\u540c\u7406\u8bba\u6846\u67b6（DDA \u6a21\u578b）\u4e0e\u5171\u540c\u4eba\u5de5\u5236\u54c1（\u6846\u67b6\u4e0e\u5411\u5bfc）", ha="center",
            fontsize=11.5, color=GRAY)
    box(ax, (22, 64), 27, 20, "\u7814\u7a761\n\u5236\u54c1\u53ef\u7528\u6027", fc=LIGHTB, fs=14.5, weight="bold",
        sub="\u90e8\u7f72\u53ef\u7528\u6027\u6d4b\u8bd5 · H1", sub_fs=10.5)
    box(ax, (50, 26), 27, 20, "\u7814\u7a762\n\u59d4\u6258\u884c\u4e3a\u4e0e\u6301\u7eed\u4f7f\u7528", fc="white", fs=14.5, weight="bold",
        sub="\u95ee\u5377＋\u8bbf\u8c08＋\u65e5\u5fd7 · H2、H3", sub_fs=10.5)
    box(ax, (78, 64), 27, 20, "\u7814\u7a763\n\u5355 vs \u591a\u667a\u80fd\u4f53", fc=LIGHTG, fs=14.5, weight="bold",
        sub="\u53d7\u63a7\u5bf9\u6bd4\u5b9e\u9a8c · H4", sub_fs=10.5)
    box(ax, (50, 82), 27, 12, "\u4e09\u89d2\u6d4b\u91cf\u7efc\u5408", fc=LIGHTO, fs=14.5, weight="bold",
        sub="\u6536\u655b\u56de\u7b54 RQ1—RQ3", sub_fs=10.5)
    arr(ax, (30, 54), (44, 36), lw=1.8, ms=15)
    arr(ax, (70, 54), (56, 36), lw=1.8, ms=15)
    arr(ax, (30, 74), (44, 76), lw=1.8, ms=15)
    arr(ax, (70, 74), (56, 76), lw=1.8, ms=15)
    arr(ax, (50, 36), (50, 76), lw=1.8, ms=15)
    note(fig, "\u6ce8：\u4f9d\u636e\u7814\u7a76\u62a5\u544a 3.1 \u7ed8\u5236；\u4e09\u4e2a\u5b50\u7814\u7a76\u4ece\u4e0d\u540c\u8bc1\u636e\u6e90\u6536\u655b\u5230\u5bf9\u7814\u7a76\u95ee\u9898\u7684\u56de\u7b54。", x=0.03)
    save(fig, "05-\u7814\u7a76\u8bbe\u8ba1\u4e09\u89d2\u6d4b\u91cf.png")


def fig_31_theory():
    """03 \u7406\u8bba\u6574\u5408\u6846\u67b6"""
    fig = new_fig(12.5, 7.0)
    ax = fig.add_axes([0.02, 0.04, 0.96, 0.90]); ax.set_axis_off()
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.text(50, 97, "\u7406\u8bba\u6574\u5408：\u4efb\u52a1\u7ea7\u59d4\u6258\u51b3\u7b56\u7684\u673a\u5236\u89e3\u91ca", ha="center",
            fontsize=16, fontweight="bold")
    box(ax, (50, 78), 30, 15, "DDA \u4e09\u9636\u6bb5\u6a21\u578b", fc=LIGHTB, fs=16, weight="bold",
        sub="\u90e8\u7f72—\u59d4\u6258—\u6c89\u6dc0（P1—P4）", sub_fs=11)
    theories = [("\u4efb\u52a1—\u6280\u672f\u5339\u914d TTF", "\u54ea\u4e9b\u4efb\u52a1\u503c\u5f97\u59d4\u6258", 14, LIGHTB),
                ("\u4ea4\u6613\u6210\u672c\u7406\u8bba", "\u59d4\u6258\u8fd8\u662f\u81ea\u5236（\u673a\u5236）", 39, LIGHTG),
                ("\u671f\u671b\u786e\u8ba4\u6a21\u578b ECT", "\u6301\u7eed\u4f7f\u7528（\u65f6\u95f4\u7ef4\u5ea6）", 64, "white"),
                ("\u7b97\u6cd5\u538c\u6076", "\u59d4\u6258\u4e2d\u7684\u884c\u4e3a\u504f\u5dee", 89, LIGHTO)]
    for t, d, x, fc in theories:
        box(ax, (x, 38), 20, 14, t, fc=fc, fs=13.5, weight="bold", sub=d, sub_fs=10.5)
    arr(ax, (20, 46), (44, 70), lw=1.8, ms=15)
    arr(ax, (42, 46), (48, 70), lw=1.8, ms=15)
    arr(ax, (62, 46), (54, 70), lw=1.8, ms=15)
    arr(ax, (84, 46), (58, 70), lw=1.8, ms=15)
    box(ax, (50, 16), 56, 10, "\u56db\u7c7b\u7406\u8bba\u6574\u5408\u4e3a DDA \u6a21\u578b，\u5bf9\u5e94\u56db\u4e2a\u53ef\u8bc1\u4f2a\u547d\u9898 P1—P4",
        fc="white", fs=12.5)
    note(fig, "\u6ce8：\u4f9d\u636e\u7814\u7a76\u62a5\u544a 2.4—2.6 \u7ed8\u5236。", x=0.03)
    save(fig, "03-\u7406\u8bba\u6574\u5408\u6846\u67b6.png")


def fig_32_attributes():
    """12 \u59d4\u6258\u8fb9\u754c\u7684\u4e09\u5c5e\u6027\u6846\u67b6"""
    fig = new_fig(11.5, 7.0)
    ax = fig.add_axes([0.02, 0.04, 0.96, 0.90]); ax.set_axis_off()
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.text(50, 97.5, "\u59d4\u6258\u8fb9\u754c\u7684\u4f4d\u7f6e\u7531\u4e09\u7c7b\u4efb\u52a1\u7ed3\u6784\u5c5e\u6027\u5171\u540c\u51b3\u5b9a", ha="center",
            fontsize=17, fontweight="bold")
    box(ax, (50, 52), 24, 14, "\u59d4\u6258\u8fb9\u754c", fc=LIGHTO, fs=16, weight="bold",
        sub="\u4efb\u52a1\u7ea7“\u81ea\u5236—\u5916\u8d2d”\u51b3\u7b56", sub_fs=11)
    box(ax, (20, 80), 22, 14, "\u8f93\u51fa\u53ef\u9a8c\u8bc1\u6027", fc=LIGHTB, fs=13.5, weight="bold",
        sub="\u7ed3\u679c\u53ef\u5feb\u901f\u6838\u5bf9", sub_fs=10.5)
    box(ax, (80, 80), 22, 14, "\u540e\u679c\u53ef\u9006\u6027", fc=LIGHTB, fs=13.5, weight="bold",
        sub="\u9519\u8bef\u53ef\u91cd\u6765", sub_fs=10.5)
    box(ax, (50, 16), 22, 14, "\u4ef7\u503c\u7f16\u7801\u7a0b\u5ea6", fc=LIGHTB, fs=13.5, weight="bold",
        sub="\u627f\u8f7d\u76ee\u6807\u4e0e\u4ef7\u503c\u5224\u65ad\u7684\u591a\u5c11", sub_fs=10.5)
    arr(ax, (30, 74), (44, 60), lw=1.8, ms=15)
    arr(ax, (70, 74), (56, 60), lw=1.8, ms=15)
    arr(ax, (50, 24), (50, 44), lw=1.8, ms=15)
    box(ax, (50, 90), 66, 6, "\u53ef\u9a8c\u8bc1\u6027↑、\u53ef\u9006\u6027↑、\u4ef7\u503c\u7f16\u7801↓ → \u59d4\u6258\u7387↑（\u4e2d\u95f4\u73af\u8282）",
        fc="white", fs=12.5)
    note(fig, "\u6ce8：\u4f9d\u636e\u7814\u7a76\u62a5\u544a 4.2.1 \u4e0e 5.2 \u7ed8\u5236；\u4efb\u52a1\u7ed3\u6784\u5c5e\u6027\u76f8\u5bf9\u7a33\u5b9a，\u6545\u59d4\u6258\u8fb9\u754c\u77ed\u671f\u7a33\u5b9a。", x=0.03)
    save(fig, "12-\u59d4\u6258\u8fb9\u754c\u4e09\u5c5e\u6027\u6846\u67b6.png")


def fig_33_summary_table():
    """33 \u6838\u5fc3\u7ed3\u679c\u6c47\u603b（\u8868\u683c）"""
    rows = [
        ["\u7814\u7a761 \u90e8\u7f72", "\u5b8c\u6210\u7387", "80%（4/5）", "H1 \u9608\u503c ≥ 80%，\u8fbe\u6210"],
        ["\u7814\u7a761 \u90e8\u7f72", "\u5e73\u5747\u90e8\u7f72\u8017\u65f6", "29.5 min（26—34）", "\u5b8c\u6210\u8005\u53e3\u5f84"],
        ["\u7814\u7a761 \u90e8\u7f72", "SUS \u5747\u503c", "72.25（68—76）", "\u5747 ≥ 68 \u53ef\u7528\u9608\u503c"],
        ["\u7814\u7a762 \u59d4\u6258", "\u4e03\u73af\u8282\u59d4\u6258\u7387\u5dee\u5f02", "Q = 54.23", "p < 0.001，\u652f\u6301 H2"],
        ["\u7814\u7a762 \u59d4\u6258", "\u9996\u6b21\u5931\u8d25\u524d\u540e 14 \u5929\u59d4\u6258\u9891\u7387", "0.135 → 0.060 \u6b21/\u5929", "W = 80，p < 0.001，\u652f\u6301 H3a"],
        ["\u7814\u7a762 \u59d4\u6258", "\u65f6\u95f4\u8f74\u884c\u6570 × \u6301\u7eed\u4f7f\u7528\u610f\u5411", "ρ = 0.850", "p < 0.001，\u652f\u6301 H3b"],
        ["\u7814\u7a762 \u59d4\u6258", "\u66f4\u65b0\u9891\u6b21 × \u6301\u7eed\u4f7f\u7528\u610f\u5411", "ρ = 0.781", "p = 0.002，\u652f\u6301 H3b"],
        ["\u7814\u7a763 \u5bf9\u6bd4", "\u603b\u65f6\u957f（\u4efb\u52a1 A）", "29.75 → 16.25 min", "r ≈ 0.91，\u65b9\u5411\u6027\u652f\u6301 H4"],
        ["\u7814\u7a763 \u5bf9\u6bd4", "\u4eba\u5de5\u4ecb\u5165\u6b21\u6570（\u4efb\u52a1 A）", "14.5 → 7.0 \u6b21", "r ≈ 0.91，\u65b9\u5411\u6027\u652f\u6301 H4"],
        ["\u7814\u7a763 \u5bf9\u6bd4", "\u4ea7\u51fa\u8d28\u91cf（\u4efb\u52a1 B）", "3.50 → 4.31 \u5206", "\u591a\u667a\u80fd\u4f53\u4e0d\u4f4e，\u8d28\u91cf\u4e0d\u964d"],
    ]
    fig = new_fig(11, 6.2)
    ax = fig.add_axes([0.01, 0.06, 0.98, 0.82]); ax.set_axis_off()
    col_w = [0.16, 0.28, 0.22, 0.34]
    headers = ["\u7814\u7a76", "\u6307\u6807", "\u7ed3\u679c", "\u68c0\u9a8c / \u5224\u5b9a"]
    tbl = ax.table(cellText=rows, colLabels=headers, colWidths=col_w,
                   cellLoc="left", loc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    tbl.scale(1, 1.7)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor(INK)
        cell.set_linewidth(0.7)
        cell.set_facecolor("white")
        if r == 0:
            cell.set_facecolor(LIGHTG)
            cell.set_text_props(fontweight="bold", ha="center")
        else:
            cell.set_text_props(ha="left" if c in (1, 2, 3) else "center")
    ax.set_title("\u7814\u7a76\u6838\u5fc3\u7ed3\u679c\u6c47\u603b", fontsize=16, loc="left", fontweight="bold", pad=12)
    note(fig, "\u6ce8：\u7814\u7a763 \u56e0\u6bcf\u6761\u4ef6 n=4，Wilcoxon \u68c0\u9a8c\u672a\u8fbe p<0.05，\u62a5\u544a\u8868\u8ff0\u4e3a“\u65b9\u5411\u6027\u652f\u6301、\u6548\u5e94\u91cf r≈0.91”。")
    save(fig, "33-\u6838\u5fc3\u7ed3\u679c\u6c47\u603b\u8868.png")


# ==================================================================

# ==================================================================
def verify(q, log, exp, mem):
    X = q[G1].apply(pd.to_numeric, errors="coerce").values
    n, k = X.shape
    total = X.sum(); col = X.sum(axis=0); row = X.sum(axis=1)
    denom = k * total - (row ** 2).sum()
    Q = (k - 1) * (k * (col ** 2).sum() - total ** 2) / denom
    p = 1 - stats.chi2.cdf(Q, k - 1)
    print(f"H2  Cochran's Q = {Q:.3f}, p = {p:.3f}")
    lg = log.dropna(subset=["event_date"]).sort_values(["user_id", "seq"])
    WIN = pd.Timedelta(days=14)
    stage_rows = []
    for uid, g in lg.groupby("user_id"):
        for st, sub in g.groupby("stage"):
            fail = sub.loc[sub["outcome"].isin(["\u5931\u8d25", "\u90e8\u5206\u6210\u529f"]), "event_date"]
            if fail.empty:
                continue
            fd = fail.min()
            nb = int(((sub["event_date"] >= fd - WIN) & (sub["event_date"] < fd)).sum())
            na = int(((sub["event_date"] > fd) & (sub["event_date"] <= fd + WIN)).sum())
            if nb < 1:
                continue
            stage_rows.append((uid, nb / 14, na / 14))
    user_rates = pd.DataFrame(stage_rows, columns=["user_id", "before", "after"]).groupby("user_id")[["before", "after"]].mean()
    w, p3 = stats.wilcoxon(user_rates["before"], user_rates["after"], method="exact")
    print(f"H3a W = {w:.1f}, p = {p3:.4f}, user-level rates {user_rates['before'].mean():.3f} -> {user_rates['after'].mean():.3f}")
    q2 = q.copy()
    q2["continuance"] = q2[["F1", "F2", "F3"]].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    m = mem.merge(q2[["link_id", "continuance"]], on="link_id", how="inner").dropna()
    r1, p1 = stats.spearmanr(m["timeline_lines"], m["continuance"])
    r2, p2 = stats.spearmanr(m["mem_updates"], m["continuance"])
    print(f"H3b rho = {r1:.3f} (p={p1:.3f}); rho = {r2:.3f} (p={p2:.3f})")
    a = exp[(exp.task == "A") & (exp.condition == "single")].total_time_min.mean()
    b = exp[(exp.task == "A") & (exp.condition == "multi")].total_time_min.mean()
    print(f"Experiment Task A total time: {a:.2f} vs {b:.2f} min")


def main():
    os.makedirs(OUT, exist_ok=True)
    q, log, exp, mem, sus = load()
    verify(q, log, exp, mem)
    jobs = [

        ("01-\u90e8\u7f72\u6210\u672c\u538b\u7f29\u793a\u610f.png", lambda: fig_04_cost_compress(sus)),

        ("02-\u7edf\u7b79\u6267\u884c\u6838\u67e5\u67b6\u6784.png", fig_29_architecture),
        ("03-\u7406\u8bba\u6574\u5408\u6846\u67b6.png", fig_31_theory),
        ("04-DDA\u4e09\u9636\u6bb5\u6a21\u578b.png", fig_28_dda),

        ("05-\u7814\u7a76\u8bbe\u8ba1\u4e09\u89d2\u6d4b\u91cf.png", fig_30_triangulation),
        ("06-SBDP\u516d\u9636\u6bb5\u90e8\u7f72\u6d41\u7a0b.png", fig_03_sbdp_flow),

        ("07-\u90e8\u7f72\u53ef\u7528\u6027\u6d4b\u8bd5\u7ed3\u679c.png", lambda: fig_01_dashboard(sus)),
        ("08-SUS\u5f97\u5206\u4e0e\u53ef\u7528\u6027\u5206\u7ea7.png", lambda: fig_02_sus_grading(sus)),

        ("09-\u4f7f\u7528\u72b6\u6001\u5206\u5e03.png", lambda: fig_18_usage_groups(q)),
        ("10-\u4efb\u52a1\u6d41\u4e03\u73af\u8282\u59d4\u6258\u7387.png", lambda: fig_05_boundary(q)),
        ("11-\u4efb\u52a1\u6d41\u4e03\u73af\u8282\u59d4\u6258\u7387-\u9762\u79ef\u56fe.png", lambda: fig_06_arch(q)),
        ("12-\u59d4\u6258\u8fb9\u754c\u4e09\u5c5e\u6027\u6846\u67b6.png", fig_32_attributes),
        ("13-\u59d4\u6258\u6536\u56de\u4e8b\u4ef6\u6d41.png", lambda: fig_07_event_flow(log)),
        ("14-\u59d4\u6258\u4e8b\u4ef6\u7ed3\u679c\u6784\u6210.png", lambda: fig_08_outcome_donut(log)),
        ("15-\u73af\u8282\u4e0e\u7ed3\u679c\u70ed\u529b\u56fe.png", lambda: fig_09_stage_outcome_heat(log)),
        ("16-\u5931\u8d25\u539f\u56e0\u5206\u5e03.png", lambda: fig_10_fail_reason(log)),
        ("17-\u9519\u8bef\u66b4\u9732\u65b9\u5f0f\u4e0e\u7ed3\u679c.png", lambda: fig_11_error_exposure(log)),
        ("18-\u8fed\u4ee3\u6b21\u6570\u5206\u5e03.png", lambda: fig_12_iterations(log)),
        ("19-\u6536\u56de\u539f\u56e0\u5206\u5e03.png", lambda: fig_13_withdraw_reasons(q)),
        ("20-\u59d4\u6258\u4e8b\u4ef6\u5468\u5ea6\u65f6\u95f4\u5e8f\u5217.png", lambda: fig_19_weekly(log)),
        ("21-\u5404\u7528\u6237\u59d4\u6258\u4e8b\u4ef6\u6784\u6210.png", lambda: fig_20_user_events(log)),
        ("22-\u9996\u6b21\u5931\u8d25\u524d\u540e\u59d4\u6258\u9891\u7387.png", lambda: fig_14_h3a(log)),
        ("23-\u8bb0\u5fc6\u79ef\u7d2f\u4e0e\u6301\u7eed\u4f7f\u7528\u610f\u5411.png", lambda: fig_15_memory(q, mem)),
        ("24-\u95ee\u5377\u91cf\u8868\u4fe1\u5ea6.png", fig_16_alpha),
        ("25-\u611f\u77e5\u6784\u5ff5\u96f7\u8fbe\u56fe.png", lambda: fig_17_radar(q)),

        ("26-\u603b\u65f6\u957f\u5bf9\u6bd4.png", lambda: fig_21_time(exp)),
        ("27-\u4eba\u5de5\u4ecb\u5165\u6b21\u6570\u5bf9\u6bd4.png", lambda: fig_22_count(exp)),
        ("28-\u4eba\u5de5\u4ecb\u5165\u65f6\u957f\u5bf9\u6bd4.png", lambda: fig_23_intervention(exp)),
        ("29-\u4ea7\u51fa\u8d28\u91cf\u5bf9\u6bd4.png", lambda: fig_24_quality(exp)),
        ("30-\u591a\u667a\u80fd\u4f53\u76f8\u5bf9\u589e\u76ca.png", lambda: fig_25_gain(exp)),
        ("31-\u914d\u5bf9\u4e2a\u4f53\u8f68\u8ff9.png", lambda: fig_26_slope(exp)),
        ("32-\u6548\u5e94\u91cf\u4e0e\u663e\u8457\u6027.png", lambda: fig_27_effect(exp)),

        ("33-\u6838\u5fc3\u7ed3\u679c\u6c47\u603b\u8868.png", fig_33_summary_table),
    ]
    print(f"\nGenerating {len(jobs)} figures -> {OUT}")
    for name, fn in jobs:
        try:
            fn()
        except Exception as e:
            import traceback
            print(f"  [FAIL] {name}: {e}")
            traceback.print_exc()
    print("All figures generated.")


if __name__ == "__main__":
    main()
