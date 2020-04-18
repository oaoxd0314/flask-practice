from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from security import authenticate,identity
from resource.user import UserRegister
from resource.item import Item,ItemList
from resource.store import Store,StoreList

app = Flask(__name__)

app.config['JWT_AUTH_URL_RULE']='/login' #改路徑，不然預設是 /auth
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800) #更改愈時時間
app.config['JWT_AUTH_USERNAME_KEY'] = 'email' #更改傳送給JWTToken 的預設欄位 只需改變 security.py 、create_table.py、user.py
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///data.db' #它會尋找由 sqlite創建的在跟目錄下的 database，也可以換成 mysql,oracle等資料庫
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #SQLALCHEMY 原本就會追蹤未儲存的物件 這關掉的只是Flask延伸的追蹤
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key ='Chris'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app,authenticate,identity) 


@jwt.auth_response_handler#改變認證完後TOKEN傳回來的訊息，但這裡通常不建議包含太多資料，因為安全問題
def customized_response_handler(access_token, identity):
    return jsonify({
                        'access_token': access_token.decode('utf-8'),
                        'user_id': identity.id,
                        'user_name':identity.email,#這裡的identity 是 security.authenticate()返回的
                        'message':'have a good time:)'
                   })

@jwt.jwt_error_handler#讓因為 jwt 發生的錯誤訊息更加容易看懂 
def customized_error_handler(error):
    return jsonify({
                       'message': error.description,
                       'code': error.status_code
                   }), error.status_code

        
api.add_resource(Item,'/item/<string:name>')

api.add_resource(ItemList, '/items')

api.add_resource(UserRegister,'/register')

api.add_resource(Store, '/store/<string:name>')

api.add_resource(StoreList, '/stores')


if __name__ =='__main__':#防止app.py被import時執行下面這段
    from db import db
    db.init_app(app)
    app.run(port=5000,debug =True)