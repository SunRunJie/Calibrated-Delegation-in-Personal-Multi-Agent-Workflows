# -*- coding: utf-8 -*-
"""
====================================================================
 04-研究报告图表 / 图表生成.py（科研论文风格版）
 为《多智能体在个人任务流中的应用》研究报告批量生成插图
--------------------------------------------------------------------
 数据：03-已收集数据/*.csv
 输出：04-研究报告图表/*.png
 用法：d:/南京大学本科/早期科研专用工作区/.venv/Scripts/python.exe 图表生成.py
====================================================================
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
warnings.filterwarnings("ignore")
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ------------------------------------------------------------------
# 全局字体与画布
# ------------------------------------------------------------------
plt.rcParams["font.family"] = ["Times New Roman", "SimSun"]
plt.rcParams["font.serif"] = ["Times New Roman", "SimSun"]
plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["savefig.facecolor"] = "white"
plt.rcParams["axes.edgecolor"] = "#111111"
plt.rcParams["axes.linewidth"] = 0.9
plt.rcParams["axes.labelcolor"] = "#111111"
plt.rcParams["xtick.color"] = "#111111"
plt.rcParams["ytick.color"] = "#111111"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

# ------------------------------------------------------------------
# 学术配色（色盲友好、对比清晰）
# ------------------------------------------------------------------
INK = "#111111"      # 正文黑
GRAY = "#555555"     # 次级文字
LGRAY = "#888888"    # 注释文字
GRIDC = "#C9C9C9"    # 网格线
BLUE = "#4C72B0"     # 蓝
ORANGE = "#DD8452"   # 橙
GREEN = "#55A868"    # 绿
RED = "#C44E52"      # 红
PURPLE = "#8172B2"   # 紫
CYAN = "#64B5CD"     # 青
BROWN = "#937860"    # 棕
GOLD = "#CCB974"     # 黄
LIGHTB = "#DCE6F2"   # 浅蓝（填充）
LIGHTG = "#E8E8E8"   # 浅灰（填充）
LIGHTO = "#FBE9DC"   # 浅橙（填充）

OUT_C = {"成功": GREEN, "部分成功": GOLD, "撤回": PURPLE, "失败": RED}
STAGES = ["需求界定", "信息检索", "信息整理", "分析推理", "内容生成", "执行操作", "判断决策"]
OUTCOMES = ["成功", "部分成功", "撤回", "失败"]
REASONS = ["能力不足", "输出不可靠", "不省时间", "隐私顾虑", "情感需求", "其他"]
EXPOSURES = ["当场发现并纠正", "事后发现", "未发现"]
G1 = [f"G1_{i}" for i in range(1, 8)]
H1 = [f"H1_{i}" for i in range(1, 6)]
SCALE_COLS = {"感知有用性": ["B1", "B2", "B3", "B4"],
              "感知易用性": ["C1", "C2", "C3", "C4"],
              "感知信任": ["D1", "D2", "D3", "D4"],
              "感知风险": ["E1", "E2", "E3"],
              "持续使用意向": ["F1", "F2", "F3"],
              "记忆感知": ["I1", "I2", "I3"]}
STAGE_LEVEL_C = {"需求界定": RED, "信息检索": BLUE, "信息整理": BLUE, "分析推理": PURPLE,
                 "内容生成": BLUE, "执行操作": PURPLE, "判断决策": RED}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "03-已收集数据")
OUT = os.path.dirname(os.path.abspath(__file__))
Q_CSV = os.path.join(DATA, "问卷数据30人.csv")
L_CSV = os.path.join(DATA, "日志编码表.csv")
E_CSV = os.path.join(DATA, "实验数据记录表.csv")
M_CSV = os.path.join(DATA, "记忆指标表.csv")
SUS_CSV = os.path.join(DATA, "部署可用性测试.csv")

# ------------------------------------------------------------------
# 基础工具
# ------------------------------------------------------------------
def load():
    q = pd.read_csv(Q_CSV, encoding="utf-8-sig")
    q = q[pd.to_numeric(q["J2"], errors="coerce") == 2].copy()      # N=29
    log = pd.read_csv(L_CSV, encoding="utf-8-sig")
    log["event_date"] = pd.to_datetime(log["event_date"], errors="coerce")
    exp = pd.read_csv(E_CSV, encoding="utf-8-sig")
    rcols = [c for c in exp.columns if c.startswith("r") and "_" in c]
    exp["quality_score"] = exp[rcols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    mem = pd.read_csv(M_CSV, encoding="utf-8-sig")
    sus = pd.read_csv(SUS_CSV, encoding="utf-8-sig")
    return q, log, exp, mem, sus


def new_fig(w=10, h=6):
    return plt.figure(figsize=(w, h), facecolor="white")


def style(ax, grid="y", xticks=True):
    """学术坐标轴：白底、黑色细框、向内刻度、浅灰网格"""
    ax.set_facecolor("white")
    for s in ax.spines.values():
        s.set_color("#111111")
        s.set_linewidth(0.9)
    ax.tick_params(colors="#111111", labelsize=11, length=4, width=0.9)
    if grid == "y":
        ax.grid(axis="y", color="#DDDDDD", lw=0.7, ls=(0, (1, 3)))
        ax.set_axisbelow(True)
    elif grid == "both":
        ax.grid(axis="both", color="#DDDDDD", lw=0.7, ls=(0, (1, 3)))
        ax.set_axisbelow(True)
    if not xticks:
        ax.set_xticks([])


def set_title(ax, text, fs=14.5, pad=12, weight="bold"):
    """左对齐图题（类似 Word 图题排版）"""
    ax.set_title(text, fontsize=fs, color="#111111", pad=pad, loc="left", fontweight=weight)


def note(fig, text, x=0.015, y=0.012, fs=9):
    """图注：左下角灰色小字，学术规范"""
    fig.text(x, y, text, fontsize=fs, color=LGRAY, ha="left", va="bottom")


def bval(ax, xs, hs, color, width=0.6, edge=INK, lw=0.8, z=3, alpha=1.0, hatch=None, bottom=0):
    """实心柱（黑描边）"""
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
    """流程/概念图方框：白底或浅色填充 + 黑色细边框"""
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
    fig.savefig(os.path.join(OUT, name), dpi=dpi, bbox_inches="tight" if tight else None,
                facecolor="white")
    plt.close(fig)
    print("  [OK]", name)


# ==================================================================
# 研究1 · 部署可用性（RQ1 / H1）
# ==================================================================
def fig_01_dashboard(sus):
    """07 部署可用性测试结果（四子图）"""
    fig = new_fig(11.5, 8.0)
    comp = (sus["completion"] == "是").sum()
    total = len(sus)
    # 完成率环形
    ax = fig.add_axes([0.06, 0.57, 0.26, 0.33])
    style(ax, grid=False); ax.set_aspect("equal")
    ax.pie([comp, total - comp], startangle=90, counterclock=False,
           colors=[BLUE, LIGHTG],
           wedgeprops=dict(width=0.32, edgecolor=INK, linewidth=1.2))
    ax.text(0, 0.14, f"{comp / total * 100:.0f}%", ha="center", va="center",
            fontsize=26, color=INK, fontweight="bold")
    ax.text(0, -0.12, "完成率（4/5）", ha="center", va="center", fontsize=11.5, color=INK)
    ax.text(0, -0.30, "阈值 ≥ 80%", ha="center", va="center", fontsize=10, color=GRAY)
    set_title(ax, "（a）部署完成率", fs=13)
    # SUS 得分
    ax = fig.add_axes([0.40, 0.57, 0.54, 0.33])
    style(ax)
    sus = sus.sort_values("sus_score")
    names = sus["subject"].tolist()
    colors = [BLUE if s == "是" else RED for s in sus["completion"]]
    y = np.arange(len(names))
    barh(ax, y, sus["sus_score"], colors, height=0.55)
    for i, (sc, c) in enumerate(zip(sus["sus_score"], colors)):
        ax.text(sc + 1.5, i, f"{sc}", va="center", fontsize=11.5, color=INK)
    ax.axvline(68, color=RED, lw=1.2, ls="--")
    ax.text(68, len(names) + 0.3, "68（可用阈值）", fontsize=10, color=RED, ha="center")
    ax.set_yticks(y); ax.set_yticklabels(names)
    ax.set_ylim(-0.6, len(names) + 0.8)
    ax.set_xlim(0, 95)
    ax.set_xlabel("SUS 得分", fontsize=12)
    set_title(ax, "（b）SUS 系统可用性得分", fs=13)
    # 部署耗时
    ax = fig.add_axes([0.06, 0.045, 0.42, 0.42])
    style(ax)
    sus_t = sus.sort_values("time_min")
    x = np.arange(len(sus_t))
    bval(ax, x, sus_t["time_min"], BLUE, width=0.5)
    for xi, v, s in zip(x, sus_t["time_min"], sus_t["subject"]):
        tag = "（放弃）" if sus_t.loc[sus_t["subject"] == s, "completion"].iloc[0] == "否" else ""
        ax.text(xi, v + 1.2, f"{v}{tag}", ha="center", fontsize=11, color=INK)
    ax.set_xticks(x); ax.set_xticklabels(sus_t["subject"])
    ax.set_ylim(0, 52)
    ax.set_ylabel("分钟", fontsize=12)
    set_title(ax, "（c）独立部署耗时", fs=13)
    # 求助点
    ax = fig.add_axes([0.53, 0.045, 0.41, 0.42])
    style(ax)
    sus_h = sus.sort_values("help_points")
    x = np.arange(len(sus_h))
    bval(ax, x, sus_h["help_points"], ORANGE, width=0.5)
    for xi, v in zip(x, sus_h["help_points"]):
        ax.text(xi, v + 0.25, f"{v}", ha="center", fontsize=11.5, color=INK)
    ax.set_xticks(x); ax.set_xticklabels(sus_h["subject"])
    ax.set_ylim(0, 5.6)
    ax.set_ylabel("次数", fontsize=12)
    set_title(ax, "（d）部署求助点", fs=13)
    fig.suptitle("研究1 自举式部署协议（SBDP）可用性测试结果", fontsize=15, y=0.99, x=0.06,
                 ha="left", fontweight="bold")
    note(fig, "注：S1—S3、S5 独立完成部署；S4 于 42 min 放弃。完成者耗时 26—34 min（M=29.5），"
              "SUS 68—76（M=72.25）。数据来源：03-已收集数据/部署可用性测试.csv。")
    save(fig, "07-部署可用性测试结果.png")


def fig_02_sus_grading(sus):
    """08 SUS 得分与可用性分级"""
    fig = new_fig(10, 6.0)
    ax = fig.add_axes([0.13, 0.16, 0.80, 0.74])
    style(ax, grid="both")
    zones = [(0, 51, RED, "差"), (51, 68, ORANGE, "勉强可用"),
             (68, 85, GOLD, "可用"), (85, 101, GREEN, "优秀")]
    for lo, hi, c, lab in zones:
        ax.axvspan(lo, hi, color=matplotlib.colors.to_rgba(c, 0.12), zorder=0)
        ax.text((lo + hi) / 2, -0.9, lab, ha="center", fontsize=11, color=INK)
    sus = sus.sort_values("sus_score")
    y = np.arange(len(sus))
    colors = [BLUE if s == "是" else RED for s in sus["completion"]]
    ax.barh(y, sus["sus_score"], height=0.55, color=LIGHTB, edgecolor=INK, lw=0.8, zorder=2)
    for yi, (_, r), c in zip(y, sus.iterrows(), colors):
        ax.scatter(r["sus_score"], yi, s=52, color=c, edgecolors=INK, linewidths=1.0, zorder=4)
        ax.text(r["sus_score"] + 3, yi, f"{r['sus_score']}", va="center", fontsize=11.5, color=INK)
    ax.axvline(68, color=RED, lw=1.3, ls="--", zorder=5)
    ax.text(68, len(sus) + 0.25, "68（可用阈值）", fontsize=10, color=RED, ha="center")
    ax.set_yticks(y); ax.set_yticklabels(sus["subject"])
    ax.set_ylim(-1.2, len(sus) + 0.7)
    ax.set_xlim(0, 103)
    ax.set_xlabel("SUS 得分", fontsize=12)
    set_title(ax, "部署被试的 SUS 得分与可用性分级", fs=15)
    handles = [mpatches.Patch(color=BLUE, label="完成部署（4人）"),
               mpatches.Patch(color=RED, label="未完成（1人）")]
    ax.legend(handles=handles, loc="lower right", fontsize=10.5, frameon=True,
              edgecolor=INK, framealpha=1.0)
    note(fig, "注：完成者 SUS 均 ≥ 68，处于“可用”区间；未完成者 S4=42。"
              "数据来源：03-已收集数据/部署可用性测试.csv。")
    save(fig, "08-SUS得分与可用性分级.png")


def fig_03_sbdp_flow():
    """06 SBDP 六阶段部署流程"""
    fig = new_fig(12, 6.6)
    ax = fig.add_axes([0.02, 0.05, 0.96, 0.88]); ax.set_axis_off()
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    steps = ["两轮信息收集", "创建入口文件", "创建记忆目录", "写入记忆档案", "完成宣告", "持续使用"]
    subs = ["配置参数＋Bootstrap采访", "VS Code＋Copilot 环境", "记忆目录结构",
            "profile/priorities 等初始化", "零代码·可审计", "时间轴日志积累"]
    fills = [LIGHTB, LIGHTB, LIGHTB, LIGHTB, LIGHTB, LIGHTB]
    xs = np.linspace(9, 91, 6)
    y0 = 56
    for i, (s, sub, x) in enumerate(zip(steps, subs, xs)):
        box(ax, (x, y0), 13, 22, s, fc=fills[i], fs=12.5, weight="bold", sub=sub, sub_fs=9.5)
        ax.text(x, y0 + 17.5, f"阶段{i + 1}", ha="center", fontsize=10.5, color=GRAY)
        if i < 5:
            arr(ax, (x + 6.8, y0), (xs[i + 1] - 6.8, y0), lw=1.6, ms=14)
    # 底部：两轮信息收集
    box(ax, (24, 18), 26, 15, "第一轮：部署参数", fc="white", fs=11.5, sub="执行权限·工具链·身份", sub_fs=9.5)
    box(ax, (50, 18), 26, 15, "第二轮：Bootstrap 采访", fc="white", fs=11.5, sub="偏好·目标·关键人物", sub_fs=9.5)
    box(ax, (76, 18), 26, 15, "合并执行", fc="white", fs=11.5, sub="部署与认识用户一次完成", sub_fs=9.5)
    for xx in (24, 50):
        arr(ax, (xx, 26), (xs[0], y0 - 11), lw=1.3, ls="--", ms=11, color=GRAY)
    ax.text(50, 96, "SBDP 自举式部署协议：六阶段流程", ha="center", fontsize=16, fontweight="bold")
    ax.text(50, 90.5, "把专家劳动编码为智能体可执行的文档流程，用户全程不接触代码",
            ha="center", fontsize=11, color=GRAY)
    note(fig, "注：依据研究报告 3.2 与 4.1 的协议结构绘制。", x=0.03)
    save(fig, "06-SBDP六阶段部署流程.png")


def fig_04_cost_compress(sus):
    """01 部署成本压缩（专家配置 vs 引导式对话）"""
    fig = new_fig(11.5, 6.2)
    ax = fig.add_axes([0.02, 0.04, 0.96, 0.88]); ax.set_axis_off()
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.text(50, 97, "部署成本的压缩：专家配置 → 引导式对话", ha="center",
            fontsize=16, fontweight="bold")
    # 左侧
    box(ax, (24, 74), 34, 14, "传统手动配置", fc=LIGHTO, fs=14.5, weight="bold")
    items_l = ["环境配置（数小时）", "理解代码 / API", "多角色编排", "依赖专家劳动"]
    for i, t in enumerate(items_l):
        ax.text(24, 56 - i * 11, t, ha="center", fontsize=13.5, color=INK)
    # 右侧
    box(ax, (76, 74), 34, 14, "SBDP 引导式对话", fc=LIGHTB, fs=14.5, weight="bold")
    items_r = ["约 30 分钟（实测 M=29.5 min）", "零代码 · 纯文档", "智能体自主执行",
               "普通用户可独立完成"]
    for i, t in enumerate(items_r):
        ax.text(76, 56 - i * 11, t, ha="center", fontsize=13.5, color=INK)
    arr(ax, (43, 40), (57, 40), lw=2.8, ms=22)
    ax.text(50, 45, "成本压缩", ha="center", fontsize=13.5, fontweight="bold")
    ax.text(50, 6, "部署的认知负荷从技术域转移到对话域；对话是普通用户已具备的能力",
            ha="center", fontsize=13, color=GRAY)
    note(fig, "注：依据研究报告 1.1 与 4.1 绘制；实测数据见 07-部署可用性测试结果。", x=0.03)
    save(fig, "01-部署成本压缩示意.png")


# ==================================================================
# 研究2 · 委托边界与持续使用（RQ2 / H2、H3）
# ==================================================================
def _rates(q):
    return q[G1].apply(pd.to_numeric, errors="coerce").mean().values


def fig_05_boundary(q):
    """10 任务流七环节委托率（主图）"""
    rates = _rates(q)
    fig = new_fig(11, 6.2)
    ax = fig.add_axes([0.08, 0.16, 0.86, 0.72])
    style(ax)
    x = np.arange(7)
    colors = [STAGE_LEVEL_C[s] for s in STAGES]
    bval(ax, x, rates, colors, width=0.55)
    for xi, v in zip(x, rates):
        valtxt(ax, xi, v, fs=12, fmt="{:.2f}")
    # 平滑趋势线
    xs = np.linspace(0, 6, 300)
    spl = interpolate.make_interp_spline(x, rates, k=3, bc_type="natural")
    ys = np.clip(spl(xs), 0, 1)
    ax.plot(xs, ys, color=INK, lw=1.4, ls="--", zorder=4)
    ax.axhline(0.5, color=LGRAY, lw=0.8, ls=":")
    ax.text(6.05, 0.51, "0.50", fontsize=9.5, color=GRAY)
    ax.set_xticks(x); ax.set_xticklabels(STAGES, fontsize=12)
    ax.set_ylim(0, 1.12)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("委托率", fontsize=12.5)
    set_title(ax, "任务流七环节委托率（N=29）", fs=15)
    handles = [mpatches.Patch(color=BLUE, label="高委托环节（检索/整理/生成）"),
               mpatches.Patch(color=PURPLE, label="中委托环节（分析/执行）"),
               mpatches.Patch(color=RED, label="低委托环节（界定/决策）")]
    ax.legend(handles=handles, loc="upper right", fontsize=9.5, frameon=True, edgecolor=INK)
    note(fig, "注：Cochran's Q = 54.23，p < 0.001，七环节委托率差异显著；分布呈“中间高、两端低”形态。"
              "数据来源：问卷 G1_1—G1_7；分析：03-委托边界与假设检验.py。")
    save(fig, "10-任务流七环节委托率.png")


def fig_06_arch(q):
    """11 七环节委托率的分布形态（面积图）"""
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
    ax.set_ylabel("委托率", fontsize=12.5)
    set_title(ax, "任务流七环节委托率的分布形态", fs=15)
    note(fig, "注：中间环节（检索/整理/生成）委托率高于两端环节（需求界定/判断决策）。"
              "数据来源：问卷 G1_1—G1_7（N=29）。")
    save(fig, "11-任务流七环节委托率-面积图.png")


def fig_07_event_flow(log):
    """13 委托—收回事件流"""
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
        fail = g[g["outcome"] == "失败"]
        if not fail.empty:
            ax.scatter(fail["seq"], [y] * len(fail), marker="x", s=70, color=INK,
                       linewidths=1.8, zorder=5)
    ax.set_yticks(range(n)); ax.set_yticklabels([users[n - 1 - i] for i in range(n)], fontsize=11)
    ax.set_xlabel("事件序号（按时间先后）", fontsize=12)
    ax.set_xlim(0, log["seq"].max() + 2)
    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c,
                          markersize=9, label=l) for l, c in OUT_C.items()]
    handles.append(plt.Line2D([0], [0], marker="x", color=INK, markersize=9, lw=1.6,
                              label="失败事件"))
    ax.legend(handles=handles, loc="lower right", fontsize=10, frameon=True,
              edgecolor=INK, ncol=2)
    set_title(ax, "委托—收回事件流（327 条委托事件）", fs=15)
    note(fig, "注：每个点代表一次委托事件，颜色表示结果；× 标记失败事件。"
              "数据来源：日志编码表；双编码 Cohen's κ=0.879—0.971。")
    save(fig, "13-委托收回事件流.png")


def fig_08_outcome_donut(log):
    """14 委托事件结果构成"""
    cnt = log["outcome"].value_counts().reindex(OUTCOMES).fillna(0).astype(int)
    fig = new_fig(9, 6.0)
    ax = fig.add_axes([0.06, 0.14, 0.58, 0.78]); style(ax, grid=False); ax.set_aspect("equal")
    wedges, _ = ax.pie(cnt.values, startangle=90, counterclock=False,
                       colors=[OUT_C[o] for o in OUTCOMES],
                       wedgeprops=dict(width=0.34, edgecolor=INK, linewidth=1.2))
    total = cnt.sum()
    ax.text(0, 0.10, f"{total}", ha="center", va="center", fontsize=28, fontweight="bold")
    ax.text(0, -0.16, "委托事件总数", ha="center", va="center", fontsize=11.5)
    for w, v in zip(wedges, cnt.values):
        ang = np.deg2rad((w.theta1 + w.theta2) / 2)
        r = 0.84
        ax.text(r * np.cos(ang), r * np.sin(ang), f"{v / total * 100:.1f}%",
                ha="center", va="center", fontsize=12, color=INK)
    ax = fig.add_axes([0.66, 0.14, 0.30, 0.78]); ax.set_axis_off()
    for i, (o, c) in enumerate(OUT_C.items()):
        ax.add_patch(Rectangle((0.03, 0.80 - i * 0.2), 0.09, 0.09,
                               facecolor=c, edgecolor=INK, linewidth=0.8))
        ax.text(0.17, 0.845 - i * 0.2, f"{o}：{cnt[o]} 次", fontsize=12.5, va="center")
    ax.text(0.0, 0.0, "成功事件占绝对主体；\n失败事件低频但影响大",
            fontsize=11.5, color=GRAY, va="bottom")
    set_title(ax, "委托事件的结果构成", fs=16, pad=4)
    note(fig, "数据来源：日志编码表（327 条委托事件）。")
    save(fig, "14-委托事件结果构成.png")


def fig_09_stage_outcome_heat(log):
    """15 环节 × 结果 热力图"""
    ct = pd.crosstab(log["stage"], log["outcome"]).reindex(index=STAGES, columns=OUTCOMES).fillna(0)
    pct = ct.div(ct.sum(axis=1), axis=0) * 100
    fig = new_fig(10.5, 6.2)
    ax = fig.add_axes([0.15, 0.16, 0.66, 0.72])
    im = ax.imshow(pct.values, cmap="RdBu_r", aspect="auto", vmin=0, vmax=100, zorder=1)
    ax.set_xticks(range(4)); ax.set_xticklabels(OUTCOMES, fontsize=12)
    ax.set_yticks(range(7)); ax.set_yticklabels(STAGES, fontsize=12)
    for i in range(7):
        for j in range(4):
            v = pct.values[i, j]
            ax.text(j, i, f"{v:.0f}%", ha="center", va="center", fontsize=11,
                    color="white" if (v > 70 or v < 25) else INK)
    ax.set_xlabel("委托结果", fontsize=12)
    ax.set_ylabel("任务流环节", fontsize=12)
    cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.03)
    cb.ax.tick_params(labelsize=10)
    cb.set_label("环节内占比（%）", fontsize=10)
    set_title(ax, "任务流环节 × 委托结果构成", fs=15)
    note(fig, "注：单元格为各环节内该结果的占比。数据来源：日志编码表（327 条委托事件）。")
    save(fig, "15-环节与结果热力图.png")


def fig_10_fail_reason(log):
    """16 委托失败/撤回原因分布"""
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
    ax.set_xlabel("事件数", fontsize=12)
    set_title(ax, "委托失败/撤回的原因分布", fs=15)
    note(fig, "注：仅统计结果非“成功”且填写了原因的事件。数据来源：日志编码表（fail_reason，κ=0.933）。")
    save(fig, "16-失败原因分布.png")


def fig_11_error_exposure(log):
    """17 错误暴露方式与结果"""
    sub = log[(log["error_exposure"].notna()) & (log["error_exposure"] != "") & (log["outcome"] != "成功")]
    order = ["当场发现并纠正", "事后发现"]
    ct = pd.crosstab(sub["error_exposure"], sub["outcome"]).reindex(index=order, columns=OUTCOMES[1:]).fillna(0)
    fig = new_fig(10, 5.6)
    ax = fig.add_axes([0.22, 0.16, 0.70, 0.72])
    style(ax, grid="x")
    y = np.arange(len(order))[::-1]
    left = np.zeros(len(order))
    for j, oc in enumerate(OUTCOMES[1:]):
        vals = ct[oc].values
        barh(ax, y, vals, OUT_C[oc], height=0.55, left=left)
        for yi, v in zip(y, vals):
            if v > 0:
                ax.text(left[yi] + v / 2, yi, f"{v}", ha="center", va="center",
                        fontsize=11, color=INK, fontweight="bold")
        left += vals
    ax.set_yticks(y); ax.set_yticklabels(order, fontsize=12)
    ax.set_xlim(0, ct.sum(axis=1).max() * 1.3)
    ax.set_xlabel("事件数（非成功事件）", fontsize=12)
    handles = [mpatches.Patch(color=OUT_C[o], label=o) for o in OUTCOMES[1:]]
    ax.legend(handles=handles, loc="lower right", fontsize=10.5, frameon=True, edgecolor=INK)
    set_title(ax, "错误暴露方式与委托结果", fs=15)
    note(fig, "注：可当场发现并纠正的失败不触发算法厌恶；事后发现的失败更易导致收回。"
              "数据来源：日志编码表（error_exposure，κ=0.879）。")
    save(fig, "17-错误暴露方式与结果.png")


def fig_12_iterations(log):
    """18 单次委托迭代轮数分布"""
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
    ax.set_xlabel("迭代轮数", fontsize=12)
    ax.set_ylabel("事件数", fontsize=12)
    ax.set_ylim(0, n.max() * 1.3)
    ax.text(it.mean() + 0.1, n.max() * 1.15, f"均值 {it.mean():.2f}", fontsize=12, color=RED)
    set_title(ax, "单次委托的迭代轮数分布", fs=15)
    note(fig, "数据来源：日志编码表（327 条委托事件）。")
    save(fig, "18-迭代次数分布.png")


def fig_13_withdraw_reasons(q):
    """19 收回委托的原因分布（问卷 H1）"""
    labs = ["能力不足", "输出不可靠", "不省时间", "隐私顾虑", "情感需求"]
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
    ax.set_xlabel("选择比例（多选）", fontsize=12)
    set_title(ax, "收回委托的原因分布（N=29）", fs=15)
    note(fig, "注：七点问卷二值题“是否因该原因收回过委托”，统计选择比例。"
              "数据来源：问卷 H1_1—H1_5；分析：01-问卷分析.py。")
    save(fig, "19-收回原因分布.png")


def fig_14_h3a(log):
    """22 首次失败前后 14 天委托频率（H3a）"""
    lg = log.dropna(subset=["event_date"]).sort_values(["user_id", "seq"])
    WIN = pd.Timedelta(days=14)
    before, after = [], []
    for uid, g in lg.groupby("user_id"):
        for st, sub in g.groupby("stage"):
            fail = sub.loc[sub["outcome"].isin(["失败", "部分成功"]), "event_date"]
            if fail.empty:
                continue
            fd = fail.min()
            nb = int(((sub["event_date"] >= fd - WIN) & (sub["event_date"] < fd)).sum())
            na = int(((sub["event_date"] > fd) & (sub["event_date"] <= fd + WIN)).sum())
            if nb < 1:
                continue
            before.append(nb / 14)
            after.append(na / 14)
    mb, ma = np.mean(before), np.mean(after)
    w, p = stats.wilcoxon(before, after)
    fig = new_fig(9, 5.8)
    ax = fig.add_axes([0.12, 0.18, 0.76, 0.70])
    style(ax)
    bval(ax, [0, 1], [mb, ma], [BLUE, RED], width=0.4)
    ax.text(0, mb + 0.006, f"{mb:.3f}", ha="center", fontsize=13, color=INK, fontweight="bold")
    ax.text(1, ma + 0.006, f"{ma:.3f}", ha="center", fontsize=13, color=INK, fontweight="bold")
    ax.text(0, mb - 0.018, "次/天", ha="center", fontsize=11, color="white", fontweight="bold")
    ax.text(1, ma - 0.018, "次/天", ha="center", fontsize=11, color="white", fontweight="bold")
    arr(ax, (0.28, mb + 0.02), (0.72, ma + 0.02), lw=1.6, ms=13)
    ax.text(0.5, max(mb, ma) + 0.024, f"W = {int(w)}，p < 0.001", ha="center",
            fontsize=12.5, color=INK, fontweight="bold")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["首次失败前 14 天", "首次失败后 14 天"], fontsize=12.5)
    ax.set_ylim(0, max(mb, ma) + 0.075)
    ax.set_ylabel("该环节委托频率（次/天）", fontsize=12)
    set_title(ax, "首次失败前后 14 天该环节委托频率（H3a）", fs=15)
    note(fig, "注：以首次失败日为界，比较前后各 14 天内该环节的委托频率（配对 Wilcoxon 符号秩检验）。"
              "数据来源：日志编码表；分析：03-委托边界与假设检验.py。")
    save(fig, "22-首次失败前后委托频率.png")


def fig_15_memory(q, mem):
    """23 记忆积累与持续使用意向（H3b）"""
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
            label=f"线性拟合（r = {lr.rvalue:.3f}）")
    ax.scatter(x, y, s=55, color=BLUE, edgecolors=INK, linewidths=0.8, zorder=4,
               label="样本（N=13）")
    for xi, yi, lk in zip(x, y, m["link_id"]):
        ax.text(xi + 4, yi + 0.1, f"#{lk}", fontsize=9, color=GRAY)
    ax.set_xlabel("时间轴日志行数（记忆积累量）", fontsize=12)
    ax.set_ylabel("持续使用意向（F1—F3 均值）", fontsize=12)
    ax.set_ylim(1, 7.4)
    ax.legend(loc="upper left", fontsize=10.5, frameon=True, edgecolor=INK)
    set_title(ax, "记忆积累与持续使用意向的关系（H3b）", fs=15)
    note(fig, "注：Spearman ρ = 0.850，p < 0.001（时间轴行数）；ρ = 0.781，p = 0.002（更新频次）。"
              "数据来源：记忆指标表 × 问卷 F 量表（link_id 匿名关联）。")
    save(fig, "23-记忆积累与持续使用意向.png")


def fig_16_alpha():
    """24 问卷量表信度（Cronbach's α）"""
    items = ["感知有用性", "感知易用性", "感知信任", "感知风险", "持续使用意向", "记忆感知"]
    alphas = [0.871, 0.778, 0.815, 0.403, 0.879, 0.814]
    fig = new_fig(10, 5.6)
    ax = fig.add_axes([0.10, 0.16, 0.80, 0.72])
    style(ax)
    x = np.arange(len(items))
    cols = [GREEN if a >= 0.70 else RED for a in alphas]
    bval(ax, x, alphas, cols, width=0.5)
    for xi, a, c in zip(x, alphas, cols):
        ax.text(xi, a + 0.03, f"{a:.3f}", ha="center", fontsize=12, color=INK)
    ax.axhline(0.70, color=INK, lw=1.2, ls="--")
    ax.text(5.4, 0.715, "0.70（常用阈值）", fontsize=10, color=INK, ha="right")
    ax.text(3, 0.403 + 0.14, "感知风险 α=0.403（量表内涵较宽）", ha="center",
            fontsize=10.5, color=RED)
    ax.set_xticks(x); ax.set_xticklabels(items, fontsize=11.5)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Cronbach's α", fontsize=12)
    set_title(ax, "问卷六量表信度（N=29）", fs=15)
    note(fig, "注：除感知风险（α=0.403，量表内涵较宽）外，各量表 α 均高于 0.70。"
              "数据来源：问卷 B/C/D/E/F/I；分析：01-问卷分析.py。")
    save(fig, "24-问卷量表信度.png")


