#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

class Research(Resource):
    def get(self):
        researches = [research.to_dict() for research in Research.query.all()]
        return make_response(researches, 200)
    
api.add_resource(Research, '/research')

class ResearchById(Resource):
    def get(self, id):
        research = Research.query.filter(Research.id == id).first()
        if research is None:
            raise ValueError({'error': 'Research paper not found'}, 400)
        return make_response(research.to_dict(), 200)
        
    def delete(self, id):
        research = Research.query.filter(Research.id == id).first()
        if research is None:
            raise ValueError({'error': 'Research paper not found'}, 400)
        db.session.delete(research)
        db.session.commit()
        return make_response({}, 204)

api.add_resource(ResearchById, '/research/<int:id>')

class Authors(Resource):
    def get(self):
        authors = [author.to_dict() for author in Author.query.all()]
        return make_response(authors, 200)
    
    def post(self):
        data = request.get_json()
        new_author = Author(name = data['name'], field_of_study = data['name'], author_id = data['author_id'])
        db.session.add(new_author)
        db.session.commit()
        return make_response(new_author.authors.to_dict(), 201)

api.add_resource(Authors, '/authors')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
