from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.database import engine, Base
from app.routers import auth, properties, favorites, inquiries
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

Base.metdata.create_all(bind=engine)

app = FastAPI(
    title="Real Estate API",
    description="A real estate listing backend API with property search, favorites and inquiries",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(properties.router)
app.include_router(favorites.router)
app.include_router(inquiries.router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")