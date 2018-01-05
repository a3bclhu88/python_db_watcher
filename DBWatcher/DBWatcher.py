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
    def query_select_execution(self,cursor,query_name,condition):
        print(query_name)
        
        #extract query statement from Json config
        query_task_detail_select = self.data[query_name]["query"]
        
        #extract conditions for where clause of the query from JSON config
        if len(self.data[query_name]["condition"])!=0:
            query_task_detail_select += " where "
            i = 0
            for con in self.data[query_name]["condition"]:
                query_task_detail_select += con
                query_task_detail_select += condition[i]
                
                #if more than one condition exist, add 'and' for connecting them together
                if i < len(self.data[query_name]["condition"])-1:
                    query_task_detail_select += " and "
                i += 1
                print(query_task_detail_select)
        
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
                #print(str(i) + column + " column value is " + str(record[i]))
                dict_record[column] = record[i]
                i += 1
                print(dict_record)
            resultset.append(dict_record)
        
        #return final query result set
        print(resultset)
        return(resultset)
    
    def query_update_execution(self,cursor,query_name,values,condition):
        print(query_name)
        
        #extract query statement from Json config
        query_task_detail_update = self.data[query_name]["query"]
        
        #extract set column and value from Json config
        i = 0
        for column in self.data[query_name]["resultcolumns"]:
            query_task_detail_update += column + " = " + values[i]
            if i < len(self.data[query_name]["resultcolumns"]) - 1:
                query_task_detail_update + ", "
        
        if len(self.data[query_name]["condition"])!=0:
            query_task_detail_update += " where "
            i = 0
            for con in self.data[query_name]["condition"]:
                query_task_detail_update += con
                query_task_detail_update += condition[i]
                
                #if more than one condition exist, add 'and' for connecting them together
                if i < len(self.data[query_name]["condition"])-1:
                    query_task_detail_update += " and "
                i += 1
        print(query_task_detail_update)
        cursor.execute(query_task_detail_update)