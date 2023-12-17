from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from models import *

###########################################################################################################
# ROUTES -------------------------------------------------------------------------------------------------#
###########################################################################################################
@app.route('/')
def hello():
    return("Hello World!")

@app.route('/hello', methods=['GET'])
def greetings():
    return("Hello, world! HELLO HELLO")

# Menu Items Route Handlers
@app.route('/menu_items', methods=['GET', 'POST'])
def menu_items():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.json
        new_menu_item = MenuItem(name=data['name'], price=data['price'], category_id=data['category_id'], image=data.get('image'))
        db.session.add(new_menu_item)
        db.session.commit()
        response_object['message'] = 'Menu item added successfully'
        response_object['id'] = new_menu_item.id
    else:   
        category_id = request.args.get('category_id')

        if category_id:
            # Filter menu items by category_id
            menu_items = MenuItem.query.filter_by(category_id=category_id).all()
        else:
            # Retrieve all menu items if no category_id is provided
            menu_items = MenuItem.query.all()

        response_object['menu_items'] = [
            {'id': item.id, 'name': item.name, 'price': item.price, 'category_id': item.category_id, 'image': item.image}
            for item in menu_items
        ]

    return jsonify(response_object)

# return menu by id
@app.route('/menu_items/<int:item_id>', methods=['PUT', 'DELETE', 'POST', 'GET'])
def single_menu_item(item_id):
    response_object = {'status': 'success'}
    menu_item = MenuItem.query.get(item_id)
    
    if request.method == 'GET':
        if menu_item:
            response_object['menu_item'] = {
                'id': menu_item.id,
                'name': menu_item.name,
                'price': menu_item.price,
                'category_id': menu_item.category_id,
                'image': menu_item.image,
                # Add other fields as needed
            }
        else:
            response_object['error'] = 'Menu item not found'
    elif request.method == 'PUT':
        if menu_item:
            data = request.json
            menu_item.name = data['name']
            menu_item.price = data['price']
            menu_item.category_id = data['category_id']
            menu_item.image = data.get('image')
            db.session.commit()
            response_object['message'] = 'Menu item updated successfully'
        else:
            response_object['error'] = 'Menu item not found'
    elif request.method == 'DELETE':
        if menu_item:
            db.session.delete(menu_item)
            db.session.commit()
            response_object['message'] = 'Menu item deleted successfully'
        else:
            response_object['error'] = 'Menu item not found'

    return jsonify(response_object)

# ability to show images
@app.route('/static/images/<path:filename>')
def serve_static(filename):
    return send_from_directory('static/images', filename)

# route for fetching category
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    categories_list = [{'category_id': category.category_id, 'name': category.name} for category in categories]
    return jsonify({'categories': categories_list})

# route for tables
@app.route('/tables', methods=['GET'])
def get_tables():
    tables = TableStatus.query.all()
    print(tables)
    tables_list = [{'table_id' : table.id, 'occupied': False if table.occupied == 0 else True} for table in tables]
    return jsonify({'tables_list': tables_list})

if __name__ == "__main__":
    app.run(debug=True)