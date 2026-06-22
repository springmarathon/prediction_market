import requests
import time
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path(__file__).parent.parent / "data" / "aviation-weather"
OUT_DIR.mkdir(parents=True, exist_ok=True)

RETRY_DELAY = 120  # seconds between retries when waiting for fresh data
ERROR_DELAY = 30   # seconds between retries on server error


def fetch_metars(station: str = "KNYC", hours: int = 10) -> list[str]:
    url = f"https://aviationweather.gov/api/data/metar?ids={station}&format=raw&hours={hours}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return [line.strip() for line in response.text.strip().splitlines() if line.strip()]


def metar_hhmm(metar: str) -> tuple[int, int] | None:
    """Parse (hour, minute) UTC from a METAR time field like '171651Z'."""
    for part in metar.split():
        if len(part) == 7 and part[:6].isdigit() and part[6] == "Z":
            return int(part[2:4]), int(part[4:6])
    return None


def poll():
    now_utc = datetime.now(timezone.utc)
    expected = ((now_utc.hour - 1) % 24, 51)

    while True:
        try:
            lines = fetch_metars(hours=72)
            if lines and metar_hhmm(lines[0]) == expected:
                ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                (OUT_DIR / f"{ts}.txt").write_text("\n".join(lines) + "\n")
                print(f"{ts} UTC saved {len(lines)} METAR(s)")
                return
            print(f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC latest is not {expected[0]:02d}:51Z yet — retrying in {RETRY_DELAY}s")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC error: {e} — retrying in {ERROR_DELAY}s")
            time.sleep(ERROR_DELAY)


def next_05_utc() -> float:
    """Unix timestamp of the next :05 mark of a UTC hour."""
    now_utc = datetime.now(timezone.utc)
    secs_into_hour = now_utc.minute * 60 + now_utc.second
    target = 5 * 60
    if secs_into_hour < target:
        return time.time() + (target - secs_into_hour)
    return time.time() + (3600 - secs_into_hour + target)


while True:
    poll()
    next_tick = next_05_utc()
    print(f"Next poll in {(next_tick - time.time()) / 60:.1f} min")
    time.sleep(max(0, next_tick - time.time()))
