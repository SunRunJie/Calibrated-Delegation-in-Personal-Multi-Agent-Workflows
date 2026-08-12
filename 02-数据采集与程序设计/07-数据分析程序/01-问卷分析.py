# -*- coding: utf-8 -*-
"""
01-问卷分析.py
输入：02-问卷/问卷-数据模板.csv（问卷星导出或HTML问卷导出后按模板整理）
输出：08-数据汇总/01-问卷分析结果.csv（各量表Cronbach's α与描述统计、委托率、收回原因、使用状态分布）
用法：python 01-问卷分析.py
"""
import os
import sys
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "02-问卷", "问卷-数据模板.csv")
OUT_DIR = os.path.join(BASE, "08-数据汇总")
OUT = os.path.join(OUT_DIR, "01-问卷分析结果.csv")

LIE_ITEM = "J2"        # 测谎项，应选择2（比较不同意）
LIE_EXPECT = 2
REVERSE = ["J1"]       # 反向题：按 8-原始分 转换

SCALES = {
    "PU感知有用性": ["B1", "B2", "B3", "B4"],
    "PEOU感知易用性": ["C1", "C2", "C3", "C4"],
    "感知信任": ["D1", "D2", "D3", "D4"],
    "感知风险": ["E1", "E2", "E3"],
    "持续使用意向": ["F1", "F2", "F3"],
    "记忆感知": ["I1", "I2", "I3"],
}

STAGES = [("G1_1", "需求界定"), ("G1_2", "信息检索"), ("G1_3", "信息整理"),
          ("G1_4", "分析推理"), ("G1_5", "内容生成"), ("G1_6", "执行操作"), ("G1_7", "判断决策")]
REASONS = [("H1_1", "能力不足"), ("H1_2", "输出不可靠"), ("H1_3", "不省时间"),
           ("H1_4", "隐私顾虑"), ("H1_5", "情感需求")]


def cronbach_alpha(items_df):
    """Cronbach's α 系数"""
    k = items_df.shape[1]
    if k < 2 or items_df.shape[0] < 2:
        return np.nan
    var_sum = items_df.var(axis=0, ddof=1).sum()
    total_var = items_df.sum(axis=1).var(ddof=1)
    if total_var == 0:
        return np.nan
    return k / (k - 1) * (1 - var_sum / total_var)


def main():
    if not os.path.exists(DATA):
        sys.exit("未找到问卷数据文件，请将问卷结果按 问卷-数据模板.csv 的格式整理后重试。")
    df = pd.read_csv(DATA, encoding="utf-8-sig")
    if df.empty:
        sys.exit("问卷数据为空。")
    n0 = len(df)

    # 测谎项检查
    if LIE_ITEM in df.columns:
        bad = df.index[df[LIE_ITEM].astype(float) != LIE_EXPECT]
        if len(bad) > 0:
            print(f"测谎项未通过，剔除 {len(bad)} 份（行号：{[i + 2 for i in bad]}）")
            df = df.drop(index=bad)

    # 反向计分
    for c in REVERSE:
        if c in df.columns:
            df[c] = 8 - df[c].astype(float)

    rows = []
    for name, items in SCALES.items():
        sub = df[items].apply(pd.to_numeric, errors="coerce").dropna(how="any")
        if sub.empty:
            rows.append({"指标": name, "N": 0, "Cronbach's α": np.nan, "均值": np.nan, "SD": np.nan})
            continue
        alpha = cronbach_alpha(sub)
        mean = sub.mean(axis=1).mean()
        sd = sub.mean(axis=1).std(ddof=1)
        rows.append({"指标": name, "N": len(sub), "Cronbach's α": round(alpha, 3),
                     "均值": round(mean, 3), "SD": round(sd, 3)})

    for col, label in STAGES:
        if col in df.columns:
            v = df[col].astype(float)
            rows.append({"指标": f"委托率·{label}", "N": len(v), "Cronbach's α": np.nan,
                         "均值": round(v.mean(), 3), "SD": round(v.std(ddof=1), 3)})
    for col, label in REASONS:
        if col in df.columns:
            v = df[col].astype(float)
            rows.append({"指标": f"收回原因·{label}", "N": len(v), "Cronbach's α": np.nan,
                         "均值": round(v.mean(), 3), "SD": round(v.std(ddof=1), 3)})

    res = pd.DataFrame(rows)
    os.makedirs(OUT_DIR, exist_ok=True)
    res.to_csv(OUT, index=False, encoding="utf-8-sig")

    print(f"有效样本量：{len(df)}（原始 {n0} 份）")
    print(res.to_string(index=False))
    if "A1" in df.columns:
        print("\n使用状态分布（A1：1每天都在用 2每周几次 3偶尔用 4已停止使用）")
        print(df["A1"].value_counts().sort_index().to_string())
    print(f"\n结果已保存：{OUT}")


if __name__ == "__main__":
    main()