def fig_17_radar(q):
    """25 感知构念均值雷达图"""
    labs = ["感知有用性", "感知易用性", "感知信任", "感知风险", "持续使用意向", "记忆感知"]
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
        sp.set_color("#111111"); sp.set_linewidth(0.9)
    ax.plot(ang, v, lw=2.0, color=BLUE, zorder=3)
    ax.fill(ang, v, color=to_rgba_light(BLUE, 0.25), zorder=2)
    ax.scatter(ang[:-1], vals, s=40, color=BLUE, edgecolors=INK, linewidths=0.8, zorder=4)
    for a, vv in zip(ang[:-1], vals):
        ax.text(a, vv + 0.5, f"{vv:.2f}", ha="center", va="center", fontsize=11, color=INK)
    ax.set_title("六构念感知均值（七点量表，N=29）", fontsize=15, pad=24, fontweight="bold")
    note(fig, "注：数值为各量表题目得分的均值。数据来源：问卷 B/C/D/E/F/I；分析：01-问卷分析.py。")
    save(fig, "25-感知构念雷达图.png")


def to_rgba_light(hexc, alpha):
    from matplotlib.colors import to_rgba
    r, g, b = to_rgba(hexc)[:3]
    return (r, g, b, alpha)


def fig_18_usage_groups(q):
    """09 工作坊成员当前使用状态"""
    cnt = q["A1"].value_counts().sort_index()
    labels = {1: "每天都在用", 2: "每周几次", 3: "偶尔使用", 4: "已停止使用"}
    vals = [int(cnt.get(k, 0)) for k in [1, 2, 3, 4]]
    colors = [GREEN, BLUE, GOLD, RED]
    fig = new_fig(9, 6.0)
    ax = fig.add_axes([0.06, 0.14, 0.56, 0.78]); style(ax, grid=False); ax.set_aspect("equal")
    wedges, _ = ax.pie(vals, startangle=90, counterclock=False, colors=colors,
                       wedgeprops=dict(width=0.36, edgecolor=INK, linewidth=1.2))
    ax.text(0, 0.10, f"{sum(vals)}", ha="center", va="center", fontsize=26, fontweight="bold")
    ax.text(0, -0.18, "有效样本", ha="center", va="center", fontsize=11.5)
    for w, v in zip(wedges, vals):
        ang = np.deg2rad((w.theta1 + w.theta2) / 2)
        r = 0.82
        ax.text(r * np.cos(ang), r * np.sin(ang), f"{v / sum(vals) * 100:.0f}%",
                ha="center", va="center", fontsize=12, color=INK)
    axr = fig.add_axes([0.64, 0.14, 0.32, 0.78]); axr.set_axis_off()
    for i, (k, c) in enumerate(zip([1, 2, 3, 4], colors)):
        axr.add_patch(Rectangle((0.04, 0.82 - i * 0.2), 0.08, 0.08,
                                facecolor=c, edgecolor=INK, linewidth=0.8))
        axr.text(0.17, 0.86 - i * 0.2, f"{labels[k]}：{vals[i]} 人", fontsize=12.5, va="center")
    axr.text(0.08, 0.02, "约 38% 已停止使用", fontsize=10, color=GRAY, va="bottom")
    set_title(ax, "工作坊成员当前使用状态（A1）", fs=16, pad=4)
    note(fig, "数据来源：问卷 A1（N=29，剔除测谎项未通过者）。")
    save(fig, "09-使用状态分布.png")


