#!/bin/bash
set -e

echo "Waiting for ClickHouse to be ready..."
until clickhouse-client --host clickhouse --query "SELECT 1" &>/dev/null; do
  sleep 1
done

sleep 2

echo "ClickHouse is ready. Executing SQL scripts..."

if ls /init-sql/*.sql 1> /dev/null 2>&1; then
  for f in /init-sql/*.sql; do
    echo "Running $f"
    cat "$f" | clickhouse-client --host clickhouse --multiquery
  done
else
  echo "No SQL scripts to execute."
fi

echo "All SQL scripts executed."