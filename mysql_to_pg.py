#!/usr/bin/env python3
"""
MySQL to PostgreSQL migration script
"""

import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "production_settings")


import mysql.connector
import psycopg2
from psycopg2.extras import execute_values

# Configuration
MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "Kang0716.",
    "database": "liang_ba",
}

# Get PostgreSQL config from environment or docker-compose
PG_CONFIG = {
    "host": "127.0.0.1",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "database": "liang_ba",
}


def get_mysql_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)


def get_pg_connection():
    return psycopg2.connect(**PG_CONFIG)


def type_converter(mysql_type, mysql_value):
    """Convert MySQL types to PostgreSQL compatible values"""
    if mysql_value is None:
        return None

    mysql_type = mysql_type.upper() if mysql_type else ""

    # Handle specific type conversions
    if "TINYINT" in mysql_type or "BOOLEAN" in mysql_type:
        return bool(mysql_value)

    return mysql_value


def migrate_table(cursor_mysql, cursor_pg, table_name):
    """Migrate a single table from MySQL to PostgreSQL"""
    # Get columns from MySQL
    cursor_mysql.execute(f"DESCRIBE {table_name}")
    columns = cursor_mysql.fetchall()

    # Get column names
    col_names = [col[0] for col in columns]

    # Get data
    cursor_mysql.execute(f"SELECT * FROM {table_name}")
    rows = cursor_mysql.fetchall()

    if not rows:
        print(f"  Table {table_name}: No data to migrate")
        return 0

    # Create INSERT statement
    col_names_str = ", ".join([f'"{col}"' for col in col_names])
    insert_sql = f"INSERT INTO {table_name} ({col_names_str}) VALUES %s"

    # Convert rows
    converted_rows = []
    for row in rows:
        converted_row = []
        for i, val in enumerate(row):
            col_type = columns[i][1] if i < len(columns) else None
            converted_val = type_converter(col_type, val)
            converted_row.append(converted_val)
        converted_rows.append(tuple(converted_row))

    # Insert into PostgreSQL
    execute_values(cursor_pg, insert_sql, converted_rows)

    print(f"  Table {table_name}: Migrated {len(rows)} rows")
    return len(rows)


def migrate_all():
    """Migrate all tables from MySQL to PostgreSQL"""
    print("Connecting to MySQL...")
    mysql_conn = get_mysql_connection()
    mysql_cursor = mysql_conn.cursor()

    print("Connecting to PostgreSQL...")
    pg_conn = get_pg_connection()
    pg_cursor = pg_conn.cursor()

    # Get tables
    mysql_cursor.execute("SHOW TABLES")
    tables = [list(row)[0] for row in mysql_cursor.fetchall()]

    print(f"\nFound {len(tables)} tables to migrate\n")

    total_rows = 0
    for table in tables:
        try:
            rows = migrate_table(mysql_cursor, pg_cursor, table)
            total_rows += rows
        except Exception as e:
            print(f"  Table {table}: ERROR - {e}")
            pg_conn.rollback()

    # Commit
    pg_conn.commit()
    print(f"\nMigration completed! Total rows migrated: {total_rows}")

    # Close connections
    mysql_cursor.close()
    mysql_conn.close()
    pg_cursor.close()
    pg_conn.close()


if __name__ == "__main__":
    migrate_all()