def fig_19_weekly(log):
    """20 委托事件按周的环节构成"""
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
    ax.set_xlabel("统计周（2026 年）", fontsize=12)
    ax.set_ylabel("委托事件数", fontsize=12)
    handles = [mpatches.Patch(color=STAGE_LEVEL_C[st], label=st, alpha=0.6) for st in STAGES]
    ax.legend(handles=handles, loc="upper left", fontsize=9, frameon=True, edgecolor=INK, ncol=4)
    set_title(ax, "委托事件按周的环节构成与使用热度", fs=15)
    note(fig, "注：工作坊后首月使用最活跃，随后回落至稳定水平。数据来源：日志编码表（327 条委托事件）。")
    save(fig, "20-委托事件周度时间序列.png")


def fig_20_user_events(log):
    """21 各用户委托事件规模与结果构成"""
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
    ax.set_xlabel("委托事件数", fontsize=12)
    handles = [mpatches.Patch(color=OUT_C[o], label=o) for o in OUTCOMES]
    ax.legend(handles=handles, loc="lower right", fontsize=10.5, frameon=True, edgecolor=INK)
    set_title(ax, "各用户的委托事件规模与结果构成", fs=15)
    note(fig, "数据来源：日志编码表（按 user_id 汇总）。")
    save(fig, "21-各用户委托事件构成.png")


