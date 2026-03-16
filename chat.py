import requests
import json
from Memory import Memory
from agent_config import AgentConfig
import json
from caller import caller
from tool_config import read_skill_list
from logo import print_mola_helper



class chat:
    def __init__(self,memory:Memory,config:AgentConfig):
        self.memory = memory
        self.config = config
        self.model = config.model
        self.url = config.url
        self.provider = config.provider
        self.headers = {"Content-Type": "application/json"}
        
        if self.provider != "ollama" and config.api_key:
            self.headers["Authorization"] = f"Bearer {config.api_key}"

    def chat(self,message:list):
        payload = self._build_payload(message)
        
        response = requests.post(
            self.url,
            headers=self.headers,
            json=payload
        )

        res = response.json()
        
        return self._parse_response(res)
    
    def _build_payload(self, message:list):
        if self.provider == "doubao":
            user_content = ""
            for msg in message:
                if msg["role"] == "user":
                    user_content += msg["content"]
                elif msg["role"] == "system":
                    user_content = msg["content"] + "\n" + user_content
            
            return {
                "model": self.model,
                "input": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": user_content
                            }
                        ]
                    }
                ]
            }
        elif self.provider == "siliconflow":
            return {
                "model": self.model,
                "messages": message
            }
        else:
            return {
                "model": self.model,
                "messages": message,
                "thinking": False
            }
    
    def _parse_response(self, res):
        if self.provider == "doubao":
           
            if "output" in res and len(res["output"]) > 0:
                # 查找message类型的output
                message_output = None
                for item in res["output"]:
                    if item.get("type") == "message" and item.get("role") == "assistant":
                        message_output = item
                        break
                
                if message_output:
                    
                    if "content" in message_output and len(message_output["content"]) > 0:
                        content_item = message_output["content"][0]
                        if "text" in content_item:
                            assistant_message = content_item["text"]
                        else:
                            assistant_message = str(content_item)
                    else:
                        assistant_message = str(message_output)
                else:
                    # 如果没有找到message类型，尝试使用第一个output
                    output_item = res["output"][0]
                   
                    if "content" in output_item:
                        if isinstance(output_item["content"], list) and len(output_item["content"]) > 0:
                            if "text" in output_item["content"][0]:
                                assistant_message = output_item["content"][0]["text"]
                            else:
                                assistant_message = str(output_item["content"][0])
                        else:
                            assistant_message = str(output_item["content"])
                    elif "text" in output_item:
                        assistant_message = output_item["text"]
                    else:
                        assistant_message = str(output_item)
                
              
                self.memory.add_context_memory(assistant_message,"assistant")
                return assistant_message
            else:
                print("响应格式异常:", res)
                return "出现错误"
        elif self.provider == "siliconflow":
            if "choices" in res and len(res["choices"]) > 0:
                message = res["choices"][0]["message"]
                assistant_message = message.get("content", "")
                self.memory.add_context_memory(assistant_message,"assistant")
                return assistant_message
            else:
                print("响应格式异常:", res)
                return "出现错误"
        else:
            if "choices" in res and len(res["choices"]) > 0:
                assistant_message = res["choices"][0]["message"]["content"]
                self.memory.add_context_memory(assistant_message,"assistant")
                return assistant_message
            else:
                print("响应格式异常:", res)
                return "出现错误"
        
class Parser:
    def __init__(self):
        pass
    def parse(self,order:str):
        ordders = ''
        try:
            order = order.strip()
          
            flag = 0
            for i in order:
               
                if i == '{' and flag == 0:
                    flag = 1
                 
                if flag == 0:
                    continue
                if flag == 1:
                    ordders += i
                    if i == '}':
                        break
               
            
            json_message = json.loads(ordders)
            return json_message
        except:
            print("json解析异常:", ordders)
            return "ERROR:json解析异常"

        
    



def main():
    print_mola_helper()
    print("\033[91mWelcome to use MOLA Helper! you can ask me any questions and I will help you. if you want to quit, please input '/quit'\033[0m")
    memory = Memory()
    config = AgentConfig()
    chater = chat(memory,config)
    parser = Parser()
    callers = caller(config)
    working = False


    task_response = ''
    while True:
        content = ''
        if working == False: 
            content = input("请输入：")
            if content == '/quit':
                break
        else:
            content = "工具调用的回复：" +  task_response
        system_prompt = "系统提示词：" + config.system_prompt
        context_memory = memory.get_context_memory()
       
       
        work_memory = memory.get_work_memory()
        if len(work_memory) == 0:
            work_memory = "无"
        work_memory = "\n工作记忆:" + work_memory
        
        if len(context_memory) == 0:
            context_memory = "无"
        context = "\n历史对话:" + context_memory  + '\n'
        system_prompt += context
        skill_info = read_skill_list()
        system_prompt += "你可以使用的skill名和skill描述如下：\n" + skill_info
        system_prompt += '当用户提出需求时，你可根据任务内容与提供的技能（skill）描述，选择合适的技能。你需要先调用read_skill工具来查看所需技能的信息。请严格按照以下格式输出 JSON：\n'
        system_prompt += '{"tool":"read_skill","name":"skill名称"}'
        system_prompt += '如果你在调用一个工具的时候出现了问题，你要检查自己的命令是否正确，然后再调用一下，如果连续三次出错，你要给用户一个错误提示：调用工具出错\n'
       

        contents = "本轮用户输入:" + content
     

        message = [{"role": "system", "content": system_prompt},{"role": "user", "content": contents}]
        memory.add_context_memory(content,"user")
        assistant_message = chater.chat(message)
        
        json_message = parser.parse(assistant_message)
     


        
        
        
        if json_message == "ERROR:json解析异常":
            working = True
            task_response = json_message
            memory.add_work_memory(task_response,"ERROR")
            continue
        else:
            para = {}
            try:
                tool_name = json_message["tool"]
            except:
                working = True
                task_response = "ERROR:json解析异常"
                memory.add_work_memory(task_response,"ERROR")
                continue
            for pair in json_message:
                if pair != "tool":
                    para[pair] = json_message[pair]

            
            task = callers.call_tool(tool_name,para)
            if tool_name == "reply":
                working = False
                message = ''
                if type(task) != str:
                    message = task[0]
                else:
                    message = task
                memory.add_work_memory("调用工具" + tool_name ,"OK")
               
                continue
            else:
                working = True
                message = ''
                if type(task) != str:
                    message = task[0]
                    task_response = task[1]
                else :
                    message = task
                    task_response = message
                memory.add_work_memory("调用工具" + tool_name ,message)
                print("****调用工具" + tool_name +" "+ message+"****")
                continue
    
    print("See you next time!")
        
            
       
     
        

        

       
      
main()
        


