from config.db import db
from sqlalchemy.dialects.mysql import LONGTEXT, DECIMAL


class JobPostModel(db.Model):
    __tablename__ = "job_post"

    job_post_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    job_post_title = db.Column(db.String(45), nullable=False)
    job_post_category = db.Column(db.String(45), nullable=False)
    hourly_wage = db.Column(DECIMAL(precision=6, scale=2), nullable=False)
    desired_education = db.Column(db.String(45), nullable=True)
    desired_age = db.Column(db.Integer, nullable=True)
    desired_gender = db.Column(db.String(45), nullable=True)
    working_days = db.Column(db.String(45), nullable=False)
    working_hours = db.Column(DECIMAL(precision=3, scale=1), nullable=False)
    working_period = db.Column(db.Integer, nullable=True)
    job_description = db.Column(LONGTEXT, nullable=False)
    date_posted = db.Column(db.Date, nullable=False)

    # foreign key
    business_profile_id = db.Column(
        db.Integer,
        db.ForeignKey("business_profile.business_profile_id"),
        nullable=False,
    )

    # relationship
    business_profile = db.relationship(
        "BusinessProfileModel", back_populates="job_post"
    )
    application = db.relationship(
        "ApplicationModel",
        back_populates="job_post",
        lazy="dynamic",
        cascade="all, delete",
    )
    post_premium = db.relationship(
        "PostPremiumModel",
        back_populates="job_post",
        lazy="dynamic",
        cascade="all, delete",
    )
    bookmark = db.relationship(
        "BookmarkModel",
        back_populates="job_post",
        lazy="dynamic",
        cascade="all, delete",
    )

    def to_dict(self):
        return {
            "job_post_id": self.job_post_id,
            "business_profile_id": self.business_profile_id,
            "job_post_title": self.job_post_title,
            "job_post_category": self.job_post_category,
            "hourly_wage": float(self.hourly_wage),
            "desired_education": self.desired_education,
            "desired_age": self.desired_age,
            "desired_gender": self.desired_gender,
            "working_days": self.working_days,
            "working_hours": float(self.working_hours),
            "working_period": self.working_period,
            "job_description": self.job_description,
            "date_posted": self.date_posted.isoformat() if self.date_posted else None,
        }
