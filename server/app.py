#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask extensions
db.init_app(app)
migrate = Migrate(app, db)

# Initialize Flask-Restful API
api = Api(app)

# Resource classes
class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
            is_in_stock=data['is_in_stock']  # Assuming is_in_stock is part of POST data
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        return make_response(jsonify(plant.to_dict()), 200)

class UpdatePlant(Resource):
    def patch(self, id):
        data = request.get_json()

        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        # Update the plant attributes based on the request data
        if 'name' in data:
            plant.name = data['name']
        if 'image' in data:
            plant.image = data['image']
        if 'price' in data:
            plant.price = data['price']
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']

        db.session.commit()

        return make_response(jsonify(plant.to_dict()), 200)

class DeletePlant(Resource):
    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response('', 204)

        db.session.delete(plant)
        db.session.commit()

        return make_response('', 204)

# Add resources to API with respective endpoints
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')
api.add_resource(UpdatePlant, '/plants/<int:id>')
api.add_resource(DeletePlant, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)