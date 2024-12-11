from flask import Flask, render_template, request, jsonify
from api.gemini_api import generate_email

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-email", methods=["POST"])
def generate_email_route():
    data = request.json
    recipient = data.get("to")
    message = data.get("message")
    tone = data.get("tone")

    # Call the helper function
    email_content = generate_email(recipient, message, tone)

    return jsonify({"email": email_content})


if __name__ == "__main__":
    app.run(debug=True)


