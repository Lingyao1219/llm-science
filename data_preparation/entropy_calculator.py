import numpy as np
import ast
from typing import List, Union, Optional

class EntropyCalculator:
    """
    A class to calculate Shannon entropy for various columns in a DataFrame.
    """
    
    @staticmethod
    def shannon_entropy(institution_list: List[str]) -> Optional[float]:
        """
        Calculate Shannon entropy for a list of institutions/values.
        Returns None if the list is empty.
        
        Args:
            institution_list (List[str]): List of institutions or other values
            
        Returns:
            Optional[float]: Calculated Shannon entropy value or None if list is empty
        """
        if not institution_list:
            return None
            
        try:
            value, counts = np.unique(institution_list, return_counts=True)
            probabilities = counts / len(institution_list)
            entropy = -np.sum(probabilities * np.log2(probabilities))
            return entropy
        except:
            return None
    
    @staticmethod
    def safe_eval_list(x: Union[str, List, None]) -> List[str]:
        """
        Safely evaluate a string representation of a list or return the list itself.
        
        Args:
            x (Union[str, List, None]): Input that could be a string representation of a list or a list
            
        Returns:
            List[str]: Converted list
        """
        if x is None:
            return []
        
        if isinstance(x, str):
            try:
                # Try to evaluate if it's a string representation of a list
                return ast.literal_eval(x)
            except (ValueError, SyntaxError):
                # If it's not a valid list representation, return empty list
                return []
        
        if isinstance(x, list):
            return x
            
        return []
    
    @staticmethod
    def clean_list(x: Union[str, List, None]) -> List[str]:
        """
        Clean a list by removing None, 'None', and empty strings.
        First converts string representations to actual lists.
        
        Args:
            x (Union[str, List, None]): List or string representation of list to clean
            
        Returns:
            List[str]: Cleaned list
        """
        if x is None:
            return []
            
        # First convert to list if it's a string representation
        x_list = EntropyCalculator.safe_eval_list(x)
        
        # Handle the case where x_list might be a nested list
        if x_list and isinstance(x_list[0], list):
            x_list = [item for sublist in x_list for item in sublist]
        
        # Replace None and 'None' with empty string
        cleaned = ['' if elem is None or elem == 'None' or elem == 'none' 
                  else str(elem) for elem in x_list]
        
        # Remove empty strings
        cleaned = [elem for elem in cleaned if elem.strip() != '']
        
        return cleaned
    
    def calculate_entropy(self, df, column_name: str):
        """
        Calculate entropy for a specific column in the DataFrame.
        Returns None for empty or None lists.
        
        Args:
            df: DataFrame containing the column
            column_name (str): Name of the column to calculate entropy for
            
        Returns:
            DataFrame with added entropy column
        """
        df = df.copy()
        
        # Clean the lists in the column
        df[column_name] = df[column_name].apply(self.clean_list)
        
        # Calculate entropy for all rows, returning None for empty lists
        df[f'{column_name}_entropy'] = df[column_name].apply(self.shannon_entropy)
        
        return df
    
    def calculate_all_entropies(self, df):
        """
        Calculate entropy for country_codes, institutions, and departments columns.
        
        Args:
            df: DataFrame containing the required columns
            
        Returns:
            DataFrame with added entropy columns
        """
        df = df.copy()
        
        # Calculate entropy for each column
        columns = ['country_codes', 'institutions', 'departments']
        for column in columns:
            if column in df.columns:
                print(f"Calculating entropy for {column}...")
                df = self.calculate_entropy(df, column)
            else:
                print(f"Warning: Column '{column}' not found in DataFrame")
        
        return df
