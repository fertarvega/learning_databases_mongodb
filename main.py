from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import pymongo
from bson.json_util import dumps, ObjectId
import db_config as database

app=Flask(__name__)
api=Api(app)

"""

    database.db.Badges.

    .database is the config file
    .db is the database name
    .CollectionName     the next part is the collection

"""

class Test(Resource):
    def get(self):
        return jsonify({"message":"Test ok, you are connect"})

class Badge(Resource):

    def get(self,by,data):
        response = self.abort_if_not_exist(by, data)
        response['_id'] = str(response['_id'])
        return jsonify(response)

    def post(self):
        _id = str(database.db.Badges.insert_one(
            {
                'header_img_url': request.json['header_img_url'],
                'profile_picture_url': request.json['profile_picture_url'],
                'name': request.json['name'],
                'age': request.json['age'],
                'city': request.json['city'],
                'followers': request.json['followers'],
                'likes': request.json['likes'],
                'posts': request.json['posts'],
                'post':request.json['post']
            }
        ).inserted_id)

        return jsonify({"_id":_id})

    def put(self, by, data):
        response = self.abort_if_not_exist(by, data)

        for key, value in request.json.items():
            response[key] = value

        database.db.Badges.update_one({'_id':ObjectId(response['_id'])},
        {'$set':{
                'header_img_url': request.json['header_img_url'],
                'profile_picture_url': request.json['profile_picture_url'],
                'name': request.json['name'],
                'age': request.json['age'],
                'city': request.json['city'],
                'followers': request.json['followers'],
                'likes': request.json['likes'],
                'posts': request.json['posts'],
                'post':request.json['post']
            }})

        response['_id'] = str(response['_id'])
        return jsonify(response)

    def abort_if_not_exist(self, by, data):
        if by == "_id":
            response = database.db.Badges.find_one({"_id":ObjectId(data)})
        else:
            response = database.db.Badges.find_one({f"_id": data})

        
        if response:
            return response
        else:
            abort(jsonify({"status":404, f"{by}":f": {data} not found"}))


class AllBadge(Resource):
    """ Get all badges"""
    def get(self):
        pass

api.add_resource(Badge,'/new/','/<string:by>-<string:data>')
api.add_resource(Test,'/test/')

if __name__ == '__main__':
    app.run(load_dotenv=True)