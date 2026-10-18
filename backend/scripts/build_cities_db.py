"""
Build script to download GeoNames data and compile SQLite database for city lookups.
License: GeoNames data is under Creative Commons Attribution 4.0 License (CC-BY 4.0).
"""

import os
import sqlite3
import urllib.request
import zipfile
import io
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "modules", "kundali", "data")
DB_PATH = os.path.join(DATA_DIR, "cities.db")
GEONAMES_URL = "https://download.geonames.org/export/dump/cities15000.zip"


def build_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(DB_PATH):
        logger.info(f"Removing existing database at {DB_PATH}")
        os.remove(DB_PATH)

    logger.info(f"Downloading GeoNames data from {GEONAMES_URL}...")
    req = urllib.request.urlopen(GEONAMES_URL)
    zip_bytes = req.read()

    logger.info("Extracting cities15000.txt...")
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        with zf.open("cities15000.txt") as f:
            lines = [line.decode("utf-8") for line in f.readlines()]

    logger.info(f"Parsed {len(lines)} cities. Initializing SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            geonameid INTEGER,
            name TEXT NOT NULL,
            ascii_name TEXT NOT NULL,
            lower_name TEXT NOT NULL,
            alternate_names TEXT,
            country TEXT NOT NULL,
            admin1 TEXT,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            timezone TEXT NOT NULL,
            population INTEGER NOT NULL,
            elevation REAL NOT NULL
        )
    """)

    cities_to_insert = []
    for line in lines:
        parts = line.strip().split("\t")
        if len(parts) < 19:
            continue

        geonameid = int(parts[0])
        name = parts[1]
        ascii_name = parts[2]
        alternate_names = parts[3]
        lat = float(parts[4])
        lon = float(parts[5])
        country = parts[8]
        admin1 = parts[10]
        population = int(parts[14]) if parts[14] else 0
        elev_str = parts[15] if parts[15] else (parts[16] if parts[16] else "0")
        try:
            elevation = float(elev_str)
        except ValueError:
            elevation = 0.0
        tz = parts[17] if parts[17] else "UTC"

        cities_to_insert.append((
            geonameid,
            name,
            ascii_name,
            name.lower(),
            alternate_names,
            country,
            admin1,
            lat,
            lon,
            tz,
            population,
            elevation,
        ))

    cursor.executemany("""
        INSERT INTO cities (
            geonameid, name, ascii_name, lower_name, alternate_names,
            country, admin1, lat, lon, timezone, population, elevation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cities_to_insert)

    cursor.execute("CREATE INDEX idx_lower_name ON cities(lower_name)")
    cursor.execute("CREATE INDEX idx_ascii_name ON cities(ascii_name)")
    cursor.execute("CREATE INDEX idx_country ON cities(country)")

    conn.commit()
    conn.close()
    logger.info(f"Successfully created {DB_PATH} with {len(cities_to_insert)} records.")


if __name__ == "__main__":
    build_db()
