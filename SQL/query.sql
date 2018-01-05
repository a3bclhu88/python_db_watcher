select T.id as task_id,T.taskname as task_name, T.taskprogress as task_progress, TS.statusname as status_name,Ts.id as status_id,TCS.stagename as stage_name,TCS.id as stage_id,E.binaryhost as binary_host,E.binarypath as binary_path, R.returncodevalue as success_return_code
from dashboard_task as T join dashboard_taskstatus as TS on TS.id = T.taskstatus_id join dashboard_taskcurrentstage as TCS on TCS.id = T.taskcurrentstage_id
join dashboard_executable as E on E.id = TCS.stageprogram_id join dashboard_returncode as R on R.id = E.codesuccess_id
where Ts.id = 1 and taskstarttime < now();

update dashboard_task set taskstatus_id = (select id from dashboard_taskstatus where statusname = 'running') where id = 3;

update dashboard_task set taskcurrentstage_id = (select id from dashboard_taskcurrentstage where stagename = 'Complete') where id = 3;

update dashboard_task set taskstatus_id = (select id from dashboard_taskstatus where statusname = 'success') where id = 3;

rollback;


select TCS.id as stage_id, T.id as task_id, T.taskname as task_name, T.taskprogress as task_progress, TS.statusname as task_name,Ts.id as task_id,TCS.stagename as stage_name,E.binaryhost as binary_host,E.binarypath as binary_path, R.returncodevalue as success_return_code from dashboard_task as T join dashboard_taskstatus as TS on TS.id = T.taskstatus_id join dashboard_taskcurrentstage as TCS on TCS.id = T.taskcurrentstage_id join dashboard_executable as E on E.id = TCS.stageprogram_id join dashboard_returncode as R on R.id = E.codesuccess_id;