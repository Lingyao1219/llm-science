import pandas as pd
from typing import Dict, Any
from tqdm import tqdm
from config_utils import APIClient, CHECK_PROMPTS, MAX_ABSTRACT_WORDS


class RelevanceChecker:
    """Class for processing and classifying academic papers."""
    
    def __init__(self):
        """Initialize the document checker."""
        self.api_client = APIClient()
    
    def create_check_prompt(self, row: pd.Series) -> str:
        """Create a prompt for checking if a paper is LLM-related."""
        title = row['title']
        abstract = row['abstract']
        keywords = row['keywords']
        topics = row['topics']
        
        # Truncate abstract if it's too long
        if isinstance(abstract, str):
            words = abstract.split()
            if len(words) > MAX_ABSTRACT_WORDS:
                abstract = ' '.join(words[:MAX_ABSTRACT_WORDS])
        else:
            abstract = "N/A"
            
        # Format the prompt using the template
        prompt = (CHECK_PROMPTS["Task"] + 
                 CHECK_PROMPTS["Input"].format(title=title, abstract=abstract, keywords=keywords, topics=topics) +
                 CHECK_PROMPTS['Instruction'] + 
                 CHECK_PROMPTS["Output"])
        return prompt
    
    def check_papers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process papers and classify them using the LLM."""
        # Create prompts for each paper
        df['prompt'] = df.apply(self.create_check_prompt, axis=1)
        tqdm.pandas(desc="Processing papers")
        df['GPT_response'] = df['prompt'].progress_apply(self.api_client.call_gpt)
        df['GPT_response'] = (df['GPT_response'].str.replace('Yes.', 'Yes').str.replace('No.', 'No'))
        return df
