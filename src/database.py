"""Functions for working with database."""

import sqlite3


def add_order_to_db(url, name, date, description, price, responses):
    """Adds data to Orders table."""
    con = sqlite3.connect("orders_list.db")
    cur = con.cursor()
    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER PRIMARY KEY,
                url TEXT,
                name TEXT,
                date TEXT,
                description TEXT,
                price TEXT,
                responses TEXT
                )
        """
    )
    data = (url, name, date, description, price, responses)
    cur.execute(
        (
            "INSERT INTO Orders (url, name, date, description, price, responses) "
            "VALUES (?, ?, ?, ?, ?, ?)"
        ),
        data,
    )
    con.commit()
    con.close()
