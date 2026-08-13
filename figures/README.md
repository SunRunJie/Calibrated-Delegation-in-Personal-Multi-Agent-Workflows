# Research Figures

This directory preserves the original 33-figure sequence, visual grammar, chart types, and numbering. The figures were translated into English without replacing the original design with a new figure system.

Run:

```bash
.venv/Scripts/python analysis/generate_figures.py
```

The script reads authorized local inputs from `data/restricted/` and writes 33 English PNG files to this directory at 300 dpi. It does not generate PDFs.

The H3a values in Figure 22 and Figure 33 use the corrected user-level specification: mean daily rate 0.122 before versus 0.051 after the first unsuccessful event, W = 1.5, exact p = .0015, n = 12 users.
