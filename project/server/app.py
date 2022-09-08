from fastapi import FastAPI, Response, Request

from project.core.database import Base, engine
from project.core.exceptions import ApplicationException

# init services
Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)

# init fastAPI`s routers


# init fastAPI`s exceptions
@app.exception_handler(ApplicationException)
def app_exception_handler(request: Request, exc: ApplicationException) -> Response:
    return Response(
        status_code=exc.code_status,
        content=exc.body
    )
