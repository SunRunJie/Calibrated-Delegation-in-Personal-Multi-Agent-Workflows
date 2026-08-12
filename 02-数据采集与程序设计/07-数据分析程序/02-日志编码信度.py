# -*- coding: utf-8 -*-
"""
02-日志编码信度.py
计算20%样本双编码者的Cohen's κ（任务流环节/结果/失败原因/错误暴露方式）
输入：05-日志编码/日志编码表.csv（主编码列＋coderB_*列）
输出：控制台κ值；08-数据汇总/02-日志编码信度.csv
用法：python 02-日志编码信度.py
"""
import os
import sys
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "05-日志编码", "日志编码表.csv")
OUT_DIR = os.path.join(BASE, "08-数据汇总")
OUT = os.path.join(OUT_DIR, "02-日志编码信度.csv")

DIMS = [
    ("stage", "coderB_stage", "任务流环节"),
    ("outcome", "coderB_outcome", "结果"),
    ("fail_reason", "coderB_fail_reason", "失败原因"),
    ("error_exposure", "coderB_error_exposure", "错误暴露方式"),
]


def cohen_kappa(a, b):
    """Cohen's κ（手动实现，避免额外依赖）"""
    a = list(a)
    b = list(b)
    n = len(a)
    if n == 0:
        return np.nan
    cats = sorted(set(a) | set(b))
    idx = {c: i for i, c in enumerate(cats)}
    table = np.zeros((len(cats), len(cats)))
    for x, y in zip(a, b):
        table[idx[x], idx[y]] += 1
    po = np.trace(table) / n
    pe = float((table.sum(axis=1) / n) @ (table.sum(axis=0) / n))
    if pe >= 1.0:
        return 1.0 if po == 1.0 else np.nan
    return (po - pe) / (1 - pe)


def main():
    if not os.path.exists(DATA):
        sys.exit("未找到日志编码表，请先完成编码并保存为 日志编码表.csv。")
    df = pd.read_csv(DATA, encoding="utf-8-sig")
    if df.empty:
        sys.exit("日志编码表为空。")

    rows = []
    for col, col_b, label in DIMS:
        if col not in df.columns or col_b not in df.columns:
            continue
        d = df[[col, col_b]].dropna()
        if d.empty:
            rows.append({"维度": label, "双编码样本量": 0, "Cohen's κ": np.nan})
            continue
        k = cohen_kappa(d[col], d[col_b])
        rows.append({"维度": label, "双编码样本量": len(d), "Cohen's κ": round(k, 3) if k == k else np.nan})

    res = pd.DataFrame(rows)
    os.makedirs(OUT_DIR, exist_ok=True)
    res.to_csv(OUT, index=False, encoding="utf-8-sig")

    print(f"编码事件总数：{len(df)}")
    print(res.to_string(index=False))
    print("\n判定：各维度 κ≥0.70 为可接受；不足时回到编码手册澄清定义，重新编码样本直至达标。")
    print(f"结果已保存：{OUT}")


if __name__ == "__main__":
    main()
