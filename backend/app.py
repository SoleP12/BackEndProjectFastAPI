from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.staticfiles import StaticFiles
import uvicorn

# Database setup
from tortoise.contrib.fastapi import register_tortoise
from models import Supplier_Pydantic, SupplierIn_Pydantic, Supplier

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

@app.post("/supplier")
async def add_supplier(supplier_info: SupplierIn_Pydantic):
    supplier_obj = await Supplier.create(**supplier_info.dict(exclude_unset = True)) 
    response = await Supplier_Pydantic.from_tortoise_orm(supplier_obj)
    return {"status": "ok", "data": response}


@app.get("/supplier")
async def get_all_suppliers():
    response = await Supplier_Pydantic.from_queryset(Supplier.all())
    return {"status": "ok", "data": response}

@app.get("/supplier/{supplier_id}")
async def get_specific_supplier(supplier_id: int):
    response = await Supplier_Pydantic.from_queryset_single(Supplier.get(id = supplier_id))
    return {"status": "ok", "data": response}

@app.put("/supplier/{supplier_id}")
async def updat_supplier(supplier_id: int, update_info: SupplierIn_Pydantic):
    supplier = await Supplier.get(id = supplier_id)
    update_info = update_info.dict(exclude_unset = True)
    supplier.name = update_info["name"]
    supplier.company = update_info["company"]
    supplier.email = update_info["email"]
    supplier.phone = update_info["phone"]
    await supplier.save()
    response = await Supplier_Pydantic.from_tortoise_orm(supplier)
    return {"status": "ok", "data": response}



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