# ==================================================================
# 研究3 · 单 vs 多智能体对比实验（RQ3 / H4）
# ==================================================================
def _exp_stats(exp):
    tasks = ["A", "B", "C"]
    metrics = [("total_time_min", "总时长(min)"), ("intervention_count", "介入次数"),
               ("intervention_time_min", "介入时长(min)"), ("quality_score", "产出质量")]
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
    ax.set_xticks(x); ax.set_xticklabels(["任务 A\n检索整理型", "任务 B\n分析型", "任务 C\n写作综合型"],
                                         fontsize=11.5)
    ax.set_ylim(0, ymax)
    ax.set_ylabel(ylab, fontsize=12)
    handles = [mpatches.Patch(facecolor=LIGHTG, edgecolor=INK, hatch="//", label="单智能体"),
               mpatches.Patch(facecolor=BLUE, edgecolor=INK, label="多智能体")]
    ax.legend(handles=handles, loc="upper right", fontsize=10.5, frameon=True, edgecolor=INK)
    set_title(ax, title, fs=15)
    note(fig, note_text)
    save(fig, fname)


def fig_21_time(exp):
    _grouped(exp, "total_time_min", "总时长（min）", "26-总时长对比.png",
             "三类任务的总时长：单智能体 vs 多智能体",
             42, 0.9, 1.9,
             "注：n=4，配对 Wilcoxon 符号秩检验（任务 A/B：p=0.125，未达 p<0.05，方向一致、效应量 r≈0.91）；"
             "任务 C：p=0.875。数据来源：实验数据记录表；分析：04-对比实验分析.py。")


