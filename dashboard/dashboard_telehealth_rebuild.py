"""
Medicare Telehealth Fraud and Utilization Analytics
REBUILD V3 Dashboard

Reads exclusively from REBUILD/results/*.csv and *.json.
No hardcoded analytical values. Every number on the page traces to a notebook cell.

Run with:
    streamlit run dashboard_telehealth_rebuild.py
"""
import json
from pathlib import Path

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================================
# Configuration
# ============================================================================

st.set_page_config(
    page_title="Medicare Telehealth Anomaly Analytics",
    page_icon=":hospital:",
    layout="wide",
)

# Path to REBUILD/results. Edit this if running from a different working directory.
RESULTS = Path(__file__).resolve().parent.parent / "results"
FIGURES = Path(__file__).resolve().parent.parent / "figures"


@st.cache_data
def load_all():
    """Load every persisted result file once."""
    data = {}
    data["universe"] = pd.read_csv(RESULTS / "scored_universe_2023.csv", dtype={"Rndrng_NPI": str})
    data["flagged"] = pd.read_csv(RESULTS / "flagged_providers_2023.csv", dtype={"Rndrng_NPI": str})
    data["state_excess"] = pd.read_csv(RESULTS / "per_state_excess_2023.csv")
    data["bootstrap"] = pd.read_csv(RESULTS / "bootstrap.csv")
    data["tier"] = pd.read_csv(RESULTS / "tier_distribution.csv")
    data["permutation"] = pd.read_csv(RESULTS / "permutation_importance.csv")
    data["threshold"] = pd.read_csv(RESULTS / "threshold_sensitivity.csv")
    data["typology"] = pd.read_csv(RESULTS / "fraud_typology.csv")
    data["temporal"] = pd.read_csv(RESULTS / "temporal_holdout.csv").iloc[0].to_dict()
    data["tmedtrend"] = pd.read_csv(RESULTS / "tmedtrend_national.csv")
    data["state_baselines"] = pd.read_csv(RESULTS / "state_baselines.csv")
    data["leie"] = pd.read_csv(RESULTS / "leie_concordance.csv")
    data["projection"] = json.load(open(RESULTS / "projection_methodology.json"))
    data["run_info"] = json.load(open(RESULTS / "RUN_INFO.json"))
    data["summary"] = json.load(open(RESULTS / "UNIFIED_RESULTS_SUMMARY.json"))
    return data


D = load_all()
u = D["universe"]
flagged = D["flagged"]


# ============================================================================
# Section 1: Header
# ============================================================================

st.title("Medicare Telehealth Anomaly Analytics")
st.markdown(
    "**Methodology framing:** Anomaly detection and risk stratification of Medicare telehealth billing patterns. "
    "**Not** a supervised fraud classifier. Anomaly scores indicate statistical deviation from peer billing patterns. "
    "Investigative review by appropriate authorities required before any inference."
)
st.caption(
    f"Author: {D['run_info']['principal_investigator']}  |  Version: {D['run_info']['version']}  |  "
    f"Run timestamp: {D['run_info']['run_timestamp_utc']}"
)


# ============================================================================
# Section 2: Methodology warning callout
# ============================================================================

st.info(
    "Risk scores in this dashboard are anomaly scores, not fraud probabilities. "
    "A high score indicates statistical deviation from peer billing patterns within the 2023 telehealth analytical universe. "
    "Flagged providers warrant investigative review by appropriate authorities. The system does not make fraud determinations."
)


# ============================================================================
# Section 3: Headline metrics
# ============================================================================

st.header("Headline Metrics: 2023 Telehealth Analytical Universe")
h = D["summary"]["headline_metrics"]
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Active telehealth providers", f"{h['T001_active_telehealth_providers_2023']:,}")
    st.caption("Unique NPIs in 2023 HCPCS-filtered universe")
