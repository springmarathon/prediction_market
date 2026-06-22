import json
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")

data = json.loads(Path("data/open-meteo/20260618_120002.json").read_text())
times = [datetime.fromisoformat(t).replace(tzinfo=NY) for t in data["minutely_15"]["time"]]
temps = data["minutely_15"]["temperature_2m"]

now = datetime.now(NY)
t0 = now - timedelta(hours=1)
t1 = now + timedelta(hours=1)

def fmt(x, pos):
    dt = mdates.num2date(x).astimezone(NY)
    if dt.hour == 0 and dt.minute == 0:
        return dt.strftime("12AM\n%b %-d")
    return dt.strftime("%-I%p")

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(times, temps, linewidth=1.2)
ax.axvspan(t0, t1, alpha=0.15, color="orange", label=f"±1h around now ({now.strftime('%-I:%M%p')})")
ax.axvline(now, color="orange", linewidth=1, linestyle="--")
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2, tz=NY))
ax.xaxis.set_major_formatter(FuncFormatter(fmt))
ax.set_ylabel("°C")
ax.set_title("HRRR temperature_2m — Central Park")
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("/tmp/temp_plot.png", dpi=150)
plt.show()
