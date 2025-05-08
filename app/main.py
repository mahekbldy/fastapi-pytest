from fastapi import FastAPI
from app.routes import auth, users
import uvicorn

app = FastAPI(
    title="FastAPI JWT Auth Example",
    description="🚀 Simple login system using JWT and static user data",
    version="1.0.0"
)

# Include Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
