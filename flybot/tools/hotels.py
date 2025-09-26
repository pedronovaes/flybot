"""
Chatbot's tools to search for and manage hotel reservations.
"""

import sqlite3
from typing import Optional
from datetime import date, datetime

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig


@tool
def search_hotels(
    config: RunnableConfig,
    location: Optional[str] = None,
    name: Optional[str] = None,
    price_tier: Optional[str] = None,
    checkin_date: Optional[date | datetime] = None,
    checkout_date: Optional[date | datetime] = None
) -> list[dict]:
    """
    Search for hotels based on location, name, price tier, check-in date, and
    check-out date.

    Returns:
        A list of hotel dictionaries matching the search criteria.
    """

    configurable = config.get('configurable', {})
    db = configurable.get('db', '')

    conn = sqlite3.connect(database=db)
    cursor = conn.cursor()

    query = "select * from hotels where 1 = 1"
    params = []

    if location:
        query += " and location like ?"
        params.append(f"%{location}%")

    if name:
        query += " and name like ?"
        params.append(f"%{name}%")

    cursor.execute(query, params)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return results


@tool
def book_hotel(hotel_id: int, config: RunnableConfig) -> str:
    """
    Book a hotel by its ID.

    Returns:
        A message indicating whether the hotel was successfully booked or not.
    """

    configurable = config.get('configurable', {})
    db = configurable.get('db', '')

    conn = sqlite3.connect(database=db)
    cursor = conn.cursor()

    query = "update hotels set booked = 1 where id = ?"
    cursor.execute(query, (hotel_id,))
    conn.commit()

    if cursor.rowcount > 0:
        return_message = f"Hotel {hotel_id} successfully booked."
    else:
        return_message = f"No hotel found with ID {hotel_id}."

    cursor.close()
    conn.close()

    return return_message


@tool
def update_hotel(
    config: RunnableConfig,
    hotel_id: int,
    checkin_date: Optional[datetime | date] = None,
    checkout_date: Optional[datetime | date] = None
) -> str:
    """
    Update a hotel's check-in and check-out dates by its ID.

    Returns:
        A message indicating whether the hotel was successfully updated or not.
    """

    configurable = config.get('configurable', {})
    db = configurable.get('db', '')

    conn = sqlite3.connect(database=db)
    cursor = conn.cursor()

    if checkin_date:
        query = "update hotels set checkin_date = ? where id = ?"
        cursor.execute(query, (checkin_date, hotel_id))

    if checkout_date:
        query = "update hotels set checkout_date = ? where id = ?"
        cursor.execute(query, (checkout_date, hotel_id))

    conn.commit()

    if cursor.rowcount > 0:
        return_message = f"Hotel {hotel_id} successfully updated."
    else:
        return_message = f"No hotel found with ID {hotel_id}."

    cursor.close()
    conn.close()

    return return_message


@tool
def cancel_hotel(hotel_id: int, config: RunnableConfig) -> str:
    """
    Cancel a hotel by its ID.

    Returns:
        A message indicating whether the hotel was successfully cancelled or not.
    """

    configurable = config.get('configurable', {})
    db = configurable.get('db', '')

    conn = sqlite3.connect(database=db)
    cursor = conn.cursor()

    query = "update hotels set booked = 0 where id = ?"
    cursor.execute(query, (hotel_id,))
    conn.commit()

    if cursor.rowcount > 0:
        return_message = f"Hotel {hotel_id} successfully cancelled."
    else:
        return_message = f"No hotel found with ID {hotel_id}."

    cursor.close()
    conn.close()

    return return_message
