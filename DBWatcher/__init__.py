from DBWatcher import *

def main():
    dbconnection = databaseconfig()
    select_new_tsk = databasequery()
    select_new_tsk.query_select_execution(dbconnection.cursor, "dashboar_task.select_pre-start_task")
    dbconnection.disconnect()
    
if __name__ == '__main__':
    main()