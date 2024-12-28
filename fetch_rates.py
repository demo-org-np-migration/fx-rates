#!/usr/bin/env python3
"""
Pega las tasas de OpenFX y las mete en postgres. Corre como CronJob cada 15 min.
"""
import os
from datetime import datetime, timezone

import requests
import psycopg

# TODO mover a secret
OPENFX_API_KEY = "ofx_live_9f3a71c2d8e44b0b9a1e6f2c3d4e5f60"

OPENFX_URL = os.environ.get("OPENFX_URL", "http://api.openfx-rates.com")
DRY_RUN = os.environ.get("DRY_RUN") == "1"

DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_NAME = os.environ.get("DB_NAME", "rates")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS fx_rates (
    id serial PRIMARY KEY,
    base char(3) NOT NULL,
    quote char(3) NOT NULL,
    rate numeric(18,6) NOT NULL,
    fetched_at timestamptz NOT NULL
);
"""

INSERT_SQL = """
INSERT INTO fx_rates (base, quote, rate, fetched_at) VALUES (%s, %s, %s, %s);
"""


def fetch_rates():
    resp = requests.get(
        f"{OPENFX_URL}/v1/latest",
        params={"base": "USD"},
        headers={"X-Api-Key": OPENFX_API_KEY},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def save_rates(data):
    base = data["base"]
    rates = data["rates"]
    fetched_at = datetime.now(timezone.utc)

    conn = psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)
            for quote, rate in rates.items():
                cur.execute(INSERT_SQL, (base, quote, rate, fetched_at))
        conn.commit()
    finally:
        conn.close()


def main():
    data = fetch_rates()
    save_rates(data)
    print(f"listo, {len(data['rates'])} tasas guardadas")


if __name__ == "__main__":
    main()
