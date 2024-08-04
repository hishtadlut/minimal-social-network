from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session, joinedload
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from datetime import datetime, timedelta, date
import jwt
import os
import bcrypt
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import time
from sqlalchemy.exc import OperationalError

# Database setup
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:secretpassword@database/socialnetwork")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sent_messages = relationship("Message", back_populates="sender", foreign_keys="Message.sender_id")
    received_messages = relationship("Message", back_populates="recipient", foreign_keys="Message.recipient_id")

def connect_with_retry(engine, max_retries=5, retry_interval=5):
    for i in range(max_retries):
        try:
            return engine.connect()
        except OperationalError:
            if i < max_retries - 1:
                time.sleep(retry_interval)
            else:
                raise

# JWT setup
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# FastAPI app
app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",  # React app's default port
    "http://localhost:8080",  # Alternative local development port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship("User", back_populates="posts")

User.posts = relationship("Post", order_by=Post.id, back_populates="author")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    sender_id = Column(Integer, ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)

    sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    recipient = relationship("User", back_populates="received_messages", foreign_keys=[recipient_id])

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: date

class UserOutBase(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    date_of_birth: date
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    author: UserOutBase

    class Config:
        orm_mode = True

class UserOut(UserOutBase):
    posts: List[PostOut] = []

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    content: str

class MessageCreate(BaseModel):
    content: str
    recipient_id: int

class MessageOut(BaseModel):
    id: int
    content: str
    sender: UserOut
    recipient: UserOut
    timestamp: datetime

    class Config:
        orm_mode = True

# Helper functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# API endpoints
@app.post("/users", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserOut.from_orm(db_user)
    except IntegrityError as e:
        db.rollback()
        error_info = str(e.orig)
        if "duplicate key value violates unique constraint" in error_info:
            if "ix_users_email" in error_info:
                raise HTTPException(status_code=400, detail="Email already registered")
            elif "ix_users_username" in error_info:
                raise HTTPException(status_code=400, detail="Username already taken")
        raise HTTPException(status_code=400, detail="Registration failed")

@app.get("/messages/unread-count", response_model=dict)
async def get_unread_message_count(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        unread_count = db.query(Message).filter(Message.recipient_id == current_user.id, Message.is_read == False).count()
        return {"count": unread_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching unread message count: {str(e)}")

@app.get("/chats", response_model=List[dict])
async def get_chats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        chats = []
        # Get all users the current user has exchanged messages with
        chat_partners = db.query(User).join(Message, 
            ((Message.sender_id == User.id) & (Message.recipient_id == current_user.id)) | 
            ((Message.recipient_id == User.id) & (Message.sender_id == current_user.id))
        ).filter(User.id != current_user.id).distinct().all()

        for partner in chat_partners:
            last_message = db.query(Message).filter(
                ((Message.sender_id == current_user.id) & (Message.recipient_id == partner.id)) |
                ((Message.sender_id == partner.id) & (Message.recipient_id == current_user.id))
            ).order_by(Message.timestamp.desc()).first()

            unread_count = db.query(Message).filter(
                Message.sender_id == partner.id,
                Message.recipient_id == current_user.id,
                Message.is_read == False
            ).count()

            chats.append({
                "id": partner.id,
                "username": partner.username,
                "lastMessage": last_message.content if last_message else "",
                "unreadCount": unread_count
            })

        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching chats: {str(e)}")

@app.get("/messages/unread-count", response_model=dict)
async def get_unread_message_count(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    unread_count = db.query(Message).filter(Message.recipient_id == current_user.id, Message.is_read == False).count()
    return {"count": unread_count}

@app.get("/chats", response_model=List[dict])
async def get_chats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chats = []
    # Get all users the current user has exchanged messages with
    chat_partners = db.query(User).join(Message, 
        ((Message.sender_id == User.id) & (Message.recipient_id == current_user.id)) | 
        ((Message.recipient_id == User.id) & (Message.sender_id == current_user.id))
    ).filter(User.id != current_user.id).distinct().all()

    for partner in chat_partners:
        last_message = db.query(Message).filter(
            ((Message.sender_id == current_user.id) & (Message.recipient_id == partner.id)) |
            ((Message.sender_id == partner.id) & (Message.recipient_id == current_user.id))
        ).order_by(Message.timestamp.desc()).first()

        unread_count = db.query(Message).filter(
            Message.sender_id == partner.id,
            Message.recipient_id == current_user.id,
            Message.is_read == False
        ).count()

        chats.append({
            "id": partner.id,
            "username": partner.username,
            "lastMessage": last_message.content if last_message else "",
            "unreadCount": unread_count
        })

    return chats

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/posts", response_model=PostOut)
async def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        db_post = Post(content=post.content, user_id=current_user.id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return PostOut.from_orm(db_post)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the post: {str(e)}")

@app.get("/posts", response_model=List[PostOut])
async def get_posts(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    posts = db.query(Post).options(joinedload(Post.author)).all()
    return [PostOut.from_orm(post) for post in posts]

@app.post("/messages", response_model=MessageOut)
async def send_message(message: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recipient = db.query(User).filter(User.id == message.recipient_id).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    db_message = Message(content=message.content, sender_id=current_user.id, recipient_id=message.recipient_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return MessageOut.from_orm(db_message)

@app.get("/messages/{recipient_id}", response_model=List[MessageOut])
async def get_messages(recipient_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    messages = db.query(Message).filter(
        ((Message.sender_id == current_user.id) & (Message.recipient_id == recipient_id)) |
        ((Message.sender_id == recipient_id) & (Message.recipient_id == current_user.id))
    ).order_by(Message.timestamp).all()
    
    # Mark messages as read
    for message in messages:
        if message.recipient_id == current_user.id and not message.is_read:
            message.is_read = True
    db.commit()
    
    return [MessageOut.from_orm(message) for message in messages]

@app.get("/users/search", response_model=List[UserOut])
async def search_users(query: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = db.query(User).filter(
        (User.username.ilike(f"%{query}%")) |
        (User.first_name.ilike(f"%{query}%")) |
        (User.last_name.ilike(f"%{query}%"))
    ).all()
    return [UserOut.from_orm(user) for user in users]

@app.get("/users/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/users/me/posts", response_model=List[PostOut])
async def read_user_posts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.user_id == current_user.id).all()
    return [PostOut.from_orm(post) for post in posts]

# Create tables
with connect_with_retry(engine) as connection:
    Base.metadata.create_all(bind=connection)

@app.get("/")
async def root():
    return {"message": "Welcome to the Minimal Social Network API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)