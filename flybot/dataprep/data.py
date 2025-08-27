"""
Script to get all data used in the chatbot building.
"""

import os
import shutil

import requests


def get_data(file: str, backup_file: str, overwrite: bool = False) -> None:
    """
    Fetch the travel-db SQLite database from Google API to use on the chatbot.

    Args:
        file: database path to be saved.
        backup_file: backup database path to be saved.
        overwrite: boolean to indicate if the database will be overwrited, if
            exists.
    """

    db_url = 'https://storage.googleapis.com/benchmarks-artifacts/travel-db/travel2.sqlite'

    if overwrite or not os.path.exists(path=file):
        print('Downloading data...')

        response = requests.get(url=db_url)
        response.raise_for_status()  # Raises an HTTPError, if one occurred.

        with open(file=file, mode='wb') as f:
            f.write(response.content)

        # Save backup file. We'll use this to "reset" the database in each time
        # the chatbot will be executed.
        shutil.copy(src=file, dst=backup_file)

        print('Flight data download with success.')
