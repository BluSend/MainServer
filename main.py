from fastapi import FastAPI
from routers import admin


app = FastAPI()

app.include_router(admin.adminRouter, prefix="/admin")
