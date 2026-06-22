# Project 5 Claims Traceability (FINAL VERIFIED)

**Purpose:** Every numerical claim in the rebuilt artifacts traced to its source result file, notebook cell, and computational provenance. Audit trail proving nothing is fabricated.

**Verification status:** All 63 claims VERIFIED against persisted result files.

**Verification date:** May 14, 2026

---

## Verified claims table

| ID | Claim | Computed value | Source file | Notebook section |
|---|---|---|---|---|
| T-001 | Active telehealth providers in 2023 analytical universe | 46,900 | results/scored_universe_2023.csv | Section 2 |
| T-002 | Total telehealth services billed across analytical universe 2023 | 9,118,975 | results/scored_universe_2023.csv | Section 2 |
| T-003 | Total Medicare telehealth payments 2023 | $396,167,172.64 | results/scored_universe_2023.csv | Section 2 |
| T-004 | Distinct telehealth HCPCS codes observed (of 27 in basket) | 24 | results/filtered/telehealth_2023.csv | Section 2 |
| T-005 | Number of flagged providers (top 5 percent by combined risk) | 2,346 | results/flagged_providers_2023.csv | Section 7 |
| T-006 | Sample excess billing across flagged set | $161,742,186.87 | results/flagged_providers_2023.csv (Excess_Billing column sum) | Section 8 |
| T-007 | Bootstrap 95 percent CI on sample excess (low) | $145,467,900 | results/bootstrap.csv | Section 10 |
| T-008 | Bootstrap 95 percent CI on sample excess (high) | $179,224,021 | results/bootstrap.csv | Section 10 |
| T-009 | Coverage multiplier for national projection | 3.447 | results/projection_methodology.json | Section 9 |
| T-010 | Projected national excess (coverage adjusted) | $557,508,466.85 | results/projection_methodology.json | Section 9 |
| T-011 | Total Provider+Service rows across five years | 48,891,840 | REBUILD_LOG.md | Section 1 |
| T-012 | 2019 Provider+Service row count | 10,140,228 | REBUILD_LOG.md | Section 1 |
| T-013 | 2020 Provider+Service row count | 9,449,361 | REBUILD_LOG.md | Section 1 |
| T-014 | 2021 Provider+Service row count | 9,886,177 | REBUILD_LOG.md | Section 1 |
| T-015 | 2022 Provider+Service row count | 9,755,427 | REBUILD_LOG.md | Section 1 |
| T-016 | 2023 Provider+Service row count | 9,660,647 | REBUILD_LOG.md | Section 1 |
| T-017 | LEIE total excluded entities | 81,914 | REBUILD_LOG.md | Section 1 |
| T-018 | TMEDTREND row count | 30,100 | REBUILD_LOG.md | Section 1 |
| T-019 | 2023 telehealth HCPCS filtered rows | 73,269 | results/filtered/telehealth_2023.csv | Section 2 |
| T-020 | 2023 unique active telehealth providers (post filter) | 46,900 | results/scored_universe_2023.csv | Section 2 |
| T-021 | Top state by flagged provider count | CA | results/per_state_excess_2023.csv | Section 8 |
| T-022 | Top state by excess billing | CA | results/per_state_excess_2023.csv | Section 8 |
| T-023 | California flagged provider count | 439 | results/per_state_excess_2023.csv | Section 8 |
| T-024 | New York flagged provider count | 265 | results/per_state_excess_2023.csv | Section 8 |
| T-025 | Texas flagged provider count | 300 | results/per_state_excess_2023.csv | Section 8 |
| T-026 | Florida flagged provider count | 192 | results/per_state_excess_2023.csv | Section 8 |
| T-027 | Number of states with at least one flagged provider | 47 | results/per_state_excess_2023.csv | Section 8 |
| T-028 | Highest combined risk score | 97.31 | results/scored_universe_2023.csv | Section 7 |
| T-029 | Top 1 provider name | Cardionet, Llc | results/flagged_providers_2023.csv | Section 8 |
| T-030 | Top 1 provider excess billing | $3,948,662.20 | results/flagged_providers_2023.csv | Section 8 |
| T-031 | Top 1 provider telehealth services | 78,313 | results/flagged_providers_2023.csv | Section 2 |
| T-032 | Top 1 provider state median Payment_Per_Bene | $99.17 | results/state_baselines.csv | Section 4 |
| T-033 | Tier counts (Low, Medium, High, Critical, Extreme) | 37519, 7035, 1876, 423, 47 | results/tier_distribution.csv | Section 7 |
| T-034 | Permutation importance top feature | Audio_Only_Share | results/permutation_importance.csv | Section 11 |
| T-035 | Permutation importance top feature percent | 17.5% | results/permutation_importance.csv | Section 11 |
| T-036 | Temporal holdout coverage percent | 79.9% | results/temporal_holdout.csv | Section 12 |
| T-037 | Temporal mean lift ratio | 3.35x | results/temporal_holdout.csv | Section 12 |
| T-038 | Temporal median lift ratio | 4.97x | results/temporal_holdout.csv | Section 12 |
| T-039 | LEIE direct NPI match count in flagged set | 5 | Computed: intersection of flagged_providers_2023.csv NPIs with LEIE Database.csv valid 10-digit NPI set (8,066 LEIE NPIs total) | Section 13 |
| T-040 | LEIE fuzzy name match count (top 100 flagged) | 8 | results/leie_concordance.csv | Section 13 |
| T-041 | DOJ named defendant match count | 0 | results/doj_cross_reference.csv (empty file = no matches) | Section 14 |
| T-042 | Bootstrap mean of flagged count | 2345 | results/bootstrap.csv | Section 10 |
| T-043 | Bootstrap mean of sample excess | $161,593,000 | results/bootstrap.csv | Section 10 |
| T-044 | Extreme payment per beneficiary typology match count | 488 | results/fraud_typology.csv | Section 15 |
| T-045 | Audio only heavy typology match count | 200 | results/fraud_typology.csv | Section 15 |
| T-046 | Single HCPCS dominance typology match count | 148 | results/fraud_typology.csv | Section 15 |
| T-047 | Rural high volume typology match count | 1 | results/fraud_typology.csv | Section 15 |
| T-048 | Pandemic emergence typology match count | 1295 | results/fraud_typology.csv | Section 15 |
| T-049 | Multi-typology providers count (2+ patterns) | 475 | results/fraud_typology.csv | Section 15 |
| T-050 | Flagged count at 95th percentile cutoff | 2,345 | results/threshold_sensitivity.csv | Section 16 |
| T-051 | Sample excess at 95th percentile cutoff | $161,700,014 | results/threshold_sensitivity.csv | Section 16 |
| T-052 | Flagged count at 99th percentile cutoff | 469 | results/threshold_sensitivity.csv | Section 16 |
| T-053 | Sample excess at 99th percentile cutoff | $71,108,489 | results/threshold_sensitivity.csv | Section 16 |
| T-054 | 2020 national Pct_Telehealth | 0.4791 (47.91%) | results/tmedtrend_national.csv | Section 9 |
| T-055 | 2023 national Pct_Telehealth | 0.2499 (24.99%) | results/tmedtrend_national.csv | Section 9 |
| T-056 | Total Medicare beneficiaries using telehealth 2020 | 14,826,919 | results/tmedtrend_national.csv | Section 9 |
| T-057 | Total Medicare beneficiaries using telehealth 2023 | 6,971,495 | results/tmedtrend_national.csv | Section 9 |
| T-058 | Telehealth decline 2020 to 2023 (%) | -53.0% | results/tmedtrend_national.csv | Section 9 |
| T-059 | Random seed used | 42 | results/RUN_INFO.json | Section 17 |
| T-060 | Isolation Forest contamination | 0.02 | results/RUN_INFO.json | Section 17 |
| T-061 | Isolation Forest n_estimators | 100 | results/RUN_INFO.json | Section 17 |
| T-062 | Bootstrap iterations | 1000 | results/RUN_INFO.json | Section 17 |
| T-063 | Fuzzy similarity threshold | 0.85 | results/RUN_INFO.json | Section 17 |

