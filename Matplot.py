"""
╔══════════════════════════════════════════════════════════════╗
║        Sales Analytics Dashboard  —  Matplotlib Project      ║
║        Run with:  python dashboard.py                         ║
║        Output:    sales_dashboard.png  (same folder)          ║
╚══════════════════════════════════════════════════════════════╝

Requirements:
    pip install matplotlib numpy
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FuncFormatter
import numpy as np

# ─────────────────────────── OUTPUT PATH ─────────────────────
# Saves the PNG in the same folder as this script — works on
# any Windows / Mac / Linux machine without any path changes.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "sales_dashboard.png")

# ─────────────────────────── THEME ───────────────────────────
BG      = "#0f1117"
PANEL   = "#1a1d27"
ACCENT  = "#6c63ff"
GREEN   = "#00d97e"
RED     = "#ff4d6d"
YELLOW  = "#ffc94d"
CYAN    = "#38bdf8"
TEXT    = "#e2e8f0"
SUBTEXT = "#94a3b8"
GRID    = "#2a2d3a"

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    PANEL,
    "axes.edgecolor":    GRID,
    "axes.labelcolor":   TEXT,
    "xtick.color":       SUBTEXT,
    "ytick.color":       SUBTEXT,
    "text.color":        TEXT,
    "grid.color":        GRID,
    "grid.linewidth":    0.6,
    "font.family":       "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

# ─────────────────────────── DATA ────────────────────────────
np.random.seed(42)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
x = np.arange(len(months))

revenue  = np.array([142, 158, 175, 161, 189, 204,
                     198, 221, 237, 215, 248, 272]) * 1000
expenses = np.array([ 98, 105, 112, 108, 121, 130,
                      127, 138, 145, 132, 149, 161]) * 1000
profit   = revenue - expenses

products = ["Software", "Services", "Hardware", "Training", "Support"]
prod_rev = np.array([38, 27, 18, 10, 7])
prod_clr = [ACCENT, GREEN, CYAN, YELLOW, RED]

regions   = ["North", "South", "East", "West", "Overseas"]
reg_sales = np.array([245, 189, 312, 178, 134]) * 1000

# Weekly heatmap data (12 weeks x 5 weekdays)
weekly = np.random.randint(40, 200, size=(12, 5)).astype(float)
weekly[weekly < 70] *= 0.5

# Forecast (linear trend)
trend    = np.polyfit(x, revenue, 1)
fore_x   = np.arange(len(months) + 4)
forecast = np.polyval(trend, fore_x)
ci_upper = forecast + 18000 + fore_x * 800
ci_lower = forecast - 18000 - fore_x * 800

# ─────────────────────────── FIGURE LAYOUT ───────────────────
fig = plt.figure(figsize=(20, 14))
fig.patch.set_facecolor(BG)

gs = gridspec.GridSpec(
    3, 4,
    figure=fig,
    hspace=0.52,
    wspace=0.40,
    left=0.05, right=0.97,
    top=0.91,  bottom=0.06,
)

# ── Main Title ───────────────────────────────────────────────
fig.text(0.5, 0.965, "Sales Analytics Dashboard",
         ha="center", va="top",
         fontsize=22, fontweight="bold", color=TEXT)
fig.text(0.5, 0.945, "Full-Year Performance Report   |   FY 2024",
         ha="center", va="top", fontsize=11, color=SUBTEXT)


# ════════════════════════════════════════════════════════════
# 1. Revenue vs Expenses  (area + line)  — top-left, 2 cols
# ════════════════════════════════════════════════════════════
ax1 = fig.add_subplot(gs[0, :2])
ax1.set_title("Revenue vs Expenses", fontsize=12, fontweight="bold",
              loc="left", pad=8, color=TEXT)

ax1.fill_between(x, revenue,  alpha=0.22, color=GREEN)
ax1.fill_between(x, expenses, alpha=0.18, color=RED)
ax1.plot(x, revenue,  color=GREEN, lw=2.5, marker="o",
         markersize=5, label="Revenue",  zorder=3)
ax1.plot(x, expenses, color=RED,   lw=2.5, marker="o",
         markersize=5, label="Expenses", zorder=3)

ax1.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v/1000:.0f}k"))
ax1.set_xticks(x)
ax1.set_xticklabels(months, fontsize=8)
ax1.legend(frameon=False, fontsize=9)
ax1.grid(axis="y", linestyle="--")


# ════════════════════════════════════════════════════════════
# 2. Monthly Profit  (bar)  — top-right, 2 cols
# ════════════════════════════════════════════════════════════
ax2 = fig.add_subplot(gs[0, 2:])
ax2.set_title("Monthly Profit", fontsize=12, fontweight="bold",
              loc="left", pad=8, color=TEXT)

bar_colors = [GREEN if p >= 0 else RED for p in profit]
bars = ax2.bar(x, profit, color=bar_colors, width=0.65,
               edgecolor=BG, linewidth=0.5, zorder=2)

for bar, val in zip(bars, profit):
    ax2.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 1500,
             f"${val/1000:.0f}k",
             ha="center", va="bottom", fontsize=7.5, color=SUBTEXT)

ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v/1000:.0f}k"))
ax2.set_xticks(x)
ax2.set_xticklabels(months, fontsize=8)
ax2.axhline(0, color=GRID, lw=1)
ax2.grid(axis="y", linestyle="--")


# ════════════════════════════════════════════════════════════
# 3. Product Revenue  (donut)  — mid col-0
# ════════════════════════════════════════════════════════════
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_title("Revenue by Product", fontsize=12, fontweight="bold",
              loc="left", pad=8, color=TEXT)

wedges, label_texts, autotexts = ax3.pie(
    prod_rev,
    labels=products,
    colors=prod_clr,
    autopct="%1.0f%%",
    pctdistance=0.78,
    startangle=90,
    wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=1.5),
)
for at in autotexts:
    at.set_fontsize(8)
    at.set_color(BG)
    at.set_fontweight("bold")
for t in label_texts:
    t.set_fontsize(8.5)
    t.set_color(TEXT)

ax3.text(0, 0, "100%\nMix",
         ha="center", va="center", fontsize=10,
         fontweight="bold", color=TEXT)


# ════════════════════════════════════════════════════════════
# 4. Regional Sales  (horizontal bar)  — mid col-1
# ════════════════════════════════════════════════════════════
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_title("Regional Sales", fontsize=12, fontweight="bold",
              loc="left", pad=8, color=TEXT)

y4     = np.arange(len(regions))
h_bars = ax4.barh(y4, reg_sales, color=ACCENT,
                  height=0.55, edgecolor=BG, linewidth=0.5)

for bar, val in zip(h_bars, reg_sales):
    ax4.text(val + 4000,
             bar.get_y() + bar.get_height() / 2,
             f"${val/1000:.0f}k",
             va="center", fontsize=8, color=SUBTEXT)

ax4.set_yticks(y4)
ax4.set_yticklabels(regions, fontsize=9)
ax4.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v/1000:.0f}k"))
ax4.set_xlim(0, max(reg_sales) * 1.25)
ax4.grid(axis="x", linestyle="--")


# ════════════════════════════════════════════════════════════
# 5. Revenue Forecast  (line + CI)  — mid col-2 & 3
# ════════════════════════════════════════════════════════════
ax5 = fig.add_subplot(gs[1, 2:])
ax5.set_title("Revenue Forecast (+4 months)", fontsize=12, fontweight="bold",
              loc="left", pad=8, color=TEXT)

all_labels = months + ["Jan'25", "Feb'25", "Mar'25", "Apr'25"]
ax5.fill_between(fore_x, ci_lower, ci_upper,
                 alpha=0.15, color=ACCENT, label="95% CI")
ax5.plot(fore_x, forecast, color=ACCENT, lw=1.5,
         linestyle="--", label="Trend")
ax5.plot(x, revenue, color=GREEN, lw=2.5,
         marker="o", markersize=5, label="Actual")
ax5.axvline(11.5, color=SUBTEXT, lw=0.8, linestyle=":")
ax5.text(11.65, max(forecast) * 0.88, "Forecast >>",
         fontsize=8, color=SUBTEXT)

ax5.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v/1000:.0f}k"))
ax5.set_xticks(fore_x)
ax5.set_xticklabels(all_labels, fontsize=7.5, rotation=30, ha="right")
ax5.legend(frameon=False, fontsize=8.5)
ax5.grid(axis="y", linestyle="--")


# ════════════════════════════════════════════════════════════
# 6. Weekly Sales Heatmap  — bottom row, full width
# ════════════════════════════════════════════════════════════
ax6 = fig.add_subplot(gs[2, :])
ax6.set_title("Weekly Sales Heatmap  (Mon - Fri, 12 Weeks)",
              fontsize=12, fontweight="bold", loc="left", pad=8, color=TEXT)

im = ax6.imshow(weekly.T, aspect="auto", cmap="RdYlGn",
                vmin=weekly.min(), vmax=weekly.max())

days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
ax6.set_yticks(range(5))
ax6.set_yticklabels(days, fontsize=9)
ax6.set_xticks(range(12))
ax6.set_xticklabels([f"Wk {i+1}" for i in range(12)], fontsize=8)

for i in range(12):
    for j in range(5):
        val = weekly[i, j]
        txt_color = "black" if val > 130 else "white"
        ax6.text(i, j, f"{val:.0f}",
                 ha="center", va="center",
                 fontsize=7.5, color=txt_color, fontweight="bold")

cbar = fig.colorbar(im, ax=ax6, orientation="vertical",
                    fraction=0.015, pad=0.01)
cbar.ax.yaxis.set_tick_params(labelsize=8)
cbar.set_label("Units Sold", color=SUBTEXT, fontsize=9)


# ════════════════════════════════════════════════════════════
# KPI Banner  — bottom strip
# ════════════════════════════════════════════════════════════
kpis = [
    ("Total Revenue",  f"${sum(revenue)/1e6:.2f} M",              GREEN),
    ("Total Expenses", f"${sum(expenses)/1e6:.2f} M",             RED),
    ("Net Profit",     f"${sum(profit)/1e6:.2f} M",               ACCENT),
    ("Avg Margin",     f"{sum(profit)/sum(revenue)*100:.1f} %",   YELLOW),
    ("Best Month",     months[int(np.argmax(revenue))],           CYAN),
]

banner_y = 0.028
for i, (label, value, color) in enumerate(kpis):
    cx = 0.10 + i * 0.20
    rect = mpatches.FancyBboxPatch(
        (cx - 0.08, banner_y - 0.013), 0.16, 0.036,
        boxstyle="round,pad=0.005",
        transform=fig.transFigure,
        facecolor=PANEL, edgecolor=color,
        linewidth=1.2, zorder=5,
    )
    fig.add_artist(rect)
    fig.text(cx, banner_y + 0.010, value,
             ha="center", fontsize=11, fontweight="bold",
             color=color, transform=fig.transFigure, zorder=6)
    fig.text(cx, banner_y - 0.002, label,
             ha="center", fontsize=8, color=SUBTEXT,
             transform=fig.transFigure, zorder=6)


# ════════════════════════════════════════════════════════════
# Save + Show
# ════════════════════════════════════════════════════════════
plt.savefig(OUTPUT_FILE, dpi=160, bbox_inches="tight", facecolor=BG)
print(f"Dashboard saved -> {OUTPUT_FILE}")
plt.show()
