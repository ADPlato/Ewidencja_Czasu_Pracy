import mysql.connector
config = {
    'user': 'user',             # domyślny użytkownik MySQL w XAMPP
    'password': 'user',             # domyślnie puste hasło w XAMPP
    'host': '192.168.1.142',        # localhost
    'database': 'inveo',   # nazwa twojej bazy danych
    'raise_on_warnings': True
}

def get_data_from_db(name, timerange, sort_by):
    db_connection = mysql.connector.connect(**config)
    timestamp_in, timestamp_out = timerange
    cursor=db_connection.cursor()
    cursor.execute(f"SELECT name, time, io FROM wejscia "\
                                 f"WHERE name LIKE '%{name}%' AND "\
                                 f"time >= '{timestamp_in}' AND time <='{timestamp_out}' "\
                                 f"ORDER BY {sort_by};")
    rows = cursor.fetchall()
    db_connection.close()
    return rows




