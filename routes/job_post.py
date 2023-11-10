from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

import datetime

from config.db import db
from models import JobPostModel, BusinessProfileModel
from schemas import JobPostSchema, ExtendedJobPostSchema, JobPostUpdateSchema


blp = Blueprint(
    "job_post",
    __name__,
    url_prefix="/api/job_post",
    description="Operations on job post",
)


@blp.route("/")
class ViewAllJobPost(MethodView):
    @jwt_required(fresh=True)
    @blp.response(200, ExtendedJobPostSchema(many=True))
    def get(self):
        business_id = (
            BusinessProfileModel.query.filter(
                BusinessProfileModel.account_id == get_jwt_identity()
            )
            .first()
            .business_profile_id
        )
        list_of_job_post = JobPostModel.query.filter(
            JobPostModel.business_profile_id == business_id
        ).all()

        if not list_of_job_post:
            abort(404, message="No Job Post found")

        return list_of_job_post, 200


@blp.route("/create")
class CreateJobPost(MethodView):
    @jwt_required(fresh=True)
    @blp.arguments(JobPostSchema)
    def post(self, job_post_data):
        new_job_post = JobPostModel(
            job_post_title=job_post_data["job_post_title"],
            job_post_category=job_post_data["job_post_category"],
            hourly_wage=job_post_data["hourly_wage"],
            desired_education=job_post_data["desired_education"],
            desired_age=job_post_data["desired_age"],
            desired_gender=job_post_data["desired_gender"],
            working_days=job_post_data["working_days"],
            working_hours=job_post_data["working_hours"],
            working_period=job_post_data["working_period"],
            job_description=job_post_data["job_description"],
            date_posted=datetime.datetime.utcnow(),
            business_profile_id=BusinessProfileModel.query.filter(
                BusinessProfileModel.account_id == get_jwt_identity()
            )
            .first()
            .business_profile_id,
        )

        db.session.add(new_job_post)
        db.session.commit()

        return {"message": "Job Post created successfully"}, 201


@blp.route("/<int:job_post_id>")
class UpdateJobPost(MethodView):
    @jwt_required(fresh=True)
    @blp.arguments(JobPostUpdateSchema)
    def put(self, job_post_data, job_post_id):
        business_id = (
            BusinessProfileModel.query.filter(
                BusinessProfileModel.account_id == get_jwt_identity()
            )
            .first()
            .business_profile_id
        )
        job_post_to_update = JobPostModel.query.filter(
            (JobPostModel.job_post_id == job_post_id)
            & (JobPostModel.business_profile_id == business_id)
        ).first()
        if not job_post_to_update:
            abort(404, message="Job Post not found")

        job_post_to_update.job_post_title = job_post_data["job_post_title"]
        job_post_to_update.job_post_category = job_post_data["job_post_category"]
        job_post_to_update.hourly_wage = job_post_data["hourly_wage"]
        job_post_to_update.desired_education = job_post_data["desired_education"]
        job_post_to_update.desired_age = job_post_data["desired_age"]
        job_post_to_update.desried_gender = job_post_data["desired_gender"]
        job_post_to_update.working_days = job_post_data["working_days"]
        job_post_to_update.working_hours = job_post_data["working_hours"]
        job_post_to_update.working_period = job_post_data["working_period"]
        job_post_to_update.job_description = job_post_data["job_description"]

        db.session.commit()

        return {"message": "Job Post updated successfully"}, 200

    @jwt_required(fresh=True)
    def delete(self, job_post_id):
        business_id = (
            BusinessProfileModel.query.filter(
                BusinessProfileModel.account_id == get_jwt_identity()
            )
            .first()
            .business_profile_id
        )
        job_post_to_delete = JobPostModel.query.filter(
            (JobPostModel.job_post_id == job_post_id)
            & (JobPostModel.business_profile_id == business_id)
        ).first()
        if not job_post_to_delete:
            abort(404, message="Job Post not found")

        db.session.delete(job_post_to_delete)
        db.session.commit()

        return make_response("Job Post deleted successfully", 200)

    @jwt_required(fresh=True)
    @blp.response(200, ExtendedJobPostSchema)
    def get(self, job_post_id):
        business_id = (
            BusinessProfileModel.query.filter(
                BusinessProfileModel.account_id == get_jwt_identity()
            )
            .first()
            .business_profile_id
        )
        job_post_return = JobPostModel.query.filter(
            (JobPostModel.job_post_id == job_post_id)
            & (JobPostModel.business_profile_id == business_id)
        ).first()
        if not job_post_return:
            abort(404, message="Job Post not found")

        return job_post_return, 200
