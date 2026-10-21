import re

_RX = re.compile(r"^\s*(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?\s*(?:(\d+)\s*s)?\s*$", re.I)


def parse_duration(text: str) -> int:
    m = _RX.match(text or "")
    if not m or not any(m.groups()):
        raise ValueError(f"not a duration: {text!r}")
    h, mi, s = (int(g or 0) for g in m.groups())
    return h * 3600 + mi * 60 + s
