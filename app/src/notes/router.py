from fastapi import APIRouter, Depends
from .dto import  *
from app.src.common.crypto import bearer, user_payload
from .service import NoteService


router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"message": "Not found"}},
)


@router.get('/{space_id}', dependencies=[Depends(bearer)])
async def get_notes(space_id: str, token: str = Depends(bearer)):
    return await NoteService.get_notes(space_id)


@router.post('/{space_id}')
async def create_note(space_id: str, note: CreateNoteDto, token: str = Depends(bearer)):
    return await NoteService.create_note(space_id, note, user_payload(token))


@router.patch('/{note_id}')
async def update_note(note_id: str, note: UpdateNoteDto, token: str = Depends(bearer)):
    await NoteService.check_right_for_edit_note(user_payload(token), note_id)
    return await NoteService.update_note(note_id, note)


@router.delete('/{note_id}')
async def delete_note(note_id: str, token: str = Depends(bearer)):
    await NoteService.check_right_for_edit_note(user_payload(token), note_id)
    return await NoteService.delete_note(note_id)
