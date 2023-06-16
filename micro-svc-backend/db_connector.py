import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Loading .env file for development


class DbConnector:
    def connect(self):
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                table_name=os.getenv("TABLE_NAME"),
                sslmode="prefer"
                if os.getenv("DB_DISABLE_SSL_MODE") == "true"
                else "require",
            )
            print("Connected to the database successfully!!")
            return conn
        except psycopg2.Error as e:
            raise Exception("Unable to connect to database: {}".format(e))