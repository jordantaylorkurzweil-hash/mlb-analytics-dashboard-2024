import streamlit as st
import pybaseball as pb

pb.cache.enable()


@st.cache_data(ttl=3600, show_spinner=False)
def load_pitching_stats(season: int, qual: int = 50):
    df = pb.pitching_stats(season, qual=qual)
    for col in ["K%", "BB%"]:
        if col in df.columns and df[col].max() > 1.5:
            df[col] = df[col] / 100
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def load_batting_stats(season: int, qual: int = 150):
    df = pb.batting_stats(season, qual=qual)
    for col in ["K%", "BB%"]:
        if col in df.columns and df[col].max() > 1.5:
            df[col] = df[col] / 100
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def load_team_pitching(season: int):
    return pb.team_pitching(season)


@st.cache_data(ttl=3600, show_spinner=False)
def load_team_batting(season: int):
    return pb.team_batting(season)
