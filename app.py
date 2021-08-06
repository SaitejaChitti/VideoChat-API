from flask import Flask
from flask_restful import Api
from resources.user import Login, Register
from flask_jwt_extended import JWTManager


app=Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JWT_SECRET_KEY']='exposysdatalabs'
api=Api(app)
jwt=JWTManager(app)
api.add_resource(Register,'/register')
api.add_resource(Login,'/login')

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'authorization_required',
        "description": "Request does not contain an access token."
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'invalid_token',
        'message': 'Signature verification failed.'
    }), 401




if __name__=='__main__':
    app.run()