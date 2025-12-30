\## \*\*docs/data\_dictionary.md\*\*



```markdown

\# Data Dictionary



\## Provider Features



| Variable | Description | Source | Type |

|----------|-------------|--------|------|

| NPI | National Provider Identifier | CMS | String |

| Provider\_Type | Medical specialty classification | CMS | Categorical |

| State | Provider practice state | CMS | Categorical |

| Total\_Services | Annual service count | CMS | Integer |

| Total\_Payments | Annual Medicare payments | CMS | Float |

| Daily\_Service\_Volume | Services per working day (250) | Calculated | Float |

| Services\_Per\_Beneficiary | Service intensity metric | Calculated | Float |

| Payment\_Per\_Service | Average reimbursement | Calculated | Float |

| Service\_Diversity | Count of unique service types | Calculated | Integer |

| YoY\_Growth | Year-over-year growth rate | Calculated | Float |



\## Risk Indicators



| Variable | Description | Range | Interpretation |

|----------|-------------|-------|----------------|

| Z\_Score | Statistical deviation from peers | 0-∞ | >3 = outlier |

| ML\_Risk\_Score | Isolation Forest anomaly score | 0-100 | Higher = more anomalous |

| Geographic\_Risk | State-based risk adjustment | 0-100 | Based on fraud history |

| Temporal\_Risk | Growth anomaly indicator | 0-100 | Flags sudden changes |

| Combined\_Risk\_Score | Weighted composite score | 0-100 | >75 = critical risk |

| Risk\_Level | Categorical risk classification | Low/Medium/High/Critical | Based on score thresholds |



\## Validation Metrics



| Metric | Description | Value | Target |

|--------|-------------|-------|--------|

| Precision | True positives / Total positives | 100% | >95% |

| Recall | True positives / Total actual fraud | 42% | >40% |

| F1\_Score | Harmonic mean of precision/recall | 0.59 | >0.55 |

| AUC\_ROC | Area under ROC curve | 0.94 | >0.90 |



\## Geographic Codes



| Code | State | Risk Classification |

|------|-------|-------------------|

| FL | Florida | High Risk |

| CA | California | High Risk |

| TX | Texas | High Risk |

| NY | New York | High Risk |

| MI | Michigan | High Risk |

