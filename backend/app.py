from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.staticfiles import StaticFiles
import uvicorn

# Database setup
from tortoise.contrib.fastapi import register_tortoise
from models import Supplier_Pydantic, SupplierIn_Pydantic, Supplier, Product_Pydantic, ProductIn_Pydantic, Product

app = FastAPI(
    swagger_ui_parameters={"customCssUrl": "/static/custom.css?v=1.0.0"}
)

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=BASE_DIR / "frontend" / "templates")

app.mount("/static", StaticFiles(directory=BASE_DIR / "frontend" / "static"), name="static")


@app.get("/")
async def Template_Render(req: Request):
    return templates.TemplateResponse(
        name = "index.html",
        context = {"request": req}
    )

# CRUD Operations for Supplier Model
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
async def update_supplier(supplier_id: int, update_info: SupplierIn_Pydantic):
    supplier = await Supplier.get(id = supplier_id)
    update_info = update_info.dict(exclude_unset = True)
    supplier.name = update_info["name"]
    supplier.company = update_info["company"]
    supplier.email = update_info["email"]
    supplier.phone = update_info["phone"]
    await supplier.save()
    response = await Supplier_Pydantic.from_tortoise_orm(supplier)
    return {"status": "ok", "data": response}

@app.delete("/supplier/{supplier_id}")
async def delete_supplier(supplier_id: int):
    await Supplier.get(id = supplier_id).delete()
    return {"status": "ok", "data": f"Supplier with id {supplier_id} has been deleted."}

# CRUD Operations for Product Model
@app.post("/product/{supplier_id}")
async def add_product(supplier_id: int, products_details: ProductIn_Pydantic):
    supplier = await Supplier.get(id = supplier_id)
    products = products_details.dict(exclude_unset = True)
    products_details['revenue'] += products_detail['quantity_sold'] * products_details['unit_price']
    product_obj = await Product.create(**products_details, supplied_by = supplier)
    response = await Product_Pydantic.from_tortoise_orm(product_obj)
    return {"status": "ok", "data": response}

@app.get("/products")
async def get_products():
    response = await Product_Pydantic.from_queryset(Product.all())
    return {"status": "ok", "data": response}

@app.get("/product/{product_id}")
async def specific_product(product_id: int):
    response = await Product_Pydantic.from_queryset_single(Product.get(id = id))
    return {"status": "ok", "data": response}

@app.put("/product/{product_id}")
async def update_product(id: int, update_info: ProductIn_Pydantic):
    product = await Product.get(product_id = product_id)
    update_info = update_info.dict(exclude_unset = True)
    product.name = update_info['name']
    product.quantity_in_stock = update_info['quantity_in_stock']
    product.revenue += (update_info['quantity'] * update_info['unit_price']) + update_info['revenue']
    product.quantity_sold += update_info['quantity_sold']
    product.unit_price = update_info['unit_price']
    await product.save()
    response = await Product_Pydantic.from_tortoise_orm(product)
    return {"status": "ok", "data": response}

@app.delete('/product/{product_id}')
async def delete_product(product_id: int):
    await Product.filter(id == product_id).delete()
    return {"status": "ok"}








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