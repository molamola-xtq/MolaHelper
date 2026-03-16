from ast import List
from imapclient import IMAPClient
from email.header import decode_header
import email as email_lib
from datetime import datetime
import os
from agent_config import AgentConfig
import email_get
from email_get import getter
from email_get import reader
from email_get import deler
from paper import arxiv_search




class tool:
    def __init__(self,config:AgentConfig,func:callable,parameters:dict):
        self.config = config
        self.func = func
        self.parameters = parameters
    def __str__(self):
        return f"tool(name={self.func.__name__},parameters={self.parameters})"
class skill:
    def __init__(self,name:str,content:str,description:str):
        self.name = name
        self.content = content
        self.description = description
    def __str__(self):
        return f"skill(name={self.name},description={self.description})"


def read_skill_list():
    skill_list = os.listdir("skills")
    res = []
    for i in skill_list:
        if i.endswith(".md"):
            res.append(i.replace(".md",""))
    skill_info = ""
    for i in res:
        with open("skills/" + i + ".info", "r") as f:
            skill_des = f.read()
            skill_info += "skill名称:" + i + " skill描述:" + skill_des + "\n"
    return skill_info#返回所有技能的信息

def read_skill(name:str):
    dir = "skills/" + name + ".md"
    if not os.path.exists(dir):
        return "ERROR:skill not found"
    with open(dir, "r") as f:
        skill = f.read()
    return ['OK',skill]#返回指定技能的内容

def reply(content:str):
    RED_DEEP = '\033[38;2;139;0;0m'  # 深红色（RGB:139,0,0）
    RESET = '\033[0m'  # 重置颜色，避免后续输出也变色
    content = content

    print(f"{RED_DEEP}{content}{RESET}")
    return "OK"

def read_skill_list():
    skill_list = os.listdir("skills")
    res = []
    for i in skill_list:
        if i.endswith(".md"):
            res.append(i.replace(".md",""))
    skill_info = ""
    for i in res:
        with open("skills/" + i + ".info", "r") as f:
            skill_des = f.read()
            skill_info += "skill名称:" + i + " skill描述:" + skill_des + "\n"
    return skill_info#返回所有技能的信息

def get_time():
    current_local_time = datetime.now()
    formatted_time = current_local_time.strftime("%Y-%m-%d %H:%M:%S")
    return ["OK",formatted_time]


class tool_config:
    def __init__(self,config:AgentConfig):
        self.config = config
        config = AgentConfig()
        gets = getter()
        reads = reader()
        dels = deler()


       
        self.tool_list = [
    tool(config,gets.email_get,{}),
    tool(config,reads.emails_read,{}),
    tool(config,dels.emails_del,{}),
    tool(config,reply,{"content":str}),
    tool(config,read_skill,{"name":str}),
    tool(config,get_time,{}),
    tool(config,arxiv_search,{"query":str,"max_results":int})

]

