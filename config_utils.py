import os
from openai import OpenAI
from typing import Dict, Optional


CHECK_PROMPTS = {
    "Task": "Please identify if the following paper is related to the topic of large language models (LLMs) or involves the use of LLMs based on the following provided information.\n",
    "Input": "Paper Title: {title}\nAbstract (if available): {abstract}\nKeywords (if available): {keywords}\nTopics (if available): {topics}\n",
    "Instruction": "Guidance: If the abstract is unavailable, please use the title and topics to make your determination. Please note that a paper mentioning concepts like 'neural network', 'machine learning', 'artificial intelligence', or any NLP tasks always suggests a connection to LLMs. For example, a paper titled 'The improved neural network model in humor detection' is very likely to involve LLMs. Respond 'Yes' for such papers.",
    "Output": "Please only respond with either 'Yes' or 'No'. Please do not return other output.\n"
}

DISCIPLINE_PROMPTS = {
    "Task": "Please extract the discipline-related information from the following author's affiliation: {affiliation}\n",
    "Instruction": "For example, for 'Department of Biological Science, Joseph Ayo Babalola University, Nigeria', return 'Biological Science'. If it is not written in English, translate it to English and return. If you cannot identify any discipline-related information, return 'None'. Please do not return other output or explanation. \n"
}

MAX_ABSTRACT_WORDS = 300

MODEL_NAME = "gpt-4o-mini"
MAX_TOKENS = 6000
TEMPERATURE = 0.0

class APIClient:
    """A client for handling OpenAI API interactions."""
    
    def __init__(self, secrets_file: str = 'secrets.txt'):
        """
        Initialize the API client.
        Args:
            secrets_file (str): Path to the secrets file containing API keys.
        Raises:
            FileNotFoundError: If the secrets file is not found.
            ValueError: If the OpenAI key is not found in the secrets file.
        """
        self.api_key = self._load_api_key(secrets_file)
        self.client = OpenAI(api_key=self.api_key)
    

    def _load_api_key(self, secrets_file: str) -> str:
        """Load the OpenAI API key from the secrets file."""
        try:
            with open(secrets_file) as f:
                for line in f:
                    key, value = map(str.strip, line.split(','))
                    if key == "openai_key":
                        return value
            raise ValueError("OpenAI key not found in secrets file")
        except FileNotFoundError:
            raise FileNotFoundError(f"Secrets file not found: {secrets_file}")
    
    
    def call_gpt(self, message: str) -> str:
        """Call the model with the specified message."""
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": message}],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        return response.choices[0].message.content