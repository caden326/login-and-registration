from flask_app import app 
# app = Flask(__name__)    

from flask_app.controllers import users




if __name__=="__main__":   
    app.run(debug=True)  