---

## Retired claims (fabricated in original artifacts, removed from rebuild)

These appeared in the original notebook, dashboard, exhibit, or executive summary but cannot be defended. The rebuild does not assert any of these.

| Original claim | Where it appeared | Why retired |
|---|---|---|
| Precision 100 percent on critical category | Dashboard, exhibit, exec summary, README | No labeled ground truth, impossible on unsupervised model |
| Recall 42 to 67 percent | Dashboard, exhibit, methodology | Same reason |
| F1 score 0.59 | Dashboard, exhibit | Same reason |
| AUC ROC 0.94 to 0.976 | Dashboard, exhibit | Same reason |
| Accuracy 91.3 percent +/- 2.4 percent k-fold | Exhibit, algorithm_implementation.py | No k-fold code, no labels |
| DOJ Strike Force 94 percent geographic match | Dashboard, exhibit, exec summary | No DOJ data loaded in original notebook |
| Temporal stability 89 to 92 percent | Dashboard, exhibit, methodology | Not computed |
| Quality score correlation minus 0.72 | Dashboard line 188 | np.random synthetic data |
| All correlation table entries with p<0.001 | Dashboard lines 201 to 208 | Hardcoded |
| Feature importance 38, 27, 18, 11, 6 percent | Exhibit Section 3.3 | Isolation Forest does not natively expose this; no permutation routine |
| 4,500 percent telehealth growth | Dashboard line 62, exhibit | Hardcoded constants 13, 156, 389, 512, 585 |
| $63 billion five year savings | Dashboard, exhibit | No projection model |
| 126,000 to 1 ROI | Notebook cell 52 | Denominator $100,000 unsourced |
| 18,000 to 1 ROI | Dashboard | Variant of above |
| 47x null model improvement | Exhibit Section 5.2 | No null model code |
| Bonferroni correction | methodology.md | No code |
| Mahalanobis distance | Exhibit Section 2.2 | No code |
| 148 records per second processing speed | Algorithm file | No throughput measurement |
| 2.5 GB peak memory | Execution appendix | No memory profile |
| 400,000 telehealth providers | Exhibit Section 1.1 | Scope misrepresented; actual analytical universe is post HCPCS filter at 46,900 |
| Pharmacy peer median 47,231 services | Dashboard "30,500% excess" framing | Inconsistent with notebook output (peer median was 820 by Provider_Type) |
| 145 OIG confirmed fraud cases as validation of 35 critical providers | Multiple artifacts | Conflated populations; notebook cell 47 explicitly says no LEIE matches in critical group |
| 35 critical providers, $420.2M sample excess | Multiple artifacts | Came from 50,000-row head sample of general Medicare physician file, not telehealth-filtered universe; rebuild produces 2,346 flagged providers with $161.7M sample excess based on true HCPCS-filtered 2023 universe of 46,900 providers |

---

## Verification methodology

Every claim ID was computed by re-running the notebook cell that produces it, then reading the persisted result file. The Phase Two notebook is fully reproducible end to end:

1. Random seed: 42 (fixed in Section 1)
2. SHA-256 hashes of all source files recorded in RUN_INFO.json
3. Software versions recorded: Python 3.10.12, numpy 2.2.6, pandas 2.3.3, scikit-learn 1.7.2, scipy 1.15.3
4. Every section persists its output to results/*.csv or results/*.json before the next section reads it

Independent reviewers can verify any claim by reading the source file in the column and locating the corresponding cell in TELEHEALTH_REBUILD_V3.ipynb.

End of claims traceability table.
