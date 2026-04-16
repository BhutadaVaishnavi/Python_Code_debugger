import requests
import os
from dotenv import load_dotenv

# LOAD API KEY

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("Hugging Face token not found. Check your .env file.")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# DEBUG FUNCTION

def debug_code(code, error):
    prompt = f"""
You are a Python expert debugger.

Code:
{code}

Error:
{error}

Tasks:
1. Explain the error in simple words
2. Identify the issue
3. Provide corrected code
"""

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    except Exception as e:
        return f"Request Failed: {str(e)}"

    # Check status code
    if response.status_code != 200:
        return f"API Error {response.status_code}:\n{response.text}"

    # Safe JSON parsing
    try:
        result = response.json()
    except:
        return f"Invalid response (not JSON):\n{response.text}"

    # Handle Hugging Face errors
    if isinstance(result, dict):
        if "error" in result:
            return f"{result['error']}"
        if "estimated_time" in result:
            return "Model is loading... please try again in a few seconds."

    # Extract output
    try:
        return result[0]["generated_text"]
    except:
        return f"Unexpected response:\n{result}"


# MAIN PROGRAM

if __name__ == "__main__":
    print("\n AI Debug Assistant \n")

    try:
        code = input("Paste your Python code:\n")
        error = input("\nPaste your error message:\n")

        print("\nAnalyzing...\n")

        output = debug_code(code, error)

        print("\nAI Response:\n")
        print(output)

    except Exception as e:
        print("Program Error:", str(e))