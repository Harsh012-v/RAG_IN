import pandas as pd
import os
from typing import Optional

def load_data(path: str = "data/tech_terms.csv") -> pd.DataFrame:
    return pd.read_csv(path)




load_data()