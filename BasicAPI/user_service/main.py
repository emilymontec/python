from fastapi import FastAPI
from database import Base, engine
from controllers.user_controller import router
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Service API"}

# Para ejecutar: uvicorn main:app --reload --port 8002
# email: admin@test.com
# password: 123456