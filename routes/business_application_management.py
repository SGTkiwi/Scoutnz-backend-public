from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

from config.db import db
from models import BusinessProfileModel, ApplicationModel, JobPostModel
from schemas import ApplicantReviewSchema


blp = Blueprint("applicant_review", __name__, url_prefix="/api/review", description="Application manager for business, to accept and view applicants")


@blp.route("/")
class ViewApplicants(MethodView):
    
    @jwt_required(fresh=True)
    @blp.response(200, ApplicantReviewSchema(many=True))
    def get(self):

        business_id = BusinessProfileModel.query.filter(BusinessProfileModel.account_id == get_jwt_identity()).first().business_profile_id
        if not business_id:
            abort(404, message="Business not found")
        
        post_ids = [post.job_post_id for post in JobPostModel.query.filter(JobPostModel.business_profile_id == business_id).all()]
        applications = ApplicationModel.query.filter(ApplicationModel.job_post_id.in_(post_ids)).all()
        
        list_of_applicants = {job_id: [] for job_id in post_ids}
    
        # for application in applications:
        #     list_of_applicants[application.job_post_id].append(application.cv_id)
        
        if not applications: #list_of_applicants:
            abort(404, message="No applicants found")
        
        return applications, 200 #list_of_applicants, 200
    
    @jwt_required(fresh=True)
    @blp.arguments(ApplicantReviewSchema)
    def post(self, application_data):
        application_to_update = ApplicationModel.query.filter((ApplicationModel.application_id == application_data["application_id"]) &
                                                              (ApplicationModel.cv_id == application_data["cv_id"]) &
                                                              (ApplicationModel.job_post_id == application_data["job_post_id"])).first()
        
        if not application_to_update:
            return {"message": "Application not found"}, 404
        
        application_to_update.status = application_data["status"]
        
        db.session.commit()
        
        return {"message": "Status updated"}, 201

    
    
    