# app/main.py
from fastapi import FastAPI
from app.api.routes import router
from app.database.mongodb import init_db

app = FastAPI(title="Depression Analysis API")

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)