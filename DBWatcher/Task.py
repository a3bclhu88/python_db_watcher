'''
Created on Dec 30, 2017

@author: Andy
'''
import os
import sys

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
        
        print(returncode)
        

#class Task():
#    def __init__(self,dbextract):        