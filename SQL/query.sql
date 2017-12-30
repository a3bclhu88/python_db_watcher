select T.taskname as task_name, T.taskprogress as task_progress, TS.statusname as status_name,Ts.id as task_id,TCS.stagename as stage_name,E.binaryhost as binary_host,E.binarypath as binary_path, R.returncodevalue as success_return_code
from dashboard_task as T join dashboard_taskstatus as TS on TS.id = T.taskstatus_id join dashboard_taskcurrentstage as TCS on TCS.id = T.taskcurrentstage_id
join dashboard_executable as E on E.id = TCS.stageprogram_id join dashboard_returncode as R on R.id = E.codesuccess_id
where Ts.id = 1;

