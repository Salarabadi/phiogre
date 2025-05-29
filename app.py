from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# تنظیمات اتصال به دیتابیس PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql://phiogre_user:uEPqnScApuIGPM7LqIxaaBS4M0OJPr6d"
    "@dpg-d0sbsg7fte5s73dmlo30-a/phiogre_db"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# مدل ساده برای بررسی اتصال
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(64), nullable=False)

# روت‌ها
@app.route("/")
def index():
    return "✅ Server running and connected to PostgreSQL"

@app.route("/api/upload", methods=["POST"])
def upload_file():
    data = request.get_json()
    new_file = File(name=data.get("name"), status="Pending")
    db.session.add(new_file)
    db.session.commit()
    return jsonify({"message": "File uploaded successfully"}), 200

@app.route("/api/files", methods=["GET"])
def list_files():
    files = File.query.all()
    return jsonify([
        {"name": f.name, "status": f.status} for f in files
    ])

@app.route("/api/investor/download/<filename>", methods=["GET"])
def download_file(filename):
    return jsonify({"message": f"Download {filename} initiated"}), 200

@app.route("/api/investor/meeting", methods=["POST"])
def schedule_meeting():
    data = request.get_json()
    return jsonify({"message": "Meeting request submitted", "data": data}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
