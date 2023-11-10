from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

from config.db import db
from models import UserMembershipModel, UserProfileModel
from schemas import UserMembershipSchema


blp = Blueprint("user_membership", __name__, url_prefix="/api/user_membership", description="Operations on user membership")


@blp.route("/")
class UserMembership(MethodView):

    @jwt_required(fresh=True)
    @blp.response(200, UserMembershipSchema)
    def get(self):
        user_id = UserProfileModel.query.filter(UserProfileModel.account_id == get_jwt_identity()).first().user_profile_id
        membership = UserMembershipModel.query.filter(UserMembershipModel.user_profile_id == user_id).first()
        
        if not membership:
            abort(404, message="User Membership not found")

        return membership, 200
