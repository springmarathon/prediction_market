# Data

## aviation-weather/

METAR observations for KNYC (Central Park, NYC) fetched from the Aviation Weather Center API.

**ASOS** (Automated Surface Observing System) is the network of automated weather stations operated jointly by the NWS, FAA, and DOD — the primary US surface-observation network. Each unit takes measurements and encodes them into a **METAR** (the report format). KNYC is a single ASOS at Central Park (WBAN 94728); its hourly METAR is the surface observation for that location.

The sensor's observation goes into NOAA/NWS's central dissemination first — NWS operates the ASOS, so the raw ob lands in their telecommunications backbone (NWSTG, the NOAAPORT satellite broadcast, and the WMO Global Telecommunication System) within seconds. Everyone else — weather.gov's public pages, The Weather Company, Google, AccuWeather, the aviation feeds — is a parallel downstream consumer of that central NOAA feed.

The official reading is recorded to the tenth of a degree Celsius and then converted to Fahrenheit.

Files are named `YYYYMMDD_HHMMSS.txt` (UTC) and contain raw METAR strings, one per line, newest first.

## open-meteo/

Temperature forecasts for Central Park (40.78°N, 73.97°W) fetched from the Open-Meteo API using the NCEP HRRR CONUS model.

HRRR major runs happen every ~6 hours, 00Z, 06Z, 12Z, 18Z, with a ~4h20m lag. HRRR minor runs happen every hour, with 30-50 minutes lag.

Files are named `YYYYMMDD_HHMMSS.json` (local time) and contain the raw API response.