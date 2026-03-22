import pandas as pd
import numpy as np

MEAN_PITCHER_WAR = 1.8
MEAN_HITTER_WAR = 2.0
PEAK_AGE = 27


def _age_factor(age: float, years_ahead: int = 1) -> float:
    future_age = age + years_ahead
    if future_age <= PEAK_AGE:
        return 1 + 0.005 * (PEAK_AGE - future_age)
    else:
        return max(0.5, 1 - 0.003 * (future_age - PEAK_AGE))


def compute_war_projections(bat_df: pd.DataFrame, pitch_df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for df, role, mean_war in [
        (bat_df, "Hitter", MEAN_HITTER_WAR),
        (pitch_df, "Pitcher", MEAN_PITCHER_WAR),
    ]:
        if "WAR" not in df.columns:
            continue
        for _, row in df.iterrows():
            name = row.get("Name", "Unknown")
            team = row.get("Team", "-")
            war = row.get("WAR", np.nan)
            age = row.get("Age", 28)
            if pd.isna(war):
                continue
            regressed_war = 0.60 * war + 0.40 * mean_war
            af = _age_factor(float(age), years_ahead=1)
            proj = round(regressed_war * af, 2)
            records.append({
                "Name": name,
                "Team": team,
                "Role": role,
                "Age": age,
                "WAR_2024": round(war, 2),
                "proj_WAR_2025": proj,
                "age_factor": round(af, 3),
            })
    return pd.DataFrame(records)


def flag_regression_candidates(pitch_df: pd.DataFrame, threshold: float = 0.75) -> pd.DataFrame:
    needed = {"ERA", "FIP", "Name"}
    if not needed.issubset(pitch_df.columns):
        return pd.DataFrame()
    df = pitch_df.copy()
    df["ERA_minus_FIP"] = (df["ERA"] - df["FIP"]).round(2)
    df["Abs_Diff"] = df["ERA_minus_FIP"].abs()
    df["Direction"] = df["ERA_minus_FIP"].apply(
        lambda x: "Likely to Improve (ERA > FIP)" if x > 0 else "Likely to Decline (ERA < FIP)"
    )
    desired_cols = ["Name", "Team", "IP", "ERA", "FIP", "xFIP", "ERA_minus_FIP", "Direction", "WAR"]
    available = [c for c in desired_cols if c in df.columns]
    alerts = (
        df[df["Abs_Diff"] >= threshold]
        .sort_values("Abs_Diff", ascending=False)[available]
        .reset_index(drop=True)
    )
    return alerts
