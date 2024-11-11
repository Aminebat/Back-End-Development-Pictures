from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

# Load the JSON data file
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")

# Helper function to load and save data
def load_data():
    with open(json_url, "r") as f:
        return json.load(f)

def save_data(data):
    with open(json_url, "w") as f:
        json.dump(data, f, indent=4)

data: list = load_data()

######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    """Return the length of the data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a picture by its ID"""
    picture = next((pic for pic in data if pic["id"] == id), None)
    if picture is None:
        return {"message": "Picture not found"}, 404
    return jsonify(picture), 200

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture"""
    new_picture = request.json
    # Ensure the picture has an ID and does not already exist
    if any(pic["id"] == new_picture["id"] for pic in data):
        return {"Message": f"Picture with id {new_picture['id']} already present"}, 409

    data.append(new_picture)
    save_data(data)
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture"""
    updated_picture = request.json
    # Find the picture with the given ID
    picture_index = next((index for index, pic in enumerate(data) if pic["id"] == id), None)
    
    if picture_index is None:
        return {"message": "Picture not found"}, 404

    # Update the picture details
    data[picture_index] = updated_picture
    save_data(data)
    return jsonify(updated_picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by its ID"""
    picture = next((pic for pic in data if pic["id"] == id), None)
    if picture is None:
        return {"message": "Picture not found"}, 404

    data.remove(picture)
    save_data(data)
    return "", 204
