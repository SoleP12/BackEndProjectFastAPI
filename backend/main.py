from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/")
async def index(req: Request):
    return templates.TemplateResponse(
        name = "index.html",
        context = {"request": req}
    )

# Database setup
@app.get("/database")
async def database():
    return {"message": "Database endpoint"}













if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)