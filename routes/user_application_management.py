from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

import datetime

from config.db import db
from models import UserProfileModel, CvModel, ApplicationModel
from schemas import ApplicationSchema


blp = Blueprint("application", __name__, url_prefix="/api/application", description="Application manager for user, apply for job, view applied job")


@blp.route("/")
class UserApplication(MethodView):
    
    @jwt_required(fresh=True)
    @blp.response(200, ApplicationSchema(many=True))
    def get(self):
        user_id = UserProfileModel.query.filter(UserProfileModel.account_id == get_jwt_identity()).first().user_profile_id
        cv_ids = [cv.cv_id for cv in CvModel.query.filter(CvModel.user_profile_id == user_id).all()]
        list_of_application = ApplicationModel.query.filter(ApplicationModel.cv_id.in_(cv_ids)).all()

        if not list_of_application:
            return {"message": "No application found"}, 404
        
        return list_of_application, 200

    @jwt_required(fresh=True)
    @blp.arguments(ApplicationSchema)
    def post(self, application_data):
        new_application = ApplicationModel(
            date_applied = datetime.datetime.utcnow(),
            cv_id = application_data["cv_id"],
            job_post_id = application_data["job_post_id"], 
            status = "On Hold"
        )

        db.session.add(new_application)
        db.session.commit()

        return {"message": "Application created successfully"}, 201
    
    
