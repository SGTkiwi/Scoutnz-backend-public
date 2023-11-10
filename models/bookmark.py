from config.db import db
from sqlalchemy.dialects.mysql import *


class BookmarkModel(db.Model):
    __tablename__ = "bookmark"

    bookmark_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )

    # foreign key
    job_post_id = db.Column(
        db.Integer, db.ForeignKey("job_post.job_post_id"), nullable=False
    )
    account_id = db.Column(
        db.Integer, db.ForeignKey("account.account_id"), nullable=False
    )

    # relationship
    job_post = db.relationship("JobPostModel", back_populates="bookmark")
    account = db.relationship("AccountModel", back_populates="bookmark")
