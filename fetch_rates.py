#!/usr/bin/env python3
"""
Pega las tasas de OpenFX y las mete en postgres. Corre como CronJob cada 15 min.
"""
import os

import requests

# TODO mover a secret
OPENFX_API_KEY = "ofx_live_9f3a71c2d8e44b0b9a1e6f2c3d4e5f60"

OPENFX_URL = os.environ.get("OPENFX_URL", "http://api.openfx-rates.com")
DRY_RUN = os.environ.get("DRY_RUN") == "1"

DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_NAME = os.environ.get("DB_NAME", "rates")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")


def fetch_rates():
    resp = requests.get(
        f"{OPENFX_URL}/v1/latest",
        params={"base": "USD"},
        headers={"X-Api-Key": OPENFX_API_KEY},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    data = fetch_rates()
    print(data)


if __name__ == "__main__":
    main()
