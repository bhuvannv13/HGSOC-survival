# 🎯 Precision Oncology - HGSOC Survival Analysis

This repository contains a Jupyter Notebook focused on applying data-driven techniques to analyze **High-Grade Serous Ovarian Cancer (HGSOC)** survival. It leverages SHAP (SHapley Additive exPlanations) to identify important clinical and genomic features contributing to patient outcomes. The dataset is sourced from **BioPortal**.

## 📁 Project Overview

This notebook includes:

* Loading and preprocessing of HGSOC clinical and genomic datasets from BioPortal
* Exploratory Data Analysis (EDA) to understand data distributions and relationships
* Survival analysis techniques to evaluate prognostic indicators
* Application of the **XGBoost Classifier** to predict patient survival
* Use of SHAP to interpret model outputs and highlight important features in ovarian cancer

## 🚀 Getting Started

### Prerequisites

To run the notebook, make sure you have the following installed:

* Python 3.8+
* Jupyter Notebook or JupyterLab
* pandas, numpy, matplotlib, seaborn
* lifelines
* scikit-learn
* shap
* xgboost

You can install the dependencies using:

```bash
pip install -r requirements.txt
```

### Running the Notebook

1. Clone the repository

```bash
git clone https://github.com/yourusername/precision-oncology-hgsoc.git
cd precision-oncology-hgsoc
```

2. Launch Jupyter Notebook

```bash
jupyter notebook
```

3. Open and run `Precisoncology4.ipynb`

## 📊 Results

The model outputs include:

* Survival curves for patient stratification
* SHAP value plots identifying top features impacting survival predictions
* Visualizations showing feature relationships and model performance

## 🧬 Dataset

The dataset used in this notebook is publicly available from [BioPortal](https://bioportal.bioontology.org/). It includes clinical and genetic features specific to ovarian cancer.

## 🧠 Interpretability

Model interpretability is a key focus. SHAP is used to provide:

* Global feature importance
* Local explanation of individual predictions

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgements

* [BioPortal](https://bioportal.bioontology.org/)
* SHAP by Scott Lundberg
* XGBoost by Tianqi Chen and contributors
* scikit-learn and Python open-source community

---

For questions or contributions, feel free to open an issue or pull request!
