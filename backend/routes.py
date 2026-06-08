from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

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
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Returns the array of all picture objects as JSON"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Finds a single picture by its ID descriptor"""
    for picture in data:
        if picture.get("id") == id:
            return jsonify(picture), 200
            
    return jsonify({"message": f"Picture with id {id} not found"}), 404


######################################################################
# CREATE A PICTURE (EXERCISE 4 UPDATED)
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Creates a new picture resource from incoming JSON body"""
    new_picture = request.get_json()
    if not new_picture:
        return jsonify({"Message": "Invalid input data"}), 400

    # Exercise 4 specific check: Return 302 and exact string matching if duplicate ID exists
    for picture in data:
        if picture.get("id") == new_picture.get("id"):
            return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    data.append(new_picture)
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Updates an existing picture matching the provided ID parameter"""
    updated_data = request.get_json()
    if not updated_data:
        return jsonify({"message": "Invalid input data"}), 400

    for index, picture in enumerate(data):
        if picture.get("id") == id:
            data[index] = updated_data
            return jsonify(data[index]), 200

    return jsonify({"message": f"Picture with id {id} not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Deletes a picture element and returns a 204 No Content status"""
    for index, picture in enumerate(data):
        if picture.get("id") == id:
            del data[index]
            return "", 204

    return jsonify({"message": f"Picture with id {id} not found"}), 404