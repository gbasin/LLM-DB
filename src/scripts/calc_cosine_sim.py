import sys
import openai
import os
from tenacity import retry, stop_after_attempt, wait_random_exponential
from openai.datalib.numpy_helper import numpy as np
from typing import List, Optional
from dotenv import load_dotenv

#@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text: str, engine="text-similarity-davinci-001", **kwargs) -> List[float]:

    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")

    return openai.Embedding.create(input=[text], engine=engine, **kwargs)["data"][0]["embedding"]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    
    # process command
    try:
        # Get the first command-line argument
        arg = sys.argv[1]

        # Split the argument into a list of strings
        str_list = arg.split('|')
        
        embeddings = [get_embedding(str, engine='text-embedding-ada-002') for str in str_list]
        
        # calc embeddings
        for i, embedding in enumerate(embeddings):
            print(cosine_similarity(embeddings[0], embedding))
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    # cache.flush()
    

if __name__ == "__main__":
    main()