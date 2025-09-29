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
