"""
Data preprocessing module for Medicare Fraud Detection
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_medicare_data(year, data_dir='data/raw'):
    """Load Medicare provider data for specified year"""
    file_path = Path(data_dir) / f'Medicare_Physician_Other_Practitioners_by_Provider_{year}.csv'
    
    dtypes = {
        'Rndrng_NPI': str,
        'Rndrng_Prvdr_Type': str,
        'Rndrng_Prvdr_State_Abrvtn': str
    }
    
    df = pd.read_csv(file_path, dtype=dtypes, low_memory=False)
    return df

def create_fraud_features(df):
    """Engineer fraud detection features from raw data"""
    
    features = pd.DataFrame()
    features['NPI'] = df['Rndrng_NPI'].astype(str)
    features['Provider_Type'] = df['Rndrng_Prvdr_Type']
    features['State'] = df['Rndrng_Prvdr_State_Abrvtn']
    
    # Service metrics
    service_cols = [col for col in df.columns if 'srvc' in col.lower()]
    if service_cols:
        numeric_cols = df[service_cols].select_dtypes(include=[np.number]).columns
        features['Total_Services'] = df[numeric_cols].fillna(0).sum(axis=1)
        features['Service_Diversity'] = (df[numeric_cols] > 0).sum(axis=1)
    
    # Payment metrics
    payment_cols = [col for col in df.columns if 'pymt' in col.lower()]
    if payment_cols:
        numeric_cols = df[payment_cols].select_dtypes(include=[np.number]).columns
        features['Total_Payments'] = df[numeric_cols].fillna(0).sum(axis=1)
        features['Payment_Variance'] = df[numeric_cols].var(axis=1)
    
    # Derived metrics
    features['Daily_Service_Volume'] = features['Total_Services'] / 250
    features['Payment_Per_Service'] = (
        features['Total_Payments'] / features['Total_Services']
    ).replace([np.inf, -np.inf], 0).fillna(0)
    
    # Remove inactive providers
    features = features[features['Total_Services'] > 0]
    
    return features

def calculate_peer_benchmarks(features):
    """Calculate specialty-state peer statistics"""
    
    benchmarks = features.groupby(['Provider_Type', 'State']).agg({
        'Total_Services': ['mean', 'median', 'std'],
        'Total_Payments': ['mean', 'median', 'std'],
        'Payment_Per_Service': ['mean', 'median']
    }).round(2)
    
    return benchmarks