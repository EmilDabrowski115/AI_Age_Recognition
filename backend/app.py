from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="AI Age Recognition")

# Health endpoint
@app.get("/health")
def health_check():
    return JSONResponse({"status": "ok", "message": "API is running"})





