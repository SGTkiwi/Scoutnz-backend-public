from config.db import db
from sqlalchemy.dialects.mysql import *


class PostPremiumModel(db.Model):
    __tablename__ = "post_premium"

    post_premium_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    post_premium_tier = db.Column(db.String(45), nullable=False)
    post_premium_start_date = db.Column(db.Date, nullable=False)
    post_premium_end_date = db.Column(db.Date, nullable=False)

    # foreign key
    job_post_id = db.Column(
        db.Integer, db.ForeignKey("job_post.job_post_id"), nullable=False, unique=True
    )

    # relationship
    job_post = db.relationship("JobPostModel", back_populates="post_premium")
    post_premium_payment = db.relationship(
        "PostPremiumPaymentModel",
        back_populates="post_premium",
        lazy="dynamic",
        cascade="all, delete",
    )

    def to_dict(self):
        return {
            "post_premium_id": self.post_premium_id,
            "job_post_id": self.job_post_id,
            "post_premium_tier": self.post_premium_tier,
            "post_premium_start_date": self.post_premium_start_date.isoformat()
            if self.post_premium_start_date
            else None,
            "post_premium_end_date": self.post_premium_end_date.isoformat()
            if self.post_premium_end_date
            else None,
        }
