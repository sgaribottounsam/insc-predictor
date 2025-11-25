import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

#carga de secretos del archivo .env
load_dotenv()

#Variables de entorno

db_user = os.environ.get("PG_USER")
db_password = os.environ.get("PG_PASSWORD")
db_host = os.environ.get("PG_HOST", "localhost")
db_port = os.environ.get("PG_PORT", "5432")
db_name = os.environ.get("PG_DBNAME")

#print(f"Intentando conectar a la base de datos {db_name} en {db_host}:{db_port} como usuario {db_user}")


# Validación de las variables de entorno
if not all([db_user, db_password, db_host, db_port, db_name]):
    raise ValueError("Faltan variables de entorno para la conexión a la base de datos.")

#URL de la conexión
connection_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

#creación del engine
try:
    engine = create_engine(connection_url)
    print("Conexión a la base de datos exitosa.")
    #Prueba
    #with engine.connect() as connection:
        #print("Prueba de conexión exitosa.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    engine = None