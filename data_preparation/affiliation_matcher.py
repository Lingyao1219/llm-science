import os
import ast
import pandas as pd
import numpy as np
from typing import List, Dict
from tqdm import tqdm


class AffiliationMatcher:
    """
    A class to process and analyze academic affiliations data.
    """
    
    def __init__(self):
        self.mapping_dict = {}
    
    def process_affiliation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process the affiliations column of the dataframe and extract various components.
        Handles both string-formatted and already-parsed dictionary affiliations.
        Args:
            df (pd.DataFrame): Input dataframe with 'affiliations' column
        Returns:
            pd.DataFrame: Processed dataframe with extracted affiliation information
        """
        df = df.copy()
        
        # Helper function to safely evaluate strings if needed
        def safe_eval(x):
            if isinstance(x, str):
                try:
                    return ast.literal_eval(x)
                except (ValueError, SyntaxError):
                    return x
            return x
        
        # Only apply literal_eval if the column contains strings
        if df['affiliations'].dtype == 'object':
            first_val = df['affiliations'].iloc[0]
            if isinstance(first_val, str):
                df['affiliations'] = df['affiliations'].apply(safe_eval)
        
        # Extract components
        def safe_extract(row, key):
            try:
                return [d[key] for d in row if isinstance(d, dict) and key in d]
            except (TypeError, AttributeError):
                return []

        df['author_names'] = df['affiliations'].apply(lambda x: safe_extract(x, 'author_name'))
        df['institutions'] = df['affiliations'].apply(lambda x: safe_extract(x, 'institution'))
        df['country_codes'] = df['affiliations'].apply(lambda x: safe_extract(x, 'country_code'))
        df['institution_types'] = df['affiliations'].apply(lambda x: safe_extract(x, 'institution_type'))
        df['affiliation_strings'] = df['affiliations'].apply(lambda x: safe_extract(x, 'affiliation_strings'))
        df['affiliation_strings'] = df['affiliation_strings'].apply(lambda x: [item for sublist in x for item in sublist] if x else [])
        return df
    

    def compile_files(self, folder_path: str) -> pd.DataFrame:
        """
        Compile multiple CSV files from a folder into a single DataFrame.
        Args:
            folder_path (str): Path to the folder containing CSV files
        Returns:
            pd.DataFrame: Concatenated DataFrame from all CSV files
        """
        df_list = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(folder_path, filename)
                try:
                    df = pd.read_csv(file_path, on_bad_lines='warn')
                    df_list.append(df)
                    #print(f"Successfully read {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
        
        if not df_list:
            print("No DataFrames were read. Please check the CSV files in the folder.")
            return pd.DataFrame()
        
        return pd.concat(df_list, ignore_index=True)
    

    def create_affiliation_mapping(self, affiliation_df: pd.DataFrame, compile_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create and process affiliation mapping DataFrame.
        Args:
            affiliation_df (pd.DataFrame): DataFrame with affiliation counts
            gpt_responses_df (pd.DataFrame, optional): DataFrame with GPT responses 
        Returns:
            pd.DataFrame: Processed affiliation mapping DataFrame
        """
        # Merge with existing GPT responses if provided
        merged_df = pd.merge(
            affiliation_df,
            compile_df[['affiliation_strings', 'gpt_response']],
            on='affiliation_strings',
            how='left'
        )
        
        merged_df['gpt_response'] = merged_df['gpt_response'].fillna("None")
        merged_df = merged_df.drop_duplicates()
        
        # Update mapping dictionary
        self.mapping_dict = {
            row['affiliation_strings']: row['gpt_response']
            for _, row in merged_df.iterrows()
            if pd.notna(row['gpt_response']) and row['gpt_response'] != "None"
        }
        return merged_df
    

    def get_disciplines(self, affiliations: List[str]) -> List[str]:
        """
        Process affiliations using exact dictionary lookup.
        
        Args:
            affiliations (List[str]): List of affiliation strings
            
        Returns:
            List[str]: List of corresponding disciplines
        """
        try:
            departments = []
            for affiliation in affiliations:
                if affiliation in self.mapping_dict:
                    departments.append(self.mapping_dict[affiliation])
            return departments
        except:
            return []
    

    def process_departments(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add departments column to the DataFrame based on affiliation strings.
        Args:
            df (pd.DataFrame): Input DataFrame with affiliation_strings column
        Returns:
            pd.DataFrame: DataFrame with added departments column
        """
        tqdm.pandas()
        df['departments'] = df['affiliation_strings'].progress_apply(self.get_disciplines)
        return df
