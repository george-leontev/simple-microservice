import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.mail_service_router import router as mail_service_router
from src.routers.auth_router import router as auth_router
from src.routers.default_router import router as default_service_router

from src.web_socket_hub import sio
from src.data_access.data_access import init_database


init_database()

app = FastAPI()

socket_app = socketio.ASGIApp(sio)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(default_service_router)
app.include_router(mail_service_router)
app.include_router(auth_router)

app.mount("/", socket_app)
