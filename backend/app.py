from flask import Flask, request
from flask_restful import Resource, Api
import robin_stocks as r
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})


class Base(Resource):
    def get(self):
        return {"about": "sup"}

class Login(Resource):
    def get(self, remember, user=None, password=None):
        store = ''
        if remember == 'true':
            store = 'True'
        else:
            store = 'False'
        data = r.login(username=user,password=password, store_session=remember)
        print(data)
        result = {}
        result['detail'] = data['detail']
        if data['detail'] == 'no pickle':
            return result
        elif 'mfa_required' in data:
            result['result'] = 'mfa'
        elif 'challenge' in data:
            result['result'] = 'challenge'
            result['challenge_id'] = data['challenge']['id']
        elif 'access_token' in data:
            result['result'] = 'success'
            return result
        elif 'error' in data:
            result['result'] = 'disconnected'
            return result
        else:
            result['result'] = 'wrong'
        result['device_token'] = data['device_token']
        return result

class Verify(Resource):
    def get(self, user, password, remember, device_token, auth_type, code, challenge_id=None):
        data = r.verify(username=user,password=password, store_session=remember, device_token=device_token, auth_type=auth_type, code=code, challenge_id=challenge_id)
        return data 

class Logout(Resource):
    def get(self):
        r.logout()
        return {}

class Balance(Resource):
    def get(self):
        return r.load_portfolio_profile()

api.add_resource(Base, "/")
api.add_resource(
    Login, 
    "/login/<string:remember>",
    "/login/<string:remember>/<string:user>/<string:password>"
)
api.add_resource(
    Verify, 
    '/verify/<string:remember>/<string:user>/<string:password>/<string:device_token>/<string:auth_type>/<string:code>',
    '/verify/<string:remember>/<string:user>/<string:password>/<string:device_token>/<string:auth_type>/<string:code>/<string:challenge_id>'
)
api.add_resource(
    Logout,
    '/logout/'
)
api.add_resource(
    Balance,
    '/balance/'
)



if __name__ == "__main__":
    app.run(debug=True)