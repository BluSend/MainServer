# BluSend
#
#
# Under development

from fastapi import APIRouter, Response, status
from queries import parcels
from queries import users
from security import otp_gen
from mailer import email_system
from models import security

mailRouter = APIRouter()


@mailRouter.get('/list/')
async def all_parcels_due():
    rawList = parcels.parcels_by_status("Priority")
    rawList += parcels.parcels_by_status("Due")
    processedList = []

    for parcel in rawList:
        processed_parcel = {}
        user = users.retrieve_user(parcel[0])
        processed_parcel["roomNumber"] = user[1]
        processed_parcel["status"] = parcel[1]
        processed_parcel["tracking_id"] = parcel[2]
        processed_parcel["compartment_number"] = parcel[5] # May be obselete depending on future design, consider removing if needed. Present right now to maximise options
        processedList.append(processed_parcel)
    return processedList

@mailRouter.put('/delivery/{id}')
async def generate_otp(id: int):
    raw_otp, hashed_otp = otp_gen.generate_otp(6)
    parcels.set_otp(id, hashed_otp)
    parcel = parcels.parcels_by_id(id)[0]
    user = users.retrieve_user(parcel[0])
    email_system.delivery_email(user[0], user[3], raw_otp)
    parcels.increment_delivery(id)
    return f"OTP generated successfully for user {user[0]}"


@mailRouter.put('/verify/{id}')
async def authenticate(id, otp: security.otp, response: Response):
    auth_status = parcels.verify_otp(id, otp.value)
    if auth_status == False:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Authentication Failed!"
    return "Authentication Successful!"
