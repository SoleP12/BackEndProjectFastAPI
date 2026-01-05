from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Supplier(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    company = fields.CharField(max_length=20)
    email = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=15)


class Product(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30, nullable=False)
    quantity_in_stock = fields.IntField(default=0)
    quantity_sold = fields.IntField(default=0)
    unit_price = fields.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    revenue = fields.DecimalField(max_digits=20, decimal_places=3, default=0.00)
    
    # ForeignKey to Supplier
    supplied_by = fields.ForeignKeyField('models.Supplier', related_name='goods_supplied')

# -----------------------------
# Pydantic Models (after class definitions)
# -----------------------------

# Product
Product_Pydantic = pydantic_model_creator(Product, name="Product")
ProductIn_Pydantic = pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True)

# Supplier
Supplier_Pydantic = pydantic_model_creator(Supplier, name="Supplier")
SupplierIn_Pydantic = pydantic_model_creator(Supplier, name="SupplierIn", exclude_readonly=True)

