# tsconv

Small stdlib-only Python 3 CLI to convert timestamps and durations. Handy when reading logs.

## Install

    pip install .      # inside a venv; provides the `tsconv` command

Or run directly: `python3 tsconv.py ...`

## Usage

    tsconv 1700000000                 # ISO UTC, local, relative, epoch s/ms
    tsconv 1700000000000              # ms epochs auto-detected (> 1e11)
    tsconv 2026-10-07T12:00:00Z       # -> epoch seconds / ms
    tsconv --dur 90061                # -> 1d 1h 1m 1s
    tsconv --dur 1d2h                 # -> 93600

Timestamps without a timezone are treated as UTC.

## Tests

    python3 -m unittest discover -s tests -v

## License

MIT
