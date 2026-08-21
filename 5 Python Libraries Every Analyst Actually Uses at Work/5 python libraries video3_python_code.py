"""
@DataViz-Wiz — Video 3
5 Python Libraries Every Data Analyst Actually Uses at Work
============================================================
Run each section independently in Jupyter.
Copy this into a notebook cell by cell — that is how to present it.

Libraries covered:
  1. Pandas   — data loading, cleaning, groupby
  2. NumPy    — numerical ops, arrays, random data
  3. Matplotlib/Seaborn — visualisation
  4. Scikit-learn        — quick ML for analysts (linear regression)
  5. SQLAlchemy          — connecting Python to databases
"""

# ─────────────────────────────────────────────────────────────
# SETUP CELL — run this first
# ─────────────────────────────────────────────────────────────
import warnings
warnings.filterwarnings("ignore")

import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Brand palette
TEAL   = "#00C4A0"
PURPLE = "#7B5EA7"
NAVY   = "#0A0A2E"
RED    = "#E74C3C"
GOLD   = "#C9A84C"
GREY   = "#95A5A6"

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor":   "white",
    "axes.edgecolor":   "#CCCCCC",
    "axes.labelcolor":  "#333333",
    "xtick.color":      "#666666",
    "ytick.color":      "#666666",
    "grid.color":       "#EEEEEE",
    "grid.linestyle":   "--",
    "text.color":       "#111111",
    "font.size":        12,
})

np.random.seed(42)
print("✅ Setup complete — ready to go!")


# ═══════════════════════════════════════════════════════════════
# LIBRARY 1 — PANDAS
# The spreadsheet of Python. You use this every single day.
# ═══════════════════════════════════════════════════════════════

# ── Step 1: Create a realistic sales dataset ───────────────────
dates     = pd.date_range("2024-01-01", periods=120, freq="D")
regions   = np.random.choice(["North", "South", "East", "West"], 120)
products  = np.random.choice(["Laptop", "Phone", "Tablet", "Monitor"], 120)
sales     = np.random.randint(5000, 50000, 120)
units     = np.random.randint(1, 20, 120)
rep_names = np.random.choice(["Priya", "Rahul", "Anita", "Suresh", "Meena"], 120)

df = pd.DataFrame({
    "Date":     dates,
    "Region":   regions,
    "Product":  products,
    "Sales":    sales,
    "Units":    units,
    "Rep":      rep_names,
})

print("📋 Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

# ── Step 2: Quick data health check (use this EVERY time you open new data)
print("\n📊 Data Types:")
print(df.dtypes)
print("\n⚠️  Missing values:")
print(df.isnull().sum())
print("\n📈 Summary statistics:")
print(df[["Sales", "Units"]].describe().round(2))


# ── Step 3: Filter — only show North region, Sales > 20,000 ───
north_high = df[(df["Region"] == "North") & (df["Sales"] > 20000)]
print(f"\n🔍 North region, high-value sales: {len(north_high)} records")
print(north_high[["Date", "Product", "Sales"]].head(5))


# ── Step 4: GroupBy — total sales by region ────────────────────
region_summary = (
    df.groupby("Region")
      .agg(
          Total_Sales   = ("Sales", "sum"),
          Avg_Sales     = ("Sales", "mean"),
          Total_Units   = ("Units", "sum"),
          Num_Deals     = ("Sales", "count"),
      )
      .round(0)
      .sort_values("Total_Sales", ascending=False)
)
print("\n📊 Sales by Region:")
print(region_summary)


# ── Step 5: Pivot table — product × region ─────────────────────
pivot = df.pivot_table(
    values  = "Sales",
    index   = "Product",
    columns = "Region",
    aggfunc = "sum",
).round(0)

print("\n📊 Pivot — Sales by Product × Region:")
print(pivot)


# ── Step 6: Plot — bar chart of region sales ───────────────────
fig, ax = plt.subplots(figsize=(9, 5))

colors = [TEAL if r == region_summary["Total_Sales"].idxmax() else "#C8E6C9"
          for r in region_summary.index]

bars = ax.bar(region_summary.index, region_summary["Total_Sales"] / 1000,
              color=colors, width=0.55, zorder=2)

for bar, val in zip(bars, region_summary["Total_Sales"]):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 8,
            f"₹{val/1000:.0f}K",
            ha="center", va="bottom", fontsize=10,
            color=TEAL, fontweight="bold")

