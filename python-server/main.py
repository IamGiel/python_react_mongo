from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers.routes import router as book_router
from routers.authRoutes import authroute as userAuth_router
from routers.postRoutes import postRoute as posts_router

from config.database import Settings
from fastapi_jwt_auth.exceptions import AuthJWTException


app = FastAPI()

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
