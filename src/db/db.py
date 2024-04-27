from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import (Session, sessionmaker)
from src.db.orm_models import Base, UserORM
from src.models import User
import json
import uuid as pyuuid

from src.errors import UserNotFoundError, UserAlreadyExists, WrongPassword

class DB:
    def __init__(self, engine):
        self.metadata = MetaData()
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        self.session = Session()


    def get_rating(self) -> list[User]:
        users = self.session.query(UserORM).order_by(UserORM.wins.desc()).all()
        usersDTO: list[User] = [User.model_validate(user).model_dump_json() for user in users]        

        return usersDTO
    
    def create_user(self, username: str, password: str):
        if self.find_by_username(username) is None:
            user = UserORM(
                uuid=pyuuid.uuid4(),
                username=username,
                password=password,
                total=0,
                wins=0,
            )

            self.session.add(user)
            self.session.commit()
        else:
            raise UserAlreadyExists(f"User `{username}` already exists")    

    def find_by_username(self, username: str):
        return self.session.query(UserORM).filter(UserORM.username == username).one_or_none()
    
    def login(self, username: str, password: str):
        user = self.find_by_username(username)
        if user is None:
            raise UserNotFoundError(f"User `{username}` not found")
        elif user.password != password: 
            raise WrongPassword(f"Wrong password for user `{username}`")

