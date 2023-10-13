import os

from flask_caching import Cache
from flask_cors import CORS

from resources import LoginResource, AuthResource, ATMsResource, OfficesResource
from utils import setup_logging, ParserConfig, FlaskApp, FlaskApi, bcrypt, database

path = os.path.dirname(os.path.abspath(__file__))

# init logger
setup_logging(os.path.join(path, 'config', 'logging.yaml'))

# load config with all dispatchers
config = ParserConfig(os.path.join(path, 'config', 'config.json'))

# init Flask App
app = FlaskApp(__name__)
cors = CORS(app, supports_credentials=True)
api = FlaskApi(app)

# store global objects
with app.app_context():
    # setup app config
    app.configuration = config['custom']
    app.config.from_mapping(config['app'])
    bcrypt.init_app(app)
    database.app = app
    database.init_app(app)

    # init Flask Cache
    cache = Cache(app)

# link resources routing
api.add_resource(LoginResource, '/login')
api.add_resource(AuthResource, '/auth')
api.add_resource(ATMsResource, '/atms')
api.add_resource(OfficesResource, '/offices')

if __name__ == '__main__':
    app.run()
