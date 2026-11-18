import unittest

from forty_attempt_features import extract_attempt_features


class FortyAttemptFeaturesTest(unittest.TestCase):
    def test_constant_acceleration_along_a_diagonal(self):
        # From rest at 5 yd/s², the runner covers 10 yd at 2 s and 40 yd at 4 s.
        # The origin is offset and the run points in the negative y direction.
        frames = []
        for tick in range(43):
            time = tick / 10
            distance = 2.5 * time**2
            frames.append((time, 12 + 0.6 * distance, 30 - 0.8 * distance, 5 * time, 5))

        features = extract_attempt_features(frames)

        expected = {
            "time_10yd_s": 2.0,
            "time_20yd_s": 2.828427,
            "time_30yd_s": 3.464102,
            "time_40yd_s": 4.0,
            "max_s_yd_s": 21.0,
            "mean_a_first_0_5s_yd_s2": 5.0,
            "mean_a_first_1_0s_yd_s2": 5.0,
            "s_at_40yd_yd_s": 20.0,
        }
        for column, value in expected.items():
            with self.subTest(column=column):
                self.assertAlmostEqual(features[column], value, delta=0.001)


    def test_clock_shift_preserves_distance_covered_before_onset(self):
        frames = []
        for tick in range(61):
            if tick < 10:
                x, speed = 0, 0
            elif tick < 20:
                x, speed = (tick - 10) / 10, 1
            else:
                x, speed = 1 + (tick - 20), 10
            frames.append((tick / 10, x, 0, speed, 0))

        for threshold in (1.0, 1.5):
            with self.subTest(threshold=threshold):
                features = extract_attempt_features(frames, onset_threshold=threshold)
                for yards, expected in ((10, 0.9), (20, 1.9), (30, 2.9), (40, 3.9)):
                    self.assertAlmostEqual(features[f"time_{yards}yd_s"], expected)
                self.assertEqual(features["s_at_40yd_yd_s"], 10)



    def test_extrapolates_only_near_finish_with_positive_final_speed(self):
        for final_distance, final_speed, expected in (
            (39.0, 8.0, 4.025),
            (38.9, 8.0, None),
            (39.0, 0.0, None),
            (40.0, 8.0, 3.9),
        ):
            with self.subTest(final_distance=final_distance, final_speed=final_speed):
                frames = [(tick / 10, tick, 0, 8, 0) for tick in range(39)]
                frames.insert(0, (-0.1, 0, 0, 0, 0))
                frames.append((3.9, final_distance, 0, final_speed, 0))
                result = extract_attempt_features(frames, onset_threshold=1.5, extrapolate=True)
                if expected is None:
                    self.assertIsNone(result["time_40yd_s"])
                    self.assertIsNone(result["s_at_40yd_yd_s"])
                else:
                    self.assertAlmostEqual(result["time_40yd_s"], expected)
                    self.assertEqual(result["s_at_40yd_yd_s"], 8)
                self.assertEqual(result["extrapolated"], expected == 4.025)


if __name__ == "__main__":
    unittest.main()
