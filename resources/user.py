from flask_restful import Resource,reqparse
from db import query
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from datetime import datetime

class User():
    def __init__(self,username,password):
        self.username=username
        self.password=password

    @classmethod
    def getUserByUsername(cls,username):
        result=query(f"""SELECT username,password FROM user WHERE username='{username}'""",return_json=False)
        if len(result)>0: return User(result[0]['username'],result[0]['password'])
        return None

class Register(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,help="username cannot be left blank!")
        parser.add_argument('email',type=str,required=True,help="email cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="password cannot be left blank!")
        data=parser.parse_args()

        try:
            query(f"""insert into user values('{data['username']}','{data['password']}','{data['email']}')""")
        except:
            return {"error":"Invalid Credentials ,Try Again!"}
        return {"message":"Registration Success"}

class Login(Resource):

    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,help="username cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="password cannot be left blank!")
        data=parser.parse_args()
        user=User.getUserByUsername(data['username'])
        if user and safe_str_cmp(user.password,data['password']):
            access_token=create_access_token(identity=user.username,expires_delta=False)
            return {'access_token':access_token,'message':"Login Success"},200
        return {"error":"Invalid Credentials!"}, 401