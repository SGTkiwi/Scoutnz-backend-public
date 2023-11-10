from config.db import db
from sqlalchemy.dialects.mysql import DECIMAL


class PostPremiumPaymentModel(db.Model):
    __tablename__ = "post_premium_payment"

    premium_payment_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    date_received = db.Column(db.Date, nullable=False)
    price = db.Column(DECIMAL(precision=6, scale=2), nullable=False)

    # foreign key
    post_premium_id = db.Column(
        db.Integer,
        db.ForeignKey("post_premium.post_premium_id"),
        nullable=False,
        unique=True,
    )

    # relationship
    post_premium = db.relationship(
        "PostPremiumModel", back_populates="post_premium_payment"
    )

    def to_dict(self):
        return {
            "premium_payment_id": self.premium_payment_id,
            "post_premium_id": self.post_premium_id,
            "date_received": self.date_received.isoformat()
            if self.date_received
            else None,
            "price": float(self.price),
        }
