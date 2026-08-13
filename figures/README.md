# Research Figures

This directory preserves the original 33-figure sequence, visual grammar, chart types, and numbering. The figures were translated into English without replacing the original design with a new figure system.

Run:

```bash
.venv/Scripts/python analysis/generate_figures.py
```

The script reads authorized local inputs from `data/restricted/` and writes 33 English PNG files to this directory at 300 dpi. It does not generate PDFs.

## Visual standard

All figures use the official `scientific-figure-assistant` research palette in numerical order. Group 1 is used first (`#8DC5E8`, `#3D6680`, `#D72828`, `#349237`, `#D2868B`); Group 2 supplies additional categorical colors only when necessary (`#6769A1`, `#B6B6B6`, `#A39571`, `#3183BA`, `#D85B75`). White is reserved for the background and annotation clearance. English text, numbers, and symbols use Times New Roman. Exports use 300 dpi and tight bounding boxes.

The figures were checked for cropped labels, text-box overflow, annotation collisions, and manuscript-order consistency.

The H3a values in Figure 22 and Figure 33 use the corrected user-level specification: mean daily rate 0.122 before versus 0.051 after the first unsuccessful event, W = 1.5, exact p = .0015, n = 12 users.
