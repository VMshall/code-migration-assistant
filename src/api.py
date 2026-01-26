from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.migrator import migrate_code
import traceback

app = FastAPI(title="Code Migration Assistant")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class MigrateRequest(BaseModel):
    source_code: str
    from_framework: str
    to_framework: str
    notes: str = ""


@app.post("/migrate")
async def migrate(req: MigrateRequest):
    if not req.source_code.strip():
        raise HTTPException(400, "Source code required")
    try:
        return migrate_code(req.source_code, req.from_framework, req.to_framework, req.notes)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, str(e))


@app.get("/health")
def health():
    return {"status": "ok"}


app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
