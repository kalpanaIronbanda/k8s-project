import mysql.connector
from flask import Flask, render_template
import os
import logging

app = Flask(__name__)

# To accept requests from all origins
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST'
    return response

# Read database credentials from ConfigMap
user = os.getenv('DB_USER', 'default-user')
host = os.getenv('DB_HOST', 'default-host')
database = os.getenv('DB_NAME', 'default-database')

# Read database password from Secret
password = os.getenv('DB_PASSWORD')

# Read table name from environment variable
table_name = os.getenv('TABLE_NAME', 'default-table')

# Check if values are from ConfigMap or Secret
if password is None:
    logging.warning("Database password not found in Secret!")
else:
    logging.info("Database password retrieved from Secret.")

if user == 'default-user':
    logging.warning("Database user not found in ConfigMap!")
else:
    logging.info("Database user retrieved from ConfigMap.")

if host == 'default-host':
    logging.warning("Database host not found in ConfigMap!")
else:
    logging.info("Database host retrieved from ConfigMap.")

if database == 'default-database':
    logging.warning("Database name not found in ConfigMap!")
else:
    logging.info("Database name retrieved from ConfigMap.")

if table_name == 'default-table':
    logging.warning("Table name not found in environment variable!")
else:
    logging.info("Table name retrieved from environment variable.")


@app.route('/')
def index():
    cnx = mysql.connector.connect(user=user, password=password,
                                   host=host, database=database)
    cursor = cnx.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    rows = cursor.fetchall()
    cnx.close()
    return render_template('table.html', rows=rows)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
