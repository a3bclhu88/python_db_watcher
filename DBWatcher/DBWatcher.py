'''
Created on Dec 26, 2017

@author: Andy
'''
import psycopg2
import sys
import json
import os
from psycopg2.psycopg1 import cursor

'''
class for database connection
'''
class databaseconfig():
    
    # loading json configuration from package for database connection info
    js = open(os.path.join(os.path.dirname(__file__), './/config//config.json'),'r').read()
    print(js)
        
    #loading json into memory
    data = json.loads(js)
        
    #extracting json config into string
    host_s = data.get('database').get('host')
    print('database host: %s'%(host_s))
    dbname_s = data.get('database').get('dbname')
    print('database name: %s'%(dbname_s))
    user_s = data.get('database').get('user')
    print('database user: %s'%(user_s))
    password_s = data.get('database').get('password')
    print('database password: %s'%(password_s))
    
    #construct db connecting string
    conn_string = 'host = \'%s\' dbname = \'%s\' user=\'%s\' password=\'%s\''%(host_s,dbname_s,user_s,password_s)
    print("connecting to databae" )
            
    #connect to postgres database
    conn = psycopg2.connect(conn_string)          
    print("connected to database")
            
    #initialize cursor
    cursor = conn.cursor()
    
    #function to invoke closing cursor and db connection after query completed.
    def disconnect(self):
        self.cursor.close()
        print("database cursor closed")
        self.conn.close()
        print("database connection closed")
    
'''
class for database query preparation and execution
'''  
class databasequery():
    
    #loading sqlmap from Json config in package
    js = open(os.path.join(os.path.dirname(__file__), './/config//sqlmap.json'),'r').read()
    print(js) 
    data = json.loads(js)
    
    #function for executing select query, taking a cursor as base from databaseconfig class and string query name return a list as result set
    def query_select_execution(self,cursor,query_name):
        print(query_name)
        
        #extract query statement from Json config
        query_task_detail_select = self.data[query_name]["query"]
        
        #executing query into result set
        cursor.execute(query_task_detail_select)
        records = cursor.fetchall()
        print(records)
        
        #extract column name of result set from json config
        query_colomn = self.data[query_name]["resultcolumns"]
        
        #convert result set into list of dict with format of "column name","value" for each row in result set as a record in the list
        resultset = []
        for record in records:
            dict_record = {}
            i = 0
            for column in query_colomn:
                dict_record[column] = record[i]
                i += 1
            resultset.append(dict_record)
        
        #return final query result set
        return(resultset)