def fig_22_count(exp):
    _grouped(exp, "intervention_count", "人工介入次数", "27-人工介入次数对比.png",
             "人工介入次数：单智能体 vs 多智能体",
             20, 0.6, 1.4,
             "注：n=4，配对 Wilcoxon 符号秩检验（任务 A：p=0.125；任务 B：p=0.25；任务 C：p=0.625）。"
             "数据来源：实验数据记录表；分析：04-对比实验分析.py。")


def fig_23_intervention(exp):
    _grouped(exp, "intervention_time_min", "人工介入时长（min）", "28-人工介入时长对比.png",
             "人工介入时长：单智能体 vs 多智能体",
             23, 0.6, 1.4,
             "注：n=4，配对 Wilcoxon 符号秩检验（任务 A/B：p=0.125；任务 C：p=0.50）。"
             "数据来源：实验数据记录表；分析：04-对比实验分析.py。")


def fig_24_quality(exp):
    _grouped(exp, "quality_score", "产出质量（盲评，5 分制）", "29-产出质量对比.png",
             "产出质量（双人盲评）：单智能体 vs 多智能体",
             5.8, 0.12, 0.26,
             "注：产出质量为两位盲评者对相关性/准确性/结构/完整性的平均分；n=4，配对 Wilcoxon 符号秩检验"
             "（任务 B：p=0.125，多智能体更高）。数据来源：实验数据记录表；分析：04-对比实验分析.py。")


