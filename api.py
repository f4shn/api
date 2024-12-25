from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/forward-webhook", methods=["POST"])
def forward_webhook():
    try:
        api_key = request.headers.get("x-api-key")
        if api_key != SECRET_API_KEY:
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "Invalid request payload"}), 400
        
        response = requests.post(WEBHOOK_URL, json=data)

        if response.status_code == 204:
            return jsonify({"success": True, "message": "Message forwarded successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to forward message"}), 500

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "Server error"}), 500


if __name__ == "__main__":
    app.run(port=3000, debug=True)
