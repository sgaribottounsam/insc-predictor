import pandas as pd
from sqlalchemy import create_engine
import sys
import os
import argparse
from pathlib import Path

from cleaners.cleaner_total_insc_cursadas import cleaner_total_insc_cursadas
from config.database import engine
from config.utils import encontrar_header_row


#Procesamiento individual
def procesar_un_archivo(file_path, periodo):
    print(f"Procesando -> {file_path.name} al periodo: {periodo}")
    COLUMNAS_CLAVE = ["Código", "Actividad", "Comisión"]
    #archivo = "data/crudos/total_insc_cursadas_2025_2.xlsx"
    try:
        fila_header = encontrar_header_row(file_path, max_rows=20, target_columns=COLUMNAS_CLAVE)
        df_crudo = pd.read_excel(file_path, header = fila_header)
        
        df_limpio = cleaner_total_insc_cursadas(df_crudo)
        df_limpio['periodo'] = periodo

        return df_limpio
    except Exception as e:
        print(f"Error procesando -> {file_path.name} al periodo: {periodo}: {e}  ")
        return None
    
    
def extraer_periodo(archivo):
        periodo = archivo.stem.removeprefix('total_insc_cursadas_').replace('_', '-')
        return periodo

# Función principal para cargar datos y parsearlos desde línea de comandos
'''def main():
    parser = argparse.ArgumentParser(description="Cargar datos de total_insc_cursadas a la base de datos.")
    parser.add_argument("-f", "--file", type=str, default="data/crudos/total_insc_cursadas_2025_2.xlsx", help="Ruta al archivo Excel de entrada.")
    parser.add_argument("-p", "--periodo", type=str, default="2025-2", help="Período académico de los datos.")
    args = parser.parse_args()

    file_path = args.file
    periodo = args.periodo

    #limpiada de datos
    COLUMNAS_CLAVE = ["Código", "Actividad", "Comisión"]
    #archivo = "data/crudos/total_insc_cursadas_2025_2.xlsx"
    fila_header = encontrar_header_row(file_path, max_rows=20, target_columns=COLUMNAS_CLAVE)
    df_crudo = pd.read_excel(file_path, header = fila_header)

    df_cursadas = cleaner_total_insc_cursadas(df_crudo, periodo)

    NOMBRE_TABLA = "total_insc_cursadas"

    try:
        print("Iniciando carga de datos para la tabla:", NOMBRE_TABLA)

        df_cursadas.to_sql(NOMBRE_TABLA, con=engine, if_exists='replace', index=False)
        print("Carga de datos completada exitosamente.")
    except Exception as e:
        print(f"Error durante la carga de datos: {e}")
        sys.exit(1)
    # Verificación de la carga


    df = pd.read_sql(f"SELECT * FROM {NOMBRE_TABLA} LIMIT 5;", con=engine)

    print()'''

def main():
    directorio_crudos = Path('../data/crudos/')
    directorio_crudos = Path('../data/crudos/')
    
    patron = "total_insc_cursadas_*.xlsx"
    lista_reales = list(directorio_crudos.glob(patron))

    if not lista_reales:
        print("no hay archivos para procesar")
        return
    
    print(f"Se encontraron {len(lista_reales)} archivos para cargar")

    ###IMPORTACIÓN A LA BD

    cantidad_hechos = 0
    nombre_tabla = "total_insc_cursadas"

    for archivo in lista_reales:
         periodo = extraer_periodo(archivo)
         df_para_cargar = procesar_un_archivo(archivo, periodo)

         if df_para_cargar is not None:
            try:
                df_para_cargar.to_sql(
                    nombre_tabla,
                    con = engine,
                    if_exists='replace',
                    index = False
                )
                cantidad_hechos += 1
                print(f"Cargado exitosamente ({len(df_para_cargar)} filas).")
            except Exception as e:
                print(f"Error al guardar en SQL: {e}")
        
    print(f"proceso finalizado, se cargaron {cantidad_hechos} ")




# Si se aejecuta, corre el main
if __name__ == "__main__":
    main()