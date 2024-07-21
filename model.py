import time
from openai import OpenAI
import google.generativeai as genai

SECRET_FILE = 'secrets.txt'
with open('secrets.txt') as f:
    lines = f.readlines()
    for line in lines:
        if line.split(',')[0].strip() == "openai_key":
            openai_key = line.split(',')[1].strip()
        elif line.split(',')[0].strip() == "gemini_key":
            gemini_key = line.split(',')[1].strip()

openai_client = OpenAI(api_key=openai_key)


def call_gpt4(message):
    """Call the GPT-4o model for text information and return the response."""
    response = openai_client.chat.completions.create(
        model = "gpt-4o", 
        messages=[{"role": "user", 
                   "content": message}],
        temperature=0.0,
        max_tokens=1000
    )
    return response.choices[0].message.content


def call_gpt35(message):
    """Call the ChatGPT model for text information and return the response."""
    response = openai_client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        temperature=0.0,
        max_tokens=1000
    )
    return response.choices[0].message.content


def call_gemini(message):
    """Call the Gemini model for text information and return the response."""
    retries = 20
    while retries > 0:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(message)
            return response.text
        except Exception as e:
            retries -= 1
            time.sleep(0.1)


def call_model(model, message):
    """Call the model based on the model name."""
    if model == 'gpt4':
        result = call_gpt4(message)
    elif model == 'gpt3.5':
        result = call_gpt35(message)
    elif model == 'gemini':
        result = call_gemini(message)
    return result


if __name__ == "__main__":
    message = "how are you?"
    call_model('gpt4', message)