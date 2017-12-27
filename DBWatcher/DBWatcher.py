'''
Created on Dec 26, 2017

@author: Andy
'''
import psycopg2
import sys
import json
import os

class databaseconfig():
    js = open(os.path.join(os.path.dirname(__file__), './/config//config.json'),'r').read()
    print(js)
        
    data = json.loads(js)
        
    host_s = data.get('database').get('host')
    print('database host: %s'%(host_s))
    dbname_s = data.get('database').get('dbname')
    print('database name: %s'%(dbname_s))
    user_s = data.get('database').get('user')
    print('database user: %s'%(user_s))
    password_s = data.get('database').get('password')
    print('database password: %s'%(password_s))
        
    #conn_string = r"host = 'localhost' dbname = 'django_test' user='postgres' password='firco'"
    conn_string = 'host = \'%s\' dbname = \'%s\' user=\'%s\' password=\'%s\''%(host_s,dbname_s,user_s,password_s)
    print("connecting to databae" )
            
    conn = psycopg2.connect(conn_string)          
    print("connected to database")
            
    cursor = conn.cursor()

    def disconnect(self):
        self.cursor.close()
        print("database cursor closed")
        self.conn.close()
        print("database connection closed")
        
class databasequery():
    js = open(os.path.join(os.path.dirname(__file__), './/config//sqlmap.json'),'r').read()
    print(js)
        
    data = json.loads(js)
