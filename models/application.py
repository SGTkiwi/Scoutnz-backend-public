from config.db import db
from sqlalchemy.dialects.mysql import *


class ApplicationModel(db.Model):
    """
    ApplicationModel is a model for application table in database. It is used to store application information.
    
    """
    __tablename__ = "application"

    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    date_applied = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(45), nullable=False, default="On Hold")

    # foreign key
    cv_id = db.Column(db.Integer, db.ForeignKey("cv.cv_id"), nullable=False)
    job_post_id = db.Column(db.Integer, db.ForeignKey("job_post.job_post_id"), nullable=False)

    # relationship
    cv = db.relationship("CvModel", back_populates="application")
    job_post = db.relationship("JobPostModel", back_populates="application")


    def to_dict(self):
        return {
            "application_id": self.application_id,
            "cv_id": self.cv_id,
            "job_post_id": self.job_post_id,
            "date_applied": self.date_applied.isoformat() if self.date_applied else None,
            "status" : self.status
        }
