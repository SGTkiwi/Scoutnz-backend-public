from config.db import db
from sqlalchemy.dialects.mysql import BLOB, LONGTEXT


class BusinessProfileModel(db.Model):
    __tablename__ = "business_profile"
    
    business_profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    business_name = db.Column(db.String(45), nullable=False)
    business_address = db.Column(db.String(45), nullable=False)
    billing_address = db.Column(db.String(45), nullable=True)
    nzbn = db.Column(db.String(45), nullable=True, unique=True)
    business_number = db.Column(db.String(100), nullable=False)
    business_logo = db.Column(BLOB, nullable=True)
    business_info = db.Column(LONGTEXT, nullable=True)
    
    # foreign key
    account_id = db.Column(db.Integer, db.ForeignKey("account.account_id"), nullable=False, unique=True)
    
    # relationship
    account = db.relationship("AccountModel", back_populates="business_profile")
    job_post = db.relationship("JobPostModel", back_populates="business_profile", lazy="dynamic", cascade="all, delete")
    

    def to_dict(self):
        return {
            "business_profile_id": self.business_profile_id,
            "account_id": self.account_id,
            "business_name": self.business_name,
            "business_address": self.business_address,
            "billing_address": self.billing_address,
            "nzbn": self.nzbn,
            "business_number": self.business_number,
            "business_logo": self.business_logo,
            "business_info": self.business_info
        }
