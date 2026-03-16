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



class getter:
    def __init__(self):
        self.config = AgentConfig()

    def email_get(self):
        for client in self.config.email_client_list:
            
            email_client = EmailClient(client.email, client.password, client.imap_server, client.smtp_port)
            email_loader = EmailLoader()
            emails = email_client.get_unread_emails()
            email_loader.save(emails)
        return "OK"
    #直接调用getter就是一个工具函数

class reader:
    def __init__(self,dir = 'emails'):
        self.config = AgentConfig()
        self.dir = dir
    def emails_read(self):
        email_loader = EmailLoader()
        emails = email_loader.load(self.dir)
    
        return ['OK',emails]

class deler:
    def __init__(self,dir = 'emails'):
        self.dir = dir
        
    def emails_del(self):
        
        for email in os.listdir(self.dir):
            os.remove(f"{self.dir}/{email}")
         
        return "OK"









