import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.database import execute_query


def create_table():
    query = """
    CREATE TABLE user (
        user_id INT auto_increment PRIMARY KEY,
        username VARCHAR(50),
        device VARCHAR(50)
    );
    """
    execute_query(query)


def new_table():
    query = """
    Alter table user add column token varchar(50);
    """
    query2 = """
    ALTER TABLE user DROP COLUMN device;
    """

    execute_query(query)
    execute_query(query2)
    print("Completed")


if __name__ == "__main__":
    new_table()
