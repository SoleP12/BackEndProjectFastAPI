# ORM - Object Relational Mapping
# A way to interact with the database using objects instead of writing raw SQL queries.

from collections.abc import AsyncGenerator
import uuid
from sqlalchemy import create_engine
from sqlalchemy import Column, Text, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
import datetime

# Allow us to connect to local database on computer called test.db
# Asynchronous as well
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Data Models(Will Create Automatically Tables in Database) Type of data you want to store
# Data Model for Storing Posts
class Post (DeclarativeBase):
    __tablename__ = "posts"

    # Every Primary Key must be unique, Generates random UUIDs for each post
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    


# Creates database engine that will look at all the models we have defined and create tables in the database accordingly
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine,expire_on_commit=False)

# Find all of the classes from the DeclarativeBase and create tables in the database
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)


# Get a session that will allow us to interact with the database asynchronously
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
