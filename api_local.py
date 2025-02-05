from flask import Flask, request, jsonify
import logging
import json
from flask_cors import CORS  # Enable CORS for frontend requests

app = Flask(__name__)
CORS(app)

BOOKINGS_FILE = "bookings.json"

# Load bookings from file
def load_bookings():
    try:
        with open(BOOKINGS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return [{"id": i, "name": f"Desk {i}", "bookings": {}} for i in range(1, 8)]

# Save bookings to file
def save_bookings(bookings):
    with open(BOOKINGS_FILE, "w") as f:
        json.dump(bookings, f, indent=2)

@app.route("/desks", methods=["GET"])
def get_desks():
    return jsonify(load_bookings())

@app.route("/desks/book", methods=["POST"])
def book_desk():
    try:
        body = request.get_json()
        desk_id = body.get("id")
        employee_name = body.get("employee_name")
        date = body.get("date")

        if not desk_id or not employee_name or not date:
            return jsonify({"message": "Missing parameters"}), 400

        bookings = load_bookings()
        desk = next((d for d in bookings if d["id"] == desk_id), None)

        if desk:
            # Check if already booked for the date
            if date in desk["bookings"] and not desk["bookings"][date]["isAvailable"]:
                return jsonify({"message": "Desk is already booked for this date"}), 400

            # Book the desk
            desk["bookings"][date] = {"isAvailable": False, "employee_name": employee_name}
            save_bookings(bookings)
            return jsonify({"message": "Desk booked successfully"}), 200

        return jsonify({"message": "Desk not found"}), 404
    except Exception as e:
        logging.error(str(e))
        return jsonify({"message": "Invalid request"}), 400

@app.route("/desks/<int:desk_id>", methods=["DELETE"])
def cancel_booking(desk_id):
    try:
        body = request.get_json()
        date = body.get("date")

        if not date:
            return jsonify({"message": "Date is required to cancel a booking"}), 400

        bookings = load_bookings()
        desk = next((d for d in bookings if d["id"] == desk_id), None)

        if desk and date in desk["bookings"]:
            # Remove booking for the date
            del desk["bookings"][date]
            save_bookings(bookings)
            return jsonify({"message": "Booking cancelled successfully"}), 200

        return jsonify({"message": "Booking not found"}), 404
    except Exception as e:
        logging.error(str(e))
        return jsonify({"message": "Invalid request"}), 400

if __name__ == "__main__":
    app.run(debug=True)
