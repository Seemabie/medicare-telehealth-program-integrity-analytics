"""
Visualization module for fraud detection results
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_risk_distribution(risk_scores, save_path='reports/figures/'):
    """Create risk score distribution histogram"""
    
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    
    # Create histogram with color coding
    n, bins, patches = ax.hist(risk_scores, bins=50, edgecolor='white')
    
    # Color by risk level
    for i, patch in enumerate(patches):
        if bins[i] < 25:
            patch.set_facecolor('#2E7D32')  # Green
        elif bins[i] < 50:
            patch.set_facecolor('#FFA726')  # Orange
        elif bins[i] < 75:
            patch.set_facecolor('#EF5350')  # Red
        else:
            patch.set_facecolor('#B71C1C')  # Dark red
    
    # Add threshold lines
    for threshold, label in zip([25, 50, 75], ['Low→Med', 'Med→High', 'High→Critical']):
        ax.axvline(threshold, color='black', linestyle='--', alpha=0.7)
        ax.text(threshold, ax.get_ylim()[1]*0.95, label, rotation=90, va='top')
    
    ax.set_xlabel('Combined Risk Score', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Providers', fontsize=12, fontweight='bold')
    ax.set_title('Distribution of Fraud Risk Scores', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{save_path}risk_distribution.png', dpi=300)
    return fig

def plot_geographic_analysis(state_data, save_path='reports/figures/'):
    """Create geographic fraud distribution plots"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)
    
    # State rankings
    top_states = state_data.nlargest(15, 'fraud_amount')
    colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(top_states)))
    
    ax1.barh(top_states['state'], top_states['fraud_amount'], color=colors)
    ax1.set_xlabel('Fraud Amount ($ Millions)', fontsize=12, fontweight='bold')
    ax1.set_title('Top 15 States by Fraud Amount', fontsize=14, fontweight='bold')
    
    # Provider concentration
    ax2.bar(top_states['state'], top_states['provider_count'], color=colors)
    ax2.set_xlabel('State', fontsize=12, fontweight='bold')
    ax2.set_ylabel('High-Risk Providers', fontsize=12, fontweight='bold')
    ax2.set_title('Geographic Concentration', fontsize=14, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(f'{save_path}geographic_analysis.png', dpi=300)
    return fig

def create_validation_dashboard(metrics, save_path='reports/figures/'):
    """Create model validation visualization"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10), dpi=300)
    
    # Confusion matrix
    cm = metrics['confusion_matrix']
    im = ax1.imshow(cm, cmap='Blues')
    ax1.set_title('Confusion Matrix', fontsize=12, fontweight='bold')
    
    # Feature importance
    features = metrics['feature_importance']
    ax2.barh(features['feature'], features['importance'])
    ax2.set_title('Feature Importance', fontsize=12, fontweight='bold')
    
    # Performance metrics
    perf = metrics['performance']
    ax3.bar(perf.keys(), perf.values())
    ax3.set_title('Model Performance', fontsize=12, fontweight='bold')
    ax3.set_ylim(0, 110)
    
    # Validation results
    val = metrics['validation']
    ax4.plot(val.keys(), val.values(), 'o-', linewidth=3, markersize=10)
    ax4.set_title('External Validation', fontsize=12, fontweight='bold')
    ax4.set_ylim(80, 105)
    
    plt.tight_layout()
    plt.savefig(f'{save_path}validation_dashboard.png', dpi=300)
    return fig