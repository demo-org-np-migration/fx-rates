#!/usr/bin/env python3
"""
Pega las tasas de OpenFX y las mete en postgres. Corre como CronJob cada 15 min.
"""
import os

OPENFX_URL = os.environ.get("OPENFX_URL", "http://api.openfx-rates.com")
DRY_RUN = os.environ.get("DRY_RUN") == "1"

DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_NAME = os.environ.get("DB_NAME", "rates")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")


def main():
    print("TODO")


if __name__ == "__main__":
    main()
