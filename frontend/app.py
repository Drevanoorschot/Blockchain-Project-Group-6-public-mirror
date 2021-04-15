import os

from flask import Flask, render_template
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

conn = psycopg2.connect(host=os.getenv('POSTGRESQL_HOST'),
                        port=os.getenv('POSTGRESQL_PORT'),
                        database=os.getenv('POSTGRESQL_DB'),
                        user=os.getenv('POSTGRESQL_USER'),
                        password=os.getenv('POSTGRESQL_PW'))
cursor = conn.cursor()


@app.route('/')
def hello_world():
    cursor.execute('SELECT c.address, c.timestamp, r.time, r.result, r.failed, r.found '
                   'FROM contract c '
                   'LEFT JOIN run r ON r.contract_address = c.address '
                   'WHERE r.contract_address IS NOT NULL '
                   'ORDER BY found DESC, failed ASC, timestamp ASC ')
    results = cursor.fetchall()

    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run()