ax.set_title("Total Sales by Region", fontsize=15, fontweight="bold", color=NAVY, pad=14)
ax.set_xlabel("Region", fontsize=11)
ax.set_ylabel("Sales (₹ Thousands)", fontsize=11)
ax.grid(axis="y", zorder=1)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("./v3_lib1_pandas.png", dpi=150)
plt.show()
print("✅ Library 1: Pandas demo complete")


# ═══════════════════════════════════════════════════════════════
# LIBRARY 2 — NUMPY
# The engine under the hood. Faster than Python lists for numbers.
# ═══════════════════════════════════════════════════════════════

# ── Step 1: Why NumPy? Speed comparison ────────────────────────
import time

python_list = list(range(1_000_000))
numpy_array = np.arange(1_000_000)

t0 = time.time(); total = sum(python_list); t_py = time.time() - t0
t0 = time.time(); total = np.sum(numpy_array); t_np = time.time() - t0

print(f"⏱  Python list sum:  {t_py*1000:.2f} ms")
print(f"⚡  NumPy array sum:  {t_np*1000:.2f} ms")
print(f"🚀  NumPy is {t_py/t_np:.0f}x faster")


# ── Step 2: Array maths you actually use at work ────────────────
revenue  = np.array([120000, 95000, 145000, 110000, 130000])
costs    = np.array([80000,  70000, 90000,  75000,  85000])
profit   = revenue - costs                       # vectorised subtraction
margin   = (profit / revenue * 100).round(2)     # vectorised division

print("\n📊 Financial summary:")
for i, (r, c, p, m) in enumerate(zip(revenue, costs, profit, margin), 1):
    print(f"  Month {i}: Revenue ₹{r:,}  |  Cost ₹{c:,}  |  Profit ₹{p:,}  |  Margin {m}%")

print(f"\n  Avg Margin: {margin.mean():.1f}%")
print(f"  Best Margin: {margin.max():.1f}% (Month {margin.argmax()+1})")
print(f"  Worst Margin: {margin.min():.1f}% (Month {margin.argmin()+1})")


# ── Step 3: Useful NumPy operations for analysts ───────────────
data = np.random.normal(loc=50000, scale=10000, size=500)  # simulate salaries

print(f"\n📈 Salary Distribution (n={len(data)}):")
print(f"  Mean:        ₹{data.mean():,.0f}")
print(f"  Median:      ₹{np.median(data):,.0f}")
print(f"  Std Dev:     ₹{data.std():,.0f}")
print(f"  25th pct:    ₹{np.percentile(data, 25):,.0f}")
print(f"  75th pct:    ₹{np.percentile(data, 75):,.0f}")
print(f"  Above 60K:   {(data > 60000).sum()} employees ({(data>60000).mean()*100:.1f}%)")


# ── Step 4: Histogram of salary distribution ──────────────────
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(data, bins=30, color=PURPLE, alpha=0.8, edgecolor="white", zorder=2)
ax.axvline(data.mean(),   color=TEAL, linewidth=2, linestyle="--", label=f"Mean ₹{data.mean():,.0f}")
ax.axvline(np.median(data), color=RED, linewidth=2, linestyle=":", label=f"Median ₹{np.median(data):,.0f}")
ax.set_title("Salary Distribution — 500 Employees", fontsize=15, fontweight="bold", color=NAVY, pad=14)
ax.set_xlabel("Annual Salary (₹)", fontsize=11)
ax.set_ylabel("Number of Employees", fontsize=11)
ax.legend(fontsize=10)
ax.grid(axis="y", zorder=1)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("./v3_lib2_numpy.png", dpi=150)
plt.show()
print("✅ Library 2: NumPy demo complete")


