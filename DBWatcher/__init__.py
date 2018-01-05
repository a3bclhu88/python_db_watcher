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
    select_new_tsk = databasequery()
    new_task_db_result = select_new_tsk.query_select_execution(dbconnection.cursor, "dashboar_task.select_pre-start_task",['1','now()'])
    new_task_list = []
    
    for task_db_row in new_task_db_result:
        task_list_item = TaskStage(task_db_row)
        new_task_list.append(task_list_item)
    
    for task_list_item in new_task_list:
        task_list_item.executestage()
        update_new_tsk = databasequery()
        update_new_tsk.query_update_execution(dbconnection.cursor, "dashboar_task.update_task_status", ["(select id from dashboard_taskstatus where statusname = 'running') "], [str(task_list_item.task_id)])
        update_new_tsk.query_update_execution(dbconnection.cursor, "dashboar_task.update_task_stage", ["(select id from dashboard_taskcurrentstage where stagename = 'Complete') "], [str(task_list_item.task_id)])
        update_new_tsk.query_update_execution(dbconnection.cursor, "dashboar_task.update_task_status", ["(select id from dashboard_taskstatus where statusname = 'success') "], [str(task_list_item.task_id)])
        dbconnection.conn.commit()
        print("task update commited")
   
    
if __name__ == '__main__':
    main()