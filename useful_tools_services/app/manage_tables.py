import os

import psycopg2


def get_connection():
    DATABASE_URL = os.environ['DATABASE_URL']
    return psycopg2.connect(DATABASE_URL, sslmode='require')


def create_table():
    create_sql = """CREATE TABLE useful_links( 
                 item_group VARCHAR(64) NOT NULL,
                 item_name VARCHAR(64) NOT NULL,
                 links TEXT [] NOT NULL,
                 resource_description TEXT
                 )"""
    return create_sql

conn = None

try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(create_table())
    cur.close()
    conn.commit()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()