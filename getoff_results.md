# Get-off results

## Qualifying players

| Population | Combine position | Players |
|---|---|---:|
| Get-off on >=20 plays | DB | 10 |
| Get-off on >=20 plays | DL | 89 |
| Get-off on >=20 plays | OL | 0 |
| Get-off on >=20 plays | TE | 0 |
| Get-off on >=20 plays | WR | 0 |
| Get-off on >=20 plays | Overall | 99 |
| Targeted with separation on >=20 plays | WR | 65 |

## Spearman rho and 95% percentile bootstrap CI

| Bootstrap unit | Resamples | Seed |
|---|---:|---:|
| Pairwise-complete player | 2,000 | 20261120 |

| Analysis | Population | Pair | Prediction | n | Rho | 95% CI | Valid resamples |
|---|---|---|---|---:|---:|---|---:|
| Primary | DL | mean_get_off vs mean_a_first_0_5s_yd_s2 | Negative | 89 | -0.274021 | [-0.449084, -0.098279] | 2,000 |
| Primary | Pooled | mean_get_off vs mean_a_first_0_5s_yd_s2 | Negative | 99 | -0.190390 | [-0.370138, +0.004794] | 2,000 |
| Secondary A | DL | mean_get_off vs time_10yd_s | Positive | 89 | +0.419476 | [+0.234962, +0.579018] | 2,000 |
| Secondary A | Pooled | mean_get_off vs time_10yd_s | Positive | 99 | +0.276858 | [+0.058674, +0.457893] | 2,000 |
| Secondary B | WR | mean_separation vs max_s_yd_s | Positive | 65 | +0.035359 | [-0.201461, +0.264496] | 2,000 |
| Secondary B | WR | mean_separation vs mean_a_first_0_5s_yd_s2 | Positive | 65 | -0.055157 | [-0.290878, +0.186173] | 2,000 |
| Sensitivity | DL, excluding extrapolated | mean_get_off vs mean_a_first_0_5s_yd_s2 | Negative | 62 | -0.319332 | [-0.518692, -0.072572] | 2,000 |
| Sensitivity | Pooled, excluding extrapolated | mean_get_off vs mean_a_first_0_5s_yd_s2 | Negative | 70 | -0.219001 | [-0.433230, +0.028284] | 2,000 |
