from config.db import db
from sqlalchemy.dialects.mysql import TINYINT, LONGTEXT
from flask_mail import Mail, Message


class AccountModel(db.Model):
    """_summary_
    AccountModel is a model for account table in database. It is used to store account information.
    Account tabel is mainly used from authentication and authorization.

    Attributes:
        __tablename__: a string of table name
        account_id: an integer of account id, primary key, autoincrement, not null
        email: a string of email, unique, not null
        password: a string of password, not null
        accout_type: an integer of account type (0: user, 1: business), not null, default 0
        data_created: a date of account created, not null
    Returns:
        AccountModel: a model of account table
    """

    __tablename__ = "account"

    account_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(LONGTEXT, nullable=False)
    account_type = db.Column(TINYINT, nullable=False, default=0)
    date_created = db.Column(db.Date, nullable=False)

    # relationship
    user_profile = db.relationship(
        "UserProfileModel",
        back_populates="account",
        lazy="dynamic",
        cascade="all, delete",
    )
    business_profile = db.relationship(
        "BusinessProfileModel",
        back_populates="account",
        lazy="dynamic",
        cascade="all, delete",
    )
    bookmark = db.relationship(
        "BookmarkModel", back_populates="account", lazy="dynamic", cascade="all, delete"
    )

    def to_dict(self):
        """_summary_
        to_dict is a method to convert AccountModel object to dictionary. For json response.
        Returns:
            _type_: _description_
            dict  : a dictionary of account information contains account_id, email, password, account_type, date_created
        """
        return {
            "account_id": self.account_id,
            "email": self.email,
            "password": self.password,
            "account_type": self.account_type,
            "date_created": self.date_created.isoformat()
            if self.date_created
            else None,
        }

    def reset_password(self, reset_password_token):
        mail = Mail()

        msg = Message(
            "scoutnz reset password",
            sender="hanjun0818@naver.com",
            recipients=[self.email],
        )
        msg.body = (
            "Your reset password link in http://127.0.0.1:3000/reset-password/"
            + reset_password_token
        )
        mail.send(msg)

        return "Sent"

    def sign_up_handler(self):
        mail = Mail()

        msg = Message(
            "Welcome to Scoutnz",
            sender="hanjun0818@naver.com",
            recipients=[self.email],
        )

        msg.body = "Welcome to Scoutnz"

        mail.send(msg)

        return "Sent"
