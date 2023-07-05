import pymysql
import datetime
import json

db_info = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'charset': 'utf8mb4'
}

def insert_into_wenda_feedback(ip_address, referer, llm_type, temperature, top_p, score, history, current_func):
    global db_info
    time = datetime.datetime.now()
    history = json.dumps(history)
    db = pymysql.connect(**db_info)
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS wenda")
    cursor.execute("USE wenda")
    cursor.execute("CREATE TABLE IF NOT EXISTS wenda_feedback (id INT AUTO_INCREMENT PRIMARY KEY, time TIMESTAMP, ip_address VARCHAR(255), referer LONGTEXT, llm_type VARCHAR(255), temperature FLOAT(10), top_p FLOAT(10), score INT(10), history LONGTEXT,current_func VARCHAR(255))")
    sql = "INSERT INTO wenda_feedback (time, ip_address, referer, llm_type, temperature, top_p, score ,history,current_func) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (time, ip_address ,referer ,llm_type ,temperature ,top_p ,score ,history,current_func)
    cursor.execute(sql,val)
    db.commit()
    db.close()

if __name__ == '__main__':
    data = {
        'ip_address': '127.0.0.1',
        'referer': 'referer',
        'llm_type': 'llm_type',
        'temperature': 0.5,
        'top_p': 0.9,
        'score': 8,
        'history': 'history',
        'current_func':'current_func'
    }

    insert_into_wenda_feedback(**data)