# ═══════════════════════════════════════════════════════════════
# LIBRARY 3 — MATPLOTLIB + SEABORN
# You already know Matplotlib. Seaborn is the upgrade.
# ═══════════════════════════════════════════════════════════════

# ── Step 1: Same plot — Matplotlib vs Seaborn side by side ────
tips = sns.load_dataset("tips")   # built-in restaurant dataset

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Matplotlib version (more code, less pretty)
axes[0].scatter(tips["total_bill"], tips["tip"],
                alpha=0.6, color=GREY, edgecolors="#999", linewidths=0.5)
m, b = np.polyfit(tips["total_bill"], tips["tip"], 1)
xr   = np.linspace(tips["total_bill"].min(), tips["total_bill"].max(), 100)
axes[0].plot(xr, m * xr + b, color=RED, linewidth=2)
axes[0].set_title("Matplotlib (more code)", fontsize=12, color=NAVY)
axes[0].set_xlabel("Total Bill ($)"); axes[0].set_ylabel("Tip ($)")
axes[0].spines[["top","right"]].set_visible(False)

# Seaborn version (one line, more beautiful)
sns.regplot(data=tips, x="total_bill", y="tip", ax=axes[1],
            scatter_kws={"alpha": 0.6, "color": TEAL, "edgecolors": "white"},
            line_kws={"color": PURPLE, "linewidth": 2})
axes[1].set_title("Seaborn (one line, confidence band FREE)", fontsize=12, color=NAVY)
axes[1].set_xlabel("Total Bill ($)"); axes[1].set_ylabel("Tip ($)")
axes[1].spines[["top","right"]].set_visible(False)

fig.suptitle("Matplotlib vs Seaborn — Same Data", fontsize=14,
             fontweight="bold", color=NAVY, y=1.02)
plt.tight_layout()
plt.savefig("./v3_lib3_mpl_vs_sns.png", dpi=150, bbox_inches="tight")
plt.show()


# ── Step 2: Seaborn's killer feature — categorical plots ──────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Box plot
sns.boxplot(data=tips, x="day", y="total_bill", ax=axes[0],
            palette=[TEAL, PURPLE, GOLD, RED])
axes[0].set_title("Box Plot — Bills by Day", fontweight="bold", color=NAVY)
axes[0].spines[["top","right"]].set_visible(False)

# Violin plot
sns.violinplot(data=tips, x="day", y="tip", ax=axes[1],
               palette=[TEAL, PURPLE, GOLD, RED], inner="box")
axes[1].set_title("Violin Plot — Tips by Day", fontweight="bold", color=NAVY)
axes[1].spines[["top","right"]].set_visible(False)

# Heatmap — correlation matrix
corr = tips[["total_bill", "tip", "size"]].corr()
sns.heatmap(corr, ax=axes[2], annot=True, fmt=".2f",
            cmap=sns.light_palette(TEAL, as_cmap=True),
            square=True, linewidths=0.5, cbar=True)
axes[2].set_title("Correlation Heatmap", fontweight="bold", color=NAVY)

plt.suptitle("Seaborn Power Features", fontsize=14, fontweight="bold", color=NAVY, y=1.02)
plt.tight_layout()
plt.savefig("./v3_lib3_seaborn.png", dpi=150, bbox_inches="tight")
plt.show()
print("✅ Library 3: Matplotlib + Seaborn demo complete")


# ═══════════════════════════════════════════════════════════════
# LIBRARY 4 — SCIKIT-LEARN
# "I'm an analyst, not a data scientist" — you don't need to be.
# ═══════════════════════════════════════════════════════════════
from sklearn.linear_model  import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics       import mean_absolute_error, r2_score
from sklearn.preprocessing  import StandardScaler

