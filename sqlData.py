import sqlite3

DATABASE_NAME="IO.db"

def create_db_table():
    db_connection = sqlite3.connect(DATABASE_NAME)
    db_connection.execute('CREATE TABLE IF NOT EXISTS io_table '
                          '(number INTEGER, '
                          'id_number INTEGER, '
                          'name CHAR(30), '
                          'cardID CHAR(11), '
                          'state CHAR(8), '
                          'time TIMESTAMP, '
                          'io CHAR(10))')
    db_connection.close()

def put_row_into_db(row:list):
    db_connection = sqlite3.connect(DATABASE_NAME)
    headers=('number', 'id_number', 'name', 'cardID', 'state', 'time', 'io')
    db_connection.execute(f'INSERT INTO io_table {headers} VALUES {row}')
    db_connection.commit()
    db_connection.close()

def get_all_from_db():
    db_connection = sqlite3.connect(DATABASE_NAME)
    cursor=db_connection.execute("select * from io_table")
    rows=cursor.fetchall()
    db_connection.close()
    return rows

def get_data_from_db(name, timerange, sort_by):
    db_connection = sqlite3.connect(DATABASE_NAME)
    timestamp_in, timestamp_out = timerange
    cursor=db_connection.execute(f"select * from io_table "\
                                 f"where name LIKE '%{name}%' and "\
                                 f"time BETWEEN {timestamp_in} and {timestamp_out} "\
                                 f"ORDER BY {sort_by}")
    rows = cursor.fetchall()
    db_connection.close()
    return rows

def delete_row_from_db(id):
    db_connection = sqlite3.connect(DATABASE_NAME)
    db_connection.execute(f"DELETE from io_table where number={id}")
    db_connection.commit()
    db_connection.close()

def delete_db_table():
    db_connection = sqlite3.connect(DATABASE_NAME)
    db_connection.execute("DROP TABLE io_table")
    db_connection.close()

def clear_db_table():
    db_connection = sqlite3.connect(DATABASE_NAME)
    db_connection.execute("DELETE from io_table where number>0")
    db_connection.close()


