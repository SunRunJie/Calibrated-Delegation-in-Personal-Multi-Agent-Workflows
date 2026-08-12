# -*- coding: utf-8 -*-
"""
05-图表生成.py
生成研究报告所需的图：
  图4-1 任务流七环节委托率（委托边界曲线）
  图4-2 委托—收回事件流（时间线散点）
  图4-3 单vs多智能体对比
输入：02-问卷/问卷-数据模板.csv、05-日志编码/日志编码表.csv、06-对比实验/实验数据记录表.csv
输出：08-数据汇总/图4-1~图4-3（PNG）
用法：python 05-图表生成.py
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "PingFang SC"]
plt.rcParams["axes.unicode_minus"] = False

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "08-数据汇总")
QDATA = os.path.join(BASE, "02-问卷", "问卷-数据模板.csv")
LDATA = os.path.join(BASE, "05-日志编码", "日志编码表.csv")
EDATA = os.path.join(BASE, "06-对比实验", "实验数据记录表.csv")

STAGES = ["需求界定", "信息检索", "信息整理", "分析推理", "内容生成", "执行操作", "判断决策"]
OUTCOME_COLORS = {"成功": "#55A868", "部分成功": "#8172B2", "撤回": "#DD8452", "失败": "#C44E52"}


def fig_4_1(q):
    """委托边界曲线：七环节委托率柱状图"""
    cols = [f"G1_{i}" for i in range(1, 8)]
    if not all(c in q.columns for c in cols):
        return False
    # 与01-问卷分析.py保持一致：剔除测谎项未通过（J2≠2）的作答
    if "J2" in q.columns:
        q = q[pd.to_numeric(q["J2"], errors="coerce") == 2]
    rates = q[cols].apply(pd.to_numeric, errors="coerce").mean()
    if rates.isna().all():
        return False
    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars = ax.bar(STAGES, rates, color="#4C72B0")
    bars[0].set_color("#C44E52")
    bars[-1].set_color("#C44E52")
    ax.set_ylim(0, 1)
    ax.set_ylabel("委托率")
    ax.set_title("图4-1 任务流七环节委托率（委托边界曲线）")
    for i, v in enumerate(rates):
        if v == v:
            ax.text(i, v + 0.02, f"{v:.2f}", ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "图4-1-委托边界曲线.png"), dpi=200)
    plt.close(fig)
    return True


def fig_4_2(log):
    """委托—收回事件流：按用户与事件序号的散点时间线"""
    need = {"user_id", "seq", "outcome"}
    if log.empty or not need.issubset(log.columns):
        return False
    log = log.sort_values(["user_id", "seq"]).reset_index(drop=True)
    users = list(log["user_id"].unique())
    fig, ax = plt.subplots(figsize=(10, max(3, 0.8 * len(users) + 1)))
    for i, uid in enumerate(users):
        g = log[log["user_id"] == uid]
        ax.scatter(g["seq"], [i] * len(g), c=g["outcome"].map(OUTCOME_COLORS), s=70, alpha=0.85, edgecolors="white")
    ax.set_yticks(range(len(users)))
    ax.set_yticklabels([str(u) for u in users])
    ax.set_xlabel("事件序号（按时间）")
    ax.set_title("图4-2 委托—收回事件流（每个点代表一次委托事件）")
    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=9, label=l)
               for l, c in OUTCOME_COLORS.items()]
    ax.legend(handles=handles, loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "图4-2-委托收回事件流.png"), dpi=200)
    plt.close(fig)
    return True


def fig_4_3(edf):
    """单vs多智能体对比：每任务两条件的均值柱状图"""
    if edf.empty or "condition" not in edf.columns or "task" not in edf.columns:
        return False
    rating_cols = [c for c in edf.columns if c.startswith("r")]
    if rating_cols:
        edf["quality_score"] = edf[rating_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    tasks = ["A", "B", "C"]
    metrics = [("total_time_min", "总时长(min)"), ("intervention_count", "介入次数"), ("quality_score", "质量(盲评)")]
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    x = np.arange(len(tasks))
    w = 0.35
    for ax, (col, label) in zip(axes, metrics):
        if col not in edf.columns:
            ax.set_visible(False)
            continue
        single_m = []
        multi_m = []
        for t in tasks:
            sv = edf[(edf["task"] == t) & (edf["condition"] == "single")][col].astype(float)
            mv = edf[(edf["task"] == t) & (edf["condition"] == "multi")][col].astype(float)
            single_m.append(sv.mean() if len(sv) else np.nan)
            multi_m.append(mv.mean() if len(mv) else np.nan)
        ax.bar(x - w / 2, single_m, w, label="单智能体", color="#4C72B0")
        ax.bar(x + w / 2, multi_m, w, label="多智能体", color="#DD8452")
        ax.set_xticks(x)
        ax.set_xticklabels([f"任务{t}" for t in tasks])
        ax.set_title(label)
        ax.legend(fontsize=8)
    fig.suptitle("图4-3 单vs多智能体对比")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "图4-3-单vs多智能体对比.png"), dpi=200)
    plt.close(fig)
    return True


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    made = []
    if os.path.exists(QDATA):
        q = pd.read_csv(QDATA, encoding="utf-8-sig")
        if fig_4_1(q):
            made.append("图4-1-委托边界曲线.png")
    if os.path.exists(LDATA):
        log = pd.read_csv(LDATA, encoding="utf-8-sig")
        if fig_4_2(log):
            made.append("图4-2-委托收回事件流.png")
    if os.path.exists(EDATA):
        edf = pd.read_csv(EDATA, encoding="utf-8-sig")
        if fig_4_3(edf):
            made.append("图4-3-单vs多智能体对比.png")
    if made:
        print("已生成：")
        for f in made:
            print(" -", f)
    else:
        print("未生成任何图。请先填写问卷（G1）、日志编码表与实验数据记录表。")
    print(f"输出目录：{OUT_DIR}")


if __name__ == "__main__":
    main()
