from tortoise.models import Model
from tortise import fields
from tortise.contrib.pydantic import pydantic_model_creator


class Product(Model):
    # ID will be primary key
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=30, nullable=False)

    quantity_in_stock = fields.IntField(default = 0)

    quantity_sold = fields.IntField(default = 0)

    unit_price = fields.DecimalField(max_digits=8, decimal_places=2, default= 0.00)
    revenue = fields.DecimalField(max_digits=20, decimal_places=3, default= 0.00)

    # Foreign Key to Supplier model
    supplied_by = fields.ForeignKeyField('models.supplier', related_name='goods_supplied')

    class Supplier(Model):
        id = fields.IntField(pk=True)
        name = fields.CharField(max_length=20)
        company = fields.CharField(max_length=20)
        email = fields.CharField(max_length= 100)
        phone = fields.CharField(max_length=15)


    # Pydantic Model Creation
    prodcut_pydantic = pydantic_model_creator(Product, name="Product")
    # Pydantic Model to Accept incoming data, Excludes Readonly fields
    prodcut_pydanticIn = pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True)


    supplier_pydantic = pydantic_model_creator(Supplier, name="Supplier")
    # Pydantic Model to Accept incoming data, Excludes Readonly fields
    supplier_pydanticIn = pydantic_model_creator(Supplier, name="SupplierIn", exclude_readonly=True)

