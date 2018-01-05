from DBWatcher import *
from Task import *
import sched, time

def main():
    dbconnection = databaseconfig()
    
    #every 60 second, db connection is established to see if any task is scheduled
    while True:
        single_parse_DB(dbconnection)
        print("DBWatcher pull completed, sleep for 60 second")
        time.sleep(60)
    dbconnection.disconnect()
    
def single_parse_DB(dbconnection):
    #dbconnection = databaseconfig()
    
    #initiate select query from task tables
    select_new_tsk = databasequery()
    
    #select a list of task that finished by now
    new_task_db_result = select_new_tsk.query_select_execution(dbconnection.cursor, "dashboar_task.select_pre-start_task",['(\'running\',\'success\')','now()'])
    max_id_result = select_new_tsk.query_select_execution(dbconnection.cursor,"dashboard_task_action.select_max_id",[])
    new_task_list = []
    if max_id_result[0]['max_id'] == None:
        max_id = 0
    else:
        max_id = max_id_result[0]['max_id']+1
    
    print("max_id: "+ str(max_id))
    #build a list tasks need to be executed
    for task_db_row in new_task_db_result:
        task_list_item = TaskStage(task_db_row)
        new_task_list.append(task_list_item)
    
    #for loop to execute every task in the to do list one by one
    for task_list_item in new_task_list:
        
        #initiate update query to update status of tasks executed
        update_new_tsk = databasequery()
        update_new_tsk.query_update_execution(dbconnection.cursor, "dashboar_task.update_task_status", ["(select id from dashboard_taskstatus where statusname = 'running') "], [str(task_list_item.task_id)])
        actionvalue = str(max_id)+','+str(task_list_item.task_id) +',\''+'task stage initiated' + '\',' + 'now()' + ',\'' +'info' + '\''
        update_new_tsk.query_insert_execution(dbconnection.cursor, "dashboard_task_action.insert_task_action", actionvalue)
        dbconnection.conn.commit()
        print('database changes commited')
        max_id += 1
        
        #get return code to decide if execution if successful
        execut_result= task_list_item.executestage()

        #if result is success (return code match success code recorded), mark task as success, stage move completion
        if execut_result:          
            update_new_tsk.query_update_execution(dbconnection.cursor, "dashboar_task.update_task_stage", ["(select id from dashboard_taskcurrentstage where stagename = 'Complete') "], [str(task_list_item.task_id)])
            update_new_tsk.query_update_execution(dbconnection.cursor, "dashboar_task.update_task_status", ["(select id from dashboard_taskstatus where statusname = 'success') "], [str(task_list_item.task_id)])
            
            #insert task action history
            actionvalue = str(max_id)+','+str(task_list_item.task_id) +',\''+'task stage completed' + '\',' + 'now()' + ',\'' +'info' + '\''
            update_new_tsk.query_insert_execution(dbconnection.cursor, "dashboard_task_action.insert_task_action", actionvalue)
        
        #if result if failed mark task a failed, do not move stage
        else:
            update_new_tsk.query_update_execution(dbconnection.cursor, "dashboar_task.update_task_status", ["(select id from dashboard_taskstatus where statusname = 'failure') "], [str(task_list_item.task_id)])
            actionvalue = str(max_id)+','+str(task_list_item.task_id) +',\''+'task stage failed' + '\',' + 'now()' + ',\'' +'error' + '\''
            update_new_tsk.query_insert_execution(dbconnection.cursor, "dashboard_task_action.insert_task_action", actionvalue)
            
        #commit all db changes
        dbconnection.conn.commit()
        max_id += 1
        print("task update commited")
   
    
if __name__ == '__main__':
    main()