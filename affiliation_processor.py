import os
import ast
import pandas as pd
from typing import List, Dict, Any
from tqdm import tqdm
from pathlib import Path
from config_utils import APIClient, DISCIPLINE_PROMPTS


class AffiliationProcessor:
    """
    A class to process and analyze academic affiliations data.
    
    Attributes:
        api_client: API client for LLM interactions
        batch_size (int): Size of batches for processing
        save_directory (Path): Directory for saving processed data
    """
    
    def __init__(self, batch_size: int = 100, save_directory: str = "processed_data"):
        """
        Initialize the AffiliationProcessor.
        
        Args:
            api_client: API client instance for LLM calls
            batch_size: Number of records to process in each batch
            save_directory: Directory path for saving processed files
        """
        self.api_client = APIClient()
        self.batch_size = batch_size
        self.save_directory = Path(save_directory)
        self.save_directory.mkdir(exist_ok=True)
    

    def extract_affiliation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process affiliation data from a DataFrame. 
        Args:
            df: DataFrame containing affiliation data  
        Returns:
            DataFrame with processed affiliation information
        """
        df = df.copy()
        df['affiliations'] = df['affiliations'].apply(ast.literal_eval)
        
        # Extract information from affiliations
        extraction_fields = {
            'author_names': 'author_name',
            'institutions': 'institution',
            'country_codes': 'country_code',
            'institution_types': 'institution_type',
            'affiliation_strings': 'affiliation_strings'
        }
        
        for field, key in extraction_fields.items():
            df[field] = df['affiliations'].apply(lambda x: [d[key] for d in x])
        # Flatten affiliation strings
        df['affiliation_strings'] = df['affiliation_strings'].apply(lambda x: [item for sublist in x for item in sublist])
        return df
    

    def create_discipline_prompt(self, row: pd.Series) -> str:
        """Create a prompt for extracting the affiliation information."""
        affiliation = row['affiliation_string']
        prompt = (DISCIPLINE_PROMPTS['Task'].format(affiliation=affiliation) + 
                  DISCIPLINE_PROMPTS['Instruction']
                  )
        return prompt


    def prepare_prompt(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare affiliation data for analysis.
        Args:
            df: DataFrame with processed affiliations
        Returns:
            DataFrame ready for discipline extraction
        """
        # Create affiliation frequency DataFrame
        affiliation_df = (df['affiliation_strings'].explode().value_counts().reset_index())
        affiliation_df.columns = ['affiliation_string', 'count']
        affiliation_df['affiliation_string'] = affiliation_df['affiliation_string'].astype(str)
        affiliation_df = affiliation_df.dropna(subset=['affiliation_string'])
        affiliation_df['prompt'] = affiliation_df.apply(self.create_discipline_prompt, axis=1)
        return affiliation_df
    

    def process_batches(self, df: pd.DataFrame) -> None:
        """
        Process data in batches and save results.
        Args:
            df: DataFrame to process in batches
        """
        for batch_num, start_idx in enumerate(range(0, len(df), self.batch_size)):
            batch = df.iloc[start_idx:start_idx + self.batch_size]
            self._process_single_batch(batch, batch_num)
    

    def _process_single_batch(self, batch: pd.DataFrame, batch_number: int) -> None:
        """
        Process a single batch of data.
        Args:
            batch: Batch of data to process
            batch_number: Current batch number
        """
        tqdm.pandas(desc=f"Processing batch {batch_number}")
        batch['gpt_response'] = batch['prompt'].progress_apply(
            lambda x: self.api_client.call_gpt(x)
        )
        output_path = self.save_directory / f'gpt_responses_batch_{batch_number}.csv'
        batch.to_csv(output_path, index=False)
        print(f"Batch {batch_number} processed and saved to {output_path}")
    

    def compile_results(self) -> pd.DataFrame:
        """
        Compile all processed batch results into a single DataFrame.
        Returns:
            Combined DataFrame of all processed results
        """
        df_list = []
        
        for file_path in self.save_directory.glob('*.csv'):
            try:
                df = pd.read_csv(file_path, on_bad_lines='warn')
                df_list.append(df)
                print(f"Successfully read {file_path}")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        
        if not df_list:
            print("No DataFrames were read. Please check the CSV files in the folder.")
            return pd.DataFrame()
        
        return pd.concat(df_list, ignore_index=True)