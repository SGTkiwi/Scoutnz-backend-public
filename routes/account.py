from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, create_refresh_token

from config.blocklist import BLOCKLIST
import datetime
from datetime import timedelta

from config.db import db
from models import AccountModel, UserProfileModel, BusinessProfileModel
from schemas import AccountSchema, UserSignUpSchema, BusinessSignUpSchema


blp = Blueprint("account", __name__, url_prefix="/api/account", description="Operations on accounts, User Profile, Business profile, Sign up, and Login")
bcrypt = Bcrypt()
ACCESS_EXPIRES = timedelta(hours=1)


@blp.route("/user/signup")
class UserSignUp(MethodView):
    """_summary_

    Args:
        MethodView (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    @blp.arguments(UserSignUpSchema)
    def post(self, account_data:dict) -> tuple:
        if AccountModel.query.filter(AccountModel.email == account_data["email"]).first():
            abort(409, message="Email already exists") 
            
        if UserProfileModel.query.filter(UserProfileModel.phone_number == account_data["phone_number"]).first():
            abort(409, message="Phone number already exists")
            
        new_user = AccountModel(
            email=account_data["email"],
            password=bcrypt.generate_password_hash(account_data["password"]).decode("utf-8"),
            account_type=0,
            date_created=datetime.datetime.utcnow()
        )

        db.session.add(new_user)
        db.session.flush()
        
        new_profile = UserProfileModel(
            first_name=account_data["first_name"],
            last_name=account_data["last_name"],
            phone_number=account_data["phone_number"],
            date_of_birth=account_data["date_of_birth"],
            gender=account_data["gender"],
            user_photo=None,
            nationality=None,
            account_id=new_user.account_id
        )
        db.session.add(new_profile)
        db.session.commit()

        return {"message": "User Account created successfully"}, 201


@blp.route("/business/signup")
class BusinessSignUp(MethodView):
    
    @blp.arguments(BusinessSignUpSchema)
    def post(self, account_data):
        if AccountModel.query.filter(AccountModel.email == account_data["email"]).first():
            abort(409, message="Email already exists") 
         
        new_user = AccountModel(
            email=account_data["email"],
            password=bcrypt.generate_password_hash(account_data["password"]).decode("utf-8"),
            account_type=1,
            date_created=datetime.datetime.utcnow()
        )
        db.session.add(new_user)
        db.session.flush()
        
        new_profile = BusinessProfileModel(
            business_name=account_data["business_name"],
            business_address=account_data["business_address"],
            business_number=account_data["business_number"],
            account_id=new_user.account_id
        )
        db.session.add(new_profile)
        db.session.commit()

        return {"message": "Business Account created successfully"}, 201 
    
@blp.route("/user/reset-password")
class UserPasswordReset(MethodView):
    
    @blp.arguments(AccountSchema(only=["email"]))
    def post(self, reset_data):
        target_account = AccountModel.query.filter(AccountModel.email == reset_data["email"]).first()
        if not target_account:
            abort(404, message="Email does not exist")
        
        if target_account.account_type != 0:
            abort(409, message="Account is not a user account")
            
        reset_password_token = create_access_token(identity=target_account.account_id, expires_delta=timedelta(minutes=30))
        target_account.reset_password()    
            
        return {"message": "Password reset email sent successfully"}, 200 


@blp.route("/login")
class Login(MethodView):

    @blp.arguments(AccountSchema)
    def post(self, account_data):
        user = AccountModel.query.filter((AccountModel.email == account_data["email"]) &
                                         (AccountModel.account_type == int(account_data["account_type"]))).first()
        
        if user and bcrypt.check_password_hash(user.password, account_data["password"]):
            access_token = create_access_token(identity=user.account_id, fresh=True)
            refresh_token = create_refresh_token(identity=user.account_id)
            return {"access_token": access_token, "refresh_token" : refresh_token}, 200
        else:
            abort(401, message="Invalid username or password")


@blp.route("/logout")
class Logout(MethodView):

    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.set(jti, "", ex=ACCESS_EXPIRES)

        return {"message": "Successfully logged out"}, 200 

@blp.route("/refresh")
class TokenRefresh(MethodView):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
    