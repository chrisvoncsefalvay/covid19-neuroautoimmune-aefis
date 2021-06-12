"""
Various reporting metrics. These typically need a squashed data frame.
"""

import pandas as pd
import numpy as np

def prr(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the proportional reporting ratio (PRR), calculated as the number of event i for drug j divided by the
    number of event i for all drugs.

    :param df: squashed VAERS data frame
    :return: data frame of PRRs
    """
    return df.div(df.sum(axis=1), axis=0)

def ror(df: pd.DataFrame) -> pd.DataFrame: