# Define type of data that we want in our endpoints
from pydantic import BaseModel



class PostCreate(BaseModel):
    title: str
    content: str