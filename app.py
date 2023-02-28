# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name =fields.Str()

movies_schema = MovieSchema()
director_schema = DirectorSchema()
api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('director')
genre_ns = api.namespace('genre')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        mov_query = Movie.query
        if director_id:
            mov_query = mov_query.filter(director_id == Movie.director_id)
        if genre_id:
            mov_query = mov_query.filter(genre_id == Movie.genre_id)
        movies = mov_query.all()
        return movies_schema.dump(movies, many=True), 200


@movie_ns.route('/<int:uid>')
class MoviesView(Resource):
    def get(self, uid: int):
        movie = Movie.query.get(uid)
        if not movie:
            return 'NOT FOUND', 404
        return movies_schema.dump(movie), 200


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return director_schema.dump(directors, many=True), 200


@director_ns.route('/<int:dirid>')
class DirectorView(Resource):
    def get(self, dirid: int):
        director = Director.query.get(dirid)
        if not director:
            return 'NOT FOUND', 404
        return director_schema.dump(director), 200

@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return director_schema.dump(genres, many=True), 200


@genre_ns.route('/<int:genid>')
class GenreView(Resource):
    def get(self, genid: int):
        genre = Genre.query.get(genid)
        if not genre:
            return 'NOT FOUND', 404
        return director_schema.dump(genre), 200




app.run()
