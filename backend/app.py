from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.staticfiles import StaticFiles
import uvicorn

# Database setup
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(
    swagger_ui_parameters={"customCssUrl": "/static/custom.css?v=1.0.0"}
)

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=BASE_DIR / "frontend" / "templates")

app.mount("/static", StaticFiles(directory=BASE_DIR / "frontend" / "static"), name="static")


@app.get("/")
async def TemplateRender(req: Request):
    return templates.TemplateResponse(
        name = "index.html",
        context = {"request": req}
    )

# Database setup
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)













if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)