from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)#要更改物件的話 需要靠搜索ID來達成 會比較方便
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self,name,price,store_id):
        self.name=name
        self.price=price
        self.store_id = store_id

    def json(self):
        return{'name':self.name,'price':self.price}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() # same as SELECT * FROM items WHERE name=name and return an 'Itme object', filter_by can .filter_by() and go on.
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query= "SELECT * FROM items WHERE name= ?"
        result = cursor.execute(query,(name,))

        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row) #or cls(row[0],row[1]) 這邊回傳的是一個物件所以需要用 cls
        '''

    def save_to_db(self):#SQLAlchemy 可以直接把物件轉換成row再儲存，所以我們不用告訴它用甚麼欄位，只要直接處理就好
        db.session.add(self)# session 是一個物件的集合 用於暫存即將被處理的物件
        db.session.commit()

        '''
        connection= sqlite3.connect('data.db')
        cursor=connection.cursor()

        query="INSERT INTO items VALUES(?,?)"

        cursor.execute(query,(self.name,self.price))

        connection.commit()
        connection.close()
        '''

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

        '''
        connection= sqlite3.connect('data.db')
        cursor=connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"

        cursor.execute(query, (self.price,self.name))

        connection.commit()
        connection.close()
        '''