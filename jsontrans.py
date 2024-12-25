from model import *
from datetime import datetime

response1 = NoteResponse(
    created_at = datetime.now(),
    updated_at = datetime.now()
)
print(response1.model_dump_json())

response2 = NoteTextResponse(
    id=123,
    text='sdjhskdhsdjh'
)
print(response2.model_dump_json())

response3 = CreateNoteResponse(
    id=123
)
print(response3.model_dump_json())

response4 = NoteListResponse(
    list={
        0: 769,
        1: 123,
        2: 456
    }
)
print(response4.model_dump_json())