from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from caching.cache_manager import CacheManager

app = FastAPI()

sessions = {}

class CacheItem(BaseModel):
    key: str
    value: str

@app.post("/session/create/{session}")
def create_session(session):
    cache_manager = CacheManager(session)
    sessions[session] = cache_manager
    return {"message": f"Created new session with session id: {session}"}

@app.get("/cache/get/{session}/{key}")
def get_cached_data(session, key):
    cache_manager = sessions.get(session)
    
    if cache_manager is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    value = cache_manager.get(key)
    return {"message": "success", "key": key, "value": value}

@app.post("/cache/set/{session}")
def store_cache(session, body: CacheItem):
    cache_manager: CacheManager = sessions[session]
    if cache_manager is None:
        raise HTTPException(status_code=404, detail="Session not found")
    cache_manager.set(body.key, body.value)
    return {"message": "success"}