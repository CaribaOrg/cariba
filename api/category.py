#!/usr/bin/python3

from flask import jsonify
from api import api_restplus
from models import strg
from models.category import Category
from flask_restx import Resource

class Categories(Resource):
    def get(self):
        categories = strg.all(Category)
        return jsonify([category.dictify() for category in categories])


class Categories2(Resource):
    def get(self, category_id):
        category = strg.search(cls=Category, id=category_id)
        if not category:
            return 'None found', 404
        category_dict = category.dictify()
        category_dict.pop('parent_id')
        category_dict['parent'] = category.parent.dictify() if category.parent else None
        category_dict['children'] = recursion(category)
        category_dict['products'] = len(category.products)
        return jsonify(category_dict)

def recursion(obj):
    if not obj.children:
        return None
    children_list = []
    for child in obj.children:
        c_dict = child.dictify()
        c_dict.pop('parent_id')
        children = recursion(child)
        if children:
            c_dict['children'] = children
        children_list.append(c_dict)
    return children_list

api_restplus.add_resource(Categories, '/categories')
api_restplus.add_resource(Categories2, '/categories/<category_id>')