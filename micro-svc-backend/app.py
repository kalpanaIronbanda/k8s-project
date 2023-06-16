import mysql.connector
from flask import Flask, render_template
import os
import logging
from dotenv import load_dotenv
from db_connector import DbConnector

app = Flask(__name__)

# To accept requests from all origins
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST'
    return response

def connect_database():
    logger.info("connecting to database...")
    app.db_conn = DbConnector().connect()
    logger.info("connected to database")

@app.route('/')
def index():
    connect_database()

    cursor = app.db_conn.cursor()
    query = f"SELECT * FROM {os.getenv('TABLE_NAME', 'default-table')}"
    cursor.execute(query)
    rows = cursor.fetchall()
    app.db_conn.close()
    return render_template('table.html', rows=rows)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
