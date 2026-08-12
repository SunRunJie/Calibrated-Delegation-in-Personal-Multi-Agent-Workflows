# -*- coding: utf-8 -*-
"""
04-对比实验分析.py
单vs多智能体对比：每个任务内配对 Wilcoxon 符号秩检验 ＋ 效应量 r ＋ 描述统计
输入：06-对比实验/实验数据记录表.csv
输出：08-数据汇总/04-对比实验分析.csv（对应研究报告表4-1）
用法：python 04-对比实验分析.py
"""
import os
import sys
import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "06-对比实验", "实验数据记录表.csv")
OUT_DIR = os.path.join(BASE, "08-数据汇总")
OUT = os.path.join(OUT_DIR, "04-对比实验分析.csv")

RATING_COLS = ["r1_relevance", "r1_accuracy", "r1_structure", "r1_completeness",
               "r2_relevance", "r2_accuracy", "r2_structure", "r2_completeness"]
METRICS = [("total_time_min", "总时长(min)"),
           ("intervention_count", "人工介入次数"),
           ("intervention_time_min", "人工介入时长(min)"),
           ("quality_score", "产出质量(盲评)")]


def effect_r(w, n):
    """由 Wilcoxon W 近似效应量 r = |Z| / sqrt(n)"""
    if n == 0:
        return np.nan
    mu = n * (n + 1) / 4
    sigma = np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    if sigma == 0:
        return np.nan
    z = (w - mu) / sigma
    return abs(z) / np.sqrt(n)


def fmt(v):
    return round(v, 3) if v == v else ""


def main():
    if not os.path.exists(DATA):
        sys.exit("未找到实验数据，请填写 实验数据记录表.csv 后重试。")
    df = pd.read_csv(DATA, encoding="utf-8-sig")
    if df.empty:
        sys.exit("实验数据为空。")

    df["quality_score"] = df[RATING_COLS].apply(pd.to_numeric, errors="coerce").mean(axis=1)

    rows = []
    for task in ["A", "B", "C"]:
        sub = df[df["task"] == task]
        s = sub[sub["condition"] == "single"]
        m = sub[sub["condition"] == "multi"]
        for col, label in METRICS:
            sv = s[col].astype(float)
            mv = m[col].astype(float)
            paired = pd.merge(s[["participant", col]], m[["participant", col]],
                              on="participant", suffixes=("_s", "_m")).dropna()
            sm, mm = paired[col + "_s"], paired[col + "_m"]
            if len(sm) >= 2:
                try:
                    w, p = stats.wilcoxon(sm, mm)
                    r = effect_r(w, len(sm))
                    verdict = "显著" if p < 0.05 else "不显著"
                except Exception as e:
                    w, p, r, verdict = np.nan, np.nan, np.nan, f"无法检验({e})"
            else:
                w, p, r, verdict = np.nan, np.nan, np.nan, "配对不足"
            rows.append({
                "任务": f"任务{task}", "指标": label,
                "单智能体M±SD": f"{sv.mean():.2f}±{sv.std(ddof=1):.2f}" if len(sv) else "",
                "多智能体M±SD": f"{mv.mean():.2f}±{mv.std(ddof=1):.2f}" if len(mv) else "",
                "配对n": len(sm), "W": fmt(w), "p值": fmt(p), "效应量r": fmt(r), "判定": verdict,
            })

    res = pd.DataFrame(rows)
    os.makedirs(OUT_DIR, exist_ok=True)
    res.to_csv(OUT, index=False, encoding="utf-8-sig")

    print(res.to_string(index=False))
    print("\n填入报告表4-1。判定说明：任务A/B上多智能体显著更低且质量不低于基线 → H4支持；")
    print("任务C无显著差异与H4的边界命题一致。")
    print(f"结果已保存：{OUT}")


if __name__ == "__main__":
    main()
