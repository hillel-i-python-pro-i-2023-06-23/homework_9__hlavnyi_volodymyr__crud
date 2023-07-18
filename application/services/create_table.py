from application.models.db_connection import DBConnection


def create_table():
    with DBConnection() as connection:
        with connection:
            connection.execute(
                """
                               CREATE TABLE IF NOT EXISTS phones (
                                    phone_id INTEGER PRIMARY KEY NOT NULL,
                                    contacted_name VARCHAR NOT NULL,
                                    phone_value VARCHAR NOT NULL
                                )
                                """
            )
