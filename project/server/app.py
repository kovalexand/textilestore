from fastapi import FastAPI, Response, Request

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
def app_exception_handler(request: Request, exc: ApplicationException) -> Response:
    return Response(status_code=exc.code_status, content=str(exc.body).encode())
