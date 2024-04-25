from flask import Flask, jsonify, render_template
from routes.main_routes import main
from routes.user_routes import user
from routes.gem_routes import gem
from routes.review_routes import review
import os
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, jwt_required, exceptions

from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_secret_key')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True  # Ensure to use True in production to send cookies over HTTPS only
app.config['JWT_COOKIE_CSRF_PROTECT'] = True  # Enable CSRF protection
app.config['JWT_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection setting


bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.register_blueprint(main)
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(gem, url_prefix='/gem')
app.register_blueprint(review, url_prefix='/review')



@app.errorhandler(exceptions.NoAuthorizationError)
def handle_auth_error(e):
    return render_template('unauthorized.html', error=str(e)), 401

@app.errorhandler(exceptions.CSRFError)
def handle_csrf_error(e):
    return jsonify(error=str(e)), 401



if __name__ == '__main__':
    app.run(ssl_context='adhoc')



    
    
   