from DBWatcher import *
from Task import *

def main():
    dbconnection = databaseconfig()
    select_new_tsk = databasequery()
    new_task_db_result = select_new_tsk.query_select_execution(dbconnection.cursor, "dashboar_task.select_pre-start_task",['1'])
    new_task_list = []
    
    for task_db_row in new_task_db_result:
        task_list_item = TaskStage(task_db_row)
        new_task_list.append(task_list_item)
    
    for task_list_item in new_task_list:
        task_list_item.executestage()
        update_new_tsk = databasequery()
        update_new_tsk.query_update_execution(dbconnection.cursor, "dashboar_task.update_task_status", ["(select id from dashboard_taskstatus where statusname = 'running') "], ['3'])
        update_new_tsk.query_update_execution(dbconnection.cursor, "dashboar_task.update_task_stage", ["(select id from dashboard_taskcurrentstage where stagename = 'Complete') "], ['3'])
        update_new_tsk.query_update_execution(dbconnection.cursor, "dashboar_task.update_task_status", ["(select id from dashboard_taskstatus where statusname = 'success') "], ['3'])
        dbconnection.conn.commit()
        print("task update commited")
    dbconnection.disconnect()    
if __name__ == '__main__':
    main()