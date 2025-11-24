import polars as pl
import pandas as pd
from typing import List


input_path = r'C:\Users\fazin\OneDrive\Documents\Nisio\Cargas Pendentes\CargasPendentes 24-25\verificaPendentes.xlsx'
out_path = r'C:\Users\fazin\OneDrive\Documents\Nisio\Cargas Pendentes\CargasPendentes 24-25\11 - Novembro\valores_restantes.xlsx'

df_pd = pd.read_excel(input_path)
classifica = pl.from_pandas(df_pd)

def remove_matching_values(df: pl.DataFrame, col1: str, col2: str) -> pl.DataFrame:
    vals1 = set(df[col1].drop_nulls().to_list())
    vals2 = set(df[col2].drop_nulls().to_list())
    comuns: List = list(vals1.intersection(vals2))
    if not comuns:
        return df
    return df.with_columns([
        pl.when(pl.col(col1).is_in(comuns)).then(pl.lit(None)).otherwise(pl.col(col1)).alias(col1),
        pl.when(pl.col(col2).is_in(comuns)).then(pl.lit(None)).otherwise(pl.col(col2)).alias(col2)
    ])

classifica = remove_matching_values(classifica, 'Bordaduras', 'Fardão')

classifica.to_pandas().to_excel(out_path, index=False)

classifica = pl.from_pandas(pd.read_excel(out_path))

classifica = remove_matching_values(classifica, 'Vinculadas', 'Fardão')

def remove_nan_and_shift_up(df: pl.DataFrame, coluna: str) -> pl.DataFrame:
    non_nulls = df[coluna].drop_nulls().to_list()
    pad = [None] * (df.height - len(non_nulls))
    nova_lista = non_nulls + pad  
    return df.with_columns(pl.Series(nova_lista).alias(coluna))

classifica = remove_nan_and_shift_up(classifica, 'Fardão')

classifica.to_pandas().to_excel(out_path, index=False)

print("Valores restantes salvos em 'valores_restantes.xlsx'")