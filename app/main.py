from fastapi import FastAPI
from app.routers import auth, checklist

app = FastAPI()
    
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(checklist.router, prefix="/checklist", tags=["Checklist"])

@app.get("/")
def read_root():
    return {"status": "The web server is working"}

