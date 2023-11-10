from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

import datetime

from config.db import db
from models import CvModel, UserProfileModel
from schemas import CvSchema


blp = Blueprint("cv", __name__, url_prefix="/api/cv", description="Operations on CV")


@blp.route("/", methods =["GET"])
@jwt_required(fresh=True)
@blp.response(200, CvSchema(many=True))
def cv():
    user_id = UserProfileModel.query.filter(UserProfileModel.account_id == get_jwt_identity()).first().user_profile_id
    list_of_cv = CvModel.query.filter(CvModel.user_profile_id == user_id).all()
    
    if not list_of_cv:
        # return {"message": "No CV found"}
        abort(404, message="No CV found")
        
    return list_of_cv, 200


@blp.route("/create")
class CreateCV(MethodView):

    @jwt_required(fresh=True)
    @blp.arguments(CvSchema)
    def post(self, cv_data):
        new_cv = CvModel(
            cv_title = cv_data["cv_title"],
            work_experience = cv_data["work_experience"],
            education = cv_data["education"],
            desired_city = cv_data["desired_city"],
            desired_suburb = cv_data["desired_suburb"],
            desired_working_days = cv_data["desired_working_days"],
            desired_working_hours = cv_data["desired_working_hours"],
            desired_working_period  = cv_data["desired_working_period"],
            date_posted_cv = datetime.datetime.utcnow(),
            public_or_private = cv_data["public_or_private"],
            user_profile_id = UserProfileModel.query.filter(UserProfileModel.account_id == get_jwt_identity()).first().user_profile_id
        )

        db.session.add(new_cv)
        db.session.commit()

        return {"message": "CV created successfully"}, 201


@blp.route("/<int:cv_id>")
class UpdateCV(MethodView):

    @jwt_required(fresh=True)
    @blp.arguments(CvSchema)
    def put(self, cv_data, cv_id):
        user_id = UserProfileModel.query.filter(UserProfileModel.account_id == get_jwt_identity()).first().user_profile_id
        cv_to_update = CvModel.query.filter((CvModel.cv_id == cv_id) &
                                            (CvModel.user_profile_id == user_id)
                                            ).first()
        if not cv_to_update:
            abort(404, message="CV not found")
        
        cv_to_update.cv_title = cv_data["cv_title"]
        cv_to_update.work_experience = cv_data["work_experience"]
        cv_to_update.education = cv_data["education"]
        cv_to_update.desired_city = cv_data["desired_city"]
        cv_to_update.desired_suburb = cv_data["desired_suburb"]
        cv_to_update.desired_working_days = cv_data["desired_working_days"]
        cv_to_update.desired_working_hours = cv_data["desired_working_hours"]
        cv_to_update.desired_working_period  = cv_data["desired_working_period"]
        cv_to_update.date_posted_cv = datetime.datetime.utcnow()
        cv_to_update.public_or_private = cv_data["public_or_private"]
        
        db.session.commit()
        
        return {"message": "CV updated successfully"}, 200
    
    @jwt_required(fresh=True)
    def delete(self, cv_id):
        user_id = UserProfileModel.query.filter(UserProfileModel.account_id == get_jwt_identity()).first().user_profile_id
        cv_to_delete = CvModel.query.filter((CvModel.cv_id == cv_id) &
                                            (CvModel.user_profile_id == user_id)).first()
        
        if not cv_to_delete:
            abort(404, message="CV not found")
        
        db.session.delete(cv_to_delete)
        db.session.commit()

        return {"message": "CV deleted successfully"}, 204
    
    @jwt_required(fresh=True)
    @blp.response(200, CvSchema)
    def get(self, cv_id):
        user_id = UserProfileModel.query.filter(UserProfileModel.account_id == get_jwt_identity()).first().user_profile_id
        cv_return = CvModel.query.filter((CvModel.cv_id == cv_id) & 
                                         (CvModel.user_profile_id == user_id)).first()
        if not cv_return:
            abort(404, message="CV not found")
        
        return cv_return, 200
