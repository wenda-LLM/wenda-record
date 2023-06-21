import pymysql
import datetime

db_info = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'charset': 'utf8mb4'
}

def insert_into_wenda_feedback(time, ip_address, history, model_type, temperature, top_p, score=0):
    global db_info
    time = datetime.datetime.now()
    db = pymysql.connect(**db_info)
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS wenda")
    cursor.execute("USE wenda")
    cursor.execute("CREATE TABLE IF NOT EXISTS wenda_feedback (id INT AUTO_INCREMENT PRIMARY KEY, time TIMESTAMP, ip_address VARCHAR(255), history VARCHAR(255), model_type VARCHAR(255), temperature FLOAT(10), top_p FLOAT(10), score INT(10))")
    sql = "INSERT INTO wenda_feedback (time, ip_address, history, model_type, temperature, top_p, score) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (time, ip_address, history, model_type, temperature, top_p, score)
    cursor.execute(sql, val)
    db.commit()
    db.close()

if __name__ == '__main__':
    data = {
        'time': datetime.datetime.now(),
        'ip_address': '127.0.0.1',
        'history': 'history',
        'model_type': 'model_type',
        'temperature': 0.5,
        'top_p': 0.9,
        'score': 8
    }

    insert_into_wenda_feedback(**data)