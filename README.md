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

From the latest full run of the notebook (GitHub Actions, see `RESULTS.md`), on a held-out test set of 124 patients:

| Metric | Value |
|---|---|
| Accuracy | 0.782 |
| ROC AUC | 0.906 |
| Macro F1 | 0.77 |

An earlier version of the notebook reported 0.903 accuracy and 0.963 AUC. Those figures were inflated by follow-up variables such as `Disease Free (Months)`, which are only known after the outcome. `tools/rerun.py` now drops those columns (and free-text identifiers) before training, and the numbers above come from that run.

Remaining caveat: `Year Cancer Initial Diagnosis` is still a feature. In TCGA, patients diagnosed earlier have had longer follow-up, so this column partly reflects follow-up time rather than biology, and the AUC is likely still optimistic for prediction at diagnosis.

## Repository contents

| File | Purpose |
|---|---|
| `Precisoncology4 (3).ipynb` | Full analysis notebook |
| `ov_tcga_clinical_data.tsv` | TCGA ovarian cancer clinical data |
| `xgb_best_model.json` | XGBoost model saved by the latest run |
| `xgb_best_model.joblib` | Model from the earlier run (trained with the follow-up columns; kept for reference) |
| `tools/rerun.py` | Downloads the data, removes leaked features and reruns the notebook |
| `RESULTS.md` | Metrics printed by the latest run |
| `requirements.txt` | Python dependencies |

## Getting started

```bash
git clone https://github.com/bhuvannv13/HGSOC-survival.git
cd HGSOC-survival
pip install -r requirements.txt
jupyter notebook
```

Then open `Precisoncology4 (3).ipynb`.

To reproduce the published run, which downloads the TCGA ovarian cancer study from [cBioPortal](https://www.cbioportal.org/) into `data/` and executes every cell:

```bash
pip install nbformat nbclient ipykernel
python tools/rerun.py
```

The same script can be run from the repository's Actions tab ("Rerun notebook", manual trigger).

## Loading the trained model

```python
import xgboost as xgb
model = xgb.XGBClassifier()
model.load_model("xgb_best_model.json")
```

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgements

- [cBioPortal](https://www.cbioportal.org/) and The Cancer Genome Atlas (TCGA)
- [SHAP](https://github.com/shap/shap), [XGBoost](https://github.com/dmlc/xgboost) and scikit-learn