def fig_25_gain(exp):
    """30 多智能体相对增益（%）"""
    rows = _exp_stats(exp)
    metrics = [("total_time_min", "总时长"), ("intervention_count", "介入次数"),
               ("intervention_time_min", "介入时长")]
    tasks = ["A", "B", "C"]
    M = np.zeros((3, 3))
    for i, (col, _) in enumerate(metrics):
        for j, t in enumerate(tasks):
            r = [x for x in rows if x["col"] == col and x["task"] == t][0]
            M[i, j] = (r["sm"] - r["mm"]) / r["sm"] * 100 if r["sm"] else 0
    fig = new_fig(9.5, 5.6)
    ax = fig.add_axes([0.13, 0.17, 0.66, 0.72])
    im = ax.imshow(M, cmap="RdBu_r", aspect="auto", vmin=-20, vmax=60, zorder=1)
    ax.set_xticks(range(3)); ax.set_xticklabels([f"任务 {t}" for t in tasks], fontsize=12)
    ax.set_yticks(range(3)); ax.set_yticklabels([m[1] for m in metrics], fontsize=12)
    for i in range(3):
        for j in range(3):
            v = M[i, j]
            ax.text(j, i, f"{v:+.0f}%", ha="center", va="center", fontsize=12.5,
                    color="white" if abs(v) > 25 else INK, fontweight="bold")
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.04)
    cb.ax.tick_params(labelsize=10)
    cb.set_label("相对增益（%，正=更省时/更少介入）", fontsize=10)
    set_title(ax, "多智能体相对单智能体的增益（%）", fs=15)
    note(fig, "注：增益 =（单−多）/单 × 100%。任务 A/B（可分解、多环节、需核查）增益明显，"
              "任务 C（单环节、强主观）增益消失。数据来源：实验数据记录表。")
    save(fig, "30-多智能体相对增益.png")


def fig_26_slope(exp):
    """31 配对个体轨迹：总时长单→多"""
    tasks = ["A", "B", "C"]
    fig = new_fig(12, 4.8)
    for k, t in enumerate(tasks):
        ax = fig.add_subplot(1, 3, k + 1)
        style(ax, grid=False)
        sub = exp[exp["task"] == t]
        s = sub[sub["condition"] == "single"].set_index("participant")["total_time_min"]
        m = sub[sub["condition"] == "multi"].set_index("participant")["total_time_min"]
        parts = [p for p in s.index if p in m.index]
        for p in parts:
            sv, mv = s[p], m[p]
            c = GREEN if mv < sv else RED
            ax.plot([0, 1], [sv, mv], color=c, lw=1.6, zorder=3)
            ax.scatter([0, 1], [sv, mv], s=42, color=c, edgecolors=INK, linewidths=0.7, zorder=4)
            ax.text(0 - 0.03, sv, f"{sv:.0f}", ha="right", va="center", fontsize=10.5)
            ax.text(1 + 0.03, mv, f"{mv:.0f}", ha="left", va="center", fontsize=10.5)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["单智能体", "多智能体"], fontsize=11.5)
        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(0, 40)
        ax.set_title(f"任务 {t}", fontsize=13, fontweight="bold")
    fig.suptitle("配对个体轨迹：每位被试的总时长（单 → 多智能体）", fontsize=15, y=0.98, fontweight="bold")
    note(fig, "注：绿线=多智能体更快，红线=多智能体更慢；每位被试一条连线。数据来源：实验数据记录表（n=4）。")
    save(fig, "31-配对个体轨迹.png")


def fig_27_effect(exp):
    """32 效应量与显著性（气泡图）"""
    rows = _exp_stats(exp)
    fig = new_fig(10.5, 6.0)
    ax = fig.add_axes([0.11, 0.16, 0.60, 0.72])
    style(ax)
    colors = {"总时长(min)": BLUE, "介入次数": PURPLE, "介入时长(min)": ORANGE, "产出质量": GREEN}
    markers = {"A": "o", "B": "s", "C": "^"}
    for r in rows:
        if not np.isfinite(r["p"]) or not np.isfinite(r["r"]):
            continue
        ax.scatter(r["p"], r["r"], s=60 + r["r"] * 420, color=colors[r["metric"]],
                   marker=markers[r["task"]], alpha=0.85, edgecolors=INK, linewidths=0.8, zorder=3)
    ax.axvspan(0, 0.05, color=LIGHTB, zorder=0)
    ax.text(0.025, 1.20, "p < 0.05", ha="center", fontsize=10.5, color=GRAY)
    ax.axhline(0.5, color=LGRAY, lw=0.8, ls=":")
    ax.text(0.98, 0.52, "r = 0.50", fontsize=10, color=GRAY, ha="right")
    ax.set_xlim(0, 1.02); ax.set_ylim(0, 1.30)
    ax.set_xlabel("p 值", fontsize=12)
    ax.set_ylabel("效应量 r（Wilcoxon 近似）", fontsize=12)
    h1 = [plt.Line2D([0], [0], marker=m, color="w", markerfacecolor="#9AA5B1",
                     markersize=8, label=f"任务 {t}") for t, m in markers.items()]
    h2 = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c,
                     markersize=8, label=l) for l, c in colors.items()]
    ax.legend(handles=h1 + h2, loc="center left", bbox_to_anchor=(1.03, 0.5),
              fontsize=10, frameon=True, edgecolor=INK, title="标记：任务 ｜ 颜色：指标",
              title_fontsize=9.5)
    set_title(ax, "对比实验各指标的效应量与显著性", fs=15)
    note(fig, "注：任务 A/B 时间与介入类指标 r≈0.91、p>0.05（小样本 n=4），结论为方向性支持。"
              "数据来源：04-对比实验分析.csv。")
    save(fig, "32-效应量与显著性.png")


# ==================================================================
# 框架与概念图（白底方框 + 黑色细边框）
# ==================================================================
def fig_28_dda():
    """04 DDA 三阶段模型"""
    fig = new_fig(16, 9.5)
    ax = fig.add_axes([0.02, 0.03, 0.96, 0.92]); ax.set_axis_off()
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.text(50, 97.5, "DDA 三阶段模型：部署 → 委托 → 沉淀", ha="center",
            fontsize=32, fontweight="bold")
    ax.text(50, 92.5, "把“系统级技术采纳”推进为“任务级委托决策”", ha="center",
            fontsize=22, color=GRAY)
    box(ax, (22, 62), 27, 30, "部署\nDeploy", fc=LIGHTB, fs=30, weight="bold",
        sub="SBDP\n自举式部署协议", sub_fs=20)
    box(ax, (50, 62), 27, 30, "委托\nDelegate", fc="white", fs=30, weight="bold",
        sub="任务级\n“自制—外购”决策", sub_fs=20)
    box(ax, (78, 62), 27, 30, "沉淀\nAccumulate", fc=LIGHTG, fs=30, weight="bold",
        sub="记忆＝\n关系专用性投资", sub_fs=20)
    arr(ax, (37, 62), (43, 62), lw=3.2, ms=26)
    arr(ax, (63, 62), (69, 62), lw=3.2, ms=26)
    # 反馈回路（曲线绕开，避免与主流程交叉）
    ax.add_patch(FancyArrowPatch((78, 77), (58, 77), arrowstyle="-|>", mutation_scale=26,
                                 linewidth=3.0, color=INK, connectionstyle="arc3,rad=0.25",
                                 shrinkA=1, shrinkB=1, zorder=2))
    ax.text(65, 83.5, "信任扩大委托边界、\n持续使用", fontsize=20, color=INK,
            ha="center", va="center", linespacing=1.6)
    # 虚线：降低转换成本（标签放在虚线正下方）
    ax.add_patch(FancyArrowPatch((22, 42), (78, 42), arrowstyle="-|>", mutation_scale=18,
                                 linewidth=2.6, color=GRAY, linestyle=(0, (4, 2)),
                                 shrinkA=1, shrinkB=1, zorder=2))
    ax.text(50, 36.5, "降低转换成本", ha="center", va="center", fontsize=20, color=GRAY)
    props = [("P1 部署触发委托", "部署成本是委托\n行为的首要门槛", BLUE),
             ("P2 委托边界的形成", "能力感知×信任×交互成本\n三元判断；失败经算法厌恶\n压低委托率", PURPLE),
             ("P3 沉淀累积信任", "记忆形成路径依赖，投入\n越深越难离开、越愿托付", GREEN),
             ("P4 架构的边界", "可分解多环节任务多智能体\n占优；单环节强主观\n任务无优势", ORANGE)]
    for i, (t, d, c) in enumerate(props):
        x = 13 + i * 25
        box(ax, (x, 14), 24, 26, t, fc="white", ec=c, fs=26, weight="bold", sub=d, sub_fs=18)
    note(fig, "注：依据研究报告 2.6 绘制；四个命题分别对应假设 H1—H4。", x=0.03, fs=14)
    save(fig, "04-DDA三阶段模型.png")


