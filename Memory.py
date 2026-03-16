from ast import List
from imapclient import IMAPClient
from email.header import decode_header
import email as email_lib
from datetime import datetime
import os
from agent_config import AgentConfig

class Memory:
    def __init__(self):
        self.config = AgentConfig()
        self.work_memory = []
        self.context_memory = []
    def add_work_memory(self,message:str,status:str):
        self.work_memory.append({"message":message,"status":status})#添加任务到工作记忆
    
    def add_context_memory(self,message:str,role:str):
        self.context_memory.append({"message":message,"role":role})#添加上下文到上下文记忆  
    
    def get_work_memory(self):
        work_memory_str = ""
        for item in self.work_memory:
            work_memory_str += "任务："+ item["message"] + " 状态:"+ item["status"] + "\n"
        return work_memory_str

    def get_context_memory(self):
        context_memory_str = ""
        for item in self.context_memory:
            context_memory_str += "角色:" + item["role"] + " 内容:" + item["message"] + "\n"
        return context_memory_str

