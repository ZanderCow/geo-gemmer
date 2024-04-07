from flask import Flask
from routes.main_routes import main
from routes.user_routes import user
from routes.gem_routes import gem

app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(gem, url_prefix='/gem')







if __name__ == '__main__':
    app.run(debug=True)



    
    
   