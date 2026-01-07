from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.staticfiles import StaticFiles
import uvicorn

# email imports for fastAPI
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from typing import List
from dotenv import dotenv_values

# Load environment variables
credentials = (dotenv_values(".env"))

# Database setup
from tortoise.contrib.fastapi import register_tortoise
from models import Supplier_Pydantic, SupplierIn_Pydantic, Supplier, Product_Pydantic, ProductIn_Pydantic, Product

app = FastAPI(
    swagger_ui_parameters={"customCssUrl": "/static/custom.css?v=2.0.0"}
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
    product_data = products_details.dict(exclude_unset=True)
    product_data['revenue'] = product_data.get('revenue', 0) + product_data['quantity_sold'] * product_data['unit_price']
    product_obj = await Product.create(**product_data, supplied_by=supplier)
    response = await Product_Pydantic.from_tortoise_orm(product_obj)
    return {"status": "ok", "data": response}

@app.get("/products")
async def get_products():
    response = await Product_Pydantic.from_queryset(Product.all())
    return {"status": "ok", "data": response}

@app.get("/product/{product_id}")
async def specific_product(product_id: int):
    response = await Product_Pydantic.from_queryset_single(Product.get(id = product_id))
    return {"status": "ok", "data": response}

@app.put("/product/{product_id}")
async def update_product(product_id: int, update_info: ProductIn_Pydantic):
    product = await Product.get(id = product_id)
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
    await Product.filter(id = product_id).delete()
    return {"status": "ok"}

class EmailSchema(BaseModel):
    email: List[EmailStr]

class EmailContent(BaseModel):
    message: str
    subject: str

# Emailing Sending
conf = ConnectionConfig(
    MAIL_USERNAME = credentials["EMAIL"],
    MAIL_PASSWORD = credentials["PASS"],
    MAIL_FROM = credentials["EMAIL"],
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
)


@app.post("/email/{product_id}")
async def send_email(product_id: int, content: EmailContent):
    product = await Product.get(id = product_id)
    supplier = await product.supplied_by 
    supplier_email = [supplier.email]


    html = f"""
    <h1>Test From Fast API sent for product {product_id}</h1>
    <br>
    <p>{content.subject}</p>
    <br>
    <p>{content.message}</p>
    <br>
    <h1>Test Now Complete</h1>
    """
    
    message = MessageSchema(
        subject = content.subject,
        recipients = supplier_email, #List of recipients
        body = html,
        subtype = "html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"status": "ok", "data": f"Email has been sent to supplier {supplier.name} for product {product.name}"}



# Database setup
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,


)

@app.get("/ProductSuppliers")
async def ProductSuppliers(request: Request):
    suppliers = await Supplier_Pydantic.from_queryset(Supplier.all())
    products = await Product_Pydantic.from_queryset(Product.all())
    return templates.TemplateResponse(
        "ProductSuppliers.html",
        {"request": request, "suppliers": suppliers, "products": products}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)


# source ./venv/bin/activate Activate virtual enviromonet