import os

import psycopg2


def get_connection():
    DATABASE_URL = os.environ['DATABASE_URL']
    return psycopg2.connect(DATABASE_URL, sslmode='require')


def create_table():
    create_sql = """CREATE TABLE useful_links( 
                 group VARCHAR(64) NOT NULL,
                 name VARCHAR(64) NOT NULL,
                 links TEXT [] NOT NULL,
                 resource_description TEXT
                 )"""
    return create_sql

conn = get_connection().cursor()
conn.execute(create_table())
conn.commit()
conn.close()
