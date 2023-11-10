from config.db import db
from sqlalchemy.dialects.mysql import *


class UserMembershipModel(db.Model):
    __tablename__ = "user_membership"

    user_membership_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    user_membership_tier = db.Column(db.String(45), nullable=False)
    date_purchased = db.Column(db.Date, nullable=False)
    user_membership_end_date = db.Column(db.Date, nullable=False)

    # foreign key
    user_profile_id = db.Column(
        db.Integer,
        db.ForeignKey("user_profile.user_profile_id"),
        nullable=False,
        unique=True,
    )

    # relationship
    user_profile = db.relationship("UserProfileModel", back_populates="user_membership")
    user_membership_payment = db.relationship(
        "UserMembershipPaymentModel",
        back_populates="user_membership",
        lazy="dynamic",
        cascade="all, delete",
    )

    def to_dict(self):
        return {
            "user_membership_id": self.user_membership_id,
            "user_profile_id": self.user_profile_id,
            "user_membership_tier": self.user_membership_tier,
            "date_purchased": self.date_purchased.isoformat()
            if self.date_purchased
            else None,
            "user_membership_end_date": self.date_purchased,
        }
