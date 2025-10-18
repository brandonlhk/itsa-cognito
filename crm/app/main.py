from fastapi import FastAPI
from app.db.database import engine
from app.db.models import Base
from app.routers import auth, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000"] # Add additional origins if required

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # use ["*"] only for non-credentialed requests
    allow_credentials=True,         # requires specific origins (no "*")
    allow_methods=["*"],            # or explicit list
    allow_headers=["*"],
    max_age=86400,                  # cache preflight responses
)

Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth.router)
app.include_router(users.router)