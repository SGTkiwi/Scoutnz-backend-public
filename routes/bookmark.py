from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response, request, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity

from config.db import db
from models import BookmarkModel, JobPostModel, AccountModel
from schemas import BookmarkSchema


blp = Blueprint(
    "bookmark",
    __name__,
    url_prefix="/api/bookmark",
    description="Bookmark manager for user, to accept and view applicants",
)


@blp.route("/")
class BookmarkList(MethodView):
    @jwt_required()
    @blp.response(200, BookmarkSchema(many=True))
    def get(self):
        try:
            account_id = get_jwt_identity()
            bookmarks = BookmarkModel.query.filter(
                BookmarkModel.account_id == account_id
            ).all()

            if not bookmarks:
                bookmarks = []

        except Exception as e:
            abort(500, message=str(e))

        return bookmarks, 200


@blp.route("/add/<int:job_post_id>")
class AddBookmark(MethodView):
    @jwt_required()
    def post(self, job_post_id: int):
        try:
            account_id = get_jwt_identity()

            if not AccountModel.query.filter(
                AccountModel.account_id == account_id
            ).first():
                abort(404, message="Account not found")

            if not JobPostModel.query.filter(
                JobPostModel.job_post_id == job_post_id
            ).first():
                abort(404, message="Job post not found")

            if BookmarkModel.query.filter(
                BookmarkModel.job_post_id == job_post_id,
                BookmarkModel.account_id == account_id,
            ).first():
                abort(409, message="Bookmark already exist")

            # add bookmark if not exist
            new_bookmark = BookmarkModel(job_post_id=job_post_id, account_id=account_id)
            db.session.add(new_bookmark)
            db.session.commit()

        except Exception as e:
            abort(500, message=str(e))

        return {"message": "Bookmark added successfully"}, 201


@blp.route("/remove/<int:job_post_id>")
class RemoveBookmark(MethodView):
    @jwt_required()
    def post(self, job_post_id: int):
        try:
            account_id = get_jwt_identity()

            pre_check = BookmarkModel.query.filter(
                BookmarkModel.job_post_id == job_post_id,
                BookmarkModel.account_id == account_id,
            ).first()

            if not pre_check:
                abort(404, message="Bookmark not found")

            db.session.delete(pre_check)
            db.session.commit()

        except Exception as e:
            abort(500, message=str(e))

        return make_response({"message": "Bookmark removed successfully"}, 200)
