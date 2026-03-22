import streamlit as st
import pandas as pd
from utils.data_loader import load_pitching_stats, load_batting_stats, load_team_pitching, load_team_batting
from utils.charts import (
    plot_era_fip_xfip,
    plot_k_bb,
    plot_war_leaderboard_pitchers,
    plot_hitter_ops_wrc,
    plot_hitter_k_bb,
    plot_hitter_war_leaderboard,
    plot_hitter_exit_velo,
    plot_team_era_fip,
    plot_team_batting,
)
from utils.projections import compute_war_projections, flag_regression_candidates

st.set_page_config(
    page_title="MLB Analytics Dashboard 2024",
    page_icon="baseball",
    layout="wide",
)

st.title("MLB Analytics Dashboard 2024")
st.markdown("Interactive sabermetrics dashboard built with pybaseball, Plotly, and Streamlit.")

# Sidebar
with st.sidebar:
    st.header("Filters")
    season = st.selectbox("Season", options=[2024, 2023, 2022], index=0)
    min_ip = st.slider("Min IP (Pitchers)", min_value=10, max_value=150, value=50, step=5)
    min_pa = st.slider("Min PA (Hitters)", min_value=50, max_value=500, value=150, step=25)
    player_search = st.text_input("Player name search", placeholder="e.g. Gerrit Cole")
    team_list = [
        "All", "ARI", "ATL", "BAL", "BOS", "CHC", "CWS", "CIN", "CLE",
        "COL", "DET", "HOU", "KC", "LAA", "LAD", "MIA", "MIL", "MIN",
        "NYM", "NYY", "OAK", "PHI", "PIT", "SD", "SEA", "SF", "STL",
        "TB", "TEX", "TOR", "WSH",
    ]
    team_filter = st.selectbox("Team", options=team_list, index=0)
    metric_options_pitch = ["ERA", "FIP", "xFIP", "K%", "BB%", "WAR", "WHIP"]
    selected_pitch_metric = st.selectbox("Pitcher highlight metric", options=metric_options_pitch)
    metric_options_hit = ["OPS", "wRC+", "K%", "BB%", "WAR", "AVG", "SLG"]
    selected_hit_metric = st.selectbox("Hitter highlight metric", options=metric_options_hit)

def apply_filters(df, name_col="Name", team_col="Team"):
    if player_search:
        df = df[df[name_col].str.contains(player_search, case=False, na=False)]
    if team_filter != "All" and team_col in df.columns:
        df = df[df[team_col] == team_filter]
    return df

with st.spinner("Loading data..."):
    pitch_df = load_pitching_stats(season, qual=min_ip)
    bat_df = load_batting_stats(season, qual=min_pa)
    team_p = load_team_pitching(season)
    team_b = load_team_batting(season)

pitch_df = apply_filters(pitch_df)
bat_df = apply_filters(bat_df)

tab_pitch, tab_hit, tab_team, tab_war, tab_alerts = st.tabs(
    ["Pitching", "Hitting", "Teams", "WAR Leaders", "Regression Alerts"]
)

with tab_pitch:
    st.subheader(f"Pitcher Dashboard - {season}")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_era_fip_xfip(pitch_df), use_container_width=True)
    with col2:
        st.plotly_chart(plot_k_bb(pitch_df), use_container_width=True)
    st.plotly_chart(plot_war_leaderboard_pitchers(pitch_df), use_container_width=True)
    with st.expander("Raw pitcher data"):
        cols = [c for c in ["Name", "Team", "IP", "ERA", "FIP", "xFIP", "K%", "BB%", "WAR"] if c in pitch_df.columns]
        st.dataframe(pitch_df[cols].sort_values("WAR", ascending=False).reset_index(drop=True), use_container_width=True)

with tab_hit:
    st.subheader(f"Hitter Dashboard - {season}")
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
        cols = [c for c in ["Name", "Team", "PA", "AVG", "OBP", "SLG", "OPS", "wRC+", "K%", "BB%", "WAR"] if c in bat_df.columns]
        st.dataframe(bat_df[cols].sort_values("WAR", ascending=False).reset_index(drop=True), use_container_width=True)

with tab_team:
    st.subheader(f"Team Dashboard - {season}")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_team_era_fip(team_p), use_container_width=True)
    with col2:
        st.plotly_chart(plot_team_batting(team_b), use_container_width=True)

with tab_war:
    st.subheader(f"WAR Leaders & 2025 Projections")
    proj_df = compute_war_projections(bat_df, pitch_df)
    st.dataframe(proj_df.sort_values("proj_WAR_2025", ascending=False).head(40).reset_index(drop=True), use_container_width=True)

with tab_alerts:
    st.subheader("ERA-FIP Regression Alert System")
    st.markdown("Flags pitchers where |ERA - FIP| > 0.75")
    alerts_df = flag_regression_candidates(pitch_df, threshold=0.75)
    if alerts_df.empty:
        st.success("No regression candidates found with current filters.")
    else:
        def highlight_direction(row):
            color = "#d4edda" if row["ERA_minus_FIP"] > 0 else "#f8d7da"
            return [f"background-color: {color}"] * len(row)
        styled = alerts_df.style.apply(highlight_direction, axis=1)
        st.dataframe(styled, use_container_width=True)
        st.markdown("**Green** = ERA > FIP: pitcher likely to improve. **Red** = ERA < FIP: pitcher likely to decline.")
