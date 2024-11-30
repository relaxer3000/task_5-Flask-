from fastapi import FastAPI

from database.connection import conn, drop_database
from routers.user import user_router


app = FastAPI()
app.include_router(user_router, prefix="/user")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
