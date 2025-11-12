from flask import Flask, request, Response
import json

app = Flask(__name__)

# Load config
with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        msg = request.form.get("Body", "").strip().lower()
        number = request.form.get("From")

        print("✅ Received:", msg, "From:", number)

        reply = cfg["responses"].get(msg, cfg["welcome_message"])

        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""

        return Response(twiml, mimetype="application/xml")

    except Exception as e:
        print("❌ ERROR:", e)
        return "error", 200

@app.route("/")
def home():
    return "✅ Sophia Cars Bot Running"

if __name__ == "__main__":
    app.run(port=5000)
