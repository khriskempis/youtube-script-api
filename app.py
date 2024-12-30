from flask import Flask
from routes.transcribe import transcribe_bp
from config import Config, logger
import asyncio

def create_app():
    app = Flask(__name__)
    app.register_blueprint(transcribe_bp)
    return app

if __name__ == '__main__':
    logger.info("Starting server...")
    logger.info(f"Proxy configured: {'Yes' if Config.PROXY else 'No'}")
    logger.info(f"OpenAI API key configured: {'Yes' if Config.OPENAI_API_KEY else 'No'}")
    
    app = create_app()
    app.run(host='0.0.0.0', port=Config.PORT)