def fig_29_architecture():
    """02 统筹—执行—核查三智能体架构"""
    fig = new_fig(12.5, 7.8)
    ax = fig.add_axes([0.02, 0.03, 0.96, 0.92]); ax.set_axis_off()
    ax.set_xlim(0, 102); ax.set_ylim(0, 100)
    ax.text(50, 97.5, "“统筹—执行—核查”三智能体协作架构", ha="center",
            fontsize=17, fontweight="bold")
    ax.text(50, 93, "orchestrator-workers × evaluator-optimizer：显式验收回路＋个人记忆层",
            ha="center", fontsize=11, color=GRAY)
    box(ax, (12, 80), 16, 14, "用户", fc="white", fs=14, sub="需求·核查·终检", sub_fs=10.5)
    box(ax, (50, 80), 26, 17, "统筹者\nOrchestrator", fc=LIGHTB, fs=14.5, weight="bold",
        sub="任务分解·结果综合·验收回灌", sub_fs=10)
    box(ax, (27, 44), 23, 17, "执行者\nWorker", fc="white", fs=14, sub="单一职责·工具调用", sub_fs=10)
    box(ax, (73, 44), 23, 17, "核查者\nChecker", fc=LIGHTG, fs=14, sub="产出比对·验收", sub_fs=10)
    box(ax, (50, 10), 44, 12, "记忆系统 Memory", fc="white", fs=13,
        sub="热记忆 / 冷记忆 / 时间轴日志（可读·可审计）", sub_fs=10)
    # 用户 ⇄ 统筹
    arr(ax, (20, 84), (37, 84), lw=2.0, ms=15)
    ax.text(28.5, 87.5, "委托需求", fontsize=11, color=INK)
    arr(ax, (37, 76), (20, 76), lw=2.0, ms=15)
    ax.text(28.5, 72.5, "产出交付", fontsize=11, color=INK)
    # ① 统筹 → 执行
    arr(ax, (44, 71.5), (28, 52.5), lw=2.0, ms=15)
    ax.text(33, 65, "① 任务分解", fontsize=11, color=INK)
    # ② 统筹 → 核查
    arr(ax, (56, 71.5), (72, 52.5), lw=2.0, ms=15)
    ax.text(67, 65, "② 分配子任务", fontsize=11, color=INK)
    # ③ 执行 → 核查
    arr(ax, (38.5, 44), (61.5, 44), lw=2.0, ms=15)
    ax.text(50, 47.5, "③ 产出送检", fontsize=11, color=INK)
    # ④ 验收回灌（右侧绕行，避免交叉）
    ax.plot([84.5, 94, 94, 63.5], [44, 44, 80, 80], color=INK, lw=1.6, zorder=2)
    ax.add_patch(FancyArrowPatch((94, 80), (63.5, 80), arrowstyle="-|>", mutation_scale=14,
                                 linewidth=1.6, color=INK, shrinkA=0, shrinkB=1, zorder=3))
    ax.text(91.5, 62, "④ 验收回灌", fontsize=11, color=INK, rotation=90, ha="center", va="center")
    # ⑤ 记忆沉淀（左侧绕行，避免与 ③ 交叉）
    ax.plot([40, 6, 6, 28], [71.5, 71.5, 10, 10], color=INK, lw=1.6, zorder=2)
    ax.add_patch(FancyArrowPatch((6, 10), (28, 10), arrowstyle="-|>", mutation_scale=14,
                                 linewidth=1.6, color=INK, shrinkA=0, shrinkB=1, zorder=3))
    ax.text(3.5, 40, "⑤ 记忆沉淀", fontsize=11, color=INK, rotation=90, ha="center", va="center")
    note(fig, "注：依据研究报告 1.1 与 2.1 绘制；①—⑤为一次委托的协作顺序。", x=0.03)
    save(fig, "02-统筹执行核查架构.png")


def fig_30_triangulation():
    """05 研究设计的三角测量"""
    fig = new_fig(11.5, 7.0)
    ax = fig.add_axes([0.02, 0.04, 0.96, 0.90]); ax.set_axis_off()
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.text(50, 97, "研究设计：三角测量（三个子研究收敛）", ha="center",
            fontsize=17, fontweight="bold")
    ax.text(50, 92.5, "共同理论框架（DDA 模型）与共同人工制品（框架与向导）", ha="center",
            fontsize=11.5, color=GRAY)
    box(ax, (22, 64), 27, 20, "研究1\n制品可用性", fc=LIGHTB, fs=14.5, weight="bold",
        sub="部署可用性测试 · H1", sub_fs=10.5)
    box(ax, (50, 26), 27, 20, "研究2\n委托行为与持续使用", fc="white", fs=14.5, weight="bold",
        sub="问卷＋访谈＋日志 · H2、H3", sub_fs=10.5)
    box(ax, (78, 64), 27, 20, "研究3\n单 vs 多智能体", fc=LIGHTG, fs=14.5, weight="bold",
        sub="受控对比实验 · H4", sub_fs=10.5)
    box(ax, (50, 82), 27, 12, "三角测量综合", fc=LIGHTO, fs=14.5, weight="bold",
        sub="收敛回答 RQ1—RQ3", sub_fs=10.5)
    arr(ax, (30, 54), (44, 36), lw=1.8, ms=15)   # 研究1 → 研究2
    arr(ax, (70, 54), (56, 36), lw=1.8, ms=15)   # 研究3 → 研究2
    arr(ax, (30, 74), (44, 76), lw=1.8, ms=15)   # 研究1 → 综合
    arr(ax, (70, 74), (56, 76), lw=1.8, ms=15)   # 研究3 → 综合
    arr(ax, (50, 36), (50, 76), lw=1.8, ms=15)   # 研究2 → 综合
    note(fig, "注：依据研究报告 3.1 绘制；三个子研究从不同证据源收敛到对研究问题的回答。", x=0.03)
    save(fig, "05-研究设计三角测量.png")


def fig_31_theory():
    """03 理论整合框架"""
    fig = new_fig(12.5, 7.0)
    ax = fig.add_axes([0.02, 0.04, 0.96, 0.90]); ax.set_axis_off()
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.text(50, 97, "理论整合：任务级委托决策的机制解释", ha="center",
            fontsize=16, fontweight="bold")
    box(ax, (50, 78), 30, 15, "DDA 三阶段模型", fc=LIGHTB, fs=16, weight="bold",
        sub="部署—委托—沉淀（P1—P4）", sub_fs=11)
    theories = [("任务—技术匹配 TTF", "哪些任务值得委托", 14, LIGHTB),
                ("交易成本理论", "委托还是自制（机制）", 39, LIGHTG),
                ("期望确认模型 ECT", "持续使用（时间维度）", 64, "white"),
                ("算法厌恶", "委托中的行为偏差", 89, LIGHTO)]
    for t, d, x, fc in theories:
        box(ax, (x, 38), 20, 14, t, fc=fc, fs=13.5, weight="bold", sub=d, sub_fs=10.5)
    arr(ax, (20, 46), (44, 70), lw=1.8, ms=15)
    arr(ax, (42, 46), (48, 70), lw=1.8, ms=15)
    arr(ax, (62, 46), (54, 70), lw=1.8, ms=15)
    arr(ax, (84, 46), (58, 70), lw=1.8, ms=15)
    box(ax, (50, 16), 56, 10, "四类理论整合为 DDA 模型，对应四个可证伪命题 P1—P4",
        fc="white", fs=12.5)
    note(fig, "注：依据研究报告 2.4—2.6 绘制。", x=0.03)
    save(fig, "03-理论整合框架.png")


