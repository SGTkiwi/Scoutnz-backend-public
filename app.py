from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS
from flask_mail import Mail

import subprocess
import atexit
import os

from config import db, BLOCKLIST

import models
import routes


def create_app():
    app = Flask(__name__)
    
    ACCESS_EXPIRES = timedelta(hours=1)
    
    # app.config_class = MailConfig
    app.config['MAIL_SERVER']='smtp.naver.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'hanjun0818@naver.com' # replace with your naver email id
    app.config['MAIL_PASSWORD'] = 'Han@132435' # replace with your password or app-specific password if applicable
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    
    mail = Mail(app)
    
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Freedom Prototype 1"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["BCRYPT_LEVEL"] = os.environ.get("BCRYPT_LEVEL")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
    
    
    db.init_app(app)
    
    api = Api(app)  
    
    # import os

    # this is for deployment--------------------------------------------------
    # export JWT_SECRET_KEY="your_jwt_secret_key_here"
    # export APP_SECRET_KEY="your_app_secret_key_here"
    # this is for terminal in linux or mac------------------------------------

    jwt = JWTManager(app) 
    
    # Start the Redis server as a background process
    redis_process = subprocess.Popen(['redis-server'], stdout=subprocess.PIPE)

    # Register a function to terminate the Redis process when the application exits
    atexit.register(redis_process.terminate)
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        user = models.AccountModel.query.filter(models.AccountModel.account_id == identity).first()
        if user.account_type == 1:
            return {"is_business": True}
        else:
            return {"is_business": False}
        
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token_in_redis = BLOCKLIST.get(jti)
        return token_in_redis is not None
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description" : "The token has been revoked", "error": "token_revoked"}
            ), 401
        )
    
    @jwt.needs_fresh_token_loader
    def requires_fresh_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "Fresh token required", "error": "fresh_token_required"}
                ), 401
            )
    
    with app.app_context():
        db.create_all()
        
    api.register_blueprint(routes.AccountBlueprint)
    api.register_blueprint(routes.ProfileBlueprint)
    api.register_blueprint(routes.CvBlueprint)
    api.register_blueprint(routes.JobPostBlueprint)
    api.register_blueprint(routes.UserMembershipBlueprint)
    api.register_blueprint(routes.UserApplicationBlueprint)
    api.register_blueprint(routes.BusinessApplicantBlueprint)
    
    @app.route("/api")
    def hello_world():
        return jsonify({"message": "된다 이기야!!"})
    
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

    return app
