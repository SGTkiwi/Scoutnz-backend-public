from config.db import db
from sqlalchemy.dialects.mysql import TINYINT, BLOB, DECIMAL


class UserMembershipPaymentModel(db.Model):
    __tablename__ = "user_membership_payment"
    
    membership_payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    date_received = db.Column(db.Date, nullable=False)
    price = db.Column(DECIMAL(precision=6, scale=2), nullable=False)

    # foreign key
    user_membership_id = db.Column(db.Integer, db.ForeignKey("user_membership.user_membership_id"), nullable=False, unique=True)
    
    # relationship
    user_membership = db.relationship("UserMembershipModel", back_populates="user_membership_payment")
    
    
    def to_dict(self):
        return {
            "membership_payment_id": self.membership_payment_id,
            "user_membership_id": self.user_membership_id,
            "date_received": self.date_received.isoformat() if self.date_received else None,
            "price": float(self.price)
        }
