import os
import string
from typing import List, Optional, Set, Tuple
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime


class DocumentProcessor:
    """
    A class to handle academic document processing and analysis.
    Attributes:
        valid_types (List[str]): List of valid document types (e.g., 'preprint', 'article')
    """
    
    def __init__(self, valid_types: List[str] = None):
        """
        Initialize the DocumentProcessor.
        
        Args:
            valid_types: List of valid document types. Defaults to ['preprint', 'article']
        """
        self.valid_types = valid_types or ['preprint', 'article']
    

    @staticmethod
    def sample_documents(directory: str, sample_percentage: float) -> pd.DataFrame:
        """
        Select a random sample from downloaded files.
        Args:
            directory: Path to directory containing CSV files
            sample_percentage: Percentage of data to sample (0.0 to 1.0)  
        Returns:
            DataFrame containing sampled data from all files
        """
        if not 0 <= sample_percentage <= 1:
            raise ValueError("sample_percentage must be between 0 and 1")
            
        all_data = []
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                data = pd.read_csv(file_path)
                sample_size = int(len(data) * sample_percentage)
                sampled_data = data.sample(n=sample_size)
                all_data.append(sampled_data)
                
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()


    @staticmethod
    def filter_by_indexed(df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter out documents with empty indexed_in lists.
        
        Args:
            df: Input DataFrame
        Returns:
            DataFrame with non-empty indexed_in entries
        """
        return df[df['indexed_in'].astype(str) != '[]']


    @staticmethod
    def process_dates(df: pd.DataFrame) -> pd.DataFrame:
        """
        Process dates to create a datetime column based on publication and created dates.
        
        Args:
            df: Input DataFrame
        Returns:
            DataFrame with processed datetime column
        """
        df = df.copy()
        
        # Convert dates to datetime
        df['publication_date'] = pd.to_datetime(df['publication_date'], format='mixed')
        df['created_date'] = pd.to_datetime(df['created_date'], format='mixed')
        
        # Create new datetime column based on conditions
        df['datetime'] = df.apply(lambda row: 
            # If publication_date is January 1st of any year, use created_date
            row['created_date'] if (row['publication_date'].month == 1 and row['publication_date'].day == 1)
            # Otherwise use publication_date
            else row['publication_date'], 
            axis=1
        )
        return df


    @staticmethod
    def filter_by_date(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Filter and sort documents by date range using the processed datetime column.
        
        Args:
            df: Input DataFrame
            start_date: Start date in string format (YYYY-MM-DD)
            end_date: End date in string format (YYYY-MM-DD)
        Returns:
            Filtered and sorted DataFrame
        """
        # Process dates to create datetime column
        df = DocumentProcessor.process_dates(df)
        
        # Convert start_date and end_date to datetime
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        # Filter by date range
        mask = (df['datetime'] >= start_date) & (df['datetime'] <= end_date)
        return df[mask].sort_values(by='datetime')



    def filter_by_type(self, df: pd.DataFrame, types: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Filter documents by type.
        Args:
            df: Input DataFrame
            types: List of document types to include. If None, uses self.valid_types 
        Returns:
            Filtered DataFrame
        """
        types = types or self.valid_types
        return df[df['type'].isin(types)]


    @staticmethod
    def preprocess_text(text: str) -> str:
        """
        Preprocess text by removing punctuation and standardizing format.
        Args:
            text: Input text string 
        Returns:
            Preprocessed text string
        """
        if not isinstance(text, str):
            return ""
        return text.translate(str.maketrans('', '', string.punctuation)).lower().strip()


    def remove_exact_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove exact duplicate documents based on preprocessed titles.
        Args:
            df: Input DataFrame
        Returns:
            DataFrame with exact duplicates removed
        """
        df = df.copy()
        df['processed_title'] = df['title'].astype(str).apply(self.preprocess_text)
        df = df.drop_duplicates(subset=['processed_title'], keep='last')
        return df.drop(columns=['processed_title'])


    @staticmethod
    def calculate_jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
        """
        Calculate Jaccard similarity between two sets of words.
        Args:
            set1: First set of words
            set2: Second set of words
        Returns:
            Jaccard similarity score (0.0 to 1.0)
        """
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union != 0 else 0.0


    def find_matching_article(
        self,
        preprint_row: pd.Series,
        articles_df: pd.DataFrame,
        threshold: float = 0.5
    ) -> Tuple[Optional[str], Optional[datetime], Optional[float]]:
        """
        Find a potential published article matching a given preprint.
        Args:
            preprint_row: Series containing preprint information
            articles_df: DataFrame containing article information
            threshold: Minimum similarity threshold for matching
        Returns:
            Tuple of (matched article title, publication date, similarity score)
        """
        preprint_date = preprint_row['publication_date']
        preprint_topic = preprint_row['topics']
        preprint_words = set(self.preprocess_text(preprint_row['title']).split())
        
        # Filter potential matches
        mask = (articles_df['publication_date'] > preprint_date) & (articles_df['topics'] == preprint_topic)
        potential_matches = articles_df[mask]
        
        if potential_matches.empty:
            return None, None, None
            
        # Find best match
        best_match = (None, None, 0.0)
        for _, article in potential_matches.iterrows():
            article_words = set(self.preprocess_text(article['title']).split())
            similarity = self.calculate_jaccard_similarity(preprint_words, article_words)
            
            if similarity > best_match[2]:
                best_match = (article['title'], article['publication_date'], similarity)
        
        if best_match[2] >= threshold:
            return best_match
        return None, None, None


    def remove_similar_documents(self, df: pd.DataFrame, similarity_threshold: float = 0.6) -> pd.DataFrame:
        """
        Remove preprints that have matching published articles.
        Args:
            df: Input DataFrame
            similarity_threshold: Minimum similarity score to consider documents as matching 
        Returns:
            DataFrame with similar preprints removed
        """
        required_columns = {'doi', 'type', 'title', 'created_date', 'topics'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"DataFrame must contain columns: {required_columns}")
            
        df = df.copy()
        df = df.sort_values(by='created_date')
        
        preprints = df[df['type'] == 'preprint']
        articles = df[df['type'] == 'article']
        
        # Find matching articles for each preprint
        matches = []
        for _, preprint in tqdm(preprints.iterrows(), total=len(preprints), desc="Processing preprints"):
            title, date, similarity = self.find_matching_article(preprint, articles)
            if similarity and similarity >= similarity_threshold:
                matches.append(preprint['doi'])
                
        # Remove matched preprints
        return df[~df['doi'].isin(matches)]
