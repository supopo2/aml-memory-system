import requests
import json

# 你设置的保护密码
headers = {
    "X-Api-Key": "my-secret-key-123",
    "Content-Type": "application/json"
}

# 1. 测试 /add
add_data = {
    "request_id": "test-001",
    "messages": [
        {"role": "user", "content": "I love apples and bananas"}
    ],
    "user_id": "user_1",
    "session_id": "session_1"
}

print("--- 测试写入 (Add) ---")
res_add = requests.post("http://127.0.0.1:8080/add", headers=headers, json=add_data)
print(f"状态码: {res_add.status_code}")
print(f"返回结果: {res_add.text}\n")


# 2. 测试 /search
search_data = {
    "query": "apples",
    "user_id": "user_1",
    "top_k": 10
}

print("--- 测试检索 (Search) ---")
res_search = requests.post("http://127.0.0.1:8080/search", headers=headers, json=search_data)
print(f"状态码: {res_search.status_code}")
print(f"返回结果: {res_search.text}\n")