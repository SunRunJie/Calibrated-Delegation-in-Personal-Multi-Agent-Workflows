# -*- coding: utf-8 -*-
"""
03-委托边界与假设检验.py
H2：七环节委托率差异（问卷G1，二值 → Cochran's Q）
H3a：环节内失败前后委托次数变化（日志，配对 Wilcoxon）
H3b：记忆积累与持续使用意向相关（记忆指标表 × 问卷F量表，Spearman）
输入：02-问卷/问卷-数据模板.csv、05-日志编码/日志编码表.csv、05-日志编码/记忆指标表.csv
输出：08-数据汇总/03-委托边界与假设检验.csv
用法：python 03-委托边界与假设检验.py
"""
import os
import sys
import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QDATA = os.path.join(BASE, "02-问卷", "问卷-数据模板.csv")
LDATA = os.path.join(BASE, "05-日志编码", "日志编码表.csv")
MDATA = os.path.join(BASE, "05-日志编码", "记忆指标表.csv")
OUT_DIR = os.path.join(BASE, "08-数据汇总")
OUT = os.path.join(OUT_DIR, "03-委托边界与假设检验.csv")

STAGES = [("G1_1", "需求界定"), ("G1_2", "信息检索"), ("G1_3", "信息整理"),
          ("G1_4", "分析推理"), ("G1_5", "内容生成"), ("G1_6", "执行操作"), ("G1_7", "判断决策")]


def cochran_q(X):
    """Cochran's Q 检验（k个相关二值样本的差异）"""
    X = np.asarray(X, dtype=float)
    n, k = X.shape
    if k < 2 or n == 0:
        return np.nan, np.nan
    total = X.sum()
    col = X.sum(axis=0)
    row = X.sum(axis=1)
    denom = k * total - (row ** 2).sum()
    if denom <= 0:
        return np.nan, np.nan
    Q = (k - 1) * (k * (col ** 2).sum() - total ** 2) / denom
    p = 1 - stats.chi2.cdf(Q, k - 1)
    return Q, p


def main():
    results = []

    # ---------- H2：问卷G1 七环节委托率差异 ----------
    if os.path.exists(QDATA):
        q = pd.read_csv(QDATA, encoding="utf-8-sig")
        # 与01-问卷分析.py保持一致：剔除测谎项未通过（J2≠2）的作答
        if "J2" in q.columns:
            q = q[pd.to_numeric(q["J2"], errors="coerce") == 2]
        cols = [c for c, _ in STAGES if c in q.columns]
        if cols:
            sub = q[cols].apply(pd.to_numeric, errors="coerce").dropna(how="any")
            if len(sub) >= 2:
                rates = sub.mean(axis=0)
                for (col, label), rate in zip(STAGES, rates):
                    results.append({"假设": "H2", "项目": f"委托率·{label}", "统计量": f"{rate:.3f}",
                                    "p值": "", "判定": ""})
                Q, p = cochran_q(sub.values)
                results.append({"假设": "H2", "项目": "Cochran's Q（七环节差异）",
                                "统计量": f"Q={Q:.3f}" if Q == Q else "",
                                "p值": f"{p:.3f}" if p == p else "",
                                "判定": "显著" if (p == p and p < 0.05) else "不显著"})

    # ---------- H3a：日志 首次失败前后14天该环节委托频率（次/天） ----------
    # 事件研究式窗口口径：以首次失败日为界，比较前后各14天内该环节的委托频率。
    # 只保留失败前14天内实际委托过该环节的配对（未用过的环节谈不上"收回"）。
    # 按天归一化并固定窗口长度，排除了"失败后经历时间更长、事件自然更多"的混淆。
    if os.path.exists(LDATA):
        log = pd.read_csv(LDATA, encoding="utf-8-sig")
        need = {"user_id", "seq", "stage", "outcome", "event_date"}
        if not log.empty and need.issubset(log.columns):
            log["event_date"] = pd.to_datetime(log["event_date"], errors="coerce")
            log = log.dropna(subset=["event_date"]).sort_values(["user_id", "seq"])
            WIN = pd.Timedelta(days=14)
            before, after = [], []
            for uid, g in log.groupby("user_id"):
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
            if len(before) >= 2 and np.any(np.array(before) != np.array(after)):
                try:
                    w, p = stats.wilcoxon(before, after)
                    results.append({"假设": "H3a", "项目": "首次失败前后14天该环节委托频率配对比较",
                                    "统计量": f"W={w:.0f}", "p值": f"{p:.3f}",
                                    "判定": "显著" if p < 0.05 else "不显著"})
                except Exception as e:
                    results.append({"假设": "H3a", "项目": "配对比较", "统计量": str(e), "p值": "", "判定": ""})
                results.append({"假设": "H3a", "项目": "失败前频率均值(次/天)", "统计量": f"{np.mean(before):.3f}",
                                "p值": "", "判定": ""})
                results.append({"假设": "H3a", "项目": "失败后频率均值(次/天)", "统计量": f"{np.mean(after):.3f}",
                                "p值": "", "判定": ""})
            elif len(before) >= 2:
                results.append({"假设": "H3a", "项目": "首次失败前后14天该环节委托频率配对比较",
                                "统计量": "两组完全相同", "p值": "", "判定": "无差异"})

    # ---------- H3b：记忆积累 × 持续使用意向 ----------
    if os.path.exists(MDATA) and os.path.exists(QDATA):
        mem = pd.read_csv(MDATA, encoding="utf-8-sig")
        q = pd.read_csv(QDATA, encoding="utf-8-sig")
        # 与01-问卷分析.py保持一致：剔除测谎项未通过（J2≠2）的作答
        if "J2" in q.columns:
            q = q[pd.to_numeric(q["J2"], errors="coerce") == 2]
        f_cols = ["F1", "F2", "F3"]
        if "link_id" in mem.columns and "link_id" in q.columns and all(c in q.columns for c in f_cols):
            q["continuance"] = q[f_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
            m = mem.merge(q[["link_id", "continuance"]], on="link_id", how="inner").dropna()
            for col, label in [("timeline_lines", "时间轴行数"), ("mem_updates", "记忆更新频次")]:
                if col in m.columns and len(m) >= 3:
                    r, p = stats.spearmanr(m[col], m["continuance"])
                    results.append({"假设": "H3b", "项目": f"记忆积累（{label}）×持续使用意向",
                                    "统计量": f"ρ={r:.3f}", "p值": f"{p:.3f}",
                                    "判定": "显著" if p < 0.05 else "不显著"})

    res = pd.DataFrame(results)
    os.makedirs(OUT_DIR, exist_ok=True)
    res.to_csv(OUT, index=False, encoding="utf-8-sig")

    if res.empty:
        print("未找到足够数据。请先填写问卷（G1）、日志编码表（含seq/outcome）与记忆指标表（link_id需与问卷一致）。")
    else:
        print(res.to_string(index=False))
    print(f"\n结果已保存：{OUT}")


if __name__ == "__main__":
    main()
