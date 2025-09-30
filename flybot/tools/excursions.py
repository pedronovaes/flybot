"""
Chatbot's tools to let the user search for things to do (and make reservations)
onde they arrive.
"""

import sqlite3
from typing import Optional
from datetime import date, datetime

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig


@tool
def search_trip_recommendations(
    config: RunnableConfig,
    location: Optional[str] = None,
    name: Optional[str] = None,
    keywords: Optional[str] = None
) -> list[dict]:
    """
    Search for trip recommendations based on location, name, and keywords.
    """

    configuration = config.get('configurable', {})
    db = configuration.get('db', '')

    conn = sqlite3.connect(database=db)
    cursor = conn.cursor()

    query = "select * from trip_recommendations where 1 = 1"
    params = []

    if location:
        query += " and location like ?"
        params.append(f"%{location}%")

    if name:
        query += " and name like ?"
        params.append(f"%{name}%")

    if keywords:
        keywords_list = keywords.split(',')
        keywords_conditions = ' or '.join(["keywords like ?" for _ in keywords_list])

        query += f" and ({keywords_conditions})"
        params.extend([f"%{keyword.strip()}%" for keyword in keywords_list])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    return results


@tool
def book_excursion(recommendation_id: int, config: RunnableConfig) -> str:
    """
    Book an excursion by its recommendation ID.
    """

    configuration = config.get('configurable', {})
    db = configuration.get('db', '')

    conn = sqlite3.connect(database=db)
    cursor = conn.cursor()

    query = "update trip_recommendations set booked = 1 where id = ?"
    cursor.execute(query, (recommendation_id,))
    conn.commit()

    if cursor.rowcount > 0:
        return_message = f"Trip recommendation {recommendation_id} successfully booked."
    else:
        return_message = f"No trip recommendation found with ID {recommendation_id}."

    cursor.close()
    conn.close()

    return return_message


@tool
def update_excursion(recommendation_id: int, details: str, config: RunnableConfig) -> str:
    """
    Update a trip recommendation's details by its ID.
    """

    configuration = config.get('configurable', {})
    db = configuration.get('db', '')

    conn = sqlite3.connect(database=db)
    cursor = conn.cursor()

    query = "update trip_recommendations set details = ? where id = ?"
    cursor.execute(query, (details, recommendation_id))
    conn.commit()

    if cursor.rowcount > 0:
        return_message = f"Trip recommendation {recommendation_id} successfully updated."
    else:
        return_message = f"No trip recommendation found with ID {recommendation_id}."

    cursor.close()
    conn.close()

    return return_message


@tool
def cancel_excursion(recommendation_id: int, config: RunnableConfig) -> str:
    """
    Cancel a trip recommendation by its ID.
    """

    configuration = config.get('configurable', {})
    db = configuration.get('db', '')

    conn = sqlite3.connect(database=db)
    cursor = conn.cursor()

    query = "update trip_recommendations set booked = 0 where id = ?"
    cursor.execute(query, (recommendation_id,))
    conn.commit()

    if cursor.rowcount > 0:
        return_message = f"Trip recommendation {recommendation_id} successfully cancelled."
    else:
        return_message = f"No trip recommendation found with ID {recommendation_id}."

    cursor.close()
    conn.close()

    return return_message
