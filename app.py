from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# اتصال به دیتابیس
def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "phiogre_db"),
        user=os.environ.get("DB_USER", "phiogre_user"),
        password=os.environ.get("DB_PASSWORD", "your-password"),
        port=os.environ.get("DB_PORT", "5432")
    )

@app.route("/")
def home():
    return "✅ Server is running successfully!"

@app.route("/api/upload", methods=["POST"])
def upload_file():
    return jsonify({"message": "File uploaded successfully"}), 200

@app.route("/api/files", methods=["GET"])
def list_files():
    return jsonify([
        {"name": "Sample_Report.pdf", "status": "Pending"},
        {"name": "Energy_Analysis.xlsx", "status": "Approved"}
    ])

@app.route("/api/db-version", methods=["GET"])
def db_version():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({"db_version": version}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/investor/download/<filename>", methods=["GET"])
def download_file(filename):
    return jsonify({"message": f"Download {filename} initiated"}), 200

@app.route("/api/investor/meeting", methods=["POST"])
def schedule_meeting():
    data = request.get_json()
    return jsonify({"message": "Meeting request submitted", "data": data}), 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
