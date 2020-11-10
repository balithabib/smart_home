import datetime

from flask import Flask, request
import mysql.connector as mysql

connection = mysql.connect(
    user='client',
    password='client',
    host='127.0.0.1',
    database='my_database',
    buffered=True)
cursor = connection.cursor()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/_set_weather', methods=["POST"])
def update_weather():
    sql = 'INSERT INTO weather (timestamp, temperature, humidity)VALUES(%s,%s,%s)'
    cursor.execute(sql, (datetime.datetime.now(), request.form["temperature"], request.form["humidity"]))
    connection.commit()
    return 'update_weather'


@app.route('/_get_weather', methods=["GET"])
def get_weather():
    cursor.execute('SELECT * FROM weather ORDER BY timestamp DESC limit 1')
    result = cursor.fetchone()
    print(result, type(result[0]))
    return {
        'timestamp': result[0],
        'temperature': result[1],
        'humidity': result[2]
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
