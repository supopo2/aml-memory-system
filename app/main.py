from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI()

# 内存存储
memory_store = {}

# --- 数据模型 ---
class AddRequest(BaseModel):
    request_id: str
    messages: List[dict]
    user_id: str
    session_id: str

class SearchRequest(BaseModel):
    query: str
    user_id: str
    top_k: int = 100

# --- 鉴权函数 ---
def check_key(x_api_key: str):
    # 这里的密码必须和测试脚本里的 "my-secret-key-123" 一致
    if x_api_key != "my-secret-key-123":
        raise HTTPException(status_code=401, detail="Invalid API Key")

# --- 接口 ---
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/add")
def add_memory(req: AddRequest, x_api_key: str = Header(None)):
    check_key(x_api_key)
    
    # 拼装内容
    content = ""
    for m in req.messages:
        content += str(m.get("content", "")) + " "
    
    # 存入内存
    if req.user_id not in memory_store:
        memory_store[req.user_id] = []
    memory_store[req.user_id].append({
        "id": str(uuid.uuid4()),
        "content": content.strip()
    })
    
    return {"success": True, "request_id": req.request_id, "user_id": req.user_id, "session_id": req.session_id}

@app.post("/search")
def search_memory(req: SearchRequest, x_api_key: str = Header(None)):
    check_key(x_api_key)
    
    results = []
    user_memories = memory_store.get(req.user_id, [])
    
    # 简单的关键词匹配
    for m in user_memories:
        if req.query.lower() in m["content"].lower():
            results.append({"content": m["content"], "score": 1.0})
            
    return {"data": results[:req.top_k]}