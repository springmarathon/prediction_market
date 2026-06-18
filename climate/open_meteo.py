import json
import time
import requests
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


URL = (
    "https://api.open-meteo.com/v1/forecast?latitude=40.78&longitude=-73.97&minutely_15=temperature_2m&models=ncep_hrrr_conus&timezone=America/New_York"
)
OUT_DIR = Path(__file__).parent.parent / "data" / "open-meteo"
INTERVAL = 300  # seconds

while True:
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        now = datetime.now(ZoneInfo("America/New_York"))
        ts = now.strftime("%Y%m%d_%H%M%S")
        out_file = OUT_DIR / f"{ts}.json"
        out_file.write_text(json.dumps(data, indent=2))
        print(f"{ts} saved to {out_file}")
    except Exception as e:
        print(f"{datetime.now().strftime('%Y%m%d_%H%M%S')} error: {e}")
    next_tick = (time.time() // INTERVAL + 1) * INTERVAL
    time.sleep(max(0, next_tick - time.time()))