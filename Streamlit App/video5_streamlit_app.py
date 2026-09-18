"""
@DataViz-Wiz — Video 5
Interactive Dashboard in 30 Lines of Python (Streamlit)
========================================================

Run this with: streamlit run video5_streamlit_app.py

Dashboard features:
- Real-time data filtering
- Interactive widgets (slider, multiselect, radio)
- Dynamic charting
- Automatic updates
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ─────────────────────────────────────────────────────────────
# LINE 1-3: Setup Streamlit page config
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="EV Sales Dashboard", layout="wide")

# Brand colors
TEAL = "#00C4A0"
PURPLE = "#7B5EA7"
NAVY = "#0A0A2E"

# ─────────────────────────────────────────────────────────────
# LINE 4-8: Create dataset (same as Video 4)
# ─────────────────────────────────────────────────────────────
years = list(range(2010, 2024))
data_dict = {
    "Tesla": [0.2, 0.5, 1.2, 2.6, 5.1, 12.5, 24.5, 36.7, 49.0, 66.0, 81.5, 77.2, 86.4, 95.0],
    "BYD": [0.1, 0.3, 0.8, 1.5, 2.9, 6.0, 10.2, 19.3, 32.8, 59.3, 74.6, 101.2, 120.5, 130.0],
    "Volkswagen": [0.0, 0.2, 0.6, 1.8, 3.9, 8.2, 15.6, 22.1, 27.4, 31.2, 35.8, 41.0, 48.2, 52.0],
    "Li Auto": [0.0, 0.0, 0.0, 0.0, 0.2, 1.4, 5.8, 13.8, 29.5, 38.2, 42.6, 48.0, 52.3, 55.0],
    "BMW": [0.0, 0.1, 0.4, 1.1, 2.3, 5.0, 9.8, 14.2, 18.5, 21.0, 24.7, 27.5, 30.2, 32.0],
    "Geely": [0.0, 0.0, 0.0, 0.3, 0.7, 1.6, 3.5, 7.2, 13.4, 18.6, 21.8, 25.0, 28.5, 31.0],
    "Hyundai": [0.0, 0.0, 0.0, 0.0, 0.1, 0.6, 2.8, 7.4, 14.0, 22.5, 29.1, 33.5, 38.9, 42.0],
    "Nissan": [0.0, 0.0, 0.1, 0.8, 2.4, 5.1, 8.9, 12.3, 14.1, 15.2, 14.8, 13.5, 12.1, 11.0],
}
df = pd.DataFrame(data_dict, index=years).T

# ─────────────────────────────────────────────────────────────
# LINE 9-12: Page title + description
# ─────────────────────────────────────────────────────────────
st.title("🔋 Global EV Sales Dashboard")
st.markdown("**Interactive exploration of electric vehicle sales (2010-2023)**")
st.markdown("Real-time filtering • Dynamic charts • No coding skills needed to use")

# ─────────────────────────────────────────────────────────────
# LINE 13-18: Sidebar controls (3 widgets)
# ─────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Controls")

# Widget 1: Year range slider
year_range = st.sidebar.slider(
    "📅 Select year range",
    min_value=2010, max_value=2023, value=(2015, 2023),
    step=1
)

# Widget 2: Maker multiselect
selected_makers = st.sidebar.multiselect(
    "🏭 Select makers",
    options=df.index.tolist(),
    default=["Tesla", "BYD", "Volkswagen"]
)

# Widget 3: Chart type radio button
chart_type = st.sidebar.radio(
    "📊 Chart type",
    options=["Line Chart", "Bar Chart", "Area Chart"],
    index=0
)

# ─────────────────────────────────────────────────────────────
# LINE 19-22: Filter data based on widgets
# ─────────────────────────────────────────────────────────────
filtered_df = df.loc[selected_makers, year_range[0]:year_range[1]]

# ─────────────────────────────────────────────────────────────
# LINE 23-33: Render chart (dynamic based on selection)
# ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))

if chart_type == "Line Chart":
    for maker in filtered_df.index:
        ax.plot(filtered_df.columns, filtered_df.loc[maker], marker="o", linewidth=2, label=maker)

elif chart_type == "Bar Chart":
    filtered_df.T.plot(kind="bar", ax=ax, width=0.8)

else:  # Area Chart
    ax.stackplot(filtered_df.columns, filtered_df.values, labels=filtered_df.index, alpha=0.7)
    ax.legend(loc="upper left")

ax.set_xlabel("Year", fontsize=11, fontweight="bold")
ax.set_ylabel("EV Sales (Millions)", fontsize=11, fontweight="bold")
ax.set_title(f"EV Sales Trend ({chart_type})", fontsize=13, fontweight="bold", color=NAVY)
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

st.pyplot(fig)

# ─────────────────────────────────────────────────────────────
# LINE 34-38: Display stats
# ─────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📈 Quick Stats")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total = filtered_df.sum().sum()
    st.metric("Total Sales", f"{total:.0f}M", delta=f"+{total/len(filtered_df.columns):.1f}M/yr")

with col2:
    leader = filtered_df.sum(axis=1).idxmax()
    leader_val = filtered_df.sum(axis=1).max()
    st.metric("Leader", leader, f"{leader_val:.0f}M")

with col3:
    latest_year = filtered_df.columns[-1]
    growth = ((filtered_df[latest_year] - filtered_df[filtered_df.columns[0]]) / filtered_df[filtered_df.columns[0]] * 100).mean()
    st.metric("Avg Growth", f"{growth:.0f}%", delta="vs 2010")

with col4:
    num_makers = len(selected_makers)
    st.metric("Makers", num_makers, delta=f"{num_makers} selected")

# ─────────────────────────────────────────────────────────────
# LINE 39-42: Data table
# ─────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📊 Data Table")
st.dataframe(filtered_df.T.round(1), use_container_width=True)

# ─────────────────────────────────────────────────────────────
# LINE 43-45: Footer
# ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("**Built with Streamlit** • Data: EV Sales 2010-2023 • @DataViz-Wiz")
