#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(jsonify(body), 200)

# Existing route for earthquake by ID
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    """Fetch an earthquake by its ID and return it as a JSON response."""
    earthquake = Earthquake.query.get(id)
    if earthquake:
        # Serialize the earthquake model to a dictionary and return
        return jsonify(earthquake.to_dict()), 200
    else:
        # Return an error message if no earthquake is found
        return jsonify({"message": f"Earthquake {id} not found."}), 404

# Existing route for earthquakes by magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    """Fetch earthquakes with a magnitude >= the given value."""
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quake_list = [quake.to_dict() for quake in earthquakes]
    response = {
        "count": len(quake_list),
        "quakes": quake_list
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
