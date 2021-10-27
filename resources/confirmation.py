from time import time

from flask_restful import Resource
from flask import make_response, render_template
from libs.mailgun import MailGunException

from resources.user import USER_NOT_FOUND
from models.confirmations import ConfirmationModel
from models.user import UserModel
from schemas.confirmation import ConfirmationModel, ConfirmationSchema

confirmation_schema = ConfirmationSchema()

NOT_FOUND = "Confirmation on reference not found."
EXPIRED = "The link has expired."
ALREAD_CONFIRMED = "Registration has already been confirmed."
RESEND_FAIL = "Internal server error. Failed to resend confirmation email."
RESEND_SUCESSFUL = "E-mail confirmation successfully re-sent."
class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        """Return confirmation HTML page"""
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": NOT_FOUND}, 404

        if confirmation.expired:
            return {"message": EXPIRED}, 400

        if confirmation.confirmed:
            return {"message": ALREAD_CONFIRMED}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()

        headers = {"Content-type": "text/html"}
        return make_response(
            render_template("confirmatio_path.html", email=confirmation.user.email),
            200,
            headers,
        )
class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):

        """Returns confirmations for a given user. Use for testing."""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        
        return (
            {
                "current_time": int(time()),
                "confirmatio": [
                    confirmation_schema_dump(each)
                    for each in user.confirmation.order_by(ConfirmationModel.expire_at)
                ],
            },
            200,
        )
    @classmethod
    def post(cls, user_id: int):

        """Resent confirmation email"""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"message": ALREAD_CONFIRMED}, 400
                confirmation.force_to_expire()
            
            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": RESEND_SUCESSFUL}, 201
        except MailGunException as e:
            return {"message": str(e)}, 500
        except:
            traceback.print_exc()
            return {"message": RESEND_FAIL}, 500