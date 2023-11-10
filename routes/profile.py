from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

from config.db import db
from models import AccountModel, UserProfileModel, BusinessProfileModel
from schemas import UserProfileSchema, UserProfileUpdateSchema, BusinessProfileSchema, BusinessProfileUpdateSchema


blp = Blueprint("profile", __name__, url_prefix="/api/profile", description="Operations on user and business profiles")


@blp.route("/user")
class UserProfile(MethodView):

    @jwt_required(fresh=True)
    @blp.response(200, UserProfileSchema)
    def get(self):
        user_profile = UserProfileModel.query.filter(UserProfileModel.account_id == get_jwt_identity()).first()

        if not user_profile:
            abort(404, message="User Profile not found")
        schema = UserProfileSchema()

        return user_profile, 200

    @jwt_required(fresh=True)
    @blp.arguments(UserProfileUpdateSchema)
    @blp.response(200, UserProfileSchema)
    def put(self, user_profile_data):
        user_profile = UserProfileModel.query.filter(UserProfileModel.account_id == get_jwt_identity()).first()

        if not user_profile:
            abort(404, message="User Profile not found")
        
        user_profile.first_name = user_profile_data["first_name"]
        user_profile.last_name = user_profile_data["last_name"]
        user_profile.phone_number = user_profile_data["phone_number"]
        user_profile.user_photo = user_profile_data["user_photo"]
        user_profile.nationality = user_profile_data["nationality"]

        db.session.commit()

        return {"message": "User Profile updated successfully"}, 200
    
    @jwt_required(fresh=True)
    def delete(self):
        user_to_delete = UserProfileModel.query.filter(UserProfileModel.account_id == get_jwt_identity()).first()
        if not user_to_delete:
            abort(404, message="User Profile not found")
        account_to_delete = AccountModel.query.filter(AccountModel.account_id == get_jwt_identity()).first()
        
        db.session.delete(user_to_delete)
        db.session.delete(account_to_delete)
        db.session.commit()

        return {"message": "Account deleted successfully"}, 204


@blp.route("/business")
class BusinessProfile(MethodView):

    @jwt_required(fresh=True)
    @blp.response(200, BusinessProfileSchema)
    def get(self):                  
        business_profile = BusinessProfileModel.query.filter(BusinessProfileModel.account_id == get_jwt_identity()).first()
        
        if not business_profile:
            abort(404, message="Business Profile not found")
        schema = BusinessProfileSchema()

        return schema.dump(business_profile), 200

    @jwt_required(fresh=True)
    @blp.arguments(BusinessProfileUpdateSchema)
    def put(self, business_profile_data):
        business_profile = BusinessProfileModel.query.filter(BusinessProfileModel.account_id == get_jwt_identity()).first()
        
        if not business_profile:
            abort(404, message="Business Profile not found")
        
        business_profile.business_name = business_profile_data["business_name"]
        business_profile.business_address = business_profile_data["business_address"]
        business_profile.billing_address = business_profile_data["billing_address"]
        business_profile.business_number = business_profile_data["business_number"]
        business_profile.business_logo = business_profile_data["business_logo"]
        business_profile.business_info = business_profile_data["business_info"]

        db.session.commit()

        return {"message": "Business Profile updated successfully"}, 200
    
    @jwt_required(fresh=True)
    def delete(self):
        business_to_delete = BusinessProfileModel.query.filter(BusinessProfileModel.account_id == get_jwt_identity()).first()
        
        if not business_to_delete:
            abort(404, message="Business Profile not found")
        account_to_delete = AccountModel.query.filter(AccountModel.account_id == get_jwt_identity()).first()
        
        db.session.delete(business_to_delete)
        db.session.delete(account_to_delete)
        db.session.commit()

        return {"message": "Account deleted successfully"}, 204
