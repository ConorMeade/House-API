import pandas as pd
from flask import Blueprint, jsonify, request, render_template, abort
from werkzeug.exceptions import InternalServerError
from . import db
from .models import House
import csv
import json

# using our Blueprint from __init__.py to create views
houses = Blueprint('houses', __name__)

def init_db():
    if db.session.query(House).first():
        # print('database already initialized')
        # if there is an entry in the database, then we have already initialized it so we return
        return
    with open('houses.csv') as f:
        # DictReader will read each column of table and make a python dictionary (hash table)
        reader = csv.DictReader(f)
        for house_dict in reader:
            # for each dictionary, we make an entry into houseapi.db
            entry = House(id=int(house_dict['House ID']), firstName=house_dict[' Owner First Name'], lastName=house_dict[' Owner Last Name'],
                            street=house_dict[' Street'], city=house_dict[' City'], state=house_dict[' State'], zip=house_dict[' Zip'], propertyType=house_dict[' Property Type'])
            db.session.add(entry)
            db.session.commit()


@houses.route('/api/houses', methods=['GET'])
def get_all_houses():
    init_db()
    houses_list_query = House.query.all()

    houses = []

    for entry in houses_list_query:
        # create our 'items' array
        houses.append({"firstName" : entry.firstName, "lastName" : entry.lastName, "street" : entry.street, "zip" : entry.zip, "propertyType" : entry.propertyType, "location": "http://" + request.host + "/api/houses/" + str(entry.id) })
    # Response Header will be Content-Type: application/json since we use jsonify
    return jsonify({'itemCount' : len(houses), 'items' : houses})

@houses.route('/api/houses/<int:id>', methods=['GET', 'PUT'])
def single_house(id):
    init_db()
    if request.method == 'GET':
        # GET request
        house_data = House.query.filter_by(id=id).first()
        if house_data is None:
            abort(400)
        # print(house_data)
        json_resp = ({"firstName" : house_data.firstName, "lastName" : house_data.lastName, "street" : house_data.street, "zip" : house_data.zip, "propertyType" : house_data.propertyType, "location": "http://" + request.host + "/api/houses/" + str(house_data.id) })
    else:
        # PUT request
        # retrieve data
        house_data = request.get_json()
        if house_data is None:
            # if we dont get any data we send a bad request
            abort(400)
        try:
            # if we do not get all this data we abort as it is a bad request
            newId=int(house_data['location'].rsplit('/', 1)[-1])
            firstName=house_data['firstName']
            lastName=house_data['lastName']
            street=house_data['street']
            city=house_data['city']
            state=house_data['state']
            zip=house_data['zip']
            propertyType=house_data['propertyType']
            location=house_data['location']
        except:
            abort(400)

        exists = house_data = House.query.filter_by(id=newId).first()

        if not exists:
            # we have a new record
            entry = House(id=newId, firstName=firstName, lastName=lastName, street=street, city=city, state=state, zip=zip, propertyType=propertyType)
            db.session.add(entry)
            db.session.commit()
            # response body 201 Created HTTP response because we have successfully added a new entry
            return jsonify({"firstName" : firstName, "lastName" : lastName, "street" : street, "zip" : zip, "propertyType" : propertyType, "location": "http://" + request.host + "/api/houses/" + str(newId)}), 201
        else:
            # a record with this id already exists
            # we delete the existing entry
            House.query.filter_by(id=newId).delete()

            # and add the new entry
            entry = House(id=newId, firstName=firstName, lastName=lastName, street=street, city=city, state=state, zip=zip, propertyType=propertyType)
            db.session.add(entry)
            db.session.commit()
            return jsonify({"firstName" : firstName, "lastName" : lastName, "street" : street, "zip" : zip, "propertyType" : propertyType, "location": "http://" + request.host + "/api/houses/" + str(newId)}), 200

    return jsonify(json_resp)


@houses.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@houses.errorhandler(400)
def bad_request(error):
    return render_template('400.html'), 400

@houses.errorhandler(InternalServerError)
def handle_500(error):
    return render_template('500.html'), 500
