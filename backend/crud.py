from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import models, schemas

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    """Get todos ordered by order field."""
    return db.query(models.Todo).order_by(models.Todo.order).offset(skip).limit(limit).all()

def create_todo(db: Session, todo: schemas.TodoCreate):
    """Create a new todo with order set to max+1."""
    max_order = db.query(func.max(models.Todo.order)).scalar() or 0
    db_todo = models.Todo(
        title=todo.title,
        completed=todo.completed,
        order=max_order + 1
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo: schemas.TodoCreate):
    """Update a todo's title and completed status."""
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        db_todo.title = todo.title
        db_todo.completed = todo.completed
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    """Delete a todo."""
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo

def reorder_todos(db: Session, todo_ids: List[int]):
    """Reorder todos based on the provided list of IDs."""
    for index, todo_id in enumerate(todo_ids):
        db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
        if db_todo:
            db_todo.order = index
    db.commit()
    return get_todos(db)
