from flask_restful import Resource, reqparse
from models.user import UserModel

#JWT_AUTH_USERNAME_KEY changed username=>email
#透過ctrl+f尋找 email 一次改回 username就復原了

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',#指定只有這個傳過去，可增加  #JWT_AUTH_USERNAME_KEY changed username=>email
        required=True,#確保的資料不能沒有以上的欄位
        type=str,#指定傳過去的格傳過去式
        help="account data fallt"#提示
    )
    parser.add_argument(
        'password',
        required =True,
        type=str,
        help='password data fallt'
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_email(data['email']): #1. if something : is mean 'something' is not none #2. JWT_AUTH_USERNAME_KEY changed username=>email
            return {"message": "account is exist"},400

        user = UserModel(data['email'],data['password'])#因為key可以直接對應 所以可以用這個對上
        user.save_to_db()

        return {"message":"user created suscessfully."} , 201