from config.db import db
from sqlalchemy.dialects.mysql import BLOB


class UserProfileModel(db.Model):
    __tablename__ = "user_profile"
    
    user_profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False, unique=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(45), nullable=False)
    user_photo = db.Column(BLOB, nullable=True)
    nationality = db.Column(db.String(45), nullable=True)
    
    # foreign key
    account_id = db.Column(db.Integer, db.ForeignKey("account.account_id"), nullable=False, unique=True)
    
    # relationship
    account = db.relationship("AccountModel", back_populates="user_profile")
    cv = db.relationship("CvModel", back_populates="user_profile", lazy="dynamic", cascade="all, delete")
    user_membership = db.relationship("UserMembershipModel", back_populates="user_profile", lazy="dynamic", cascade="all, delete")
    

    def to_dict(self):
        return {
            "user_profile_id": self.user_profile_id,
            "account_id": self.account_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "gender": self.gender,
            "user_photo": self.user_photo,
            "nationality": self.nationality
        }
