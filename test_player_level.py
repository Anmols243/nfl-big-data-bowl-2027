import unittest

import polars as pl

from player_level import aggregate_players


class PlayerLevelTest(unittest.TestCase):
    def test_keeps_fastest_attempt_and_normalizes_career_counts(self):
        attempts = pl.DataFrame({
            "nfl_id": [1, 1, 2, 2], "draft_year": [2023, 2023, 2025, 2025],
            "event_id": ["a", "a", "b", "b"], "attempt": [1, 2, 1, 2],
            "time_40yd_s": [4.8, 4.6, None, 4.7],
            "time_10yd_s": [1.5, 1.7, 1.4, 1.8],
            "extrapolated": [False, True, False, False],
        })
        results = pl.DataFrame({
            "nfl_id": [1, 2], "draft_year": [2023, 2025],
            "combine_position": ["DB", "WR"], "forty": [4.5, 4.8],
        })
        career = pl.DataFrame({
            "nfl_id": [1, 2], "career_games_active": [30, 10],
            "career_games_started": [12, 3], "pro_bowl_original_ballot": [1, 0],
            "ap_all_pro_1st_team": [1, 0], "ap_all_pro_2nd_team": [1, 0],
        })
        plays = pl.DataFrame({"nfl_id": [1], "play_count": [7]})
        got = aggregate_players(attempts, results, career, plays)
        self.assertEqual(got.select(
            "nfl_id", "attempt", "time_10yd_s", "extrapolated", "seasons",
            "games_played_per_season", "games_started_per_season",
            "pro_bowls", "all_pros", "play_count",
        ).rows(), [
            (1, 2, 1.7, True, 3, 10.0, 4.0, 1, 2, 7),
            (2, 2, 1.8, False, 1, 10.0, 3.0, 0, 0, None),
        ])
        incomplete = attempts.with_columns(
            pl.when(pl.col("nfl_id") == 2).then(None).otherwise(pl.col("time_40yd_s"))
            .alias("time_40yd_s")
        )
        self.assertEqual(
            aggregate_players(incomplete, results, career, plays)
            .filter(pl.col("nfl_id") == 2).select("attempt", "time_10yd_s", "extrapolated", "forty").row(0),
            (None, None, None, 4.8),
        )
