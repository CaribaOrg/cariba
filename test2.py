#!/usr/bin/python3

from models.category import Category
from models.product import Product
from models.base_model import BaseModel, Base
from models import strg

cat_dict = {
        'name': 'main_cat',
        'description': 'car part',
        'active': True,
        'icon': 'None'
        }

cat = Category(**cat_dict)
cat.save()

print('------------Category:')
print(cat.__dict__)

cat1_dict = {
        'name': 'sub_cat1',
        'parent_id': cat.id
        }

cat1 = Category(**cat1_dict)
cat1.save()

print('------------Category: 1')
print(cat1.__dict__)

cat2_dict = {
        'name': 'sub_cat2',
        'parent_id': cat.id
        }

cat2 = Category(**cat2_dict)
cat2.save()

print('------------Category: 2')
print(cat2.__dict__)

print('------------Relationships:')
print('cat.parent')
print(cat.parent)
print('cat.children')
for child in cat.children:
    print(child.id)
print('cat1.parent')
print(cat1.parent.id)
print('cat1.children')
for child in cat1.children:
    print(child.id)
print('cat2.parent')
print(cat2.parent.id)
print('cat2.children')
for child in cat2.children:
    print(child.id)

prod1_dict = {
        'name': 'prod1',
        'category_id': cat1.id,
        'price': 14,
        'oem_number': '123'
        }

prod1 = Product(**prod1_dict)
prod1.save()

print('------------Product: 1')
print(prod1.__dict__)

prod2_dict = {
        'name': 'prod2',
        'category_id': cat1.id,
        'price': 14.99,
        }

prod2 = Product(**prod2_dict)
prod2.save()

print('------------Product: 2')
print(prod2.__dict__)

print('cat1.products')
for product in cat1.products:
    print(product.id)
print('prod1.category')
print(prod1.category.id)

