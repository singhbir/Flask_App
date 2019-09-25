import datetime
import connexion
from models import init_db
from flask_jwt_extended import JWTManager

connex_app = connexion.FlaskApp(__name__)
connex_app.add_api('login.yaml')
app = connex_app.app
app.config['JWT_SECRET_KEY'] = 'thisisme'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=10)
init_db(app)
jwt = JWTManager(app)

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.secret_key = "BIRSINGH"
    app.run(debug=True)
