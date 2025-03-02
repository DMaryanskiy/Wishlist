import fastapi
from fastapi.middleware import cors

from backend.categories import router as categories_router
from backend.subscriptions import router as subscription_router
from backend.users import router as user_router
from backend.wishes import router as wishes_router

app = fastapi.FastAPI()

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых источников
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

api_router = fastapi.APIRouter(prefix='/api/v1')
api_router.include_router(user_router.ROUTER)
api_router.include_router(subscription_router.ROUTER)
api_router.include_router(wishes_router.ROUTER)
api_router.include_router(categories_router.ROUTER)

app.include_router(api_router)
