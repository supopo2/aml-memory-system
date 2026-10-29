from fastapi import FastAPI, Header, HTTPException, Request, Response
from typing import List, Optional
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
def check_key(x_api_key: Optional[str] = Header(None), authorization: Optional[str] = Header(None)):
    expected_key = "my-secret-key-123"
    
    # 1. 检查 X-Api-Key
    if x_api_key == expected_key:
        return
        
    # 2. 检查 Authorization: Token 或 Bearer
    if authorization:
        # 把 "Token xxx" 或 "Bearer xxx" 拆开，拿到后面的 xxx
        parts = authorization.split(" ")
        if len(parts) == 2 and parts[1] == expected_key:
            return
            
    # 如果都不对，拦截
    raise HTTPException(status_code=401, detail="Invalid API Key")

# --- 接口 ---
@app.get("/health")
def health():
    return {"status": "ok"}

@app.api_route("/add", methods=["POST", "HEAD"])
def add_memory(request: Request, req: Optional[AddRequest] = None, x_api_key: Optional[str] = Header(None), authorization: Optional[str] = Header(None)):
    # ⚠️ 遇到 HEAD 请求，直接返回 200
    if request.method == "HEAD":
        return Response(status_code=200)
        
    check_key(x_api_key, authorization)
    
    if not req:
        raise HTTPException(status_code=400, detail="Missing body")

    # ... 下面是你原本的 add 逻辑，保持不变 ...
    content = ""
    for m in req.messages:
        content += str(m.get("content", "")) + " "
    
    if req.user_id not in memory_store:
        memory_store[req.user_id] = []
    memory_store[req.user_id].append({"id": str(uuid.uuid4()), "content": content.strip()})
    
    return {"success": True, "request_id": req.request_id, "user_id": req.user_id, "session_id": req.session_id}


@app.api_route("/search", methods=["POST", "HEAD"])
def search_memory(request: Request, req: Optional[SearchRequest] = None, x_api_key: Optional[str] = Header(None), authorization: Optional[str] = Header(None)):
    # ⚠️ 遇到 HEAD 请求，直接返回 200
    if request.method == "HEAD":
        return Response(status_code=200)
        
    check_key(x_api_key, authorization)
    
    if not req:
        raise HTTPException(status_code=400, detail="Missing body")

    # ... 下面是你原本的 search 逻辑，保持不变 ...
    results = []
    user_memories = memory_store.get(req.user_id, [])
    for m in user_memories:
        if req.query.lower() in m["content"].lower():
            results.append({"content": m["content"], "score": 1.0})
            
    return {"data": results[:req.top_k]}