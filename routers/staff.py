# BluSend
#
# "Router" handling all API endpoints relating to the staff interface

from fastapi import APIRouter
from queries import users

staffFERouter = APIRouter()


@staffFERouter.get("/users/list")
async def return_users():
    data = users.all_users()
    processed_data = []
    for user in data:
        processed_user = {
            "name": user[0],
            "roomNumber": user[1],
            "userID": user[2],
            "email": user[3]
        }
        processed_data.append(processed_user)
    return processed_data
