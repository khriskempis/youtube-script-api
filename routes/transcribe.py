from flask import Blueprint, request, jsonify
import asyncio
from utils.youtube import get_youtube_id, process_transcript
from utils.openai_helper import improve_text_with_gpt4
from auth import require_custom_authentication
from config import logger

transcribe_bp = Blueprint('transcribe', __name__)

@transcribe_bp.route('/transcribe', methods=['POST'])
@require_custom_authentication
def transcribe():
    youtube_url = request.json.get('url')
    if not youtube_url:
        return jsonify({"error": "No YouTube URL provided"}), 400

    video_id = get_youtube_id(youtube_url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        logger.info(f"Processing video ID: {video_id}")
        transcript_text = process_transcript(video_id)
        logger.info("Transcript fetched successfully")
        improved_text = asyncio.run(improve_text_with_gpt4(transcript_text))
        return jsonify({"result": improved_text})
    
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

        