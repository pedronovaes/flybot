"""
Manage functions to deal with datetime info, such as convert dates and so on.
"""

import shutil
import sqlite3

import pandas as pd


def update_dates(file: str, backup_file: str) -> str:
    """
    Convert the flights time info to current time during Flybot runtime, as we
    want to look like it's current.

    Args:
        file: database path.
        backup_file: backup database path.
    """

    # Using original database file. This file is stored in the backup path.
    shutil.copy(src=backup_file, dst=file)

    conn = sqlite3.connect(database=file)

    # Get names from all tables.
    tables = (
        pd.read_sql(sql="select name from sqlite_master where type = 'table'", con=conn)
        .name
        .to_list()
    )

    # Convert each table to pandas dataframe.
    tdf = {}
    for t in tables:
        tdf[t] = pd.read_sql(sql=f"select * from {t}", con=conn)

    # Get reference time to use this info to conver timestamps.
    example_time = (
        pd.to_datetime(tdf['flights']['actual_departure'])
        .max()
    )
    current_time = pd.to_datetime('now').tz_localize(example_time.tz)
    time_diff = current_time - example_time

    # Convert timestamps to current time in Flights and Bookings tables.
    tdf['bookings']['book_date'] = (
        pd.to_datetime(tdf['bookings']['book_date'], utc=True) + time_diff
    )

    datetime_flights_columns = [
        'scheduled_departure',
        'scheduled_arrival',
        'actual_departure',
        'actual_arrival'
    ]
    for column in datetime_flights_columns:
        tdf['flights'][column] = pd.to_datetime(tdf['flights'][column]) + time_diff

    # Save updated sqlite tables.
    for table_name, df in tdf.items():
        df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()

    return file
