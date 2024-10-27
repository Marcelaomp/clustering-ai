from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['ai_caracteristic_matcher']
collection = db['calibration']


def save_calibration_parameter(eps):
    calibration = {
        'eps': eps,
        'min_samples': 1,
        'data_insercao': datetime.now()
    }
    collection.insert_one(calibration)


def get_calibration_parameter():
    return collection.find_one(sort=[('data_insercao', -1)])
