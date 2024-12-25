from fastapi import APIRouter, HTTPException, Depends, Query
import os
from model import *

api_router = APIRouter()

NOTES_DIR = "notes"
TOKENS_FILE = "tokens.txt"

def load_token(token: str = Query(...)):
    with open(TOKENS_FILE, "r") as f:
        tokens = f.read().splitlines()
    if token not in tokens:
        raise HTTPException(status_code=403, detail="Invalid token")

@api_router.post("/note", response_model=CreateNoteResponse)
def create_note(token: str = Depends(load_token)):
    note_id = len(os.listdir(NOTES_DIR)) + 1
    time = datetime.now().isoformat()
    note_path = os.path.join(NOTES_DIR, f"{note_id}.txt")
    with open(note_path, "w") as f:
        f.write(f"created_at:{time}\nupdated_at:{time}\ntext:\n")
    return CreateNoteResponse(id=note_id)

@api_router.get("/note/{note_id}", response_model=NoteTextResponse)
def get_note_text(note_id: str, token: str = Depends(load_token)):
    note_path = os.path.join(NOTES_DIR, f"{note_id}.txt")
    if not os.path.exists(note_path):
        raise HTTPException(status_code=404, detail="Note not found")
    with open(note_path, "r") as f:
        lines = f.readlines()
    text = "".join(line.split(":", 1)[1] for line in lines if line.startswith("text"))
    return NoteTextResponse(id=note_id, text=text.strip())

@api_router.get("/note-info/{note_id}", response_model=NoteResponse)
def get_note_info(note_id: str, token: str = Depends(load_token)):
    note_path = os.path.join(NOTES_DIR, f"{note_id}.txt")
    if not os.path.exists(note_path):
        raise HTTPException(status_code=404, detail="Note not found")
    with open(note_path, "r") as f:
        lines = f.readlines()
    created_at = "".join(line.split(":", 1)[1] for line in lines if line.startswith("created_at"))
    updated_at = "".join(line.split(":", 1)[1] for line in lines if line.startswith("updated_at"))
    return NoteResponse(created_at=datetime.fromisoformat(created_at.strip()), updated_at=datetime.fromisoformat(updated_at.strip()))

@api_router.patch("/note/{note_id}")
def update_note(note_id: str, text: str, token: str = Depends(load_token)):
    note_path = os.path.join(NOTES_DIR, f"{note_id}.txt")
    if not os.path.exists(note_path):
        raise HTTPException(status_code=404, detail="Note not found")
    time = datetime.now().isoformat()
    with open(note_path, "r") as f:
        lines = f.readlines()
    with open(note_path, "w") as f:
        for line in lines:
            if line.startswith("updated_at"):
                f.write(f"updated_at:{time}\n")
            elif line.startswith("text"):
                f.write(f"text:{text}\n")
            else:
                f.write(line)
    return {"status": "updated"}

@api_router.delete("/note/{note_id}")
def delete_note(note_id: str, token: str = Depends(load_token)):
    note_path = os.path.join(NOTES_DIR, f"{note_id}.txt")
    if not os.path.exists(note_path):
        raise HTTPException(status_code=404, detail="Note not found")
    os.remove(note_path)
    return {"status": "deleted"}

@api_router.get("/note", response_model=NoteListResponse)
def list_notes(token: str = Depends(load_token)):
    note_ids = [file.split(".")[0] for file in os.listdir(NOTES_DIR) if file.endswith(".txt")]
    return NoteListResponse(list={idx: note_id for idx, note_id in enumerate(note_ids)})


