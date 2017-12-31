from DBWatcher import *
from Task import *

def main():
    dbconnection = databaseconfig()
    select_new_tsk = databasequery()
    new_task_db_result = select_new_tsk.query_select_execution(dbconnection.cursor, "dashboar_task.select_pre-start_task")
    dbconnection.disconnect()
    new_task_list = []
    
    for task_db_row in new_task_db_result:
        task_list_item = TaskStage(task_db_row)
        new_task_list.append(task_list_item)
    
    for task_list_item in new_task_list:
        task_list_item.executestage()
        
if __name__ == '__main__':
    main()