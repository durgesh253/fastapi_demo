from fastapi import FastAPI
import uvicorn
from database import Base,engine
from routes.user_route import router as user_router
from routes.book_route import router as book_router



Base.metadata.create_all(bind=engine)

app =  FastAPI()

@app.get("/user")
def root():
    return {"hello world"}

app.include_router(user_router,prefix="/api/v1", tags=["Users"])
app.include_router(book_router,prefix="/api/v1", tags=["Books"])



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1",port=8000)