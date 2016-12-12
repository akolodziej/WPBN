import os
import os.path as op
from itertools import product

import numpy as np
import pandas as pd


# wczytujemy pliki
folder_in = os.getcwd()
files = [f for f in os.listdir(folder_in) if f.endswith('lsx')
         and not f.startswith('~$')]
dfs = [pd.read_excel(op.join(folder_in, f)) for f in files]

# sprawdzamy wymiary
n_rows = [df.shape[0] for df in dfs]
n_columns = [df.shape[1] for df in dfs]
prod_rows = np.prod(n_rows)
sum_columns = np.sum(n_columns)

# nazwy wszystkich kolumn
col_names = list()
for df in dfs:
    col_names.extend(df.columns)

# pusty dataframe do wypelnienia
out_df = pd.DataFrame(index=range(prod_rows), columns=col_names)

# wszystkie kombinacje indeksow:
indices = [range(r) for r in n_rows]
combinations = product(*indices)

# idziemy przez kombinacje
for irow, cmb in enumerate(combinations):
    icol = 0
    # idziemy przez kombinowane dataframe'y
    for df_idx in range(len(cmb)):
        # idziemy przez kolejne kolumny
        for from_col in range(n_columns[df_idx]):
            out_df.iloc[irow, icol] = dfs[df_idx].iloc[cmb[df_idx], from_col]
            icol += 1

# zapisujemy:
out_df.to_excel('output.xlsx')
print('gotowe!')
