from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

parking_lot = {}
rate_per_hour = 20


@app.route("/park", methods=["POST"])
def park_vehicle():
    data = request.json
    vehicle_number = data["vehicle_number"]

    if vehicle_number in parking_lot:
        return jsonify({"message": "Vehicle already parked"})

    entry_time = datetime.now()
    parking_lot[vehicle_number] = entry_time

    return jsonify({
        "message": "Vehicle parked",
        "vehicle": vehicle_number,
        "entry_time": str(entry_time)
    })


@app.route("/exit", methods=["POST"])
def exit_vehicle():
    data = request.json
    vehicle_number = data["vehicle_number"]

    if vehicle_number not in parking_lot:
        return jsonify({"message": "Vehicle not found"})

    entry_time = parking_lot.pop(vehicle_number)
    exit_time = datetime.now()

    duration = (exit_time - entry_time).seconds / 3600
    fee = duration * rate_per_hour

    return jsonify({
        "vehicle": vehicle_number,
        "parking_fee": round(fee, 2)
    })


@app.route("/vehicles")
def vehicles():
    return jsonify(list(parking_lot.keys()))


if __name__ == "__main__":
    app.run(debug=True)
