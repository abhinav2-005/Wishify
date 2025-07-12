import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
password = os.getenv("password")

def establish_connection():
    return mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = password,
            database = 'Whishify'
        )
establish_connection()