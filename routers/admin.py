# BluSend
#
# "Router" handling all API endpoints relating to admin tasks
# Pending initial developemnt

from fastapi import APIRouter
from queries import users, parcels
from models import database

adminRouter = APIRouter()


@adminRouter.get("/users/all")
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

@adminRouter.get("/users/{id}")
async def return_user(id: int):
    data = users.retrieve_user(id)
    return {
        "name": data[0],
        "roomNumber": data[1],
        "userID": data[2],
        "email": data[3]
    }

@adminRouter.post("/users/add")
async def add_user(user: database.User):
    data = users.add_user(user.name, user.roomNumber, user.email)
    return {
        data
    }

@adminRouter.delete("/users/remove/{id}")
async def remove_user(id: int):
    data = users.remove_user(id)
    return {
        data
    }

@adminRouter.put("/users/modify")
async def change_user(user: database.UserStrict):
    data = users.change_user(user.userID, user.name, user.roomNumber, user.email)
    return {
        data
    }

@adminRouter.get("/parcels/all")
async def return_parcels():
    data = parcels.all_parcels()
    processed_data = []
    for parcel in data:
        processed_parcel = {
            "userID": parcel[0],
            "status": parcel[1],
            "tracking_id": parcel[2],
            "nDelivery": parcel[3]
        }
        processed_data.append(processed_parcel)
    return processed_data

@adminRouter.post("/parcels/add")
async def add_parcel(input: database.IDOnly):
    data = parcels.add_parcel(input.id)
    return {
        data
    }


@adminRouter.delete("/parcels/remove")
async def remove_parcel(input: database.IDOnly):
    data = parcels.remove_parcel(input.id)
    return {
        data
    }

@adminRouter.put("/parcels/modify")
async def change_parcel(parcel: database.Parcel):
    if parcel.status != None:
        parcels.change_status(parcel.tracking_id, parcel.status)
    if parcel.userID != None:
        parcels.change_owner(parcel.tracking_id, parcel.userID)
    return {
        f"Change processed. New owner id = {parcel.userID}, New status: {parcel.status}, changing nDelivery is NOT allowed"
    }
