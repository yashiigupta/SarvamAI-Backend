import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.database import execute_query


def create_chat_data_table():
    query = """
    CREATE TABLE chat_data (
    id INT auto_increment PRIMARY KEY,
    user_token VARCHAR(50),
    description VARCHAR(50),
    data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """

    execute_query(query)
    print("completed")


def something():
    query = """
    ALTER TABLE chat_data ADD COLUMN user_token varchar(55);
    ALTER TABLE chat_data DROP COLUMN user_id;
    """

    execute_query(query)
    print("completed")


if __name__ == "__main__":
    # create_chat_data_table()
    something()
