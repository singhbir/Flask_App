import connexion
from connexion.resolver import RestyResolver
from models import init_db

connex_app = connexion.FlaskApp(__name__)
connex_app.add_api('login.yaml')
app = connex_app.app
init_db(app)


if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.secret_key = "BIRSINGH"
    app.run(debug=True)
