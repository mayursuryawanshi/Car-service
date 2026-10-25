import os
import sqlite3

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# keep the database file next to app.py, so it does not matter
# which folder we run the program from
DB = os.path.join(os.path.dirname(__file__), "carcare.db")


# make the database and the bookings table if they are not there yet
def create_table():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            car_model TEXT,
            service TEXT,
            date TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()


create_table()


# get all the bookings
@app.route("/api/bookings")
def get_bookings():
    conn = sqlite3.connect(DB)
    rows = conn.execute("SELECT * FROM bookings ORDER BY id").fetchall()
    conn.close()

    bookings = []
    for row in rows:
        bookings.append({
            "id": row[0],
            "name": row[1],
            "phone": row[2],
            "car_model": row[3],
            "service": row[4],
            "date": row[5],
            "time": row[6]
        })

    return jsonify(bookings)


# save a new booking
@app.route("/api/bookings", methods=["POST"])
def add_booking():
    data = request.get_json()

    name = data.get("name", "")
    phone = data.get("phone", "")
    car_model = data.get("car_model", "")
    service = data.get("service", "")
    date = data.get("date", "")
    time = data.get("time", "")

    if not name or not phone or not car_model or not service or not date or not time:
        return jsonify({"message": "Please fill all fields."}), 400

    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO bookings (name, phone, car_model, service, date, time) VALUES (?, ?, ?, ?, ?, ?)",
        (name, phone, car_model, service, date, time)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Booking saved successfully!"})


# delete one booking by id
@app.route("/api/bookings/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Booking deleted."})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
