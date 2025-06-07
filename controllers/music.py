from flask import jsonify
import yt_dlp

def get_audio_stream_url(request, as_dict=False):
    url = request.args.get('url')
    if not url:
        result = {'error': 'Invalid or missing URL'}
        return result if as_dict else (jsonify(result), 400)

    # Minimal yt-dlp options for the fastest possible extraction of audio URL
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'noplaylist': True,
        'skip_download': True,
        'extract_flat': False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Try to get the direct audio URL from info
            audio_url = info.get('url')
            if not audio_url:
                # Fallback: find best audio-only format with a URL
                formats = info.get('formats', [])
                audio_formats = [
                    f for f in formats
                    if f.get('acodec') != 'none'
                    and f.get('vcodec') == 'none'
                    and f.get('url')
                ]
                if not audio_formats:
                    raise Exception('No valid audio streams found')
                # Use the highest bitrate available
                best_audio = max(audio_formats, key=lambda f: f.get('abr') or 0)
                audio_url = best_audio.get('url')

            data = {
                'audioUrl': audio_url
            }
            return data if as_dict else jsonify(data)
    except Exception as e:
        result = {
            'error': 'Failed to fetch audio URL',
            'details': str(e)
        }
        return result if as_dict else (jsonify(result), 500)



def get_audio_details(request):
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            data = {
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration'),
                'uploader': info.get('uploader'),
                'url': info.get('webpage_url'),
            }
            return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get audio details', 'details': str(e)}), 500

def search_songs(request):
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Missing search query'}), 400
    try:
        ydl_opts = {
            'quiet': True,
            'default_search': 'ytsearch10',
            'skip_download': True,
            'extract_flat': False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            results = []
            for entry in info.get('entries', []):
                results.append({
                    'title': entry.get('title'),
                    'thumbnail': entry.get('thumbnail'),
                    'uploader': entry.get('uploader'),
                    'duration': entry.get('duration'),
                    'url': entry.get('webpage_url'),
                })
            return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': 'Failed to search songs', 'details': str(e)}), 500

def get_related_songs(request):
    video_id = request.args.get('videoId')
    if not video_id:
        return jsonify({'error': 'Missing videoId'}), 400
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            related = []
            for r in info.get('related_videos', [])[:10]:
                related.append({
                    'title': r.get('title'),
                    'url': f"https://www.youtube.com/watch?v={r.get('id')}",
                    'thumbnail': None,
                    'duration': r.get('duration'),
                    'uploader': r.get('uploader'),
                })
            return jsonify({'related': related})
    except Exception as e:
        return jsonify({'error': 'Failed to fetch related videos', 'details': str(e)}), 500