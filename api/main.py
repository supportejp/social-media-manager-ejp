from fastapi import FastAPI
from db.database import engine, Base

from api.models.post import Post
from api.models.account import Account
from api.models.calendar_item import CalendarItem
from api.models.schedule import Schedule
from api.models.log import Log
from api.models.organization import Organization
from api.models.user import User
from api.routes.post_routes import router as post_router
from api.routes.account_routes import router as account_router
from api.routes.calendar_routes import router as calendar_router
from api.routes.schedule_routes import router as schedule_router
from api.routes.log_routes import router as log_router
from api.routes.user_routes import router as user_router
from api.routes.organization_routes import router as organization_router
from api.routes.auth_routes import router as auth_router

app = FastAPI(title="Social Media Manager Local")

Base.metadata.create_all(bind=engine)
app.include_router(post_router)
app.include_router(account_router)
app.include_router(calendar_router)
app.include_router(schedule_router)
app.include_router(log_router)
app.include_router(user_router)
app.include_router(organization_router)
app.include_router(auth_router)

@app.get("/")
def health_check():
    return {"status": "ok"}