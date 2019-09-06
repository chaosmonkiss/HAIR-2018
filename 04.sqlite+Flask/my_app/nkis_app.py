from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///newDB')
app = Flask(__name__)
api = Api(app)

class ReportID(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute('select reportid from nkisdata2;')
        return {'reportid':[i for i in query.cursor.fetchall()]}
"""
class Category (Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute('select * from class')
        result = {'category': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class PubYear (Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select pubyear from content;")
        result = {'title': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Title (Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select title from content")
        return {'reportid':[i[0] for i in query.cursor.fetchall()]} """

api.add_resource(ReportID, '/reportid') # Route_1

"""
api.add_resource(Category, '/category') # Route_2
api.add_resource(PubYear, '/publishyear') # Route_3
api.add_resource(Title, '/publish/<employee_id>') # Route_4 """

if __name__ == '__main__':
     app.run()
