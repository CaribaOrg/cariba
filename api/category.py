#!/usr/bin/python3

from flask import jsonify, request
from api import api_restx
from models import strg
from models.category import Category
from flask_restx import Resource, fields

category_model = api_restx.model('Category', {
    'name': fields.String(required=True, description='Name of the category'),
    'parent_id': fields.String(required=False, description='Parent ID of the category', default=None),
    'active': fields.Boolean(required=False, description='Active status of the category', default=True),
})

class Categories(Resource):
    @api_restx.response(200, 'Successful Operation')
    def get(self):
        categories = strg.all(Category)
        return jsonify([category.dictify() for category in categories])
    
    @api_restx.response(200, 'Successful Operation')
    @api_restx.response(400, 'Invalid Request Format')
    @api_restx.response(404, 'Invalid ID supplied')
    @api_restx.expect(category_model)
    def post(self):
        data = request.get_json()
        if not data:
            return {'error': 'Invalid request format, expected JSON'}, 400
        if 'name' not in data:
            return {'error': 'Name is required'}, 404
        category = Category(name=data.get('name'), parent_id=data.get('parent_id'), active=data.get('active', True))
        return jsonify(category.dictify())


class Categories2(Resource):
    @api_restx.response(200, 'Successful Operation')
    @api_restx.response(404, 'Invalid ID supplied')
    def get(self, category_id):
        category = strg.search(cls=Category, id=category_id)
        if not category:
           return {'error': 'None found'}, 404
        category_dict = category.dictify()
        category_dict.pop('parent_id')
        category_dict['parent'] = category.parent.dictify() if category.parent else None
        category_dict['children'] = recursion(category)
        category_dict['products'] = len(category.products)
        return jsonify(category_dict)
    
    @api_restx.expect(category_model)
    @api_restx.response(200, 'Successful Operation')
    @api_restx.response(400, 'Invalid Request Format')
    @api_restx.response(404, 'Invalid ID supplied')
    def put(self, category_id):
        category = strg.search(cls=Category, id=category_id)
        if not category:
           return {'error': 'None found'}, 404
        data = request.get_json()
        if not data:
            return {'error': 'Invalid request format, expected JSON'}, 400
        ignore_list = ['id', 'created_at', 'updated_at', 'parents', 'children', 'products']
        for key, value in data.items():
            if key not in ignore_list:
                setattr(category, key, value)
        category.save()
        return jsonify(category.dictify())
    
    @api_restx.response(200, 'Successful Operation')
    @api_restx.response(404, 'Invalid ID supplied')
    def delete(self, category_id):
        category = strg.search(cls=Category, id=category_id)
        if not category:
            return {'error': 'None found'}, 404
        category.delete()
        return jsonify({})

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

class CategoryPart(Resource):
    @api_restx.response(200, 'Successful Operation')
    @api_restx.response(404, 'Invalid ID supplied')
    def get(self, category_id):
        category = strg.search(cls=Category, id=category_id)
        if not category:
           return {'error': 'None found'}, 404
        cat_dict = {}
        cat_dict['name'] = category.name
        prod_list = []
        for prod in category.products:
            p_dict = prod.dictify()
            p_dict.pop('category_id')
            prod_list.append(p_dict)
        cat_dict['parts'] = prod_list
        return jsonify(cat_dict)

api_restx.add_resource(Categories, '/categories')
api_restx.add_resource(Categories2, '/categories/<category_id>')
api_restx.add_resource(CategoryPart, '/categories/<category_id>/parts')