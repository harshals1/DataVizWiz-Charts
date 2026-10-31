"""Seaborn vs Matplotlib on synthetic loan-portfolio data.
Same 3 charts built both ways, with a lines-of-code count.
No input file needed: the script writes synthetic_bank_loans.csv (SYNTHETIC - say so on screen).
Units: monthly loan disbursals as an INDEX (Jan 2024 = 100), so there is no currency or country.
Outputs: v8b_*.png (chart pairs), v8b_comparison.png, v8b_loc.png, v8b_polished.png, v8b_thumb_base.png
"""
import inspect
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns

NAVY, TEAL, PURPLE, GOLD, RED = "#0F1419", "#1AC9A3", "#6B4FA6", "#D4AF37", "#FF6B6B"
PALETTE = [TEAL, PURPLE, GOLD, RED]

# ---- shared brand styling (NOT counted in the line comparison) ------------
plt.rcParams.update({"figure.facecolor": NAVY, "axes.facecolor": NAVY, "savefig.facecolor": NAVY,
                     "text.color": "white", "axes.labelcolor": "white", "xtick.color": "white",
                     "ytick.color": "white", "axes.edgecolor": "#3a4350", "grid.color": "#2a313b",
                     "axes.titlecolor": "white", "legend.facecolor": NAVY, "legend.labelcolor": "white",
                     "font.size": 10})

# ---- 1. SYNTHETIC LOAN-PORTFOLIO DATA (index, Jan 2024 = 100) -------------
products = ["Home", "Auto", "Personal", "Small Business"]
rng = np.random.default_rng(42)
months = pd.date_range("2024-01-31", periods=24, freq="ME")
trend = {"Home": .004, "Auto": .007, "Personal": .012, "Small Business": .002}
season = 1 + .08 * np.sin(2 * np.pi * (months.month - 7) / 12)          # year-end uplift
df = pd.DataFrame({"Date": months})
for p in products:
    noise = rng.normal(0, .025, 24).cumsum() * .5
    df[p] = 100 * np.exp(trend[p] * np.arange(24) + noise) * season
df.assign(**{p: df[p].round(1) for p in products}).to_csv("synthetic_bank_loans.csv", index=False)

long = df.melt(id_vars="Date", var_name="Product", value_name="Disbursals")
long["Year"] = long["Date"].dt.year
chg = df.set_index("Date")[products].pct_change().dropna().mul(100)
chg_long = chg.reset_index().melt(id_vars="Date", var_name="Product", value_name="Change %")
years = sorted(long["Year"].unique())

# ============ CHART 1: LINE ==================================================
def mpl_line():
    fig, ax = plt.subplots(figsize=(6, 3.6))
    for p, c in zip(products, PALETTE):
        ax.plot(df["Date"], df[p], color=c, label=p, linewidth=2)
    ax.set_title("Monthly loan disbursals by product (index)")
    ax.legend()
    ax.grid(alpha=.4)
    fig.autofmt_xdate()
    return fig

def sns_line():
    fig, ax = plt.subplots(figsize=(6, 3.6))
    sns.lineplot(data=long, x="Date", y="Disbursals", hue="Product", palette=PALETTE, linewidth=2, ax=ax)
    ax.set_title("Monthly loan disbursals by product (index)")
    return fig

# ============ CHART 2: GROUPED BAR ==========================================
def mpl_bar():
    fig, ax = plt.subplots(figsize=(6, 3.6))
    x, w = np.arange(len(products)), .38
    for i, y in enumerate(years):
        vals = [long[(long.Product == p) & (long.Year == y)].Disbursals.mean() for p in products]
        ax.bar(x + (i - .5) * w, vals, w, label=str(y), color=[TEAL, PURPLE][i])
    ax.set_xticks(x)
    ax.set_xticklabels(products)
    ax.legend()
    ax.set_title("Average monthly disbursals by product and year")
    return fig

def sns_bar():
    fig, ax = plt.subplots(figsize=(6, 3.6))
    sns.barplot(data=long, x="Product", y="Disbursals", hue="Year", palette=[TEAL, PURPLE], errorbar=None, ax=ax)
    ax.set_title("Average monthly disbursals by product and year")
    return fig

# ============ CHART 3: DISTRIBUTION (BOX) ===================================
def mpl_box():
    fig, ax = plt.subplots(figsize=(6, 3.6))
    bp = ax.boxplot([chg[p] for p in products], tick_labels=products, patch_artist=True)
    for patch, c in zip(bp["boxes"], PALETTE):
        patch.set_facecolor(c)
    for m in bp["medians"]:
        m.set_color("white")
    ax.set_title("Monthly % change in disbursals by product")
    return fig

def sns_box():
    fig, ax = plt.subplots(figsize=(6, 3.6))
    sns.boxplot(data=chg_long, x="Product", y="Change %", hue="Product", palette=PALETTE, legend=False, ax=ax)
    ax.set_title("Monthly % change in disbursals by product")
    return fig

