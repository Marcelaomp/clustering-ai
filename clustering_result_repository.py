from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['ai_caracteristic_matcher']
collection = db['clustering_result']


def save_clustering_result(clustering_result):
    clustering_result = {"recomendation": clustering_result}
    clustering_result = collection.insert_one(clustering_result)
    return str(clustering_result.inserted_id)


def get_all_clustering_result_feedback():
    return [doc['good_feedback'] for doc in collection.find({'good_feedback': {'$exists': True}})]


def update_clustering_result(id, good_feedback):
    filtro = {'_id': ObjectId(id)}
    clustering_result = collection.find_one(filtro)
    if clustering_result:
        clustering_result['good_feedback'] = good_feedback
        collection.update_one(filtro, {'$set': clustering_result})
