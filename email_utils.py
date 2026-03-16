from ast import List
from imapclient import IMAPClient
from email.header import decode_header
import email as email_lib
from datetime import datetime
import os
import ssl



class Email:
    def __init__(self, uid, subject, sender, date, content, has_attachments):
        self.uid = uid
        self.subject = subject
        self.sender = sender
        self.date = date
        self.content = content
        self.has_attachments = has_attachments
    
    def __str__(self):
        return f"""邮件信息:
  UID: {self.uid}
  主题: {self.subject}
  发件人: {self.sender}
  时间: {self.date}
  有附件: {'是' if self.has_attachments else '否'}
  内容预览: {self.content}"""


class EmailClient:
    def __init__(self, email, password, imap_server="imap.163.com", port=993):
        """初始化邮件客户端"""
        self.email = email
        self.password = password
        self.imap_server = imap_server
        self.port = port
        self.server = None
    
    def _connect(self):
        """建立IMAP连接"""
        if not self.server:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            self.server = IMAPClient(self.imap_server, ssl=True, port=self.port, ssl_context=ssl_context)
            self.server.login(self.email, self.password)
            self.server.id_({"name": "IMAPClient", "version": "2.1.0"})
    
    def _disconnect(self):
        """关闭连接"""
        if self.server:
            self.server.logout()
            self.server = None
    
    def _parse_address(self, address):
        """解析邮件地址"""
        if not address:
            return "未知", "未知"
        
        email = "未知"
        name = ""
        
        if isinstance(address, tuple):
            email = address[0] if address[0] else "未知"
            if len(address) > 1 and address[1]:
                name = address[1]
        elif hasattr(address, 'addr'):
            email = address.addr or "未知"
            name = address.name or ""
        else:
            return str(address), "未知"
        
        if name:
            if isinstance(name, bytes):
                name = name.decode('utf-8')
            if isinstance(name, str):
                decoded = decode_header(name)[0]
                if isinstance(decoded[0], bytes):
                    name = decoded[0].decode(decoded[1] or 'utf-8')
                else:
                    name = decoded[0]
        
        return name or email, email
    
    def _parse_subject(self, subject):
        """解析邮件主题"""
        if not subject:
            return "无主题"
        if isinstance(subject, bytes):
            subject = subject.decode('utf-8')
        decoded = decode_header(subject)[0]
        if isinstance(decoded[0], bytes):
            return decoded[0].decode(decoded[1] or 'utf-8')
        return decoded[0]
    
    def _decode_content(self, content_bytes):
        """智能解码内容，尝试多种编码"""
        if not content_bytes:
            return ""
        
        encodings = ['utf-8', 'gbk', 'gb2312', 'iso-8859-1']
        for encoding in encodings:
            try:
                return content_bytes.decode(encoding)
            except:
                continue
        # 最后尝试忽略错误
        return content_bytes.decode('utf-8', errors='ignore')
    
    def get_unread_emails(self):
        """获取所有未读邮件"""
        self._connect()
        
        try:
            self.server.select_folder('INBOX')
            message_ids = self.server.search(['UNSEEN'])
          
            
            emails = []
            num = 0
            for msg_id in message_ids:
                msg_data = self.server.fetch(msg_id, ['ENVELOPE', 'BODYSTRUCTURE', 'BODY[]'])
                
                for uid, data in msg_data.items():
                    envelope = data[b'ENVELOPE']
                    body_structure = data.get(b'BODYSTRUCTURE', b'')
                    raw_body = data.get(b'BODY[]', b'')
                    
                    subject = self._parse_subject(envelope.subject)
                    sender_name, sender_email = self._parse_address(envelope.from_)
                    sender = f"{sender_name} <{sender_email}>"
                    
                    date = envelope.date
                    if date:
                        date_str = date.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        date_str = "未知"
                    
                    has_attachments = False
                    if body_structure:
                        body_str = str(body_structure)
                        has_attachments = 'attachment' in body_str.lower()
                    
                    content = ""
                    if raw_body:
                        try:
                            msg = email_lib.message_from_bytes(raw_body)
                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    if content_type in ['text/plain', 'text/html']:
                                        try:
                                            part_content = part.get_payload(decode=True)
                                            if part_content:
                                                content = self._decode_content(part_content)
                                                if content_type == 'text/plain':
                                                    break
                                        except:
                                            continue
                            else:
                                content_type = msg.get_content_type()
                                if content_type in ['text/plain', 'text/html']:
                                    part_content = msg.get_payload(decode=True)
                                    if part_content:
                                        content = self._decode_content(part_content)
                        except Exception as e:
                            content = f"解析失败: {e}"
                    
                    email_obj = Email(uid, subject, sender, date_str, content.strip(), has_attachments)
                    emails.append(email_obj)
                
                    num += 1
            
            return emails
        finally:
            self._disconnect()
    
    def get_latest_emails(self, max_count=10):
        """获取最新邮件"""
        self._connect()
        
        try:
            self.server.select_folder('INBOX')
            message_ids = self.server.search(['ALL'])
            latest_ids = message_ids[-max_count:]
            
            emails = []
            for msg_id in reversed(latest_ids):
                msg_data = self.server.fetch(msg_id, ['ENVELOPE', 'BODYSTRUCTURE', 'BODY[]'])
                
                for uid, data in msg_data.items():
                    envelope = data[b'ENVELOPE']
                    body_structure = data.get(b'BODYSTRUCTURE', b'')
                    raw_body = data.get(b'BODY[]', b'')
                    
                    subject = self._parse_subject(envelope.subject)
                    sender_name, sender_email = self._parse_address(envelope.from_)
                    sender = f"{sender_name} <{sender_email}>"
                    
                    date = envelope.date
                    if date:
                        date_str = date.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        date_str = "未知"
                    
                    has_attachments = False
                    if body_structure:
                        body_str = str(body_structure)
                        has_attachments = 'attachment' in body_str.lower()
                    
                    content = ""
                    if raw_body:
                        try:
                            msg = email_lib.message_from_bytes(raw_body)
                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    if content_type in ['text/plain', 'text/html']:
                                        try:
                                            content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                            if content_type == 'text/plain':
                                                break
                                        except:
                                            continue
                            else:
                                content_type = msg.get_content_type()
                                if content_type in ['text/plain', 'text/html']:
                                    content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                        except Exception as e:
                            content = f"解析失败: {e}"
                    
                    email_obj = Email(uid, subject, sender, date_str, content.strip(), has_attachments)
                    emails.append(email_obj)
            
            return emails
        finally:
            self._disconnect()


        
class EmailLoader:
    def __init__(self):
        self.email = None
        
    def save(self,email,dir = 'emails'):
        self.email = email
        for email in self.email:
            
            with open(f"{dir}/{email.uid}.txt", "w", encoding="utf-8") as f:
                f.write(email.__str__())
    
    def load(self,dir):
        all = ''
        for email in os.listdir(dir):
            with open(f"{dir}/{email}", "r", encoding="utf-8") as f:
                all = all + f.read()
        return all


class client_data:
    def __init__(self, email, password, imap_server,  smtp_port):
        self.email = email
        self.password = password
        self.imap_server = imap_server
        self.smtp_port = smtp_port

