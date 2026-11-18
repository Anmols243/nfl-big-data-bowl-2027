"""Extract per-attempt forty-yard dash features and check official-time agreement."""

from datetime import datetime
from math import hypot
from pathlib import Path
from statistics import correlation, median
from tempfile import NamedTemporaryFile

import polars as pl


ATTEMPT_KEY = ["draft_year", "event_id", "nfl_id", "drill_name", "attempt"]
SPLIT_COLUMNS = [f"time_{yards}yd_s" for yards in (10, 20, 30, 40)]
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "nfl-bdb2027" / "nfl-big-data-bowl-2027"
OUTPUT = ROOT / "data" / "derived" / "forty_attempt_features.csv"
MAX_MEDIAN_ABS_ERROR_S = 0.15
MIN_CROSSINGS = 600
EXPECTED_ATTEMPTS = 793
ONSET_THRESHOLDS = (1.0, 1.5)


def extract_attempt_features(
    frames: list[tuple[float, float, float, float, float]],
    *,
    onset_threshold: float | None = None,
    extrapolate: bool = False,
) -> dict[str, float | bool | None]:
    """Accept (time in s, x, y, s, a) frames for one attempt."""
    times, xs, ys, speeds, accelerations = zip(*sorted(frames))
    if any(later <= earlier for earlier, later in zip(times, times[1:])):
        raise ValueError("Each attempt must have distinct frame timestamps.")
    onset = 0 if onset_threshold is None else next(
        (i for i in range(len(speeds) - 2) if min(speeds[i:i + 3]) > onset_threshold),
        None,
    )
    # Changing the clock does not change the coordinates or the crossing position.
    elapsed = [time - times[onset or 0] for time in times]
    dx, dy = xs[-1] - xs[0], ys[-1] - ys[0]
    span = hypot(dx, dy)
    progress = (
        [((x - xs[0]) * dx + (y - ys[0]) * dy) / span for x, y in zip(xs, ys)]
        if span
        else [0.0] * len(times)
    )

    def early_mean(window: float) -> float | None:
        if onset is None or elapsed[-1] < window:
            return None
        area = 0.0
        for i in range(onset, len(elapsed) - 1):
            start, end = elapsed[i:i + 2]
            width = min(end, window) - start
            left = accelerations[i]
            right = left + (accelerations[i + 1] - left) * width / (end - start)
            area += (left + right) * width / 2
            if end >= window:
                break
        return area / window

    features = dict.fromkeys(SPLIT_COLUMNS)
    speed_at_40 = None
    for yards, column in zip((10, 20, 30, 40), SPLIT_COLUMNS):
        for i, (left, right) in enumerate(zip(progress, progress[1:])):
            if left < yards <= right:
                fraction = (yards - left) / (right - left)
                if onset is not None:
                    features[column] = elapsed[i] + fraction * (elapsed[i + 1] - elapsed[i])
                if yards == 40:
                    speed_at_40 = speeds[i] + fraction * (speeds[i + 1] - speeds[i])
                break
    recovered = (
        extrapolate and onset is not None and features["time_40yd_s"] is None
        and 39 <= max(progress) < 40 and speeds[-1] > 0
    )
    if recovered:
        features["time_40yd_s"] = elapsed[-1] + (40 - progress[-1]) / speeds[-1]
        speed_at_40 = speeds[-1]
    return {
        **features,
        "extrapolated": recovered,
        "max_s_yd_s": max(speeds),
        "mean_a_first_0_5s_yd_s2": early_mean(0.5),
        "mean_a_first_1_0s_yd_s2": early_mean(1.0),
        "s_at_40yd_yd_s": speed_at_40,
    }


