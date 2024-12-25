from pydantic import BaseModel
from datetime import datetime
from typing import Dict

class NoteResponse(BaseModel):
    created_at: datetime
    updated_at: datetime

class NoteTextResponse(BaseModel):
    id: int
    text: str

class CreateNoteResponse(BaseModel):
    id: int

class NoteListResponse(BaseModel):
    list: Dict[int, int]
