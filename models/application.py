from config.db import db
from sqlalchemy.dialects.mysql import *
from flask_mail import Mail, Message


class ApplicationModel(db.Model):
    """
    ApplicationModel is a model for application table in database. It is used to store application information.

    """

    __tablename__ = "application"

    application_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    date_applied = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(45), nullable=False, default="On Hold")

    # foreign key
    cv_id = db.Column(db.Integer, db.ForeignKey("cv.cv_id"), nullable=False)
    job_post_id = db.Column(
        db.Integer, db.ForeignKey("job_post.job_post_id"), nullable=False
    )

    # relationship
    cv = db.relationship("CvModel", back_populates="application")
    job_post = db.relationship("JobPostModel", back_populates="application")

    def to_dict(self):
        return {
            "application_id": self.application_id,
            "cv_id": self.cv_id,
            "job_post_id": self.job_post_id,
            "date_applied": self.date_applied.isoformat()
            if self.date_applied
            else None,
            "status": self.status,
        }

    def application_handler(self):
        mail = Mail()

        msg = Message(
            "New Application received",
            sender="hanjun0818@naver.com",
            recipients=[self.job_post.business_profile.account.email],
        )

        msg.body = (
            "You have received a new application from "
            + self.cv.user_profile.first_name
            + " "
            + self.cv.user_profile.last_name
            + " for the job post "
            + self.job_post.job_post_title
            + "."
            + "\n\n"
            + "Please login to your account to view the application."
        )

        mail.send(msg)

        return "Sent"
