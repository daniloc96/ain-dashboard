from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import get_db
from services.mock_data import is_demo_mode, get_mock_todos

router = APIRouter(
    prefix="/api/v1/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if is_demo_mode():
        return [schemas.Todo(**todo) for todo in get_mock_todos()]
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

@router.post("/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    if is_demo_mode():
        # In demo mode, return a fake created todo (won't persist)
        return schemas.Todo(id=999, title=todo.title, completed=todo.completed, order=99)
    return crud.create_todo(db=db, todo=todo)

@router.put("/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    if is_demo_mode():
        return schemas.Todo(id=todo_id, title=todo.title, completed=todo.completed, order=0)
    db_todo = crud.update_todo(db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    if is_demo_mode():
        return {"ok": True}
    crud.delete_todo(db, todo_id=todo_id)
    return {"ok": True}

@router.post("/reorder", response_model=List[schemas.Todo])
def reorder_todos(reorder: schemas.TodoReorder, db: Session = Depends(get_db)):
    """Reorder todos based on the provided list of IDs."""
    if is_demo_mode():
        return [schemas.Todo(**todo) for todo in get_mock_todos()]
    return crud.reorder_todos(db, todo_ids=reorder.order)
