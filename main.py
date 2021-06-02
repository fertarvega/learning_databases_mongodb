from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_restful import Api
from flask_pymongo import pymongo
import db_config as database

#resources
from res.badge import Badge
from res.badges import Badges

app=Flask(__name__)
api=Api(app)


@app.route('/all/kids')
def get_kids():
    response = list(database.db.Badges.find({'age': {"$gte": 7}}))

    for document in response:
        document["_id"] = str(document['_id'])

    return jsonify(response)

@app.route('/all/badges_name')
def get_all_badges():
    response = list(database.db.Badges.find_many({{'name':1}}))

    for document in response:
        document["_id"] = str(document['_id'])

    return jsonify(response)


api.add_resource(Badge,'/new/','/<string:by>-<string:data>/')
api.add_resource(Badges, '/all/', '/delete/all/')


if __name__ == '__main__':
    app.run(load_dotenv=True)