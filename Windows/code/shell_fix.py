import requests
import json
import subprocess
import os
import sys

# 定义基础URL和sessionid
base_url = "your_base_url"
sessionid = "your_session_id"

# 设置标准输出编码为utf-8
sys.stdout.reconfigure(encoding='utf-8')

class ShellFix:
    def __init__(self):
        self.base_url = base_url
        self.sessionid = sessionid
        self.headers = {
            "Authorization": f"Bearer {self.sessionid}"
        }
        self.conversation_id = None
        
        if os.name == 'nt':  # Windows系统
            self.history_file = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'PowerShell', 'PSReadLine', 'ConsoleHost_history.txt')
        else:  # Unix类系统
            self.history_file = os.path.expanduser("~/.bash_history")

    def get_last_failed_command(self):
        """获取最后一条失败的命令"""
        try:
            if not os.path.exists(self.history_file):
                return None, "找不到命令历史文件"
                
            with open(self.history_file, 'r', encoding='utf-8', errors='ignore') as f:
                commands = f.readlines()
            
            if not commands:
                return None, "没有找到命令历史记录"
            
            # 获取最后一条命令（跳过当前shell_fix.py的执行命令）
            for cmd in reversed(commands[:-1]):
                cmd = cmd.strip()
                if cmd and not any(ignore in cmd for ignore in ["python .\\shell_fix.py", "python ./shell_fix.py"]):
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='ignore'
                    )
                    if result.returncode != 0:
                        return cmd, result.stderr
            
            return None, "没有找到最近失败的命令"
                
        except Exception as e:
            return None, f"读取命令历史时出错: {str(e)}"

    def get_fix_suggestion(self, command, error):
        """使用AI获取修复建议"""
        prompt = f"""
        以下命令执行失败：
        ```
        {command}
        ```
        
        错误信息：
        ```
        {error}
        ```
        
        请你按照以下格式分析错误原因并给出Windows用户修正后的命令建议，其中错误原因尽量简洁，修改建议只给出命令。
        错误原因：

        修改建议：
        """
        
        payload = {
            "model": "doubao",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": True
        }
        
        if self.conversation_id:
            payload["conversation_id"] = self.conversation_id

        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=self.headers,
                json=payload,
                stream=True
            )
            
            if response.status_code == 200:
                suggestion = ""
                for chunk in response.iter_lines():
                    if chunk:
                        chunk_data = chunk.decode('utf-8').strip()
                        if chunk_data == "data: [DONE]":
                            break
                        if chunk_data.startswith("data:"):
                            try:
                                chunk_json = json.loads(chunk_data[5:])
                                if "choices" in chunk_json and chunk_json["choices"]:
                                    delta = chunk_json["choices"][0]["delta"]
                                    if "content" in delta:
                                        suggestion += delta["content"]
                            except json.JSONDecodeError:
                                continue
                
                return suggestion
            else:
                return f"获取建议时出错: {response.status_code}"
                
        except Exception as e:
            return f"连接AI服务时出错: {str(e)}"

def main():
    fixer = ShellFix()
    
    print("正在分析最后执行的命令...")
    command, error = fixer.get_last_failed_command()
    
    if command:
        print(f"\n执行失败的命令: {command}")
        print(f"\n错误信息:\n{error}")
        
        print("\n正在获取修复建议...")
        suggestion = fixer.get_fix_suggestion(command, error)
        
        print(f"\n修复建议:\n{suggestion}")
    else:
        print(f"\n提示: {error}")

if __name__ == "__main__":
    main()