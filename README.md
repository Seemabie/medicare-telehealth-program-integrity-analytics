# medicare-telehealth-program-integrity-analytics

**Medicare Telehealth Fraud and Utilization Analytics: An Unsupervised Anomaly Detection Framework on Post-COVID HCPCS-Level Provider Service Data**

Author: Seemab Hassan (Independent Researcher)
SSRN preprint: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6978839

## Overview

Complete, reproducible analytical pipeline for an unsupervised anomaly-detection and
risk-stratification system applied to 46,900 active Medicare telehealth providers, built entirely from public CMS data.
Results are presented as anomaly detection for investigative prioritization, not as
fraud determinations.

## Contents

- `notebook/` reproducible Jupyter notebook implementing the full pipeline
- `dashboard/` interactive Streamlit dashboard (reads only from the persisted result files; no hardcoded values)
- `results/` persisted result files (CSV/JSON), including `RUN_INFO.json`, the reproducibility envelope with software versions, the fixed random seed (42), and SHA-256 hashes of every source file
- `figures/` publication-quality figures (300 DPI)
- `preprint/` the SSRN methodology preprint (PDF)
- `CLAIMS_TRACEABILITY.*` maps each numerical claim to its source result file

## Reproduce

```bash
pip install -r requirements.txt
```

The raw CMS source data files are public and are not redistributed here (see Data Availability).
`RUN_INFO.json` records the SHA-256 hash of each source file, so you can verify you have the exact
inputs. With the same source files and the fixed random seed of 42, the notebook reproduces every
headline figure within the reported confidence-interval bounds.

## Interactive dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard/dashboard_telehealth_rebuild.py
```

## Data availability

All inputs are public:
- CMS Medicare Public Use Files: https://data.cms.gov
- HHS-OIG List of Excluded Individuals and Entities (LEIE): https://oig.hhs.gov/exclusions/

Additional federal sources are documented in the notebook and in `results/RUN_INFO.json`.

## License

MIT License (see `LICENSE`).