with c2:
    st.metric("Flagged providers (top 5%)", f"{h['T005_flagged_providers_top_5pct']:,}")
    st.caption("Combined Risk Score >= 95th percentile")
with c3:
    st.metric("Sample excess billing", f"${h['T006_sample_excess_billing_usd']/1e6:.1f}M")
    st.caption(f"95% CI: ${h['T007_bootstrap_ci_low']/1e6:.1f}M to ${h['T008_bootstrap_ci_high']/1e6:.1f}M")
with c4:
    st.metric("Projected national excess", f"${h['T010_projected_national_excess_usd']/1e6:.1f}M")
    st.caption(f"Coverage multiplier: {h['T009_coverage_multiplier']:.2f}x (no recovery rate applied)")


# ============================================================================
# Section 4: Top outlier callout
# ============================================================================

st.subheader("Highest-Excess Flagged Provider")
top1 = flagged.iloc[0]
st.warning(
    f"**{top1['Last_Name']}** ({top1['State']}, {top1['Provider_Type']}): "
    f"${top1['Excess_Billing']/1e6:.2f}M sample excess. "
    f"Telehealth services: {int(top1['Telehealth_Services_Total']):,}. "
    f"Beneficiaries: {int(top1['Telehealth_Benes_Max']):,}. "
    f"Combined Risk Score: {top1['Combined_Risk_Score']:.1f}. "
    f"Caveat: anomalous billing pattern warrants investigative review; not a fraud determination."
)


# ============================================================================
# Section 5: Risk tier distribution
# ============================================================================

st.header("Risk Tier Distribution")
tier_order = ["Low", "Medium", "High", "Critical", "Extreme"]
t = D["tier"].set_index("Tier").reindex(tier_order).reset_index()
fig = px.bar(
    t,
    x="Tier",
    y="count",
    color="Tier",
    color_discrete_sequence=["#5A9CD8", "#94B95C", "#D8A03A", "#D8633A", "#A6192E"],
    log_y=True,
    title="Provider Count by Risk Tier (log scale)",
)
fig.update_layout(showlegend=False, height=400)
st.plotly_chart(fig, use_container_width=True)

tier_def = pd.DataFrame(
    {
        "Tier": tier_order,
        "Percentile cutpoint": ["<80", "80 to 95", "95 to 99", "99 to 99.9", ">=99.9"],
        "Count": t["count"].astype(int).tolist(),
        "Action posture": [
            "Standard monitoring",
            "Quarterly review",
            "Priority investigative review",
            "Immediate investigative review",
            "Highest priority investigative review",
        ],
    }
)
st.dataframe(tier_def, use_container_width=True, hide_index=True)


# ============================================================================
# Section 6: Per-state excess billing
# ============================================================================

st.header("Per-State Sample Excess Billing")
top_states = D["state_excess"].head(15)
fig = px.bar(
    top_states,
    x="Excess_Millions",
    y="State",
    orientation="h",
    color="Excess_Millions",
    color_continuous_scale="YlOrRd",
    title="Top 15 States by Flagged Provider Excess Billing ($ millions)",
    text="Excess_Millions",
    hover_data=["Flagged_Providers", "Total_Payment", "Beneficiaries_Served"],
)
fig.update_traces(texttemplate="$%{text:.1f}M", textposition="outside")
fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=550)
st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# Section 7: Permutation feature importance
# ============================================================================

st.header("Permutation Feature Importance")
st.caption(
    "Measured contributions of each ML feature to the Isolation Forest anomaly score. "
    "Computed by shuffling each feature column, recomputing anomaly scores, and measuring drop in Spearman rank correlation with original scores. "
    "Averaged across 5 repeats. Replaces fabricated importance tables from prior artifacts."
)
imp = D["permutation"].sort_values("Importance_Pct", ascending=True)
fig = px.bar(
    imp,
    x="Importance_Pct",
    y="Feature",
    orientation="h",
    title="Permutation Feature Importance (% contribution)",
    text="Importance_Pct",
    color_discrete_sequence=["#0F6E7E"],
)
fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig.update_layout(height=400, showlegend=False)
st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# Section 8: Validation suite
# ============================================================================

