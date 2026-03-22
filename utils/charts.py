import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def plot_era_fip_xfip(df: pd.DataFrame, top_n: int = 30) -> go.Figure:
    plot_df = df.nlargest(top_n, "WAR")[["Name", "ERA", "FIP", "xFIP"]].melt(
        id_vars="Name", var_name="Metric", value_name="Value"
    )
    fig = px.bar(
        plot_df, x="Name", y="Value", color="Metric", barmode="group",
        title=f"ERA vs FIP vs xFIP - Top {top_n} Starters by WAR",
        color_discrete_map={"ERA": "#003087", "FIP": "#E31937", "xFIP": "#FDB827"},
    )
    fig.update_layout(xaxis_tickangle=-45, height=450)
    return fig


def plot_k_bb(df: pd.DataFrame, top_n: int = 30) -> go.Figure:
    plot_df = df.nlargest(top_n, "WAR")
    fig = px.scatter(
        plot_df, x="BB%", y="K%", text="Name", size="WAR", color="WAR",
        color_continuous_scale="Blues",
        title=f"K% vs BB% - Top {top_n} Starters by WAR",
    )
    fig.update_traces(textposition="top center", textfont_size=9)
    fig.update_layout(height=450)
    return fig


def plot_war_leaderboard_pitchers(df: pd.DataFrame, top_n: int = 20) -> go.Figure:
    plot_df = df.nlargest(top_n, "WAR").sort_values("WAR")
    fig = px.bar(
        plot_df, x="WAR", y="Name", orientation="h", color="WAR",
        color_continuous_scale="Blues",
        title=f"Pitcher WAR Leaderboard - Top {top_n}",
    )
    fig.update_layout(height=500, yaxis_title=None)
    return fig


def plot_hitter_ops_wrc(df: pd.DataFrame, top_n: int = 40) -> go.Figure:
    plot_df = df.nlargest(top_n, "WAR")
    if not {"OPS", "wRC+", "Name", "WAR"}.issubset(df.columns):
        return go.Figure().update_layout(title="Missing required columns")
    fig = px.scatter(
        plot_df, x="OPS", y="wRC+", text="Name", size="WAR", color="WAR",
        color_continuous_scale="Reds",
        title=f"OPS vs wRC+ - Top {top_n} Hitters by WAR",
    )
    fig.update_traces(textposition="top center", textfont_size=9)
    fig.update_layout(height=450)
    return fig


def plot_hitter_k_bb(df: pd.DataFrame, top_n: int = 40) -> go.Figure:
    plot_df = df.nlargest(top_n, "WAR")
    fig = px.scatter(
        plot_df, x="BB%", y="K%", text="Name", size="WAR", color="WAR",
        color_continuous_scale="Oranges",
        title=f"K% vs BB% - Top {top_n} Hitters by WAR",
    )
    fig.update_traces(textposition="top center", textfont_size=9)
    fig.update_layout(height=450)
    return fig


def plot_hitter_war_leaderboard(df: pd.DataFrame, top_n: int = 20) -> go.Figure:
    plot_df = df.nlargest(top_n, "WAR").sort_values("WAR")
    fig = px.bar(
        plot_df, x="WAR", y="Name", orientation="h", color="WAR",
        color_continuous_scale="Reds",
        title=f"Hitter WAR Leaderboard - Top {top_n}",
    )
    fig.update_layout(height=500, yaxis_title=None)
    return fig


def plot_hitter_exit_velo(df: pd.DataFrame, top_n: int = 30) -> go.Figure:
    ev_col = next((c for c in ["EV", "AvgEV", "avg_exit_velo"] if c in df.columns), None)
    if ev_col is None:
        return go.Figure().update_layout(title="Exit velocity data not available", height=350)
    plot_df = df.nlargest(top_n, ev_col).sort_values(ev_col, ascending=False)
    fig = px.bar(
        plot_df, x="Name", y=ev_col, color=ev_col,
        color_continuous_scale="YlOrRd",
        title=f"Avg Exit Velocity - Top {top_n} Hitters",
    )
    fig.update_layout(xaxis_tickangle=-45, height=400)
    return fig


def plot_team_era_fip(df: pd.DataFrame) -> go.Figure:
    if "ERA" not in df.columns or "FIP" not in df.columns:
        return go.Figure().update_layout(title="ERA/FIP columns not found")
    team_col = next((c for c in ["Team", "teamID", "team"] if c in df.columns), None)
    fig = px.scatter(df, x="FIP", y="ERA", text=team_col, title="Team ERA vs FIP")
    mn = min(df["ERA"].min(), df["FIP"].min()) - 0.1
    mx = max(df["ERA"].max(), df["FIP"].max()) + 0.1
    fig.add_shape(type="line", x0=mn, y0=mn, x1=mx, y1=mx, line=dict(color="gray", dash="dash"))
    fig.update_traces(textposition="top center")
    fig.update_layout(height=450)
    return fig


def plot_team_batting(df: pd.DataFrame) -> go.Figure:
    metric = "wRC+" if "wRC+" in df.columns else ("OPS" if "OPS" in df.columns else None)
    if metric is None:
        return go.Figure().update_layout(title="No batting metric available")
    team_col = next((c for c in ["Team", "teamID", "team"] if c in df.columns), None)
    plot_df = df.sort_values(metric, ascending=False)
    fig = px.bar(
        plot_df, x=team_col, y=metric, color=metric,
        color_continuous_scale="RdYlGn",
        title=f"Team {metric} Ranking",
    )
    fig.update_layout(xaxis_tickangle=-45, height=400)
    return fig
