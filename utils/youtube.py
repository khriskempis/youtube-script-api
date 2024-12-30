import re
from youtube_transcript_api import YouTubeTranscriptApi
from config import logger, Config

def get_youtube_id(url):
    video_id = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return video_id.group(1) if video_id else None

def process_transcript(video_id):
    """
    Fetch YouTube transcript with optional proxy support.
    """
    try:
        logger.info("Attempting to fetch transcript without proxy...")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        logger.info("Successfully fetched transcript without proxy")
        
    except Exception as e:
        logger.warning(f"Failed to fetch without proxy: {str(e)}")
        
        if Config.PROXY:
            logger.info(f"Attempting to fetch transcript with proxy...")
            try:
                transcript = YouTubeTranscriptApi.get_transcript(
                    video_id,
                    proxies={"http": Config.PROXY, "https": Config.PROXY}
                )
                logger.info("Successfully fetched transcript with proxy")
            except Exception as proxy_error:
                logger.error(f"Proxy attempt failed: {str(proxy_error)}")
                raise proxy_error
        else:
            logger.error("No proxy configured and direct access failed")
            raise e

    return ' '.join([entry['text'] for entry in transcript])