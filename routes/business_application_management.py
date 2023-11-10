from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

from config.db import db
from models import BusinessProfileModel, ApplicationModel, JobPostModel
from schemas import ApplicantReviewSchema


blp = Blueprint(
    "applicant_review",
    __name__,
    url_prefix="/api/review",
    description="Application manager for business, to accept and view applicants",
)


@blp.route("/")
class ViewApplicants(MethodView):
    @jwt_required(fresh=True)
    @blp.response(200, ApplicantReviewSchema(many=True))
    def get(self):

        business_id = (
            BusinessProfileModel.query.filter(
                BusinessProfileModel.account_id == get_jwt_identity()
            )
            .first()
            .business_profile_id
        )
        if not business_id:
            abort(404, message="Business not found")

        post_ids = [
            post.job_post_id
            for post in JobPostModel.query.filter(
                JobPostModel.business_profile_id == business_id
            ).all()
        ]
        applications = ApplicationModel.query.filter(
            ApplicationModel.job_post_id.in_(post_ids)
        ).all()

        if not applications:  # list_of_applicants:
            abort(404, message="No applicants found")

        return applications, 200  # list_of_applicants, 200

    @jwt_required(fresh=True)
    @blp.arguments(ApplicantReviewSchema)
    def post(self, application_data):
        application_to_update = ApplicationModel.query.filter(
            (ApplicationModel.application_id == application_data["application_id"])
            & (ApplicationModel.cv_id == application_data["cv_id"])
            & (ApplicationModel.job_post_id == application_data["job_post_id"])
        ).first()

        if not application_to_update:
            abort(404, message="Application not found")

        # if application_data["status"] not in [
        #     "On Hold",
        #     "Accepted",
        #     "Rejected",
        #     "Interview",
        # ]:
        #     abort(400, message="Invalid status")

        if application_data["status"] == application_to_update.status:
            abort(400, message="Invalid status: status is the same as before")

        application_to_update.status = application_data["status"]

        db.session.commit()

        application_to_update.appicant_handler()

        return {"message": "Status updated"}, 200
