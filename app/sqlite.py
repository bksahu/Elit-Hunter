import os
from sqlite3 import connect, OperationalError, IntegrityError, ProgrammingError, Error

os.chdir(os.path.dirname(os.path.abspath(__file__)))

DB_name = 'elitDB'

def connect_to_db(db=None):
    """Connect to a sqlite DB. Create the database if there isn't one yet.

    Open a connection to a SQLite DB (either a DB file or an in-memory DB).
    When a database is accessed by multiple connections, and one of the
    processes modifies the database, the SQLite database is locked until that
    transaction is committed.

    Parameters
    ----------
    db : str
        database name (without .db extension). If None, create an In-Memory DB.

    Returns
    -------
    connection : sqlite3.Connection
        connection object
    """
    if db is None:
        mydb = ':memory:'
        print('New connection to in-memory SQLite DB...')
    else:
        mydb = '{}.db'.format(db)
        print('New connection to SQLite DB...')
    connection = connect(mydb)
    return connection

def connection(func):
    """Decorator to (re)open a sqlite database connection when needed.

    A database connection must be open when we want to perform a database query
    but we are in one of the following situations:
    1) there is no connection
    2) the connection is closed

    Parameters
    ----------
    func : function
        function which performs the database query

    Returns
    -------
    inner func : function
    """
    def inner_func(conn, *args, **kwargs):
        try:
            conn.execute('SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, ProgrammingError):
            conn = connect_to_db(DB_name)
        return func(conn, *args, **kwargs)
    return inner_func

def disconnect_from_db(db=None, conn=None):
    if db is not DB_name:
        print("You are trying to disconnect from a wrong DB")
    if conn is not None:
        conn.close()

def scrub(input_string):
    """Clean an input string (to prevent SQL injection).

    Parameters
    ----------
    input_string : str

    Returns
    -------
    str
    """
    return ''.join(k for k in input_string if k.isalnum())

@connection
def create_table(conn, table_name):
    table_name = scrub(table_name)
    sql = 'CREATE TABLE {} (rowid INTEGER PRIMARY KEY AUTOINCREMENT,' \
          'title TEXT , link TEXT, link_id INTEGER, website TEXT)'.format(table_name)
    try:
        conn.execute(sql)
    except OperationalError as e:
        print(e)

@connection
def insert_one(conn, title, link, link_id, website, table_name):
    """ Insert single row into table
    """
    table_name = scrub(table_name)
    sql = "INSERT INTO {} ('title', 'link', 'link_id', 'website') VALUES (?, ?, ?, ?)"\
        .format(table_name)
    try:
        conn.execute(sql, (title, link, link_id, website))
        conn.commit()
    except Error as e:
        print(e)

@connection
def insert_many(conn, items, table_name):
    """ Insert many rows into table
    """
    table_name = scrub(table_name)
    sql = "INSERT INTO {} ('title', 'link', 'link_id', 'website') VALUES (?, ?, ?, ?)"\
        .format(table_name)
    entries = list()
    for x in items:
        entries.append((x['title'], x['link'], x['link_id'], x['website']))
    try:
        conn.executemany(sql, entries)
        conn.commit()
    except Error as e:
        print(e)

def tuple_to_dict(mytuple):
    """ Convert tuples to dict
    """
    mydict = dict()
    mydict['id'] = mytuple[0]
    mydict['title'] = mytuple[1]
    mydict['link'] = mytuple[2]
    mydict['link_id'] = mytuple[3]
    mydict['website'] = mytuple[4]
    return mydict

@connection
def select_one(conn, table_name, col_name=None, reversed=False):
    """ Return first or last row of the table

    Parameters
    ----------
    conn : sqlite3.Connection
        connection object
    table_name: str
        name of table to query
    col_name: str
        name of the column according to which the data is needed to be arranged
    reversed: bool
        query latest record if True

    Returns
    -------
    dict: dict
        dictonary with query results
    """

    table_name = scrub(table_name)
    if col_name:
        col_name = scrub(col_name)
    if reversed and col_name:
        sql = "SELECT * FROM {} ORDER BY {} DESC LIMIT 1".format(table_name, col_name)
    else:
        sql = "SELECT * FROM {} LIMIT 1".format(table_name)
    c = conn.execute(sql)
    result = c.fetchone()
    if result is not None:
        return tuple_to_dict(result)
    else:
        raise Exception(
            "Can\'t read '{}' because it's not in table ''{}"
            .format(col_name, table_name))

@connection
def select_all(conn, table_name, col_name=None, reversed=False):
    """ Return all rows of the table

    Parameters
    ----------
    conn : sqlite3.Connection
        connection object
    table_name: str
        name of table to query
    col_name: str
        name of the column according to which the data is needed to be arranged
    reversed: bool
        query latest record if True

    Returns
    -------
    dict: dict
        dictonary with query results
    """

    table_name = scrub(table_name)
    if col_name:
        col_name = scrub(col_name)
    if reversed and col_name:
        sql = "SELECT * FROM {} ORDER BY {} DESC".format(table_name, col_name)
    else:
        sql = "SELECT * FROM {}".format(table_name)
    c = conn.execute(sql)
    results = c.fetchall()
    return list(map(lambda x: tuple_to_dict(x), results))

@connection
def select_last_id(conn, website, table_name):
    table_name = scrub(table_name)
    sql = "SELECT link_id FROM {} WHERE website='{}' ORDER BY rowid DESC limit 1".format(
        table_name, website
    )
    c = conn.execute(sql)
    result = c.fetchone()
    return result[0]

# if __name__ == "__main__":
#     conn = connect_to_db(DB_name)
#     create_table(conn, "movies")
#     my_items = [
#         {'title': "Movie 2", "link": "www.movie2.com", "link_id": "23"},
#         {'title': "Movie 3", "link": "www.movie3.com", "link_id": "43"},
#         {'title': "Movie 4", "link": "www.movie4.com", "link_id": "56"},
#     ]

#     insert_many(conn, my_items, table_name='movies')
#     print(select_all(conn, "movies"))
#     disconnect_from_db(DB_name, conn)