PAIRS = [("Line", mpl_line, sns_line), ("Grouped bar", mpl_bar, sns_bar), ("Box plot", mpl_box, sns_box)]

def loc(fn):  # plotting lines inside the function: skip def, blanks, comments, return
    body = inspect.getsource(fn).splitlines()[1:]
    return sum(1 for l in body if l.strip() and not l.strip().startswith(("#", "return")))

counts = {}
for name, m, s in PAIRS:
    key = name.split()[0].lower()
    fm, fs = m(), s()
    fm.savefig(f"v8b_{key}_mpl.png", dpi=130); fs.savefig(f"v8b_{key}_sns.png", dpi=130)
    plt.close(fm); plt.close(fs)
    counts[name] = (loc(m), loc(s))
    print(f"{name:12s} matplotlib {counts[name][0]:>2d} lines | seaborn {counts[name][1]:>2d} lines")

# ---- side-by-side comparison grid -----------------------------------------
fig, axs = plt.subplots(3, 2, figsize=(11, 10))
for i, (name, _, _) in enumerate(PAIRS):
    key = name.split()[0].lower()
    for j, lib in enumerate(["mpl", "sns"]):
        axs[i, j].imshow(mpimg.imread(f"v8b_{key}_{lib}.png")); axs[i, j].axis("off")
        axs[i, j].set_title(f"{'Matplotlib' if lib=='mpl' else 'Seaborn'}: {counts[name][j]} lines", color=TEAL, fontsize=12)
fig.tight_layout(); fig.savefig("v8b_comparison.png", dpi=120); plt.close(fig)

# ---- lines-of-code chart ---------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4))
x, w = np.arange(len(PAIRS)), .36
ax.bar(x - w/2, [c[0] for c in counts.values()], w, color=PURPLE, label="Matplotlib")
ax.bar(x + w/2, [c[1] for c in counts.values()], w, color=TEAL, label="Seaborn")
for i, c in enumerate(counts.values()):
    ax.text(i - w/2, c[0] + .2, c[0], ha="center"); ax.text(i + w/2, c[1] + .2, c[1], ha="center")
ax.set_xticks(x); ax.set_xticklabels(counts.keys()); ax.legend(frameon=False)
ax.set_title("Lines of plotting code for the same chart", loc="left")
for sp in ["top", "right"]: ax.spines[sp].set_visible(False)
fig.tight_layout(); fig.savefig("v8b_loc.png", dpi=150); plt.close(fig)

# ============ THE BEST OF BOTH: seaborn draws, matplotlib finishes ==========
def polished():
    fig, ax = plt.subplots(figsize=(8, 4.4))
    sns.lineplot(data=long, x="Date", y="Disbursals", hue="Product", palette=PALETTE, linewidth=2.2, ax=ax)   # seaborn: fast
    top = long.loc[long.Disbursals.idxmax()]
    ax.annotate(f"Peak: {top.Product}, {top.Date:%b %Y}", (top.Date, top.Disbursals), xytext=(-150, 6),
                textcoords="offset points", color=GOLD, arrowprops=dict(arrowstyle="->", color=GOLD))      # matplotlib: story
    sns.despine(ax=ax)                                                                                      # clean frame
    ax.set_title("Which loan product is driving growth?", loc="left", fontsize=13)                          # left title
    ax.set_ylabel("Disbursals (index, Jan 2024 = 100)")
    ax.legend(frameon=False, ncol=4, loc="lower center", bbox_to_anchor=(.5, -.28))
    return fig
fig = polished(); fig.tight_layout(); fig.savefig("v8b_polished.png", dpi=150); plt.close(fig)

# ---- thumbnail base: code (left) vs result (right) ------------------------
snippet = ("x = np.arange(4)\n"
           "for i, y in enumerate(years):\n"
           "    vals = [mean(p, y) for p in products]\n"
           "    ax.bar(x + (i-.5)*w, vals, w)\n"
           "ax.set_xticks(x)\n"
           "ax.set_xticklabels(products)\n"
           "ax.legend()")
fig = plt.figure(figsize=(12.8, 7.2))
axl = fig.add_axes([0.03, 0.1, 0.46, 0.8]); axl.axis("off")
axl.text(0, .95, snippet, va="top", ha="left", family="monospace", fontsize=17, color="#8E74C8", linespacing=1.7)
fig.add_artist(plt.Line2D([0.5, 0.5], [0.08, 0.92], color=TEAL, lw=3))
axr = fig.add_axes([0.55, 0.14, 0.42, 0.72])
sns.barplot(data=long, x="Product", y="Disbursals", hue="Year", palette=[TEAL, PURPLE], errorbar=None, ax=axr, legend=False)
axr.set_xlabel(""); axr.set_ylabel(""); axr.tick_params(labelsize=14)
for sp in ["top", "right"]: axr.spines[sp].set_visible(False)
fig.savefig("v8b_thumb_base.png", dpi=100); plt.close(fig)
print("\nSaved all images. Gotcha for the video: plt.style.use('seaborn') now raises an error -> use 'seaborn-v0_8'.")
