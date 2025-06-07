from flask import Flask, jsonify
from flask_cors import CORS

# Import your music blueprint (router equivalent)
from routes.music import music_bp

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/')
def home():
    return "Welcome to the Music API"

# Register the music blueprint at /api/music
app.register_blueprint(music_bp, url_prefix='/api/music')

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)