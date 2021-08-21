import os
import psycopg2 as psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()
dbname = os.getenv("dbname")
username_bd = os.getenv("username").lower()
password_bd = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")


# Подключение к базе данных
try:
    with psycopg2.connect(
        dbname=dbname,
        user=username_bd,
        password=password_bd,
        host=host,
        port=port
    ) as connection:
        pass


except (Exception, Error) as e:
    print(e)


connection.autocommit = True
cursor = connection.cursor()
