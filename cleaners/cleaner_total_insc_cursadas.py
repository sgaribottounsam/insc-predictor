import pandas as pd
import numpy as np
import unicodedata
import re

def to_snake_case(name):
    norm_str = unicodedata.normalize('NFD', name)

    replacements = {
    'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
    'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
    'ñ': 'n', 'Ñ': 'N', '.': '', ',': '', '-': '_', '/': '_',
    '__': '_',
    }
    cleaned_str = ''.join(replacements.get(c, c) for c in norm_str if unicodedata.category(c) != 'Mn')
    #print(cleaned_str)  # Output: Ano de evacuacion
    cleaned_str = re.sub(r'\s+', '_', cleaned_str).lower()
    
    return cleaned_str

def cleaner_total_insc_cursadas(df, periodo):
    filas_problem = df[df['Actividad'].isna()]
    df_limpio = df.drop(filas_problem.index) # Borra filas nulas

    headers_repetidos = df_limpio[df['Actividad'] == 'Actividad']
    df_limpio = df_limpio.drop(headers_repetidos.index) # Borra filas repetidas de headers

    df_limpio.columns = df_limpio.columns.to_series().apply(to_snake_case)
    df_limpio['periodo'] = periodo
    return df_limpio

# Importar el DF y limpiarlo
"""df = pd.read_excel('data/crudos/total_insc_cursadas_2025_2.xlsx', header=3)
df_limpio = cleaner_total_insc_cursadas(df)
df_limpio.info()"""