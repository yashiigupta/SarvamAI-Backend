from fastapi import FastAPI

from routes.auth import router as auth_router
from routes.chat import router as chat_router

app = FastAPI()

# Include the routes
app.include_router(chat_router, prefix="/api/v1", tags=["ai"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])

# Run the app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
