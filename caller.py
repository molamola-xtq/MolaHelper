from ast import List
from imapclient import IMAPClient
from email.header import decode_header
import email as email_lib
from datetime import datetime
from email_utils import Email
from email_utils import EmailClient
from email_utils import EmailLoader
from agent_config import AgentConfig
import os
from tool_config import tool
from tool_config import tool_config

class caller:
    def __init__(self,config:AgentConfig):
        self.config = config
        self.tool_config = tool_config(config)
        self.tools = self.tool_config.tool_list
        

    def add_tool(self,tool):
        self.tools.append(tool)
        
    def get_tools(self):
        return self.tools

    def call_tool(self,tool_name:str,parameters:dict):
        for tool in self.tools:
            if tool.func.__name__ == tool_name:
                for param in tool.parameters:
                    if (param not in parameters) or (not isinstance(parameters[param],tool.parameters[param])):
                        return "ERROR:parameter not found or not the right type"
                return tool.func(**parameters)
        return "ERROR:tool not found，please check the tool name and follow the tool description"

