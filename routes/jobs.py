from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from math import ceil

from config.db import db
from models import JobPostModel, BusinessProfileModel
from schemas import JobPostSchema, ExtendedJobPostSchema, JobPostUpdateSchema

blp = Blueprint("jobs", __name__, url_prefix="/api/jobs", description="View jobs for both authenticated and unauthenticated users")

@blp.route("/", defaults={'page_number': 1})
@blp.route("/<int:page_number>")
class Jobs(MethodView):
    
    @blp.response(200, ExtendedJobPostSchema(many=True))
    def post(self, page_number:int):
        items_per_page = 10
        total_items = db.session.query(JobPostModel).count()
        total_pages = ceil(total_items / items_per_page)

        page = max(1, page_number)
        page = min(page, total_pages)
        
        jobs = JobPostModel.query.order_by(JobPostModel.date_posted.desc()).paginate(page=page, per_page=items_per_page, error_out=False).items
        
        return jobs