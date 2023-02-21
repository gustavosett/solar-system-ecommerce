from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import r as routers
from database import database
import uvicorn

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

for router in routers:
    app.include_router(router)
    
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")