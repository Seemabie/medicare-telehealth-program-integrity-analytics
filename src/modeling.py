"""
Fraud detection modeling module
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class MedicareFraudDetector:
    """Medicare fraud detection using combined risk scoring"""
    
    def __init__(self, contamination=0.01, random_state=42):
        self.contamination = contamination
        self.random_state = random_state
        self.isolation_forest = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        
    def calculate_statistical_score(self, features, benchmarks):
        """Calculate z-score based statistical outliers"""
        z_scores = []
        
        for col in ['Total_Services', 'Daily_Service_Volume', 'Payment_Per_Service']:
            if col in features.columns:
                mean = features[col].mean()
                std = features[col].std()
                if std > 0:
                    z = np.abs((features[col] - mean) / std)
                    z_scores.append(z)
        
        if z_scores:
            return np.mean(z_scores, axis=0) * 20
        return np.zeros(len(features))
    
    def calculate_ml_anomaly_score(self, features):
        """Calculate ML-based anomaly scores"""
        feature_cols = ['Total_Services', 'Service_Diversity', 
                       'Daily_Service_Volume', 'Payment_Per_Service']
        
        X = features[feature_cols].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        self.isolation_forest.fit(X_scaled)
        scores = self.isolation_forest.score_samples(X_scaled)
        
        # Normalize to 0-100
        normalized = (scores.min() - scores) / (scores.min() - scores.max()) * 100
        return normalized
    
    def calculate_geographic_risk(self, states):
        """Adjust for geographic fraud risk"""
        high_risk_states = ['FL', 'CA', 'TX', 'NY', 'MI']
        return states.isin(high_risk_states).astype(int) * 100
    
    def calculate_risk_scores(self, features, weights=None):
        """Calculate combined fraud risk scores"""
        
        if weights is None:
            weights = {
                'statistical': 0.30,
                'ml': 0.40,
                'geographic': 0.15,
                'temporal': 0.15
            }
        
        # Component scores
        statistical = self.calculate_statistical_score(features, None)
        ml = self.calculate_ml_anomaly_score(features)
        geographic = self.calculate_geographic_risk(features['State'])
        
        # Combine with weights
        combined = (
            statistical * weights['statistical'] +
            ml * weights['ml'] +
            geographic * weights['geographic']
        )
        
        # Create output
        results = pd.DataFrame({
            'NPI': features['NPI'],
            'Risk_Score': np.clip(combined, 0, 100),
            'Risk_Level': pd.cut(combined, 
                                bins=[0, 25, 50, 75, 100],
                                labels=['Low', 'Medium', 'High', 'Critical'])
        })
        
        return results