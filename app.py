import streamlit as st
import pandas as pd
from utils.data_loader import load_pitching_stats, load_batting_stats, load_team_pitching, load_team_batting
from utils.charts import (
    plot_era_fip_xfip, plot_k_bb, plot_war_leaderboard_pitchers,
    plot_hitter_ops_wrc, plot_hitter_k_bb, plot_hitter_war_leaderboard,
    plot_hitter_exit_velo, plot_team_era_fip, plot_team_batting,
)
from utils.projections import compute_war_projections, flag_regression_candidates

st.set_page_config(
    page_title="MLB Analytics Dashboard 2024",
    page_icon="⚾",
    layout="wide",
)

st.title("MLB Analytics Dashboard 2024")
st.markdown("Interactive sabermetrics dashboard built with pybaseball, Plotly, and Streamlit.")

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    season = st.selectbox("Season", options=[2024, 2023, 2022], index=0)
    min_ip = st.slider("Min IP (Pitchers)", min_value=10, max_value=150, value=50, step=5)
    min_pa = st.slider("Min PA (Hitters)", min_value=50, max_value=500, value=150, step=25)

# ── FIX 1: Cache data loads with fixed qual=1 so sliders don't re-fetch ──────
# Sliders filter in-memory — they never trigger a new API call.
# This prevents Streamlit from re-running the full script and resetting the tab.
@st.cache_data(show_spinner=False)
def get_pitching(season):
    return load_pitching_stats(season, qual=1)

@st.cache_data(show_spinner=False)
def get_batting(season):
    return load_batting_stats(season, qual=1)

@st.cache_data(show_spinner=False)
def get_team_pitching(season):
    return load_team_pitching(season)

@st.cache_data(show_spinner=False)
def get_team_batting(season):
    return load_team_batting(season)

with st.spinner("Loading data from FanGraphs…"):
    pitch_df_raw = get_pitching(season)
    bat_df_raw   = get_batting(season)
    team_p       = get_team_pitching(season)
    team_b       = get_team_batting(season)

# ── Apply IP / PA minimums in-memory (no re-fetch) ───────────────────────────
pitch_df_raw = pitch_df_raw[pitch_df_raw["IP"] >= min_ip] if "IP" in pitch_df_raw.columns else pitch_df_raw
bat_df_raw   = bat_df_raw[bat_df_raw["PA"] >= min_pa]     if "PA" in bat_df_raw.columns  else bat_df_raw

# ── Remaining sidebar filters ─────────────────────────────────────────────────
with st.sidebar:
    player_search = st.text_input("Player name search", placeholder="e.g. Gerrit Cole")

    all_teams = sorted(
        set(pitch_df_raw["Team"].dropna().tolist()) |
        set(bat_df_raw["Team"].dropna().tolist())
    )
    team_filter = st.selectbox("Team", options=["All"] + all_teams, index=0)

    selected_pitch_metric = st.selectbox(
        "Pitcher highlight metric", options=["ERA", "FIP", "xFIP", "K%", "BB%", "WAR", "WHIP"]
    )
    selected_hit_metric = st.selectbox(
        "Hitter highlight metric", options=["OPS", "wRC+", "K%", "BB%", "WAR", "AVG", "SLG"]
    )

# ── Apply name / team filters ─────────────────────────────────────────────────
def apply_filters(df, name_col="Name", team_col="Team"):
    if player_search:
        df = df[df[name_col].str.contains(player_search, case=False, na=False)]
    if team_filter != "All" and team_col in df.columns:
        df = df[df[team_col] == team_filter]
    return df

pitch_df = apply_filters(pitch_df_raw)
bat_df   = apply_filters(bat_df_raw)

# ── KPI strip ─────────────────────────────────────────────────────────────────
if not pitch_df.empty and not bat_df.empty:
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Pitchers shown", len(pitch_df))
    k2.metric(
        f"Avg {selected_pitch_metric}",
        f"{pitch_df[selected_pitch_metric].mean():.2f}"
        if selected_pitch_metric in pitch_df.columns else "—",
    )
    k3.metric("Hitters shown", len(bat_df))
    k4.metric(
        f"Avg {selected_hit_metric}",
        f"{bat_df[selected_hit_metric].mean():.2f}"
        if selected_hit_metric in bat_df.columns else "—",
    )

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_pitch, tab_hit, tab_team, tab_war, tab_alerts = st.tabs(
    ["⚾ Pitching", "🏏 Hitting", "🏟️ Teams", "📊 WAR Leaders", "🚨 Regression Alerts"]
)

