from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "Data" / "preprocessedDataset.csv"

df = pd.read_csv(DATA_PATH)
df["engine_group"] = pd.cut(
    df["engine"],
    bins=[0, 1000, 1500, 2000, 2500, 3000, float("inf")],
    labels=["<1000","1000-1499","1500-1999","2000-2499","2500-2999","3000+"])

grouped = (
    df.groupby(["engine_group"],observed=True)["mileage"].agg(["min", "max","count"])
)

