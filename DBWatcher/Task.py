'''
Created on Dec 30, 2017

@author: Andy
'''
import os
import sys
from sqlite3 import Timestamp

class TaskStage():
    
    task_id = None
    stage_id = None
    stage_program_host = None
    stage_name = None
    binary_path = None
    success_code = None
    
    def __init__(self,dbextract):
        self.task_id = dbextract["task_id"]
        self.stage_id = dbextract["stage_id"]
        self.stage_program_host = dbextract["binary_host"]
        self.stage_name = dbextract["stage_name"]
        self.binary_path = dbextract["binary_path"]
        self.success_code = dbextract["success_return_code"]
    
    def executestage(self):
        if self.stage_program_host != "localhost":
            print("host of binary is on another computer")
        
        command = "python "+ self.binary_path
        returncode = os.system(command)
        if str(returncode) == str(self.success_code):
            print(returncode)
            print("success execution on task")
            return True
        else:
            print(returncode)
            print("failure execution on task")
            return False

class TaskActionItem():
    id = None
    Taskid = None
    TaskAction = None
    ActionTime = None
    ActionType = None
    def __init__(self,Action,Timestamp,ActionType):
        self.TaskAction = Action
        self.ActionTime = Timestamp
        self.ActionType = ActionType
    
    

#class Task():
#    def __init__(self,dbextract):        