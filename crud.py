
from sqlalchemy.orm import Session
import models, schemas, database
import password as passwd

def get_user(db: Session, id: int):
    return db.query(models.User).filter(
        models.User.id == id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username).first()

def get_last_id(db:Session)-> int:
    return db.query(models.User).order_by(models.User.id.desc()).first().id

def create_user(db: Session, user: schemas.UserCreate):
    id = (get_last_id(db))+1
    db_user = models.User(
        id = id,
        username = user.username, 
        hashed_password = passwd.get_hashed_password(user.password),
        role=False
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_by_username(db: Session, username: str):
    db.query(models.User).filter(models.User.username == username).delete()
    db.commit()

if __name__ == "__main__":
    with database.DBContext() as db:
        # create_user(db = db, user = schemas.UserCreate(username="user", password="1234"))
        user:schemas.User = get_user_by_username(db, "nam")
        print(user.username)
        