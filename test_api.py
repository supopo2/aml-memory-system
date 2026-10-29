import requests

# 你的公网基础地址
BASE_URL = "https://aml-memory-api-whktvwewcc.cn-hangzhou.fcapp.run"

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
# ⚠️ 注意这里：加了 /add
res_add = requests.post(f"{BASE_URL}/add", headers=headers, json=add_data)
print(f"状态码: {res_add.status_code}")
print(f"返回结果: {res_add.text}\n")


# 2. 测试 /search
search_data = {
    "query": "apples",
    "user_id": "user_1",
    "top_k": 10
}

print("--- 测试检索 (Search) ---")
# ⚠️ 注意这里：加了 /search
res_search = requests.post(f"{BASE_URL}/search", headers=headers, json=search_data)
print(f"状态码: {res_search.status_code}")
print(f"返回结果: {res_search.text}\n")