with tab_pitch:
    st.subheader(f"Pitcher Dashboard — {season}")
    if pitch_df.empty:
        st.warning("No pitchers match the current filters.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_era_fip_xfip(pitch_df), use_container_width=True)
        with col2:
            st.plotly_chart(plot_k_bb(pitch_df), use_container_width=True)
        st.plotly_chart(plot_war_leaderboard_pitchers(pitch_df), use_container_width=True)
        with st.expander("Raw pitcher data"):
            cols = [c for c in ["Name", "Team", "IP", "ERA", "FIP", "xFIP", "K%", "BB%", "WAR"]
                    if c in pitch_df.columns]
            sort_col = selected_pitch_metric if selected_pitch_metric in pitch_df.columns else "WAR"
            st.dataframe(
                pitch_df[cols].sort_values(sort_col, ascending=False).reset_index(drop=True),
                use_container_width=True,
            )

with tab_hit:
    st.subheader(f"Hitter Dashboard — {season}")
    if bat_df.empty:
        st.warning("No hitters match the current filters.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_hitter_ops_wrc(bat_df), use_container_width=True)
        with col2:
            st.plotly_chart(plot_hitter_k_bb(bat_df), use_container_width=True)
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(plot_hitter_war_leaderboard(bat_df), use_container_width=True)
        with col4:
            st.plotly_chart(plot_hitter_exit_velo(bat_df), use_container_width=True)
        with st.expander("Raw hitter data"):
            cols = [c for c in ["Name", "Team", "PA", "AVG", "OBP", "SLG", "OPS", "wRC+", "K%", "BB%", "WAR"]
                    if c in bat_df.columns]
            sort_col = selected_hit_metric if selected_hit_metric in bat_df.columns else "WAR"
            st.dataframe(
                bat_df[cols].sort_values(sort_col, ascending=False).reset_index(drop=True),
                use_container_width=True,
            )

with tab_team:
    st.subheader(f"Team Dashboard — {season}")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_team_era_fip(team_p), use_container_width=True)
    with col2:
        st.plotly_chart(plot_team_batting(team_b), use_container_width=True)

with tab_war:
    st.subheader("WAR Leaders & 2025 Projections")
    proj_df = compute_war_projections(bat_df, pitch_df)
    st.dataframe(
        proj_df.sort_values("proj_WAR_2025", ascending=False).head(40).reset_index(drop=True),
        use_container_width=True,
    )

with tab_alerts:
    st.subheader("🚨 ERA–FIP Regression Alert System")
    st.markdown(
        "Flags pitchers where **|ERA − FIP| > 0.75**. "
        "A large gap signals the pitcher's ERA is unlikely to be sustainable."
    )
    alerts_df = flag_regression_candidates(pitch_df, threshold=0.75)
    if alerts_df.empty:
        st.success("No regression candidates found with current filters.")
    else:
        # ── FIX 3: Corrected color logic and labels ───────────────────────────
        # ERA > FIP → pitcher got LUCKY (ERA looks better than underlying skills)
        #             → ERA likely to RISE = RED warning
        # ERA < FIP → pitcher got UNLUCKY (ERA looks worse than underlying skills)
        #             → ERA likely to FALL = GREEN (good news for pitcher)
        def highlight_direction(row):
            if row["ERA_minus_FIP"] > 0:
                color = "#f8d7da"  # red — ERA > FIP, likely to regress upward
            else:
                color = "#d4edda"  # green — ERA < FIP, likely to improve
            return [f"background-color: {color}"] * len(row)

        st.dataframe(
            alerts_df.style.apply(highlight_direction, axis=1),
            use_container_width=True,
        )
        st.markdown(
            "🔴 **Red** = ERA > FIP: pitcher has been **lucky** — ERA likely to **rise**. "
            "🟢 **Green** = ERA < FIP: pitcher has been **unlucky** — ERA likely to **drop**."
        )
