"""
Squash function – calculates unstratified occurrence numbers (Ns).
"""
import pandas as pd
import numpy as np


def squash(df: pd.DataFrame, on: str="type") -> pd.DataFrame:
    if on in ("type", "manu", "name", "lot", "route", "site"):
        return pd.pivot_table(df,
                       values="VAERS_ID",
                       index="SYMPTOM",
                       columns=f"VAX_{on.upper()}",
                       aggfunc=np.count_nonzero,
                       fill_value=0)
    else:
        raise ValueError