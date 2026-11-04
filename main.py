from fastapi import FastAPI
from routers import admin, mail


app = FastAPI()

app.include_router(admin.adminRouter, prefix="/admin")
app.include_router(mail.mailRouter, prefix="/mail")