st.header("Validation Suite")
v1, v2, v3 = st.columns(3)
with v1:
    st.subheader("Temporal Holdout")
    st.metric("Coverage", f"{D['temporal']['holdout_coverage_pct']:.1f}%")
    st.caption(
        f"Of {int(D['temporal']['training_flagged_npis']):,} NPIs flagged in 2021+2022 pool, "
        f"{int(D['temporal']['training_flagged_present_in_2023_holdout']):,} reappear in 2023 holdout."
    )
    st.metric("Mean lift", f"{D['temporal']['mean_lift_ratio']:.2f}x")
    st.caption(
        f"Flagged carryover mean Payment/Bene: ${D['temporal']['flagged_carryover_mean_payment_per_bene']:.0f} "
        f"vs population mean ${D['temporal']['population_mean_payment_per_bene']:.0f}"
    )
    st.metric("Median lift", f"{D['temporal']['median_lift_ratio']:.2f}x")

with v2:
    st.subheader("OIG LEIE Concordance")
    st.metric("Direct NPI matches in flagged set", f"{D['summary']['validation_suite']['T039_leie_direct_match_count_flagged']}")
    st.caption("LEIE entities billed Medicare while excluded. Direct NPI match.")
    st.metric("Fuzzy name matches (top 100)", f"{len(D['leie'])}")
    st.caption("Top 100 flagged providers against LEIE business and individual names at 0.85 SequenceMatcher threshold. Most fuzzy matches are common-name coincidences.")
    st.info(
        "Honest framing: LEIE concordance is a name-pattern surveillance signal, not a fraud probability validation. "
        "Excluded providers are by definition barred from billing Medicare."
    )

with v3:
    st.subheader("Bootstrap CI (n=1000)")
    bs = D["bootstrap"]
    st.metric("Sample excess mean", f"${bs['sample_excess'].mean()/1e6:.1f}M")
    st.metric("95% CI low", f"${bs['sample_excess'].quantile(0.025)/1e6:.1f}M")
    st.metric("95% CI high", f"${bs['sample_excess'].quantile(0.975)/1e6:.1f}M")
    st.caption(f"Flagged count CI: [{int(bs['flagged_count'].quantile(0.025))}, {int(bs['flagged_count'].quantile(0.975))}]")


# ============================================================================
# Section 9: Fraud typology
# ============================================================================

st.header("Telehealth Fraud Typology Pattern Alignment")
typology = D["typology"]
typology_cols = [
    "T1_Extreme_PaymentPerBene",
    "T2_Audio_Only_Heavy",
    "T3_Single_HCPCS_Dominant",
    "T4_Rural_HighVolume",
    "T5_Pandemic_Emergence",
]
typology_descs = {
    "T1_Extreme_PaymentPerBene": "Payment per beneficiary > 10x state median",
    "T2_Audio_Only_Heavy": "Audio-only services > 80% of telehealth volume",
    "T3_Single_HCPCS_Dominant": "Telehealth HCPCS diversity <= 1 (single-code dominance)",
    "T4_Rural_HighVolume": "Rural RUCA (8-10) and > 5,000 telehealth services",
    "T5_Pandemic_Emergence": "No 2019 telehealth presence and > 1,000 services in 2023",
}
typology_df = pd.DataFrame(
    {
        "Typology": [c.replace("T", "Pattern ").replace("_", " ") for c in typology_cols],
        "Description": [typology_descs[c] for c in typology_cols],
        "Flagged Count": [int(typology[c].sum()) for c in typology_cols],
        "% of Flagged Set": [f"{typology[c].sum()/len(typology)*100:.1f}%" for c in typology_cols],
    }
)
st.dataframe(typology_df, use_container_width=True, hide_index=True)


