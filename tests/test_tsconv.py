import io, os, sys, unittest
from contextlib import redirect_stdout
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tsconv


class T(unittest.TestCase):
    def test_epoch_s(self):
        self.assertEqual(tsconv.parse_timestamp("1700000000").isoformat(), "2023-11-14T22:13:20+00:00")

    def test_epoch_ms_autodetect(self):
        self.assertEqual(tsconv.parse_timestamp("1700000000000"), tsconv.parse_timestamp("1700000000"))

    def test_iso_z(self):
        self.assertEqual(int(tsconv.parse_timestamp("2026-10-07T12:00:00Z").timestamp()), 1791374400)

    def test_naive_is_utc(self):
        self.assertEqual(tsconv.parse_timestamp("2026-10-07T12:00:00").tzinfo, timezone.utc)

    def test_format_duration(self):
        self.assertEqual(tsconv.format_duration(90061), "1d 1h 1m 1s")
        self.assertEqual(tsconv.format_duration(0), "0s")

    def test_parse_duration(self):
        self.assertEqual(tsconv.parse_duration("1d2h"), 93600)
        self.assertEqual(tsconv.parse_duration("90"), 90)

    def test_bad_duration(self):
        with self.assertRaises(ValueError):
            tsconv.parse_duration("abc")

    def test_relative(self):
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.assertEqual(tsconv.relative(datetime(2025, 12, 31, 23, tzinfo=timezone.utc), now), "1h ago")
        self.assertEqual(tsconv.relative(datetime(2026, 1, 1, 0, 1, tzinfo=timezone.utc), now), "in 1m")

    def test_cli(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(tsconv.main(["--dur", "90061"]), 0)
        self.assertEqual(buf.getvalue().strip(), "1d 1h 1m 1s")

    def test_cli_error(self):
        self.assertEqual(tsconv.main(["--dur", "zzz"]), 2)


if __name__ == "__main__":
    unittest.main()
