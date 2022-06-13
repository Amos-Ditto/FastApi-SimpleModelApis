import email
import sqlalchemy.orm as _orm

import core.models.databases as _database
import core.models.models as _models
import core.schemas.schemas as _schemas

def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionalLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_email(db: _orm.Session, email:str):
    return db.query(_models.User).filter(_models.User.email == email).first()

def create_user(db: _orm.Session, user: _schemas.UserCreate):
    fake_password = user.password + "notsecure"
    db_user = _models.User(email=user.email, hashed_password=fake_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db:_orm.Session, skip: int, limit: int):
    return db.query(_models.User).offset(skip).limit(limit).all()

def get_user(db:_orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()

def create_post(db: _orm.Session, post: _schemas.PostCreate, user_id: int):
    post = _models.Post(**post.dict(), owner_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post