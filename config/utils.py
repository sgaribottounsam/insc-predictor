import pandas as pd


def encontrar_header_row(file_path, target_columns, max_rows=20):

    """
    Encuentra la fila del encabezado en un archivo Excel.
    
    Parámetros:
    file_path (str): Ruta al archivo Excel.
    max_rows (int): Número máximo de filas a revisar para encontrar el encabezado.
    
    Retorna:
    int: Índice de la fila del encabezado si se encuentra, de lo contrario -1.
    """
    try:
        df_preview = pd.read_excel(file_path, nrows=max_rows, header=None)
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        return -1
    target_set = set(target_columns)
    for idx, row in df_preview.iterrows():
        row_values = set(str(v).strip() for v in row if v)

        if target_set.issubset(row_values):
            print(f"Encabezado encontrado en la fila: {idx}")
            return idx
        
    raise ValueError(f"No se encontró el encabezado en las primeras filas especificadas para las columnas {target_columns}.")

### TEST
"""
COLUMNAS_CLAVE = ["Actividad"]
archivo_test = "data/crudos/total_insc_cursadas_2025_2.xlsx"
fila_header = encontrar_header_row(archivo_test, max_rows=20, target_columns=COLUMNAS_CLAVE)
print(f"Fila del encabezado encontrada en: {fila_header}")
"""
