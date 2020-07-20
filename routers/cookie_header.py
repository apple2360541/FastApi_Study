from fastapi import APIRouter,Cookie,Header
from typing import List
app=APIRouter()

@app.get("/items/")
async def get_cookie(*,id:str=Cookie(None),name:str=Cookie(None),x_token:List[str]=Header(None),user_agent:str=Header(None)):
    return {"id":id,"name":name,"user_agent":user_agent,"x-token":x_token}

