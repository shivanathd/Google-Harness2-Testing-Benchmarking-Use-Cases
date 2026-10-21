### output/durations.py
import re


def parse_duration(text: str) -> int:
    """Convert a duration such as "1h30m", "45s" or "2h 5m 10s" to seconds.

    Units are h, m and s, case-insensitive; whitespace around and between parts is
    allowed. Each unit may appear at most once, in h-m-s order. Raise ValueError for
    empty input, unknown units, or text that is not a duration.
    """
    match = re.fullmatch(
        r"(?:(\d+)h)?\s*(?:(\d+)m)?\s*(?:(\d+)s)?", text.strip(), re.IGNORECASE
    )
    if not match or not any(match.groups()):
        raise ValueError(f"invalid duration: {text!r}")
    hours, minutes, seconds = (int(part or 0) for part in match.groups())
    return hours * 3600 + minutes * 60 + seconds


### src/durations.py
import re


def parse_duration(text: str) -> int:
    """Convert a duration such as "1h30m", "45s" or "2h 5m 10s" to seconds.

    Units are h, m and s, case-insensitive; whitespace around and between parts is
    allowed. Each unit may appear at most once, in h-m-s order. Raise ValueError for
    empty input, unknown units, or text that is not a duration.
    """
    match = re.fullmatch(
        r"(?:(\d+)h)?\s*(?:(\d+)m)?\s*(?:(\d+)s)?", text.strip(), re.IGNORECASE
    )
    if not match or not any(match.groups()):
        raise ValueError(f"invalid duration: {text!r}")
    hours, minutes, seconds = (int(part or 0) for part in match.groups())
    return hours * 3600 + minutes * 60 + seconds
