import sqlite3
from typing import Optional
from datetime import date, datetime

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig


@tool
def search_car_rentals(
    config: RunnableConfig,
    location: Optional[str] = None,
    name: Optional[str] = None,
    price_tier: Optional[str] = None,
    start_date: Optional[date | datetime] = None,
    end_date: Optional[date | datetime] = None
) -> list[dict]:
    """
    Search for car rentals based on location, name, price tier, start date, and
    end date.

    Args:
        location: The location of the car rental.
        name: The name of the car rental company.
        price_tier: The price tier of the car rental.
        start_date: The start date of the car rental.
        end_date: The end date of the car rental.

    Returns:
        A list of car rental dictionaries matching the search criterea.
    """

    configuration = config.get('configurable', {})
    db = configuration.get('db', '')

    conn = sqlite3.connect(database=db)
    cursor = conn.cursor()

    query = "select * from car_rentals where 1 = 1"
    params = []

    if location:
        query += " and location like ?"
        params.append(f"%{location}%")

    if name:
        query += " and name like ?"
        params.append(f"%{name}%")

    # For this tutorial, I will let the chatbot match any dates and price
    # tier, since the dataset doesn't have much data.

    cursor.execute(query, params)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return results


@tool
def book_car_rental(rental_id: int, config: RunnableConfig) -> str:
    """
    Book a car rental by its ID.
    """

    configurable = config.get('configurable', {})
    db = configurable.get('db', '')

    conn = sqlite3.connect(database=db)
    cursor = conn.cursor()

    query = "update car_rentals set booked = 1 where id = ?"
    cursor.execute(query, (rental_id,))
    conn.commit()

    if cursor.rowcount > 0:
        return_message = f"Car rental {rental_id} successfully booked."
    else:
        return_message = f"No car rental found with ID {rental_id}."

    cursor.close()
    conn.close()

    return return_message
