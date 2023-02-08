from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers.routes import router as book_router
from routers.authRoutes import authroute as userAuth_router
from routers.postRoutes import postRoute as posts_router

from config.database import Settings
from fastapi_jwt_auth.exceptions import AuthJWTException

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@app.get("/")
async def root():
    return 'Hello world - Its Python! 🐍 '

@app.on_event("startup")
def startup_db_client():
    Settings.startDB()
    
@app.on_event("shutdown")
def shutdown_db_client():
    Settings.stopDB()
    
app.include_router(book_router)
app.include_router(userAuth_router)
app.include_router(posts_router)
