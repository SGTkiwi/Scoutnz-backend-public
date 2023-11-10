from config.db import db
from sqlalchemy.dialects.mysql import TINYINT, LONGTEXT, DECIMAL


class CvModel(db.Model):
    __tablename__ = "cv"

    cv_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    cv_title = db.Column(db.String(45), nullable=False)
    work_experience = db.Column(LONGTEXT, nullable=True)
    education = db.Column(db.String(45), nullable=True)
    desired_city = db.Column(db.String(45), nullable=True)
    desired_suburb = db.Column(db.String(45), nullable=True)
    desired_working_days = db.Column(db.Integer, nullable=True)
    desired_working_hours = db.Column(DECIMAL(precision=3, scale=1), nullable=True)
    desired_working_period = db.Column(db.Integer, nullable=True)
    date_posted_cv = db.Column(db.Date, nullable=False)
    public_or_private = db.Column(TINYINT, nullable=False, default=0)

    # foreign key
    user_profile_id = db.Column(
        db.Integer, db.ForeignKey("user_profile.user_profile_id"), nullable=False
    )

    # relationship
    user_profile = db.relationship("UserProfileModel", back_populates="cv")
    application = db.relationship(
        "ApplicationModel", back_populates="cv", lazy="dynamic", cascade="all, delete"
    )

    def to_dict(self):
        return {
            "cv_id": self.cv_id,
            "user_profile_id": self.user_profile_id,
            "cv_title": self.cv_title,
            "work_experience": self.work_experience,
            "education": self.education,
            "desired_city": self.desired_city,
            "desired_suburb": self.desired_suburb,
            "desired_working_days": self.desired_working_days,
            "desired_working_hours": float(self.desired_working_hours),
            "desired_working_period": self.desired_working_period,
            "date_posted_cv": self.date_posted_cv.isoformat()
            if self.date_posted_cv
            else None,
            "public_or_private": self.public_or_private,
        }
