import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # Loading .env file for development


class DbConnector:
    def connect(self):
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
            )
            print("Connected to the database successfully!!")
            return conn
        except mysql.connector.Error as e:
            raise Exception("Unable to connect to database: {}".format(e))
