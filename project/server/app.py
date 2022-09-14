from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from project.core.database import Base, engine
from project.core.exceptions import ApplicationException
from project.auth.delivery.controller import auth

# init services
Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)

# init fastAPI`s routers
app.include_router(auth)


# init fastAPI`s exceptions
@app.exception_handler(ApplicationException)
async def app_exception_handler(request: Request, exc: ApplicationException) -> JSONResponse:
    return JSONResponse(status_code=exc.code_status, content=exc.body)
