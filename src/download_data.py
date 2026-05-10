"""
Download the French Motor TPL dataset from OpenML and save as CSV.

Run once to populate the data/ folder. The dataset has ~680k policies.
"""

from pathlib import Path
from sklearn.datasets import fetch_openml

# Pasta de destino
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

print("Downloading French Motor TPL frequency dataset (freMTPL2freq)...")
freq = fetch_openml(data_id=41214, as_frame=True, parser="auto")
freq_df = freq.frame
freq_path = DATA_DIR / "freMTPL2freq.csv"
freq_df.to_csv(freq_path, index=False)
print(f"  Saved: {freq_path} ({len(freq_df):,} rows)")

print("\nDownloading French Motor TPL severity dataset (freMTPL2sev)...")
sev = fetch_openml(data_id=41215, as_frame=True, parser="auto")
sev_df = sev.frame
sev_path = DATA_DIR / "freMTPL2sev.csv"
sev_df.to_csv(sev_path, index=False)
print(f"  Saved: {sev_path} ({len(sev_df):,} rows)")

print("\nDone! Both datasets are now in data/ folder.")