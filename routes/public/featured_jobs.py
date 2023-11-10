from flask.views import MethodView
from flask_smorest import Blueprint, abort
from math import ceil

from config.db import db
from models import JobPostModel, PostPremiumModel
from schemas import FeaturedJobPostSchema

blp = Blueprint("featured_jobs", __name__, url_prefix="/api/featured_jobs", description="View featured_jobs for both authenticated and unauthenticated users")

@blp.route("/", defaults={'page_number': 1})
@blp.route("/<int:page_number>")
class ListOfFeaturedJobs(MethodView):
    
    @blp.response(200, FeaturedJobPostSchema(many=True))
    def post(self, page_number:int):
        items_per_page = 4
        total_items = db.session.query(JobPostModel).count()
        total_pages = ceil(total_items / items_per_page)

        page = max(1, page_number)
        page = min(page, total_pages)
        
        featured_jobs = PostPremiumModel.query.order_by(PostPremiumModel.post_premium_start_date.desc()).paginate(page=page, per_page=items_per_page, error_out=False).items
        return featured_jobs

@blp.route("/post/<int:post_premium_id>")
class FeaturedJob(MethodView):
    
    @blp.response(200, FeaturedJobPostSchema)
    def post(self, post_premium_id:int):
        featured_job = PostPremiumModel.query.get_or_404(post_premium_id)
        return featured_job
        