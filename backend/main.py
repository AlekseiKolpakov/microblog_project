from fastapi import FastAPI

from api.follows import router as follows_routes
from api.likes import router as likes_routes
from api.media import router as medias_routes
from api.tweets import router as tweets_routes
from api.users import router as users_routes

app = FastAPI(
    title="Microblog",
    description="Асинхронный API сервиса микроблогов для корпоративных систем.",
    version="1.0.0",
)

app.include_router(tweets_routes)
app.include_router(users_routes)
app.include_router(medias_routes)
app.include_router(follows_routes)
app.include_router(likes_routes)
