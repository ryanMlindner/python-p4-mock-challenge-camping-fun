#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Index(Resource):
    
    def get(self):

        response_dict = {
            "index" : "Fun with Camping. Camping with Fun."
        }

        response = make_response(
            response_dict,
            200
        )
        
        return response

class Campers(Resource):

    def get(self):
        #why exactly are we limiting this get? I'll do it but it makes no sense
        campers_dict = []
        for camper in Camper.query.all():
            camper_dict = {
                "id": camper.id,
                "name": camper.name,
                "age": camper.age,
            }
            campers_dict.append(camper_dict)

        response = make_response(
            campers_dict,
            200
        )
        return response
    
    def post(self):
        json = request.get_json()

        try:
            new_camper = Camper(
                name = json["name"],
                age = json["age"]
            )
            db.session.add(new_camper)
            db.session.commit()
            camper_dict = new_camper.to_dict()

            response = make_response(
                camper_dict,
                201
            )
            return response
        
        except ValueError as ve:
            response = make_response(
                {"errors": ["validation errors"]},
                400
            )
            return response
        
class CampersByID(Resource):

    def get(self, id):
        camper = Camper.query.filter(Camper.id == id).first()

        if camper == None:
            response = make_response(
                {"error": "Camper not found"},
                404
            )
        else:
            camper_dict = camper.to_dict()
            response = make_response(
                camper_dict,
                200
            )
        return response
    
    def patch(self, id):
        camper = Camper.query.filter(Camper.id == id).first()
        try:
            if camper == None:
                response = make_response(
                    {"error": "Camper not found"},
                    404
                )
                return response
            else:
                json = request.get_json()
                
                camper.name = json["name"]
                camper.age = json["age"]
                #TODO validation errors???
                camper_dict = {
                    "id": camper.id,
                    "name": camper.name,
                    "age": camper.age,
                }

                response = make_response(
                    camper_dict,
                    202
                )
                return response
        except ValueError as ve:
            response = make_response(
                {"errors": ["validation errors"]},
                400
            )
            return response

class Activities(Resource):
    
    def get(self):
        #again with the formatting weirdness
        activities_dict = []
        for activity in Activity.query.all():
            activity_dict = {
                "id": activity.id,
                "name": activity.name,
                "difficulty": activity.difficulty,
            }
            activities_dict.append(activity_dict)

        response = make_response(
            activities_dict,
            200
        )
        return response

class ActivitiesByID(Resource):

    def delete(self, id):
        activity = Activity.query.filter(Activity.id == id).first()
        if activity == None:
            response = make_response(
                {"error": "Activity not found"},
                404
            )
        else:
            db.session.delete(activity)
            db.session.commit()
            response = make_response(
                {},
                204
            )
        return response

class Signups(Resource):

    def post(self):
        json = request.get_json()

        try:
            new_signup = Signup(
                camper_id = json["camper_id"],
                activity_id = json["activity_id"],
                time = json["time"]
            )
            db.session.add(new_signup)
            db.session.commit()
            camper_dict = new_signup.to_dict()

            response = make_response(
                camper_dict,
                201
            )
            return response
        
        except ValueError as ve:
            response = make_response(
                {"errors": ["validation errors"]},
                400
            )
            return response
        



api.add_resource(Index, '/')
api.add_resource(Campers, '/campers')
api.add_resource(CampersByID, '/campers/<int:id>')
api.add_resource(Activities, '/activities')
api.add_resource(ActivitiesByID, '/activities/<int:id>')
api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
