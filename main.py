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



# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session, relationship
# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# from typing import Optional
# from pydantic import BaseModel

# # Configuration
# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Database setup
# SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # Models
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     role = Column(String, default="user")
#     posts = relationship("Post", back_populates="owner")

# class Post(Base):
#     __tablename__ = "posts"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     content = Column(String)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#     owner = relationship("User", back_populates="posts")

# # Pydantic models
# class UserCreate(BaseModel):
#     username: str
#     email: str
#     password: str

# class PostCreate(BaseModel):
#     title: str
#     content: str

# class PostUpdate(BaseModel):
#     title: Optional[str] = None
#     content: Optional[str] = None

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# # Create tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # Dependencies
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
    
#     user = db.query(User).filter(User.username == username).first()
#     if user is None:
#         raise credentials_exception
#     return user

# # Routes
# @app.post("/users/", response_model=dict)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = User(
#         username=user.username,
#         email=user.email,
#         hashed_password=get_password_hash(user.password)
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return {"message": "User created successfully"}

# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.post("/posts/")
# async def create_post(
#     post: PostCreate,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     db_post = Post(**post.dict(), owner_id=current_user.id)
#     db.add(db_post)
#     db.commit()
#     db.refresh(db_post)
#     return {"message": "Post created successfully"}

# @app.put("/posts/{post_id}")
# async def update_post(
#     post_id: int,
#     post_update: PostUpdate,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     db_post = db.query(Post).filter(Post.id == post_id).first()
#     if not db_post:
#         raise HTTPException(status_code=404, detail="Post not found")
    
#     if db_post.owner_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
#     update_data = post_update.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_post, key, value)
    
#     db.commit()
#     return {"message": "Post updated successfully"}

# @app.get("/posts/")
# async def get_posts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     posts = db.query(Post).filter(Post.owner_id == current_user.id).all()
#     return posts
