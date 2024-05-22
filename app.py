from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['movies_db']
movies_collection = db['movies']

@app.route('/')
def home():
    return "Welcome to the Movies API!"

@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    movie_id = movies_collection.insert_one(data).inserted_id
    return jsonify(str(movie_id)), 201

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = list(movies_collection.find())
    for movie in movies:
        movie['_id'] = str(movie['_id'])
    return jsonify(movies), 200

@app.route('/movies/<id>', methods=['GET'])
def get_movie(id):
    movie = movies_collection.find_one({'_id': ObjectId(id)})
    if movie:
        movie['_id'] = str(movie['_id'])
        return jsonify(movie), 200
    return jsonify({'error': 'Movie not found'}), 404

@app.route('/movies/<id>', methods=['PATCH'])
def update_movie(id):
    data = request.get_json()
    result = movies_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Movie updated'}), 200
    return jsonify({'error': 'Movie not found'}), 404

@app.route('/movies/<id>', methods=['DELETE'])
def delete_movie(id):
    result = movies_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Movie deleted'}), 200
    return jsonify({'error': 'Movie not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
