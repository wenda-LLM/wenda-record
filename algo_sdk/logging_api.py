import pymysql 
import datetime
import json

db_info = { 
    'host': 'localhost', 
    'user': 'root', 
    'password': 'password', 
    'charset': 'utf8mb4' 
} 

def insert_into_wenda_logging(ip_address, local_ip_address, llm_type, prompt, response, history): 
    global db_info 
    time = datetime.datetime.now()
    history = json.dumps(history)
    db = pymysql.connect(**db_info) 
    cursor = db.cursor() 
    cursor.execute("CREATE DATABASE IF NOT EXISTS wenda") 
    cursor.execute("USE wenda") 
    cursor.execute("CREATE TABLE IF NOT EXISTS wenda_logging (id INT AUTO_INCREMENT PRIMARY KEY, time TIMESTAMP, ip_address VARCHAR(255), local_ip_address VARCHAR(255), llm_type VARCHAR(255), prompt LONGTEXT, response LONGTEXT, history LONGTEXT)") 
    sql = "INSERT INTO wenda_logging (time, ip_address, local_ip_address, llm_type, prompt, response, history) VALUES (%s,%s,%s,%s,%s,%s,%s)" 
    val = (time, ip_address, local_ip_address, llm_type, prompt, response, history) 
    cursor.execute(sql, val) 
    db.commit() 
    db.close() 

if __name__ == '__main__': 
    data = { 
        'ip_address': '127.0.0.1', 
        'local_ip_address':'local_ip_address',
        'llm_type':'llm_type',
        'prompt': 'prompt', 
        'response': 'response',
        'history':'history'
    } 
    
    insert_into_wenda_logging(**data)