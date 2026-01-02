# FASTAPI APP CODE
from fastapi import FastAPI
from fastapi import HTTPException
from app.schemas import PostCreate
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager


@asynccontextmanager
# Take in app which is an instance of FastAPI 
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# Endpoint to create a new post
