import base64
from time import strftime
from flask import request, jsonify, Flask
from flask_pymongo import MongoClient
import bson
from Admin_23_09_19 import client
import struct

app = Flask(__name__)
@app.route('/admin/add_vehicle', methods=['POST', 'GET'])
def New_vehicle_test():
    db = client.db
    coll = db.vehicles
    vehicle_name = request.json['vehicle_name']
    model = request.json['model']
    vehicle_number = request.json['vehicle_number']
    updated_time = strftime("%Y/%m/%d %H:%M:%S %I%p")
    output = []
    v_id = []
    try:
        if len(vehicle_number) == 0:
            return jsonify({'status': "fail", 'message': 'vehicle number is not none', 'output': output})
        else:
            for i in coll.find():
                v_id = i['vehicle_number']
            if vehicle_number != v_id:
                coll.insert(
                        {'vehicle_name': vehicle_name, 'model': model, 'updated_time': updated_time,
                        'vehicle_number': vehicle_number})
                output.append(
                        {'vehicle_name': vehicle_name, 'model': model,
                        'updated_time': updated_time, 'vehicle_number': vehicle_number})
                return jsonify({'status': 'success', 'message': 'insert vehicle success', 'result': output})
            else:
                return jsonify({'status': 'fail', "message": "vehicle is already added", "result": output})
    except Exception as e:
        return jsonify(status="Fail", message=str(e))


if __name__ == '__main__':
    app.run(debug=True)
