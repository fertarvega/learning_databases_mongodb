from flask import jsonify, request
from flask_restful import Resource, abort
from flask_pymongo import pymongo
from bson.json_util import ObjectId
import db_config as database

class Badge(Resource):
    ''' Handeling the data from one badge at one time'''

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
                'header_img_url': response['header_img_url'],
                'profile_picture_url': response['profile_picture_url'],
                'name': response['name'],
                'age': response['age'],
                'city': response['city'],
                'followers': response['followers'],
                'likes': response['likes'],
                'posts': response['posts'],
                'post':response['post']
            }})

        response['_id'] = str(response['_id'])
        return jsonify(response)

    def delete(self, by, data):
        response = self.abort_if_not_exist(by, data)
        database.db.Badges.delete_one({'_id':response['_id']})
        response['_id'] = str(response['_id'])
        return jsonify({"deleted":response})

    def abort_if_not_exist(self, by, data):
        if by == "_id":
            response = database.db.Badges.find_one({"_id":ObjectId(data)})
        else:
            response = database.db.Badges.find_one({f"_id": data})

        
        if response:
            return response
        else:
            abort(jsonify({"status":404, f"{by}":f": {data} not found"}))




if __name__ == '__main__':
    app.run(load_dotenv=True)