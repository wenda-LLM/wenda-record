import pymysql 
import datetime

db_info = { 
    'host': 'localhost', 
    'user': 'root', 
    'password': 'password', 
    'charset': 'utf8mb4' 
} 

def insert_into_wenda_logging(time, ip_address, prompt, response): 
    global db_info 
    time = datetime.datetime.now()
    db = pymysql.connect(**db_info) 
    cursor = db.cursor() 
    cursor.execute("CREATE DATABASE IF NOT EXISTS wenda") 
    cursor.execute("USE wenda") 
    cursor.execute("CREATE TABLE IF NOT EXISTS wenda_logging (id INT AUTO_INCREMENT PRIMARY KEY, time TIMESTAMP, ip_address VARCHAR(255), prompt VARCHAR(255), response VARCHAR(255))") 
    sql = "INSERT INTO wenda_logging (time, ip_address, prompt, response) VALUES (%s, %s, %s, %s)" 
    val = (time, ip_address, prompt, response) 
    cursor.execute(sql, val) 
    db.commit() 
    db.close() 

if __name__ == '__main__': 
    data = { 
        'time': datetime.datetime.now(), 
        'ip_address': '127.0.0.1', 
        'prompt': 'prompt', 
        'response': 'response' 
    } 
    
    insert_into_wenda_logging(**data)