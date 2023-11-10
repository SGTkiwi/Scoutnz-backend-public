from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_
from math import ceil

from config.db import db
from models import JobPostModel, BusinessProfileModel
from schemas import ExtendedJobPostSchema

blp = Blueprint(
    "jobs",
    __name__,
    url_prefix="/api/jobs",
    description="View jobs for both authenticated and unauthenticated users",
)


@blp.route("/", defaults={"page_number": 1})
@blp.route("/<int:page_number>")
class Jobs(MethodView):
    @blp.response(200, ExtendedJobPostSchema(many=True))
    def post(self, page_number: int):
        items_per_page = 5
        total_items = db.session.query(JobPostModel).count()
        total_pages = ceil(total_items / items_per_page)

        page = max(1, page_number)
        page = min(page, total_pages)

        jobs = (
            JobPostModel.query.order_by(JobPostModel.date_posted.desc())
            .paginate(page=page, per_page=items_per_page, error_out=False)
            .items
        )

        return jobs


@blp.route("/search/<string:search_query>")
class SearchJobs(MethodView):
    @blp.response(200, ExtendedJobPostSchema(many=True))
    def get(self, search_query: str):

        jobs = (
            db.session.query(JobPostModel)
            .join(BusinessProfileModel)
            .filter(
                or_(
                    JobPostModel.job_post_title.ilike(f"%{search_query}%"),
                    JobPostModel.job_description.ilike(f"%{search_query}%"),
                    BusinessProfileModel.business_name.ilike(f"%{search_query}%"),
                )
            )
            .all()
        )
        return jobs
