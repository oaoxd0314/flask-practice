from models.user import UserModel

def authenticate(email,password):#JWT_AUTH_USERNAME_KEY changed username=>email
    user = UserModel.find_by_email(email)#JWT_AUTH_USERNAME_KEY changed username=>email
    if user and user.password == password:
        return user

def identity(payload):
    user_id =payload['identity']
    return UserModel.find_by_id(user_id)