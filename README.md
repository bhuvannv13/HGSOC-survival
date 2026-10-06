# Precision Oncology: HGSOC Survival Prediction

Predicting survival in High-Grade Serous Ovarian Cancer (HGSOC) from TCGA clinical and mutation data, using XGBoost with SHAP explanations to show which features drive each prediction.

> Research and learning project. Not intended for clinical decision-making.

## Overview

The notebook covers:

- Loading and cleaning TCGA ovarian cancer clinical and mutation data (downloaded from cBioPortal)
- Exploratory data analysis of clinical and genomic features
- Building a binary survival target and training an **XGBoost classifier**
- Hyperparameter tuning with randomised search (5-fold cross-validation, ROC AUC scoring)
- Model interpretation with **SHAP**: global feature importance and per-patient explanations

## Results

From the saved notebook outputs, on a held-out test set of 124 patients:

| Metric | Value |
|---|---|
| Accuracy | 0.903 |
| ROC AUC | 0.963 |
| Macro F1 | 0.90 |

A caveat on these numbers: the feature set includes follow-up variables such as `Disease Free (Months)`, which are only known after the outcome and are closely tied to it. The scores therefore overstate how well survival could be predicted at diagnosis. Removing these columns is the main planned improvement.

## Repository contents

| File | Purpose |
|---|---|
| `Precisoncology4 (3).ipynb` | Full analysis notebook |
| `ov_tcga_clinical_data.tsv` | TCGA ovarian cancer clinical data |
| `xgb_best_model.joblib`, `xgb_best_model.json` | Trained XGBoost model |
| `requirements.txt` | Python dependencies |

## Getting started

```bash
git clone https://github.com/bhuvannv13/HGSOC-survival.git
cd HGSOC-survival
pip install -r requirements.txt
jupyter notebook
```

Then open `Precisoncology4 (3).ipynb`.

The notebook was written in Google Colab and reads files from Google Drive. To run it locally, update the file paths in the first cells. The mutation file (`data_mutations.txt`) is not included here; download the TCGA ovarian cancer study from [cBioPortal](https://www.cbioportal.org/).

## Loading the trained model

```python
import joblib
model = joblib.load("xgb_best_model.joblib")
```

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgements

- [cBioPortal](https://www.cbioportal.org/) and The Cancer Genome Atlas (TCGA)
- [SHAP](https://github.com/shap/shap), [XGBoost](https://github.com/dmlc/xgboost) and scikit-learn
