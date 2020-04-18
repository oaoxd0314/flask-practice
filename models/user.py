
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id= db.Column(db.Integer,primary_key = True)#因為是 PRIMARY key 所以再新增時會自動增加
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self,email,password):
        self.email = email #JWT_AUTH_USERNAME_KEY changed username=>email
        self.password = password
     
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()