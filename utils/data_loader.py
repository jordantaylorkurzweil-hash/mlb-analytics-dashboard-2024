import time
import streamlit as st
import pybaseball as pb
import pandas as pd

pb.cache.enable()


def _retry(func, *args, retries=3, delay=5, **kwargs):
    """Call func(*args, **kwargs) with automatic retries on HTTP errors."""
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e


@st.cache_data(ttl=3600, show_spinner=False)
def load_pitching_stats(season: int, qual: int = 50) -> pd.DataFrame:
    df = _retry(pb.pitching_stats, season, qual=qual)
    for col in ["K%", "BB%"]:
        if col in df.columns and df[col].max() > 1.5:
            df[col] = df[col] / 100
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def load_batting_stats(season: int, qual: int = 150) -> pd.DataFrame:
    df = _retry(pb.batting_stats, season, qual=qual)
    for col in ["K%", "BB%"]:
        if col in df.columns and df[col].max() > 1.5:
            df[col] = df[col] / 100
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def load_team_pitching(season: int) -> pd.DataFrame:
    return _retry(pb.team_pitching, season)


@st.cache_data(ttl=3600, show_spinner=False)
def load_team_batting(season: int) -> pd.DataFrame:
    return _retry(pb.team_batting, season)
