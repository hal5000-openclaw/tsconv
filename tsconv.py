#!/usr/bin/env python3
"""tsconv: convert timestamps and durations."""
import argparse
import re
import sys
from datetime import datetime, timezone

MS_THRESHOLD = 1e11


def parse_duration(s):
    """Parse '1d2h', '90s', '1h 30m' or plain seconds into seconds."""
    s = s.strip().lower()
    if re.fullmatch(r"\d+(\.\d+)?", s):
        return int(float(s))
    units = {"w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}
    parts = re.findall(r"(\d+)\s*([wdhms])", s)
    if not parts or re.sub(r"(\d+)\s*([wdhms])|\s", "", s):
        raise ValueError("invalid duration: %r" % s)
    return sum(int(n) * units[u] for n, u in parts)


def format_duration(sec):
    sec = int(sec)
    sign = "-" if sec < 0 else ""
    sec = abs(sec)
    d, r = divmod(sec, 86400)
    h, r = divmod(r, 3600)
    m, s = divmod(r, 60)
    out = [f"{v}{u}" for v, u in ((d, "d"), (h, "h"), (m, "m"), (s, "s")) if v]
    return sign + (" ".join(out) if out else "0s")


def parse_timestamp(s):
    """Return aware datetime from epoch (s or ms) or ISO 8601 string."""
    s = s.strip()
    if re.fullmatch(r"-?\d+(\.\d+)?", s):
        v = float(s)
        if abs(v) > MS_THRESHOLD:
            v /= 1000.0
        return datetime.fromtimestamp(v, tz=timezone.utc)
    iso = s[:-1] + "+00:00" if s.endswith(("Z", "z")) else s
    dt = datetime.fromisoformat(iso)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def relative(dt, now=None):
    now = now or datetime.now(timezone.utc)
    delta = int((dt - now).total_seconds())
    text = format_duration(abs(delta))
    return f"in {text}" if delta > 0 else (f"{text} ago" if delta < 0 else "now")


def describe(s, now=None):
    dt = parse_timestamp(s)
    epoch = dt.timestamp()
    return "\n".join([
        "iso:      " + dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "local:    " + dt.astimezone().isoformat(),
        "relative: " + relative(dt, now),
        "epoch:    %d" % int(epoch // 1),
        "epoch_ms: %d" % int(round(epoch * 1000)),
    ])


def main(argv=None):
    p = argparse.ArgumentParser(prog="tsconv", description="Convert timestamps and durations.")
    p.add_argument("value", help="epoch (s/ms), ISO 8601, or duration with --dur")
    p.add_argument("--dur", action="store_true", help="treat value as a duration")
    a = p.parse_args(argv)
    try:
        if a.dur:
            v = a.value
            if re.fullmatch(r"-?\d+", v.strip()):
                print(format_duration(int(v)))
            else:
                print(parse_duration(v))
        else:
            print(describe(a.value))
    except ValueError as e:
        print("tsconv: %s" % e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
