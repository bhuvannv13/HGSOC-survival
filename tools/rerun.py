"""Apply the data-leakage fix to the HGSOC notebook and re-execute it end to end.

Run from the repository root:  python tools/rerun.py
Use --no-run to apply the edits without executing.
"""
import re
import sys

import nbformat

NOTEBOOK = "Precisoncology4 (3).ipynb"

DOWNLOAD_CELL = '''# Data: TCGA ovarian cancer study (ov_tcga) from the cBioPortal DataHub
import os
import tarfile
import urllib.request

if not os.path.exists("data/ov_tcga/data_mutations.txt"):
    os.makedirs("data", exist_ok=True)
    urllib.request.urlretrieve(
        "https://cbioportal-datahub.s3.amazonaws.com/ov_tcga.tar.gz", "data/ov_tcga.tar.gz"
    )
    with tarfile.open("data/ov_tcga.tar.gz") as archive:
        archive.extractall("data")
print(sorted(os.listdir("data/ov_tcga"))[:10])'''

LEAKAGE_BLOCK = '''

# Remove follow-up and outcome variables. They are only known after the outcome
# and are closely tied to survival status, so keeping them leaks the answer.
LEAKAGE_COLUMNS = [
    'Overall Survival (Months)',
    'Disease Free (Months)',
    'Disease Free Status',
    'Last Alive Less Initial Pathologic Diagnosis Date Calculated Day Value',
    'days_to_patient_progression_free',
    'days_to_tumor_progression',
    'New Neoplasm Event Post Initial Therapy Indicator',
    'Primary Therapy Outcome Success Type',
    'Person Neoplasm Status',
    'Form completion date',
]
# Free-text identifiers carry no clinical signal and only add thousands of one-hot columns.
IDENTIFIER_COLUMNS = [
    'Other Patient ID', 'Other Sample ID',
    'Pathology Report File Name', 'Pathology report uuid',
]
X = X.drop(columns=[c for c in LEAKAGE_COLUMNS + IDENTIFIER_COLUMNS if c in X.columns])
print("Feature columns after removing leakage and identifiers:", X.shape[1])
'''

PATHS = [
    ("/content/drive/MyDrive/PrecisonOncology/ov_tcga/ov_tcga/", "data/ov_tcga/"),
    ("/content/drive/MyDrive/PrecisonOncology/ov_tcga_clinical_data.tsv", "ov_tcga_clinical_data.tsv"),
    ("/content/drive/MyDrive/PrecisonOncology/ov_tcga/df_cleaned.tsv", "data/df_cleaned.tsv"),
]

LEAKED_INPUTS = [
    '"Disease Free (Months)",',
    '"Overall Survival (Months)",',
    '"Person Neoplasm Status_WITH TUMOR",',
    '"Primary Therapy Outcome Success Type_Progressive Disease",',
]


def apply_edits(nb):
    log = []
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        src = cell.source
        if "drive.mount(" in src:
            src = DOWNLOAD_CELL
            log.append("replaced Google Drive mount with data download")
        for old, new in PATHS:
            if old in src:
                src = src.replace(old, new)
                log.append(f"path -> {new}")
        if "LEAKAGE_COLUMNS" not in src:
            m = re.search(r"X = df_cleaned\.drop\(columns=\[.*?\]\)", src, flags=re.S)
            if m and "Survival_Binary" in m.group(0):
                src = src[: m.end()] + LEAKAGE_BLOCK + src[m.end():]
                log.append("inserted leakage column removal")
        if "input_features = [" in src:
            for item in LEAKED_INPUTS:
                if item in src:
                    src = re.sub(r"[ \t]*" + re.escape(item) + r"[ \t]*\n?", "", src)
                    log.append(f"removed leaked input {item}")
        cell.source = src
    return log


def summarise(nb):
    lines, errors = [], []
    pat = re.compile(r"^(Accuracy|AUC|Best|Feature columns|\s+accuracy|\s+macro avg)", re.I)
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        for out in cell.get("outputs", []):
            if out.output_type == "error":
                errors.append(f"cell {i}: {out.ename}: {out.evalue}")
            text = out.get("text", "") if out.output_type == "stream" else ""
            for line in text.splitlines():
                if pat.search(line):
                    lines.append(f"cell {i}: {line.rstrip()}")
    return lines, errors


def main():
    nb = nbformat.read(NOTEBOOK, as_version=4)
    for entry in apply_edits(nb):
        print("EDIT:", entry)
    if "--no-run" in sys.argv:
        nbformat.write(nb, NOTEBOOK)
        return
    from nbclient import NotebookClient

    NotebookClient(nb, timeout=None, kernel_name="python3", allow_errors=True).execute()
    lines, errors = summarise(nb)
    print("\n".join(lines))
    with open("RESULTS.md", "w") as fh:
        fh.write("# Results from the latest notebook run\n\n```\n" + "\n".join(lines) + "\n```\n")
        if errors:
            fh.write("\n## Cells that raised errors\n\n```\n" + "\n".join(errors) + "\n```\n")
    if errors:
        print("ERRORS:\n" + "\n".join(errors))
    nbformat.write(nb, NOTEBOOK)
    with open("run_errors.txt", "w") as fh:
        fh.write("\n".join(errors))


if __name__ == "__main__":
    main()
