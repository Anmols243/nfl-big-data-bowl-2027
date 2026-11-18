"""Build the player-level cohort and report pairwise Spearman correlations."""

from collections import Counter
from pathlib import Path
from statistics import correlation

import polars as pl


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "nfl-bdb2027" / "nfl-big-data-bowl-2027"
DERIVED = ROOT / "data" / "derived"
FEATURES = [
    "time_10yd_s", "time_20yd_s", "time_40yd_s", "max_s_yd_s",
    "mean_a_first_0_5s_yd_s2", "mean_a_first_1_0s_yd_s2", "s_at_40yd_yd_s",
    "forty", "ten_yd_split",
]
SPEED_OUTCOMES = ["player_play_mean_top_speed", "player_play_max_top_speed"]
OUTCOMES = [
    "games_played_per_season", "games_started_per_season", "pro_bowls", "all_pros",
    "play_count", *SPEED_OUTCOMES,
]
PRIMARY = [
    ("time_10yd_s", "games_started_per_season"),
    ("max_s_yd_s", "player_play_max_top_speed"),
    ("time_40yd_s", "games_started_per_season"),
    ("forty", "games_started_per_season"),
]


def aggregate_players(
    attempts: pl.DataFrame, results: pl.DataFrame, career: pl.DataFrame, plays: pl.DataFrame,
) -> pl.DataFrame:
    fastest = (attempts.drop_nulls("time_40yd_s")
               .sort("nfl_id", "time_40yd_s", "event_id", "attempt")
               .unique(subset=["nfl_id"], keep="first", maintain_order=True))
    cohort = attempts.select("nfl_id", "draft_year").unique()
    return (
        cohort.join(fastest, on=["nfl_id", "draft_year"], how="left", validate="1:1")
        .join(results, on=["nfl_id", "draft_year"], how="left", validate="1:1")
        .join(career, on="nfl_id", how="left", validate="1:1")
        .join(plays, on="nfl_id", how="left", validate="1:1")
        .with_columns(seasons=2026 - pl.col("draft_year"))
        .with_columns(
            games_played_per_season=pl.col("career_games_active") / pl.col("seasons"),
            games_started_per_season=pl.col("career_games_started") / pl.col("seasons"),
            pro_bowls=pl.col("pro_bowl_original_ballot"),
            all_pros=pl.col("ap_all_pro_1st_team") + pl.col("ap_all_pro_2nd_team"),
        )
        .sort("nfl_id")
    )


def spearman(group: pl.DataFrame, feature: str, outcome: str) -> str:
    paired = group.select(feature, outcome).drop_nulls()
    x, y = paired[feature], paired[outcome]
    n = paired.height
    if n < 2 or x.n_unique() < 2 or y.n_unique() < 2:
        return f"NA (n={n})"
    rho = correlation(x.rank(method="average"), y.rank(method="average"))
    return f"{rho:.3f} (n={n})"


def report(players: pl.DataFrame, missing_play_all: int) -> str:
    groups = [("Overall", players)] + [
        (position, players.filter(pl.col("combine_position") == position))
        for position in sorted(players["combine_position"].unique())
    ]

    def table(pairs: list[tuple[str, str]]) -> str:
        header = ["Feature", "Outcome"] + [f"{label} ({g.height})" for label, g in groups]
        rows = [header, ["---"] * len(header)]
        rows.extend([f"`{x}`", f"`{y}`", *[spearman(g, x, y) for _, g in groups]] for x, y in pairs)
        return "\n".join("| " + " | ".join(row) + " |" for row in rows)

    secondary = [(x, y) for x in FEATURES for y in OUTCOMES if (x, y) not in PRIMARY]
    intro = (
        "# Player-level Spearman correlations\n\n"
        "Each cell gives Spearman rho and the pairwise complete player count. Tied values use average "
        "ranks. NA denotes too few pairs or a constant variable. Column headers give cohort sizes.\n\n"
        "The fastest derived 40-yard attempt supplies the tracking features. Ties use event ID and "
        f"attempt number. {players['attempt'].null_count()}/418 players had no timed 40-yard attempt "
        "and have blank selected-attempt fields. Games rates use career_games_active and career_games_started divided "
        "by 2026 minus draft year. Pro Bowls use the original ballot count and All-Pros sum AP first "
        "and second teams.\n\n"
        "The supplied player_play.csv has no recorded speed column. Mean and max top speed "
        "are missing for all players. Play count uses the number of supplied player-play rows. "
        f"{missing_play_all}/510 players had no player_play rows in the supplied data. "
        f"In the 418-player cohort, {players['play_count'].null_count()}/418 had no rows.\n"
    )
    return intro + "\n## Primary\n\n" + table(PRIMARY) + "\n\n## Secondary\n\n" + table(secondary) + "\n"


def main() -> None:
    attempts = pl.read_csv(DERIVED / "forty_attempt_features.csv").select(
        "nfl_id", "draft_year", "event_id", "attempt", "extrapolated", *FEATURES[:-2],
    )
    results = pl.read_csv(SOURCE / "combine_results.csv", null_values="NA").select(
        "nfl_id", "draft_year", "combine_position", "forty", "ten_yd_split",
    )
    career = pl.read_csv(SOURCE / "player_career_successes.csv", null_values="NA")
    career = career.select(
        "nfl_id", "career_games_active", "career_games_started", "pro_bowl_original_ballot",
        "ap_all_pro_1st_team", "ap_all_pro_2nd_team",
    )
    plays = (pl.scan_csv(SOURCE / "player_play.csv", null_values="NA")
             .select("nfl_id").drop_nulls().group_by("nfl_id").len(name="play_count")
             .collect(engine="streaming"))
    universe = pl.read_csv(SOURCE / "players.csv", columns=["nfl_id"])
    unrepresented = universe.join(plays, on="nfl_id", how="anti").height
    assert universe.height == 510 and unrepresented == 13
    players = aggregate_players(attempts, results, career, plays).with_columns(
        pl.lit(None, dtype=pl.Float64).alias(name) for name in SPEED_OUTCOMES
    )
    assert players.height == players["nfl_id"].n_unique() == 418
    assert players.select(
        "combine_position", "career_games_active", "career_games_started",
    ).null_count().row(0) == (0, 0, 0)
    players.write_csv(DERIVED / "player_level.csv")
    (ROOT / "player_level_correlations.md").write_text(report(players, unrepresented), encoding="utf-8")
    print(f"Rows: {players.height}. Combine positions: {dict(Counter(players['combine_position']))}.")
    print(f"Selected extrapolated attempts: {players['extrapolated'].sum()}.")
    print(f"Players without supplied play rows: {players['play_count'].null_count()}/418.")


if __name__ == "__main__":
    main()
