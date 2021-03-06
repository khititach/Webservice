import pymongo
from flask import Flask,request
from flask_restful import Resource ,Api ,reqparse
from datetime import datetime,date

client = pymongo.MongoClient('localhost',27017)

app= Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('firstname')
parser.add_argument('lastname')
parser.add_argument('number')

db = client.db_EX01
mb = db.mb

class Reg(Resource):
        def post(self):
                args = parser.parse_args()
                id = args['number']
                firstname = args['firstname']
                lastname = args['lastname']
                password = args['password']
                data = mb.find_one({"user.number":id})
                if(data):
                        return {"err":"has this id"}
                mb.insert({"user":{"number":id,"firstname":firstname,"lastname":lastname,"password":password},"list":[]})
                return {"firstname":firstname,"lastname":lastname,"number":id,"password":password}


class History(Resource):
        def get(self):
                args = parser.parse_args()
                id = args['id']
                data = mb.find_one({"user.number":id})
                if(data):
                        firstname = data['user']['firstname']
                        lastname = data['user']['lastname']
                        list_work = data['list']
                        return {"firstname":firstname,"lastname":lastname,"list":list_work}
                return {}

class Login(Resource):
        def post(self):
                args = parser.parse_args()
                username = args['username']
                password = args['password']
                data = mb.find_one({"user.number":username,"user.password":password})
                if(data):
                        firstname = data['user']['firstname']
                        lastname = data['user']['lastname']
                        datetime_login = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        mb.update({"user.number":username},{"$push":{"list":{"datetime":datetime_login}}})
                        return {"firstname":firstname,"lastname":lastname,"datetime":datetime_login}
                return {}
api.add_resource(Reg,'/api/regis')
api.add_resource(Login,'/api/login')
api.add_resource(History,'/api/list')

if __name__ == '__main__':
        app.run(host='0.0.0.0',port=5001)
