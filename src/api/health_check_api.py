from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Bot is running"})


def run_flask():
    """
    Run Flask application in a separate thread
    """
    app.run(host='0.0.0.0', port=8000)