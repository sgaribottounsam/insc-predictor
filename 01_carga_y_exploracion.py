import pandas as pd

ruta = "./data/crudos/inscripciones_cursadas_2025_1.xlsx"

df = pd.read_excel(ruta, header = 5)

#print(df.head())
#df.info()
#print(df.describe())

# Recuento de aceptados por comisión

df_aceptados = df[df["Estado Insc."] == "Aceptada"]
conteo_aceptados = df_aceptados["Comisión"].value_counts()
print(conteo_aceptados)