import sqlite3


CREATE_MACROS_TABLE = 'CREATE TABLE IF NOT EXISTS macros (' \
                      'id INTEGER PRIMARY KEY,' \
                      'label VARCHAR(255),' \
                      'quantity FLOAT(25),' \
                      'unit VARCHAR(255);'

INSERT_MACRO = 'INSERT INTO macros (label, quantity, unit) VALUES (?, ?, ?);'


def create_tables(connection):
    with connection:
        connection.execute(CREATE_MACROS_TABLE)


def add_macro(connection, label, quantity, unit):
    with connection:
        connection.execute(INSERT_MACRO, (label, quantity, unit))