def build_features(source: Path) -> dict[float, pl.DataFrame]:
    frames = (
        pl.scan_csv(source / "combine_tracking.csv", null_values="NA")
        .filter((pl.col("drill_type") == "FORTY_YARD_DASH") & (pl.col("entity_type") == "PLAYER"))
        .select(*ATTEMPT_KEY, "time", "x", "y", "s", "a")
        .collect(engine="streaming")
    )
    if not frames.height or any(frames.null_count().row(0)):
        raise ValueError("Expected complete PLAYER forty tracking records.")
    rows = {threshold: [] for threshold in ONSET_THRESHOLDS}
    for key, attempt in frames.partition_by(ATTEMPT_KEY, as_dict=True).items():
        ordered = attempt.sort("time").select("time", "x", "y", "s", "a")
        origin = datetime.fromisoformat(ordered["time"][0])
        measurements = [
            ((datetime.fromisoformat(time) - origin).total_seconds(), x, y, s, a)
            for time, x, y, s, a in ordered.iter_rows()
        ]
        for threshold in ONSET_THRESHOLDS:
            features = extract_attempt_features(measurements, onset_threshold=threshold, extrapolate=True)
            rows[threshold].append(dict(zip(ATTEMPT_KEY, key)) | features)
    feature_types = {name: pl.Float64 for name in [
        *SPLIT_COLUMNS, "max_s_yd_s", "mean_a_first_0_5s_yd_s2",
        "mean_a_first_1_0s_yd_s2", "s_at_40yd_yd_s",
    ]}
    return {
        threshold: pl.DataFrame(attempts, schema_overrides=feature_types).sort(ATTEMPT_KEY)
        for threshold, attempts in rows.items()
    }


def validate(features: pl.DataFrame, official: pl.DataFrame) -> tuple[int, float]:
    joined = features.join(official, on=["draft_year", "nfl_id"], how="left", validate="m:1")
    groups = [("Overall", joined)] + [
        (str(year), joined.filter(pl.col("draft_year") == year))
        for year in sorted(joined["draft_year"].unique())
    ]
    print("year,total,crossings_before,crossings_after,mode,n,pearson_r,median_signed_s,median_abs_s")
    coverage, overall_error = 0, float("nan")
    for label, group in groups:
        observed = group.filter(~pl.col("extrapolated"))
        before = len(observed) - observed["time_40yd_s"].null_count()
        after = len(group) - group["time_40yd_s"].null_count()
        for mode, subset in (("observed", observed), ("with_extrapolation", group)):
            pairs = subset.select("time_40yd_s", "forty").drop_nulls()
            derived, recorded = pairs["time_40yd_s"], pairs["forty"]
            errors = list(derived - recorded)
            r = correlation(derived, recorded) if derived.n_unique() > 1 and recorded.n_unique() > 1 else float("nan")
            signed = median(errors) if errors else float("nan")
            absolute = median(map(abs, errors)) if errors else float("nan")
            print(f"{label},{len(group)},{before},{after},{mode},{len(pairs)},{r:.6f},{signed:.6f},{absolute:.6f}")
            if label == "Overall" and mode == "with_extrapolation":
                coverage, overall_error = after, absolute
    return coverage, overall_error


def main(source: Path = SOURCE, output: Path = OUTPUT) -> None:
    official = pl.read_csv(
        source / "combine_results.csv", columns=["draft_year", "nfl_id", "forty"], null_values="NA"
    )
    candidates = build_features(source)
    passing = []
    for threshold, features in candidates.items():
        if features.height != EXPECTED_ATTEMPTS:
            raise ValueError(f"Expected {EXPECTED_ATTEMPTS} attempts, found {features.height}.")
        print(f"Onset threshold: {threshold:.1f} yd/s")
        coverage, error = validate(features, official)
        if error < MAX_MEDIAN_ABS_ERROR_S and coverage >= MIN_CROSSINGS:
            passing.append((coverage, -threshold))
    if not passing:
        raise SystemExit("STOP: neither method met both gates. Existing output preserved.")

    coverage, negative_threshold = max(passing)
    threshold = -negative_threshold
    output.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=output.parent, delete=False) as temp:
        pending_output = Path(temp.name)
    try:
        candidates[threshold].write_csv(pending_output)
        pending_output.replace(output)
    finally:
        pending_output.unlink(missing_ok=True)
    print(f"PASS: selected {threshold:.1f} yd/s with {coverage}/{EXPECTED_ATTEMPTS} crossings")
    print(f"Saved {EXPECTED_ATTEMPTS} attempts to {output}")


if __name__ == "__main__":
    main()