# ============================================================================
# Section 10: Threshold sensitivity
# ============================================================================

st.header("Threshold Sensitivity")
sens = D["threshold"]
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=sens["Percentile_Threshold"],
        y=sens["Flagged_Count"],
        mode="lines+markers",
        name="Flagged count",
        yaxis="y1",
        line=dict(color="#1F3A68", width=3),
        marker=dict(size=10),
    )
)
fig.add_trace(
    go.Scatter(
        x=sens["Percentile_Threshold"],
        y=sens["Sample_Excess"] / 1e6,
        mode="lines+markers",
        name="Sample excess ($M)",
        yaxis="y2",
        line=dict(color="#A6192E", width=3),
        marker=dict(size=10),
    )
)
fig.add_vline(x=95, line_dash="dash", line_color="gray", annotation_text="Chosen cutoff: 95")
fig.update_layout(
    title="Flagged Count and Sample Excess by Percentile Threshold",
    xaxis_title="Percentile Threshold",
    yaxis=dict(title="Flagged Provider Count", side="left", color="#1F3A68"),
    yaxis2=dict(title="Sample Excess ($M)", side="right", overlaying="y", color="#A6192E"),
    height=500,
)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(sens, use_container_width=True, hide_index=True)


# ============================================================================
# Section 11: Top 10 outliers detail
# ============================================================================

st.header("Top 10 Flagged Providers by Excess Billing")
top10 = flagged.head(10)[
    [
        "Rndrng_NPI",
        "Last_Name",
        "First_Name",
        "State",
        "Provider_Type",
        "Telehealth_Services_Total",
        "Telehealth_Benes_Max",
        "Telehealth_Payment_Total",
        "Payment_Per_Bene",
        "Combined_Risk_Score",
        "Tier",
        "Excess_Billing",
    ]
].copy()
top10.columns = [
    "NPI",
    "Last/Org Name",
    "First Name",
    "State",
    "Provider Type",
    "Services",
    "Beneficiaries",
    "Payment ($)",
    "Payment/Bene ($)",
    "Risk Score",
    "Tier",
    "Excess ($)",
]
st.dataframe(top10, use_container_width=True, hide_index=True)


# ============================================================================
# Section 12: Federal source citations
# ============================================================================

st.header("Federal Source Citations")
st.markdown(
    """
- **CMS Medicare Physician and Other Practitioners by Provider and Service** (2019 to 2023 public use files): primary analytical input
- **CMS Medicare Telehealth Trends Public File** (TMEDTREND_PUBLIC_250522): national telehealth utilization context
- **HHS-OIG List of Excluded Individuals/Entities** (LEIE Database): exclusion concordance
- **HHS-OIG OEI-02-20-00720** (Telehealth Program Integrity Risk Report)
- **DOJ Healthcare Fraud Strike Force June 2025 Takedown** ($14.6B, 324 defendants)
- **GAO 23-106203** High Risk Series: Medicare program integrity
- **CMS FY 2024 Improper Payments Fact Sheet**: baseline magnitude reference
"""
)


# ============================================================================
# Section 13: Reproducibility footer
# ============================================================================

st.header("Reproducibility Envelope")
with st.expander("View RUN_INFO.json (full reproducibility envelope)"):
    st.json(D["run_info"])

st.caption(
    f"Analytical universe: providers billing any of {len(D['run_info']['telehealth_hcpcs_basket'])} telehealth HCPCS codes "
    f"in 2023 with Tot_Benes >= 11 and Avg_Mdcr_Pymt_Amt > 0. "
    f"Random seed: 42. Bootstrap iterations: {D['run_info']['parameters']['bootstrap_iterations']}. "
    f"Permutation repeats: {D['run_info']['parameters']['permutation_repeats']}. "
    f"All numbers on this page trace to a notebook cell and persisted result file."
)
