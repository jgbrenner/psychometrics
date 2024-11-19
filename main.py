# scripts/main.py

import os
import sys
import openai
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv
from groq import Groq
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri, numpy2ri
import rpy2.robjects.packages as rpackages

# Activate the automatic conversion of pandas and numpy objects to R
pandas2ri.activate()
numpy2ri.activate()

def load_api_keys():
    """Load API keys from the .env file."""
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')
    groq_api_key = os.getenv('GROQ_API_KEY')
    
    if not openai_api_key or not groq_api_key:
        print("Error: API keys not found. Please check your .env file.")
        sys.exit(1)
    
    return openai_api_key, groq_api_key

def generate_test_items(client):
    """Generate test items using Groq API."""
    messages = [
        {"role": "system", "content": "You are an expert psychometrician creating test items."},
        {"role": "user", "content": "Generate two items for the construct of Rigid Perfectionism: one regular-keyed and one reverse-keyed. Make them concise and clear."}
    ]
    
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
        print("Generated Test Items:\n", response_text)
        
        # TODO: Parse response_text to extract items if necessary
        # For now, we'll use example items
        items = [
            {
                "item": "I often feel anxious when I make a mistake, even if it's a minor one, and I worry that it will affect my overall performance.",
                "type": "regular-keyed"
            },
            {
                "item": "I am comfortable with the idea that I may not be perfect all the time, and I don't get too upset when I make a mistake or things don't go exactly as planned.",
                "type": "reverse-keyed"
            }
        ]
        
        return pd.DataFrame(items)
    
    except Exception as e:
        print(f"Error generating test items: {e}")
        sys.exit(1)

def save_items_to_csv(items_df, filepath='data/rigid_perfectionism_items.csv'):
    """Save the generated items to a CSV file."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        items_df.to_csv(filepath, index=False)
        print(f"Items saved to {filepath}")
    except Exception as e:
        print(f"Error saving items to CSV: {e}")
        sys.exit(1)

def obtain_embeddings(items_df, openai_api_key, embedding_endpoint="https://api.openai.com/v1/embeddings", embedding_model="text-embedding-3-small"):
    """Obtain embeddings for each item using OpenAI's API."""
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    
    embeddings = []
    for item in items_df["item"]:
        try:
            response = requests.post(
                embedding_endpoint,
                headers=headers,
                json={"model": embedding_model, "input": item}
            )
            response.raise_for_status()
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                embeddings.append(data["data"][0]["embedding"])
            else:
                print(f"Warning: No embedding found for item: {item}")
                embeddings.append(None)
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining embedding for item '{item}': {e}")
            embeddings.append(None)
    
    # Remove any None embeddings
    embeddings = [emb for emb in embeddings if emb is not None]
    embeddings_array = np.array(embeddings)
    return embeddings_array

def perform_ega(embeddings_array):
    """Perform Exploratory Graph Analysis (EGA) using R's EGAnet package."""
    # Transfer embeddings to R
    robjects.globalenv['embeddings_array'] = embeddings_array
    
    # Load EGAnet library in R
    try:
        EGAnet = rpackages.importr('EGAnet')
    except Exception as e:
        print(f"Error importing EGAnet in R: {e}")
        sys.exit(1)
    
    # Perform EGA
    try:
        robjects.r('''
            library(EGAnet)
            ega_result <- EGA(as.matrix(embeddings_array))
            print(ega_result)
        ''')
    except Exception as e:
        print(f"Error performing EGA in R: {e}")
        sys.exit(1)

def main():
    """Main function to orchestrate the workflow."""
    openai_api_key, groq_api_key = load_api_keys()
    
    # Initialize Groq client
    client = Groq(api_key=groq_api_key)
    
    # Generate test items
    items_df = generate_test_items(client)
    
    # Save items to CSV
    save_items_to_csv(items_df)
    
    # Obtain embeddings
    embeddings_array = obtain_embeddings(items_df, openai_api_key)
    
    # Perform EGA
    perform_ega(embeddings_array)

if __name__ == "__main__":
    main()
