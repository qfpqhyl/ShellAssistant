import requests
import json

# 定义基础URL和sessionid
base_url = "your_base_url"
sessionid = "your_session_id"

# 定义请求头
headers = {
    "Authorization": f"Bearer {sessionid}"
}

def get_response(message):
    # 构建请求数据
    system_prompt = "你是一个shell命令助手。对于Windows用户的每个问题，你都需要推荐合适的shell命令。请严格按照以下格式回答：\n回答：[解释为什么推荐这个命令，解释清楚且简介]，\n建议命令："
    
    payload = {
        "model": "doubao",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": True
    }
    
    # 发送请求
    response = requests.post(
        f"{base_url}/v1/chat/completions", 
        headers=headers, 
        json=payload, 
        stream=True
    )
    
    if response.status_code == 200:
        response_text = ""
        print("Shell助手：")
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
                                print(delta["content"], end='', flush=True)
                                response_text += delta["content"]
                    except json.JSONDecodeError:
                        continue
        
        print()  # 换行
        return response_text
    else:
        return f"错误: {response.status_code}"

def main():
    print("请描述你想要完成的任务，助手会推荐合适的shell命令。")
    user_input = input("你的问题: ")
    get_response(user_input)

if __name__ == "__main__":
    main()