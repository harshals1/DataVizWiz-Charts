"""
@DataViz-Wiz — Video 6 
Interactive Sales Dashboard Every Analyst Needs (Streamlit App REady Code)
=================================================

Run this with: streamlit run video6_sales_dashboard.py

Universal use case — every analyst, in every industry, touches sales data.
Features:
- Sales pipeline data (deals, stages, reps, amounts)
- Multi-filter (stage, rep, region, date range)
- KPI metrics (revenue, win rate, avg deal size, close time)
- Funnel chart (pipeline stages)
- Rep leaderboard
- Deal size vs close probability matrix
- Export-ready
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ─────────────────────────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Sales Pipeline Dashboard", layout="wide")

TEAL = "#00C4A0"
PURPLE = "#7B5EA7"
NAVY = "#0A0A2E"
RED = "#E74C3C"
GREEN = "#2ECC71"
GOLD = "#F5A623"

# ─────────────────────────────────────────────────────────────
# SYNTHETIC SALES DATA
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_sample_data():
    np.random.seed(42)
    n = 400
    
    reps = ['Priya S.', 'Rahul K.', 'Ananya M.', 'Vikram J.', 'Sneha R.']
    stages = ['Prospecting', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    regions = ['North', 'South', 'East', 'West']
    
    df = pd.DataFrame({
        'Deal_ID': [f'DEAL_{str(i).zfill(4)}' for i in range(1, n+1)],
        'Sales_Rep': np.random.choice(reps, n),
        'Stage': np.random.choice(stages, n, p=[0.25, 0.20, 0.18, 0.12, 0.15, 0.10]),
        'Deal_Amount_Lakhs': np.random.choice([2, 5, 8, 12, 18, 25, 35, 50], n),
        'Region': np.random.choice(regions, n),
        'Days_In_Pipeline': np.random.randint(3, 120, n),
        'Close_Probability': np.random.randint(10, 95, n),
    })
    return df

# ─────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────
st.title("📈 Sales Pipeline Dashboard")
st.markdown("**Real-time deal tracking and revenue analytics**")
st.markdown("---")

df = load_sample_data()
st.info(f"✅ Loaded {len(df)} deals in pipeline")

# ─────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Filters")

stage_filter = st.sidebar.multiselect(
    "🎯 Deal Stage",
    options=df['Stage'].unique(),
    default=df['Stage'].unique()
)

rep_filter = st.sidebar.multiselect(
    "👤 Sales Rep",
    options=df['Sales_Rep'].unique(),
    default=df['Sales_Rep'].unique()
)

region_filter = st.sidebar.multiselect(
    "🌍 Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

amount_range = st.sidebar.slider(
    "💰 Deal Amount (Lakhs)",
    min_value=int(df['Deal_Amount_Lakhs'].min()),
    max_value=int(df['Deal_Amount_Lakhs'].max()),
    value=(2, 50)
)

# ─────────────────────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────────────────────
filtered_df = df[
    (df['Stage'].isin(stage_filter)) &
    (df['Sales_Rep'].isin(rep_filter)) &
    (df['Region'].isin(region_filter)) &
    (df['Deal_Amount_Lakhs'] >= amount_range[0]) &
    (df['Deal_Amount_Lakhs'] <= amount_range[1])
]

# ─────────────────────────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────────────────────────
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_pipeline = filtered_df['Deal_Amount_Lakhs'].sum()
    st.metric("Total Pipeline", f"₹{total_pipeline:.0f}L")

with col2:
    won = filtered_df[filtered_df['Stage'] == 'Closed Won']
    win_rate = (len(won) / max(len(filtered_df[filtered_df['Stage'].isin(['Closed Won','Closed Lost'])]), 1) * 100)
    st.metric("Win Rate", f"{win_rate:.0f}%")

with col3:
    avg_deal = filtered_df['Deal_Amount_Lakhs'].mean()
    st.metric("Avg Deal Size", f"₹{avg_deal:.1f}L")

with col4:
    avg_days = filtered_df['Days_In_Pipeline'].mean()
    st.metric("Avg Days in Pipeline", f"{avg_days:.0f}d")

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# FUNNEL CHART — Pipeline Stages
# ─────────────────────────────────────────────────────────────
st.subheader("🔻 Pipeline Funnel")
col1, col2 = st.columns(2)

with col1:
    stage_order = ['Prospecting', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won']
    stage_counts = filtered_df[filtered_df['Stage'].isin(stage_order)]['Stage'].value_counts().reindex(stage_order).fillna(0)
    
    fig_funnel = go.Figure(go.Funnel(
        y=stage_counts.index,
        x=stage_counts.values,
        marker={"color": [TEAL, PURPLE, GOLD, "#4EA8DE", GREEN]}
    ))
    fig_funnel.update_layout(height=400, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_funnel, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# REP LEADERBOARD
# ─────────────────────────────────────────────────────────────
with col2:
    st.markdown("**🏆 Rep Leaderboard (Closed Won)**")
    won_by_rep = filtered_df[filtered_df['Stage'] == 'Closed Won'].groupby('Sales_Rep')['Deal_Amount_Lakhs'].sum().sort_values(ascending=True)
    
    fig_leader, ax = plt.subplots(figsize=(8, 5))
    colors_bar = [TEAL if i == len(won_by_rep)-1 else PURPLE for i in range(len(won_by_rep))]
    ax.barh(won_by_rep.index, won_by_rep.values, color=colors_bar)
    ax.set_xlabel('Revenue Closed (Lakhs)', fontweight='bold', fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for i, v in enumerate(won_by_rep.values):
        ax.text(v + 0.5, i, f'₹{v:.0f}L', va='center', fontweight='bold', fontsize=9)
    st.pyplot(fig_leader, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# DEAL SIZE VS CLOSE PROBABILITY
# ─────────────────────────────────────────────────────────────
st.subheader("🎯 Deal Size vs Close Probability")
fig_scatter, ax = plt.subplots(figsize=(12, 5))

stage_colors = {'Prospecting': '#888888', 'Qualified': PURPLE, 'Proposal': GOLD,
                 'Negotiation': "#4EA8DE", 'Closed Won': GREEN, 'Closed Lost': RED}
colors = [stage_colors.get(s, '#888888') for s in filtered_df['Stage']]

ax.scatter(filtered_df['Close_Probability'], filtered_df['Deal_Amount_Lakhs'],
           c=colors, s=70, alpha=0.6, edgecolors='black', linewidth=0.4)
ax.set_xlabel('Close Probability (%)', fontweight='bold', fontsize=10)
ax.set_ylabel('Deal Amount (Lakhs)', fontweight='bold', fontsize=10)
ax.set_title('Which deals should reps prioritise?', fontweight='bold', fontsize=12, color=NAVY)
ax.grid(alpha=0.2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=c, label=s) for s, c in stage_colors.items()]
ax.legend(handles=legend_elements, loc='upper left', fontsize=8, ncol=2)

st.pyplot(fig_scatter, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# REGION BREAKDOWN
# ─────────────────────────────────────────────────────────────
st.subheader("🌍 Revenue by Region")
region_rev = filtered_df.groupby('Region')['Deal_Amount_Lakhs'].sum().sort_values(ascending=False)
fig_region = px.bar(x=region_rev.index, y=region_rev.values, color=region_rev.index,
                     color_discrete_sequence=[TEAL, PURPLE, GOLD, "#4EA8DE"])
fig_region.update_layout(height=350, showlegend=False, xaxis_title="Region", yaxis_title="Pipeline (Lakhs)")
st.plotly_chart(fig_region, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# DATA TABLE & EXPORT
# ─────────────────────────────────────────────────────────────
st.subheader("📋 Deal Details")
st.dataframe(filtered_df, use_container_width=True, height=300)

csv = filtered_df.to_csv(index=False)
st.download_button("📥 Download CSV", data=csv, file_name="sales_pipeline.csv", mime="text/csv")

st.markdown("---")
st.markdown("**Built with Streamlit • @DataViz-Wiz**")