def fig_32_attributes():
    """12 委托边界的三属性框架"""
    fig = new_fig(11.5, 7.0)
    ax = fig.add_axes([0.02, 0.04, 0.96, 0.90]); ax.set_axis_off()
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.text(50, 97.5, "委托边界的位置由三类任务结构属性共同决定", ha="center",
            fontsize=17, fontweight="bold")
    box(ax, (50, 52), 24, 14, "委托边界", fc=LIGHTO, fs=16, weight="bold",
        sub="任务级“自制—外购”决策", sub_fs=11)
    box(ax, (20, 80), 22, 14, "输出可验证性", fc=LIGHTB, fs=13.5, weight="bold",
        sub="结果可快速核对", sub_fs=10.5)
    box(ax, (80, 80), 22, 14, "后果可逆性", fc=LIGHTB, fs=13.5, weight="bold",
        sub="错误可重来", sub_fs=10.5)
    box(ax, (50, 16), 22, 14, "价值编码程度", fc=LIGHTB, fs=13.5, weight="bold",
        sub="承载目标与价值判断的多少", sub_fs=10.5)
    arr(ax, (30, 74), (44, 60), lw=1.8, ms=15)
    arr(ax, (70, 74), (56, 60), lw=1.8, ms=15)
    arr(ax, (50, 24), (50, 44), lw=1.8, ms=15)
    box(ax, (50, 90), 66, 6, "可验证性↑、可逆性↑、价值编码↓ → 委托率↑（中间环节）",
        fc="white", fs=12.5)
    note(fig, "注：依据研究报告 4.2.1 与 5.2 绘制；任务结构属性相对稳定，故委托边界短期稳定。", x=0.03)
    save(fig, "12-委托边界三属性框架.png")


def fig_33_summary_table():
    """33 核心结果汇总（表格）"""
    rows = [
        ["研究1 部署", "完成率", "80%（4/5）", "H1 阈值 ≥ 80%，达成"],
        ["研究1 部署", "平均部署耗时", "29.5 min（26—34）", "完成者口径"],
        ["研究1 部署", "SUS 均值", "72.25（68—76）", "均 ≥ 68 可用阈值"],
        ["研究2 委托", "七环节委托率差异", "Q = 54.23", "p < 0.001，支持 H2"],
        ["研究2 委托", "首次失败前后 14 天委托频率", "0.135 → 0.060 次/天", "W = 80，p < 0.001，支持 H3a"],
        ["研究2 委托", "时间轴行数 × 持续使用意向", "ρ = 0.850", "p < 0.001，支持 H3b"],
        ["研究2 委托", "更新频次 × 持续使用意向", "ρ = 0.781", "p = 0.002，支持 H3b"],
        ["研究3 对比", "总时长（任务 A）", "29.75 → 16.25 min", "r ≈ 0.91，方向性支持 H4"],
        ["研究3 对比", "人工介入次数（任务 A）", "14.5 → 7.0 次", "r ≈ 0.91，方向性支持 H4"],
        ["研究3 对比", "产出质量（任务 B）", "3.50 → 4.31 分", "多智能体不低，质量不降"],
    ]
    fig = new_fig(11, 6.2)
    ax = fig.add_axes([0.01, 0.06, 0.98, 0.82]); ax.set_axis_off()
    col_w = [0.12, 0.30, 0.24, 0.34]
    headers = ["研究", "指标", "结果", "检验 / 判定"]
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
    ax.set_title("研究核心结果汇总", fontsize=16, loc="left", fontweight="bold", pad=12)
    note(fig, "注：研究3 因每条件 n=4，Wilcoxon 检验未达 p<0.05，报告表述为“方向性支持、效应量 r≈0.91”。")
    save(fig, "33-核心结果汇总表.png")


# ==================================================================
# 主流程
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
    before, after = [], []
    for uid, g in lg.groupby("user_id"):
        for st, sub in g.groupby("stage"):
            fail = sub.loc[sub["outcome"].isin(["失败", "部分成功"]), "event_date"]
            if fail.empty:
                continue
            fd = fail.min()
            nb = int(((sub["event_date"] >= fd - WIN) & (sub["event_date"] < fd)).sum())
            na = int(((sub["event_date"] > fd) & (sub["event_date"] <= fd + WIN)).sum())
            if nb < 1:
                continue
            before.append(nb / 14); after.append(na / 14)
    w, p3 = stats.wilcoxon(before, after)
    print(f"H3a W = {w:.0f}, p = {p3:.3f}, 频率 {np.mean(before):.3f} → {np.mean(after):.3f}")
    q2 = q.copy()
    q2["continuance"] = q2[["F1", "F2", "F3"]].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    m = mem.merge(q2[["link_id", "continuance"]], on="link_id", how="inner").dropna()
    r1, p1 = stats.spearmanr(m["timeline_lines"], m["continuance"])
    r2, p2 = stats.spearmanr(m["mem_updates"], m["continuance"])
    print(f"H3b ρ = {r1:.3f} (p={p1:.3f}); ρ = {r2:.3f} (p={p2:.3f})")
    a = exp[(exp.task == "A") & (exp.condition == "single")].total_time_min.mean()
    b = exp[(exp.task == "A") & (exp.condition == "multi")].total_time_min.mean()
    print(f"实验 任务A 总时长: {a:.2f} vs {b:.2f} min")


def main():
    os.makedirs(OUT, exist_ok=True)
    q, log, exp, mem, sus = load()
    verify(q, log, exp, mem)
    jobs = [
        # —— 第一章 引言 · 1.1 研究背景与问题提出 ——
        ("01-部署成本压缩示意.png", lambda: fig_04_cost_compress(sus)),
        # —— 第二章 文献综述与理论框架 ——
        ("02-统筹执行核查架构.png", fig_29_architecture),
        ("03-理论整合框架.png", fig_31_theory),
        ("04-DDA三阶段模型.png", fig_28_dda),
        # —— 第三章 研究设计与方法 ——
        ("05-研究设计三角测量.png", fig_30_triangulation),
        ("06-SBDP六阶段部署流程.png", fig_03_sbdp_flow),
        # —— 第四章 研究发现 · 4.1 研究1 ——
        ("07-部署可用性测试结果.png", lambda: fig_01_dashboard(sus)),
        ("08-SUS得分与可用性分级.png", lambda: fig_02_sus_grading(sus)),
        # —— 4.2 研究2 ——
        ("09-使用状态分布.png", lambda: fig_18_usage_groups(q)),
        ("10-任务流七环节委托率.png", lambda: fig_05_boundary(q)),
        ("11-任务流七环节委托率-面积图.png", lambda: fig_06_arch(q)),
        ("12-委托边界三属性框架.png", fig_32_attributes),
        ("13-委托收回事件流.png", lambda: fig_07_event_flow(log)),
        ("14-委托事件结果构成.png", lambda: fig_08_outcome_donut(log)),
        ("15-环节与结果热力图.png", lambda: fig_09_stage_outcome_heat(log)),
        ("16-失败原因分布.png", lambda: fig_10_fail_reason(log)),
        ("17-错误暴露方式与结果.png", lambda: fig_11_error_exposure(log)),
        ("18-迭代次数分布.png", lambda: fig_12_iterations(log)),
        ("19-收回原因分布.png", lambda: fig_13_withdraw_reasons(q)),
        ("20-委托事件周度时间序列.png", lambda: fig_19_weekly(log)),
        ("21-各用户委托事件构成.png", lambda: fig_20_user_events(log)),
        ("22-首次失败前后委托频率.png", lambda: fig_14_h3a(log)),
        ("23-记忆积累与持续使用意向.png", lambda: fig_15_memory(q, mem)),
        ("24-问卷量表信度.png", fig_16_alpha),
        ("25-感知构念雷达图.png", lambda: fig_17_radar(q)),
        # —— 4.3 研究3 ——
        ("26-总时长对比.png", lambda: fig_21_time(exp)),
        ("27-人工介入次数对比.png", lambda: fig_22_count(exp)),
        ("28-人工介入时长对比.png", lambda: fig_23_intervention(exp)),
        ("29-产出质量对比.png", lambda: fig_24_quality(exp)),
        ("30-多智能体相对增益.png", lambda: fig_25_gain(exp)),
        ("31-配对个体轨迹.png", lambda: fig_26_slope(exp)),
        ("32-效应量与显著性.png", lambda: fig_27_effect(exp)),
        # —— 第六章 结论与展望 · 6.1 结论 ——
        ("33-核心结果汇总表.png", fig_33_summary_table),
    ]
    print(f"\n开始生成 {len(jobs)} 张图表 → {OUT}")
    for name, fn in jobs:
        try:
            fn()
        except Exception as e:
            import traceback
            print(f"  [FAIL] {name}: {e}")
            traceback.print_exc()
    print("全部完成。")


if __name__ == "__main__":
    main()
