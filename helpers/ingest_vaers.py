"""
Helpers for VAERS ingestion.
"""
import numpy as np
import pandas as pd


def destructure_symptoms(symptoms: pd.DataFrame) -> pd.DataFrame:
    """
    Destructures a VAERS symptoms data file to yield one symptom per row.

    :param symptoms: Pandas data frame of a VAERS symptoms file
    :return: Pandas data frame with one symptom per row
    """

    _res = pd.melt(symptoms,
                   id_vars="VAERS_ID",
                   value_vars=(f"SYMPTOM{i}" for i in range(1, 6))).drop("variable", axis=1)

    _res.columns = ("VAERS_ID", "SYMPTOM")

    return _res


def ingest_files(data: str, symptoms: str, vax: str) -> pd.DataFrame:
    """
    Fully destructured file ingestion and joining for VAERS data, using a Cartesian cross join.

    :param data: path to DATA file
    :param symptoms: path to SYMPTOMS file
    :param vax: path to VAX file
    :return: Pandas data frame of Cartesian joined results
    """
    data, symptoms, vax = pd.read_csv(data), pd.read_csv(symptoms), pd.read_csv(vax)

    symptoms = destructure_symptoms(symptoms)

    _res = symptoms.merge(vax, how="inner", on="VAERS_ID").merge(data, on="VAERS_ID")
    return _res[pd.isnull(_res.SYMPTOM) == False]

def ingest_year(year: int, path: str = "data/") -> pd.DataFrame:
    if year >= 1990:
        return ingest_files(data=f"{path}/{year}VAERSDATA.csv",
                            symptoms=f"{path}/{year}VAERSSYMPTOMS.csv",
                            vax=f"{path}/{year}VAERSVAX.csv")
    else:
        raise ValueError

def ingest(*years, **kwargs) -> pd.DataFrame:
    return pd.concat(ingest_year(year, path=kwargs.get("path", "")) for year in years)