# ── Step 1: Build a sales prediction model ────────────────────
# Real use case: predict next month's sales from ad spend + team size

np.random.seed(42)
n = 200
ad_spend      = np.random.uniform(10000, 100000, n)
team_size     = np.random.randint(2, 20, n)
experience_yr = np.random.uniform(1, 10, n)

# Sales = real formula + noise (simulates real-world data)
sales_rev = (
    0.5 * ad_spend +
    15000 * team_size +
    8000 * experience_yr +
    np.random.normal(0, 20000, n)
)

data_ml = pd.DataFrame({
    "Ad_Spend":    ad_spend,
    "Team_Size":   team_size,
    "Experience":  experience_yr,
    "Sales":       sales_rev,
})

print("📊 Dataset for ML:")
print(data_ml.describe().round(0))

# ── Step 2: Train / Test split ────────────────────────────────
X = data_ml[["Ad_Spend", "Team_Size", "Experience"]]
y = data_ml["Sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\n📦 Train size: {len(X_train)} | Test size: {len(X_test)}")

# ── Step 3: Train a Linear Regression model ───────────────────
model = LinearRegression()
model.fit(X_train, y_train)

# ── Step 4: Evaluate ──────────────────────────────────────────
y_pred = model.predict(X_test)
mae    = mean_absolute_error(y_test, y_pred)
r2     = r2_score(y_test, y_pred)

print(f"\n🎯 Model Performance:")
print(f"   R² Score:  {r2:.3f}  ({r2*100:.1f}% of variance explained)")
print(f"   MAE:       ₹{mae:,.0f}  (avg prediction error)")

print(f"\n📊 Feature Importance (Coefficients):")
for feat, coef in zip(X.columns, model.coef_):
    print(f"   {feat:15s}: {coef:+.0f}")

# ── Step 5: Predict for a new scenario ────────────────────────
new_scenario = pd.DataFrame({
    "Ad_Spend":   [50000],
    "Team_Size":  [8],
    "Experience": [5],
})
predicted = model.predict(new_scenario)[0]
print(f"\n🔮 Prediction: Ad spend ₹50K + 8-person team + 5yr exp")
print(f"   → Predicted Sales: ₹{predicted:,.0f}")

# ── Step 6: Actual vs Predicted scatter ───────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(y_test / 1e5, y_pred / 1e5, color=PURPLE, alpha=0.6,
           s=50, edgecolors="white", linewidths=0.5, zorder=3)
perfect_line = np.linspace(y_test.min(), y_test.max(), 100) / 1e5
ax.plot(perfect_line, perfect_line, color=TEAL, linewidth=2,
        linestyle="--", label="Perfect prediction", zorder=2)
ax.set_title(f"Actual vs Predicted Sales\nR² = {r2:.3f}",
             fontsize=14, fontweight="bold", color=NAVY, pad=12)
ax.set_xlabel("Actual Sales (₹ Lakhs)", fontsize=11)
ax.set_ylabel("Predicted Sales (₹ Lakhs)", fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, zorder=1)
ax.spines[["top", "right"]].set_visible(False)

# Annotate with R² on chart
ax.text(0.05, 0.92, f"R² = {r2:.3f}\nMAE = ₹{mae/1000:.0f}K",
        transform=ax.transAxes, fontsize=10, color=TEAL,
        bbox=dict(facecolor="white", edgecolor=TEAL, boxstyle="round,pad=0.3"))

plt.tight_layout()
plt.savefig("./v3_lib4_sklearn.png", dpi=150)
plt.show()
print("✅ Library 4: Scikit-learn demo complete")


# ═══════════════════════════════════════════════════════════════
# LIBRARY 5 — SQLALCHEMY
# Every real job has a database. This is how Python talks to it.
# ═══════════════════════════════════════════════════════════════
from sqlalchemy import create_engine, text

