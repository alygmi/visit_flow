#!/bin/sh
# Membuat database terpisah untuk pytest saat container pertama kali dibuat.
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    SELECT 'CREATE DATABASE visitflow_test OWNER $POSTGRES_USER'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'visitflow_test')\gexec
EOSQL
