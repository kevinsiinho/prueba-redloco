
#librerias necesarias
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId  # Para manejar los IDs de MongoDB

# Configuración
app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/redloco_db"
mongo = PyMongo(app)
db = mongo.db  # Acceso a la base de datos


#CRUD apis

@app.route('/items', methods=['GET'])
def get_items():
    items = list(db.items.find({}))  # Obtener todos los items
    # Convertir ObjectId a string para JSON
    for item in items:
        item['_id'] = str(item['_id'])
    return jsonify(items)


@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    # MongoDB automáticamente añade un _id único
    result = db.items.insert_one(data)
    # Devolver el item creado con su ID
    new_item = db.items.find_one({'_id': result.inserted_id})
    new_item['_id'] = str(new_item['_id'])
    return jsonify(new_item), 201

@app.route('/items/<string:id>', methods=['PUT'])
def update_item(id):
    data = request.json
    # Convertir el string ID a ObjectId
    obj_id = ObjectId(id)
    db.items.update_one({'_id': obj_id}, {'$set': data})
    updated_item = db.items.find_one({'_id': obj_id})
    updated_item['_id'] = str(updated_item['_id'])
    return jsonify(updated_item)

@app.route('/items/<string:id>', methods=['DELETE'])
def delete_item(id):
    obj_id = ObjectId(id)
    db.items.delete_one({'_id': obj_id})
    return jsonify({'message': 'Item deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)