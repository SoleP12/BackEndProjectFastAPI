# FASTAPI APP CODE
from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi import HTTPException
from app.schemas import PostCreate
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
from imagekitio.lib.requests.upload_file_request_options import UploadFileRequestOptions
import shutil
import uuid
import os
import tempfile

@asynccontextmanager
# Take in app which is an instance of FastAPI 
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# Endpoint to create a new post
@app.post("/upload")
async def upload_file(
    # Recives Files object from this endpoint
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session),
):
    # Create Object of Post 
    # Create a temporary file to store the contents 
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix = os.path.splittext) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file,temp_file)
        
        upload_result = imagekit.upload_file(
            file = open(temp_file_path, "rb"),
            file_name = file.filename,
            options = UploadFileRequestOptions(
                use_unique_file_name = True,
                tags=["backend-upload"]
            ) 
        )
        if upload_result.respons_metadata_e.http_status_code == 200:

            post = Post(
                caption = caption,
                url = upload_result.response.url,
                file_type = file.content_type,
                file_name = file.filename
            )

            # Adds post to database session, Commit the session, make sure to commit to session
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
    except Exception as e:
        raise HTTPException(status_code = 500,detail = str(e) )
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()



@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    # Look through post ordering by which they were created 
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    # Give all results from query
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append(
            {
            "id": str(post.id),
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at.isoformat()
            }
        )
    return {"posts": posts_data}