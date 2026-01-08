import httpx
from Prebuilt import gunc
# Task 1: Sentiment Analysis API Call
def analyze_sentiment():
    return gunc('q-llm-sentiment-analysis')

# Task 2: Generate Random US Addresses
def generate_addresses():
    return gunc('q-generate-addresses-with-llms')
import os
import tiktoken

def llm_token(file_name: str, model: str = "gpt-4o-mini") -> int:
    """
    Reads a file, sets its path to the 'tmp' directory, and returns the token count.
    
    Args:
        file_name (str): The name of the file to process.
        model (str): The LLM model to use for tokenization (default is "gpt-4o-mini").
    
    Returns:
        int: The number of tokens in the file content.
    """
    # Define the file path inside the 'tmp' directory
    file_path = os.path.join(os.getcwd(), "tmp", file_name)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_name}' not found in 'tmp' directory.")
    
    # Read the file content
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Get the tokenizer for the specified model
    enc = tiktoken.encoding_for_model(model)
    
    # Tokenize the content and return the token count
    return len(enc.encode(content))

# Example usage:
# token_count = llm_token("example.txt")
# print(f"Number of tokens: {token_count}")
import base64
def extract_text_from_image(image_file):
    image_path=os.path.join(os.getcwd(),'tmp',image_file)
    """
    Converts an image to Base64, sends it to OpenAI's API, and extracts text.
    
    Parameters:
    image_path (str): Path to the image file.
    api_key (str): OpenAI API key.
    
    Returns:
    dict: API response containing the extracted text.
    """
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    
    request_body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract text from this image."},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                ]
            }
        ]
    }
    


    return request_body
# Task 3: Extract Text from Invoice Image
def extract_invoice_text(image_base64):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": "Bearer {AIPROXY_TOKEN}"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": "Extract text from this image."},
                {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
            ]}
        ]
    }
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Task 4: Generate Text Embeddings
def generate_text_embeddings():
  return gunc('q-llm-embeddings')
def most_similar_embedding():
    return gunc('q-embedding-similarity')




def LLM_say_yes():
    return gunc('q-get-llm-to-say-yes')