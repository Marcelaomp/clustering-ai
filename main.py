from flask import Flask, jsonify, request
from clustering import clusterize
from clustering_result_repository import update_clustering_result

app = Flask(__name__)


@app.route('/preferences', methods=['POST'])
def post_preference_informations():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    people = []
    for emp in data:
        id = emp.get("id")
        gender = emp.get("gender")
        age = emp.get("age")
        hobby = emp.get("hobby")
        personality = emp.get("personality")
        people.append([id, gender, age, hobby, personality])

    doctors = clusterize(people)

    return jsonify({"doctor_recomendation": doctors}), 200


@app.route('/avaliation', methods=['POST'])
def post_avaliation():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    id = data.get("id")
    good_feedback = data.get("good_feedback")

    update_clustering_result(id, good_feedback)

    return 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
