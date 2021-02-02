import unittest
import json
import sys
sys.path.append("..")
from flask import Flask, request, Response
from api.models import House
from api.views import houses
from api import db, create_app


app = create_app()

def valid_json(json_str):
    try:
        json_obj = json.loads(json_str)
    except ValueError as e:
        return False
    return True

class MyTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_houses(self):
        page = self.app.get('/api/houses')
        data_str = page.data.decode("utf-8")
        assert page.data is not None
        assert page.content_type == 'application/json'
        assert valid_json(page.data.decode("utf-8"))
        json_obj = json.loads(data_str)
        assert page.status == '200 OK'
        assert json_obj['itemCount'] == 11

    def test_single_house(self):
        page = self.app.get('/api/houses/1')
        data_str = page.data.decode("utf-8")
        assert page.data is not None
        assert page.content_type == 'application/json'
        assert valid_json(page.data.decode("utf-8"))
        assert page.status == '200 OK'
        json_obj = json.loads(data_str)
        assert json_obj['firstName'] == " Jack"
        assert json_obj['lastName'] == " Smith"
        assert json_obj['street'] == " South St"
        assert json_obj['zip'] == " 01749"
        assert json_obj['propertyType'] == " Single Family"

    def test_single_house_2(self):
        page = self.app.get('/api/houses/7')
        data_str = page.data.decode("utf-8")
        assert page.data is not None
        assert page.content_type == 'application/json'
        assert valid_json(page.data.decode("utf-8"))
        json_obj = json.loads(data_str)
        assert page.status == '200 OK'
        assert json_obj['firstName'] == " Jake"
        assert json_obj['lastName'] == " Wilcox"
        assert json_obj['street'] == " Carter St"
        assert json_obj['zip'] == " 01749"
        assert json_obj['propertyType'] == " Multi Family"

    def test_404(self):
        page = self.app.get('/notapage')
        assert page.status == '404 NOT FOUND'

    def test_400(self):
        data = {"firstName": 'Homer', "lastName": 'Simpson'}
        # incomplete payload so it should 400
        page = self.app.put('/api/houses/9', json=data)
        assert page.status == "400 BAD REQUEST"

    def test_put(self):
        data = {
            "firstName": "John",
            "lastName": "Smith",
            "street": "Broad St",
            "city": "Hudson",
            "state": "MA",
            "zip": "01749",
            "propertyType": "Single Family",
            "location":"http://127.0.0.1:5000/api/houses/11"
        }
        page = self.app.put('/api/houses/11', json=data)
        data_str = page.data.decode("utf-8")
        # resp = make_response
        # print(resp.headers)
        assert page.status == '200 OK' or page.status == '201 CREATED'
        assert page.content_type == 'application/json'
        assert page.data is not None
        assert valid_json(page.data.decode("utf-8"))


if __name__ == '__main__':
    unittest.main()