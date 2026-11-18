# Player-level Spearman correlations

Each cell gives Spearman rho and the pairwise complete player count. Tied values use average ranks. NA denotes too few pairs or a constant variable. Column headers give cohort sizes.

The fastest derived 40-yard attempt supplies the tracking features. Ties use event ID and attempt number. 1/418 players had no timed 40-yard attempt and have blank selected-attempt fields. Games rates use career_games_active and career_games_started divided by 2026 minus draft year. Pro Bowls use the original ballot count and All-Pros sum AP first and second teams.

The supplied player_play.csv has no recorded speed column. Mean and max top speed are missing for all players. Play count uses the number of supplied player-play rows. 13/510 players had no player_play rows in the supplied data. In the 418-player cohort, 11/418 had no rows.

## Primary

| Feature | Outcome | Overall (418) | DB (102) | DL (93) | OL (95) | TE (34) | WR (94) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `time_10yd_s` | `games_started_per_season` | -0.079 (n=417) | -0.165 (n=102) | -0.104 (n=93) | -0.196 (n=94) | 0.012 (n=34) | -0.232 (n=94) |
| `max_s_yd_s` | `player_play_max_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `time_40yd_s` | `games_started_per_season` | -0.070 (n=417) | -0.160 (n=102) | -0.115 (n=93) | -0.303 (n=94) | 0.176 (n=34) | -0.268 (n=94) |
| `forty` | `games_started_per_season` | -0.049 (n=418) | -0.122 (n=102) | -0.060 (n=93) | -0.258 (n=95) | 0.152 (n=34) | -0.225 (n=94) |

## Secondary

| Feature | Outcome | Overall (418) | DB (102) | DL (93) | OL (95) | TE (34) | WR (94) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `time_10yd_s` | `games_played_per_season` | -0.055 (n=417) | -0.109 (n=102) | -0.035 (n=93) | -0.103 (n=94) | -0.124 (n=34) | -0.054 (n=94) |
| `time_10yd_s` | `pro_bowls` | -0.036 (n=417) | 0.089 (n=102) | -0.075 (n=93) | -0.174 (n=94) | NA (n=34) | -0.031 (n=94) |
| `time_10yd_s` | `all_pros` | 0.022 (n=417) | 0.164 (n=102) | -0.031 (n=93) | 0.017 (n=94) | NA (n=34) | -0.033 (n=94) |
| `time_10yd_s` | `play_count` | -0.061 (n=406) | -0.215 (n=99) | -0.272 (n=90) | -0.306 (n=93) | -0.181 (n=31) | -0.300 (n=93) |
| `time_10yd_s` | `player_play_mean_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `time_10yd_s` | `player_play_max_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `time_20yd_s` | `games_played_per_season` | -0.069 (n=417) | -0.127 (n=102) | -0.076 (n=93) | -0.162 (n=94) | -0.054 (n=34) | -0.120 (n=94) |
| `time_20yd_s` | `games_started_per_season` | -0.074 (n=417) | -0.149 (n=102) | -0.127 (n=93) | -0.254 (n=94) | 0.146 (n=34) | -0.270 (n=94) |
| `time_20yd_s` | `pro_bowls` | -0.046 (n=417) | 0.113 (n=102) | -0.156 (n=93) | -0.174 (n=94) | NA (n=34) | -0.044 (n=94) |
| `time_20yd_s` | `all_pros` | -0.011 (n=417) | 0.154 (n=102) | -0.062 (n=93) | -0.029 (n=94) | NA (n=34) | -0.046 (n=94) |
| `time_20yd_s` | `play_count` | -0.018 (n=406) | -0.190 (n=99) | -0.273 (n=90) | -0.342 (n=93) | -0.154 (n=31) | -0.280 (n=93) |
| `time_20yd_s` | `player_play_mean_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `time_20yd_s` | `player_play_max_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `time_40yd_s` | `games_played_per_season` | -0.085 (n=417) | -0.151 (n=102) | -0.087 (n=93) | -0.199 (n=94) | -0.008 (n=34) | -0.233 (n=94) |
| `time_40yd_s` | `pro_bowls` | -0.067 (n=417) | 0.050 (n=102) | -0.222 (n=93) | -0.170 (n=94) | NA (n=34) | -0.077 (n=94) |
| `time_40yd_s` | `all_pros` | -0.043 (n=417) | 0.049 (n=102) | -0.082 (n=93) | -0.117 (n=94) | NA (n=34) | -0.079 (n=94) |
| `time_40yd_s` | `play_count` | 0.003 (n=406) | -0.198 (n=99) | -0.240 (n=90) | -0.354 (n=93) | -0.140 (n=31) | -0.229 (n=93) |
| `time_40yd_s` | `player_play_mean_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `time_40yd_s` | `player_play_max_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `max_s_yd_s` | `games_played_per_season` | 0.089 (n=417) | 0.143 (n=102) | 0.080 (n=93) | 0.206 (n=94) | 0.006 (n=34) | 0.314 (n=94) |
| `max_s_yd_s` | `games_started_per_season` | 0.052 (n=417) | 0.143 (n=102) | 0.059 (n=93) | 0.304 (n=94) | -0.111 (n=34) | 0.145 (n=94) |
| `max_s_yd_s` | `pro_bowls` | 0.097 (n=417) | 0.070 (n=102) | 0.241 (n=93) | 0.063 (n=94) | NA (n=34) | 0.087 (n=94) |
| `max_s_yd_s` | `all_pros` | 0.075 (n=417) | 0.161 (n=102) | 0.074 (n=93) | 0.170 (n=94) | NA (n=34) | 0.087 (n=94) |
| `max_s_yd_s` | `play_count` | -0.042 (n=406) | 0.122 (n=99) | 0.162 (n=90) | 0.284 (n=93) | 0.128 (n=31) | 0.081 (n=93) |
| `max_s_yd_s` | `player_play_mean_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `mean_a_first_0_5s_yd_s2` | `games_played_per_season` | 0.062 (n=417) | 0.152 (n=102) | 0.028 (n=93) | 0.041 (n=94) | 0.240 (n=34) | 0.011 (n=94) |
| `mean_a_first_0_5s_yd_s2` | `games_started_per_season` | 0.125 (n=417) | 0.183 (n=102) | 0.147 (n=93) | 0.180 (n=94) | 0.164 (n=34) | 0.199 (n=94) |
| `mean_a_first_0_5s_yd_s2` | `pro_bowls` | 0.034 (n=417) | -0.055 (n=102) | 0.038 (n=93) | 0.170 (n=94) | NA (n=34) | 0.037 (n=94) |
| `mean_a_first_0_5s_yd_s2` | `all_pros` | -0.010 (n=417) | -0.157 (n=102) | 0.054 (n=93) | 0.025 (n=94) | NA (n=34) | 0.038 (n=94) |
| `mean_a_first_0_5s_yd_s2` | `play_count` | 0.153 (n=406) | 0.268 (n=99) | 0.302 (n=90) | 0.270 (n=93) | 0.257 (n=31) | 0.301 (n=93) |
| `mean_a_first_0_5s_yd_s2` | `player_play_mean_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `mean_a_first_0_5s_yd_s2` | `player_play_max_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `mean_a_first_1_0s_yd_s2` | `games_played_per_season` | 0.065 (n=417) | 0.166 (n=102) | 0.043 (n=93) | -0.005 (n=94) | 0.143 (n=34) | 0.092 (n=94) |
| `mean_a_first_1_0s_yd_s2` | `games_started_per_season` | 0.118 (n=417) | 0.184 (n=102) | 0.174 (n=93) | 0.130 (n=94) | 0.056 (n=34) | 0.296 (n=94) |
| `mean_a_first_1_0s_yd_s2` | `pro_bowls` | 0.085 (n=417) | -0.043 (n=102) | 0.128 (n=93) | 0.170 (n=94) | NA (n=34) | 0.070 (n=94) |
| `mean_a_first_1_0s_yd_s2` | `all_pros` | 0.039 (n=417) | -0.066 (n=102) | 0.109 (n=93) | 0.032 (n=94) | NA (n=34) | 0.071 (n=94) |
| `mean_a_first_1_0s_yd_s2` | `play_count` | 0.106 (n=406) | 0.286 (n=99) | 0.311 (n=90) | 0.195 (n=93) | 0.241 (n=31) | 0.384 (n=93) |
| `mean_a_first_1_0s_yd_s2` | `player_play_mean_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `mean_a_first_1_0s_yd_s2` | `player_play_max_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `s_at_40yd_yd_s` | `games_played_per_season` | 0.092 (n=417) | 0.118 (n=102) | 0.097 (n=93) | 0.201 (n=94) | 0.083 (n=34) | 0.334 (n=94) |
| `s_at_40yd_yd_s` | `games_started_per_season` | 0.045 (n=417) | 0.110 (n=102) | 0.068 (n=93) | 0.250 (n=94) | -0.074 (n=34) | 0.138 (n=94) |
| `s_at_40yd_yd_s` | `pro_bowls` | 0.097 (n=417) | 0.070 (n=102) | 0.252 (n=93) | 0.006 (n=94) | NA (n=34) | 0.125 (n=94) |
| `s_at_40yd_yd_s` | `all_pros` | 0.081 (n=417) | 0.161 (n=102) | 0.089 (n=93) | 0.170 (n=94) | NA (n=34) | 0.125 (n=94) |
| `s_at_40yd_yd_s` | `play_count` | -0.043 (n=406) | 0.084 (n=99) | 0.183 (n=90) | 0.243 (n=93) | 0.102 (n=31) | 0.070 (n=93) |
| `s_at_40yd_yd_s` | `player_play_mean_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `s_at_40yd_yd_s` | `player_play_max_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `forty` | `games_played_per_season` | -0.103 (n=418) | -0.131 (n=102) | -0.094 (n=93) | -0.195 (n=95) | 0.026 (n=34) | -0.428 (n=94) |
| `forty` | `pro_bowls` | -0.101 (n=418) | -0.037 (n=102) | -0.258 (n=93) | -0.070 (n=95) | NA (n=34) | -0.206 (n=94) |
| `forty` | `all_pros` | -0.092 (n=418) | -0.162 (n=102) | -0.126 (n=93) | -0.117 (n=95) | NA (n=34) | -0.207 (n=94) |
| `forty` | `play_count` | 0.042 (n=407) | -0.112 (n=99) | -0.173 (n=90) | -0.220 (n=94) | -0.103 (n=31) | -0.105 (n=93) |
| `forty` | `player_play_mean_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `forty` | `player_play_max_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `ten_yd_split` | `games_played_per_season` | -0.072 (n=418) | -0.181 (n=102) | -0.131 (n=93) | -0.077 (n=95) | -0.116 (n=34) | -0.223 (n=94) |
| `ten_yd_split` | `games_started_per_season` | -0.052 (n=418) | -0.168 (n=102) | -0.055 (n=93) | -0.154 (n=95) | -0.055 (n=34) | -0.200 (n=94) |
| `ten_yd_split` | `pro_bowls` | -0.042 (n=418) | 0.007 (n=102) | -0.246 (n=93) | -0.121 (n=95) | NA (n=34) | -0.020 (n=94) |
| `ten_yd_split` | `all_pros` | -0.039 (n=418) | -0.087 (n=102) | -0.142 (n=93) | 0.077 (n=95) | NA (n=34) | -0.022 (n=94) |
| `ten_yd_split` | `play_count` | 0.063 (n=407) | -0.200 (n=99) | -0.164 (n=90) | -0.106 (n=94) | 0.029 (n=31) | -0.088 (n=93) |
| `ten_yd_split` | `player_play_mean_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| `ten_yd_split` | `player_play_max_top_speed` | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
