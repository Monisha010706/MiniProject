from flask import Flask, render_template, request, redirect, url_for, session, send_file
from gtts import gTTS
import pandas as pd
import qrcode
import io
import urllib.parse
import json
import os
import uuid   
app = Flask(__name__)
app.secret_key = "a57c2be079bd14aacfcf483d173e0ca9"

# Load dataset
df = pd.read_csv("extended_hunger_dataset.csv")

# Persistent storage for used QR codes
USED_CODES_FILE = "used_codes.json"

if os.path.exists(USED_CODES_FILE):
    with open(USED_CODES_FILE, "r") as f:
        used_qr_codes = set(json.load(f))
else:
    used_qr_codes = set()

def save_used_codes():
    """Save used QR codes to file."""
    with open(USED_CODES_FILE, "w") as f:
        json.dump(list(used_qr_codes), f)

# Function to determine marker color
def get_color(score):
    if score >= 0.7:
        return "red"
    elif score >= 0.5:
        return "orange"
    else:
        return "green"

# Login page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if (username == "admin" and password == "admin123") or (username == "user" and password == "user123"):
            session["user"] = username
            return redirect(url_for("map_page"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

# Map page
@app.route("/map")
def map_page():
    markers = []
    for _, row in df.iterrows():
        markers.append({
            "region": row["Region"],
            "month": row["Month"],
            "lat": row["Latitude"],
            "lng": row["Longitude"],
            "color": get_color(row["Hunger_Score"])
        })
    return render_template("map.html", markers=markers)

# QR code generation
@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.json
    region = data.get("region", "Unknown")
    month = data.get("month", "Unknown")
    tokens = 10

    qr_text = f"Region: {region}, Month: {month}, Tokens: {tokens}"
    verification_url = request.url_root.rstrip("/") + "/verify_qr?code=" + urllib.parse.quote(qr_text)

    img = qrcode.make(verification_url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

# Pie chart statistics (fixed to match map thresholds)
@app.route("/piechart")
def piechart():
    red = (df["Hunger_Score"] >= 0.7).sum()
    orange = ((df["Hunger_Score"] >= 0.5) & (df["Hunger_Score"] < 0.7)).sum()
    green = (df["Hunger_Score"] < 0.5).sum()
    return render_template("piechart.html", red=red, orange=orange, green=green)

# QR verification page
@app.route("/verify")
def verify_page():
    return render_template("verify.html")

# QR verification logic with persistent storage + speech
@app.route("/verify_qr", methods=["GET", "POST"])
def verify_qr():
    if request.method == "POST":
        qr_text = request.form.get("qr_text", "").strip()
        language = request.form.get("language", "en")
    else:
        qr_text = request.args.get("code", "").strip()
        language = request.args.get("language", "en")

    if not qr_text:
        message = "❌ No QR code data provided."
        return render_template("verify.html", message=message)

    if qr_text in used_qr_codes:
        message = "❌ This QR code has already been used."
    else:
        used_qr_codes.add(qr_text)
        save_used_codes()
        message = f"✅ QR code verified successfully. Details: {qr_text}"

    # ✅ Generate clean speech (no emojis or links)
    speech_text = f"QR code verification result. {message.replace('✅', '').replace('❌', '')}"

    # Ensure audio folder exists
    audio_dir = os.path.join("static", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    # Save unique audio file
    audio_path = os.path.join(audio_dir, f"{uuid.uuid4()}.mp3")
    tts = gTTS(speech_text, lang=language)
    tts.save(audio_path)

    return render_template(
        "verify.html",
        message=message,
        audio_file="/" + audio_path
    )

if __name__ == "__main__":
    app.run(debug=True)
