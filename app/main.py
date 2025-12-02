from fastapi import FastAPI
from app.routers import auth, checklist
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8081",
    "http://192.168.1.37:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(checklist.router, prefix="/checklist", tags=["Checklist"])

@app.get("/")
def read_root():
    return {"status": "The web server is working"}

