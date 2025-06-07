from flask import Blueprint, request, jsonify
from controllers.music import (
    get_audio_stream_url,
    get_audio_details,
    search_songs,
    get_related_songs,
)

music_bp = Blueprint('music', __name__)

@music_bp.route('/get-audio', methods=['GET'])
def audio_stream_url():
    return get_audio_stream_url(request)

@music_bp.route('/get-audio-details', methods=['GET'])
def audio_details():
    return get_audio_details(request)

@music_bp.route('/search-songs', methods=['GET'])
def search_songs_route():
    return search_songs(request)

@music_bp.route('/related-songs', methods=['GET'])
def related_songs():
    return get_related_songs(request)

@music_bp.route('/demo', methods=['GET'])
def demo():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400
    info = get_audio_stream_url(request, as_dict=True)
    if not info or not info.get('audioUrl'):
        return jsonify({'error': 'Audio URL not found'}), 404
    return jsonify({'title': info.get('title'), 'audioUrl': info.get('audioUrl')})