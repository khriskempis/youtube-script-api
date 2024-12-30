from openai import AsyncOpenAI, OpenAIError
import tiktoken
from config import Config, logger

client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)

def chunk_text(text, max_tokens=16000):
    """
    Splits the text into chunks of approximately max_tokens tokens each.
    """
    tokenizer = tiktoken.encoding_for_model("gpt-4o-mini")
    words = text.split()
    chunks = []
    current_chunk = []
    current_token_count = 0

    for word in words:
        word_token_count = len(tokenizer.encode(word + " "))

        if current_token_count + word_token_count > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_token_count = 0

        current_chunk.append(word)
        current_token_count += word_token_count

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

async def process_chunk(chunk):
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """You are a helpful assistant that improves text formatting and adds punctuation. 
                 You will be given texts from YouTube transcriptions and your task is to apply good formatting.
                 Do NOT modify individual words."""},
                {"role": "user", "content": chunk}
            ]
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        return f"OpenAI API error: {str(e)}"

async def improve_text_with_gpt4(text):
    if not Config.OPENAI_API_KEY:
        return "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."

    chunks = chunk_text(text)
    tasks = [process_chunk(chunk) for chunk in chunks]
    improved_chunks = await asyncio.gather(*tasks)
    return ' '.join(improved_chunks)