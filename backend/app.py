# FastApi imports
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.staticfiles import StaticFiles
import uvicorn


# Database setup imports and models 
from tortoise.contrib.fastapi import register_tortoise
from models import Supplier_Pydantic, SupplierIn_Pydantic, Supplier, Product_Pydantic, ProductIn_Pydantic, Product


# FastAPI app initialization with custom CSS for Swagger UI
app = FastAPI(
    title="Supplier and Product Management API"
)


#Returns the parent directory of the current file we use this to point to frontend files
BASE_DIR = Path(__file__).resolve().parent.parent


# Create templates variable to point to the templates directory using BASE_DIR
templates = Jinja2Templates(directory=BASE_DIR / "frontend" / "templates")


# Home Root that will render index.html that we created in the templates directory for the homepage
@app.get("/")
async def Template_Render(req: Request):
    return templates.TemplateResponse(
        name = "index.html",
        context = { "request": req}
    )


# CRUD Operations for Supplier Model
# Create Supplier endpoint that will add a new supplier to the database
# The supplier_info parameter is of type SupplierIn_Pydantic which is a Pydantic model that we created in models.py
# The functions takes the supplier_info and creates a new Supplier object in the database
# It then returns the created Supplier object as a response
@app.post("/supplier")
async def add_supplier(supplier_info: SupplierIn_Pydantic):
    supplier_obj = await Supplier.create(**supplier_info.dict(exclude_unset = True)) 
    response = await Supplier_Pydantic.from_tortoise_orm(supplier_obj)
    return {"status": "ok", "data": response}


# Supplier endpoint that will get all suppliers from the database
# The function queries all Supplier objects and converts to 
@app.get("/supplier")
async def get_all_suppliers():
    response = await Supplier_Pydantic.from_queryset(Supplier.all())
    return {"status": "ok", "data": response}


# Returns a specific supplier based on the supplier_id passed in the URL
# Query the database with the supplier_id and returns the supplier object as a response
@app.get("/supplier/{supplier_id}")
async def get_specific_supplier(supplier_id: int):
    response = await Supplier_Pydantic.from_queryset_single(Supplier.get(id = supplier_id))
    return {"status": "ok", "data": response}


# Updates the supplier based on the supplier_id passed in the URL
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


# Finds the specific supplier based on the supplier_id and delets teh from the database and returns a response
@app.delete("/supplier/{supplier_id}")
async def delete_supplier(supplier_id: int):
    await Supplier.get(id = supplier_id).delete()
    return {"status": "ok", "data": f"Supplier with id {supplier_id} has been deleted."}


# CRUD Operations for Product Model
# Create Product endpoint that will add a new product to the database
# Use function add_product that will take supplier_id and product_details as parameters
# Get supplier object with supplier_id, creates product_data dictionary from product_details 
# Calculate revenue based on quantity_sold and unit_price and returns created Product object as response
# Then cretaes new product_obj in database linked to supplier by supplier_id
@app.post("/product/{supplier_id}")
async def add_product(supplier_id: int, products_details: ProductIn_Pydantic):
    supplier = await Supplier.get(id = supplier_id)
    product_data = products_details.dict(exclude_unset=True)
    product_data['revenue'] = product_data.get('revenue', 0) + product_data['quantity_sold'] * product_data['unit_price']
    product_obj = await Product.create(**product_data, supplied_by=supplier)
    response = await Product_Pydantic.from_tortoise_orm(product_obj)
    return {"status": "ok", "data": response}


# Gets all products from teh database by queries all product objects
@app.get("/products")
async def get_products():
    response = await Product_Pydantic.from_queryset(Product.all())
    return {"status": "ok", "data": response}


# Finds a specific product based on the product_id passed in the URL
@app.get("/product/{product_id}")
async def specific_product(product_id: int):
    response = await Product_Pydantic.from_queryset_single(Product.get(id = product_id))
    return {"status": "ok", "data": response}


# Updates a specific product based upon the product_id passed in url
# Creates temp variable update_info to hold the updated information passed in the request body
# Then updates the product fields accordingly and saves the changes to the database
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


# Deletes specific product based on the product_id passed in the URL with delete query
@app.delete('/product/{product_id}')
async def delete_product(product_id: int):
    await Product.filter(id = product_id).delete()
    return {"status": "ok"}


# Database setup using sqlite database used locally, has built in error handling and ORM exceptions
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


# Template rendering for ProductSuppliers.html that will display all suppliers and products from the database
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