# ── Step 1: Create an in-memory SQLite database ───────────────
# (In real job: replace 'sqlite:///:memory:' with your DB connection string)
#
# PostgreSQL:  postgresql://user:password@localhost:5432/dbname
# MySQL:       mysql+pymysql://user:password@localhost/dbname
# SQL Server:  mssql+pyodbc://user:password@server/db?driver=ODBC+Driver+17
# Oracle:      oracle+cx_oracle://user:password@host:1521/dbname

engine = create_engine("sqlite:///:memory:", echo=False)
print("✅ Database connection created (SQLite in-memory)")

# ── Step 2: Load a DataFrame directly INTO the database ───────
df.to_sql("sales", engine, if_exists="replace", index=False)
print(f"✅ {len(df)} rows written to 'sales' table")

# ── Step 3: Query with SQL — exactly like you do at work ───────
query_1 = """
    SELECT
        Region,
        Product,
        COUNT(*)         AS Num_Deals,
        SUM(Sales)       AS Total_Sales,
        AVG(Sales)       AS Avg_Sale,
        MAX(Sales)       AS Best_Deal
    FROM sales
    GROUP BY Region, Product
    ORDER BY Total_Sales DESC
    LIMIT 10
"""
result_1 = pd.read_sql(query_1, engine)
print("\n📊 SQL Query Result — Top 10 Region × Product combinations:")
print(result_1.to_string(index=False))

# ── Step 4: More realistic query — monthly trend ───────────────
query_2 = """
    SELECT
        SUBSTR(Date, 1, 7)   AS Month,
        SUM(Sales)           AS Monthly_Sales,
        COUNT(*)             AS Num_Transactions,
        ROUND(AVG(Sales), 0) AS Avg_Transaction
    FROM sales
    GROUP BY Month
    ORDER BY Month
"""
monthly = pd.read_sql(query_2, engine)
print("\n📅 Monthly Sales Trend from SQL:")
print(monthly.to_string(index=False))

# ── Step 5: Plot monthly trend from SQL result ─────────────────
fig, ax = plt.subplots(figsize=(11, 5))
ax.fill_between(range(len(monthly)), monthly["Monthly_Sales"] / 1000,
                alpha=0.15, color=TEAL)
ax.plot(range(len(monthly)), monthly["Monthly_Sales"] / 1000,
        color=TEAL, linewidth=2.5, marker="o", markersize=5, zorder=3)

ax.set_xticks(range(len(monthly)))
ax.set_xticklabels(monthly["Month"], rotation=45, ha="right", fontsize=9)
ax.set_title("Monthly Sales — Queried Directly from SQL Database",
             fontsize=14, fontweight="bold", color=NAVY, pad=14)
ax.set_xlabel("Month", fontsize=11)
ax.set_ylabel("Sales (₹ Thousands)", fontsize=11)
ax.grid(axis="y", zorder=1)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("./v3_lib5_sqlalchemy.png", dpi=150)
plt.show()
print("✅ Library 5: SQLAlchemy demo complete")


# ═══════════════════════════════════════════════════════════════
# SUMMARY — The 5 Libraries Cheat Sheet
# ═══════════════════════════════════════════════════════════════
print("""
╔══════════════════════════════════════════════════════════════╗
║   5 Python Libraries Every Analyst Actually Uses at Work     ║
╠══════════════════════════════════════════════════════════════╣
║  1. Pandas       → Load, clean, filter, groupby, pivot       ║
║  2. NumPy        → Fast number-crunching, statistics         ║
║  3. Matplotlib   → Full chart control & customisation        ║
║     + Seaborn    → Beautiful stats charts in one line        ║
║  4. Scikit-learn → Regression, classification, clustering    ║
║  5. SQLAlchemy   → Connect Python to any database            ║
╠══════════════════════════════════════════════════════════════╣
║  Install all:                                                ║
║  pip install pandas numpy matplotlib seaborn scikit-learn    ║
║               sqlalchemy                                     ║
╚══════════════════════════════════════════════════════════════╝
""")
