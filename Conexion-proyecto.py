import mysql.connector
from mysql.connector import connect, Error
import pandas as pd

# Función para conectar con la base de datos
def conectar():
    try:
        dbConexion = connect(host="localhost", user="root", password="quesadillas1", database="datos")
        cursor = dbConexion.cursor()
        print("Conexión establecida", "\n")
        return dbConexion, cursor
    except Error as e:
        print(e)
        return None, None

def crear_tabla_amazon():
    dbConexion, cursor = conectar()
    try:
        crear_tabla_query = """
        CREATE TABLE IF NOT EXISTS amazon (
            nombre VARCHAR(255),
            rating VARCHAR(255),
            precio VARCHAR(255),
            fecha_entrega VARCHAR(255)
        )
        """
        cursor.execute(crear_tabla_query)
        dbConexion.commit()
        print("Tabla amazon creada")
    except Error as e:
        print(e)

def crear_tabla_mercado():
    dbConexion, cursor = conectar()
    try:
        crear_tabla_query = """
        CREATE TABLE IF NOT EXISTS mercado_libre (
            nombre VARCHAR(255),
            precio VARCHAR(255),
            rating VARCHAR(255)
        )
        """
        cursor.execute(crear_tabla_query)
        dbConexion.commit()
        print("Tabla mercado libre creada")
    except Error as e:
        print(e)

def crear_tabla_productos_mejor_calificados_amazon():
    dbConexion, cursor = conectar()
    try:
        crear_tabla_query = """
        CREATE TABLE IF NOT EXISTS productos_mejor_calificados_amazon (
            nombre VARCHAR(255),
            rating VARCHAR(255)
        )
        """
        cursor.execute(crear_tabla_query)
        dbConexion.commit()
        print("Tabla productos mejor calificados creada")
    except Error as e:
        print(e)
def insertar_datos_desde_csv(archivo_csv):
    dbConexion, cursor = conectar()
    try:
        # Leer el archivo CSV
        df = pd.read_csv(archivo_csv)

        # Iterar sobre las filas y agregarlas a la base de datos
        for index, row in df.iterrows():
            # Verificar si hay valores NaN en la fila
            if row.notna().all():
                insertar_datos_query = """
                INSERT INTO amazon (nombre, rating, precio, fecha_entrega)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insertar_datos_query, (row["nombre"], row["rating"], row["precio"], row["fecha_entrega"]))

        dbConexion.commit()
        print("Datos insertados")
    except Error as e:
        print(e)

def crear_tabla_productos_mejor_calificados_mercado():
    dbConexion, cursor = conectar()
    try:
        crear_tabla_query = """
        CREATE TABLE IF NOT EXISTS productos_mejor_calificados_mercado (
            nombre VARCHAR(255),
            rating VARCHAR(255)
        )
        """
        cursor.execute(crear_tabla_query)
        dbConexion.commit()
        print("Tabla productos mejor calificados de mercado libre creada")
    except Error as e:
        print(e)
    finally:
        cursor.close()
        dbConexion.close()

def insertar_datos_desde_csv_2(archivo_csv2):
    dbConexion, cursor = conectar()
    try:
        # Leer el archivo CSV
        df = pd.read_csv(archivo_csv2)

        # Iterar sobre las filas y agregarlas a la base de datos
        for index, row in df.iterrows():
            # Verificar si hay valores NaN en la fila
            if row.notna().all():
                insertar_datos_query = """
                INSERT INTO mercado_libre (nombre, precio, rating)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insertar_datos_query, (row["nombre"], row["precio"], row["rating"]))

        dbConexion.commit()
        print("Datos insertados en tabla mercado libre")
    except Error as e:
        print(e)


def insertar_datos_desde_csv_3(archivo_csv):
    dbConexion, cursor = conectar()
    try:
        # Leer el archivo CSV
        df = pd.read_csv(archivo_csv)

        # Iterar sobre las filas y agregarlas a la base de datos
        for index, row in df.iterrows():
            # Verificar si hay valores NaN en la fila
            if row.notna().all():
                insertar_datos_query = """
                INSERT INTO productos_mejor_calificados_amazon(nombre, rating)
                VALUES (%s, %s)
                """
                cursor.execute(insertar_datos_query, (row["nombre"], row["rating"]))

        dbConexion.commit()
        print("Datos insertados en productos mas pedidos")
    except Error as e:
        print(e)

def insertar_datos_desde_csv_4(archivo_csv2):
    dbConexion, cursor = conectar()
    try:
        # Leer el archivo CSV
        df = pd.read_csv(archivo_csv2)

        # Iterar sobre las filas y agregarlas a la base de datos
        for index, row in df.iterrows():
            # Verificar si hay valores NaN en la fila
            if row.notna().all():
                insertar_datos_query = """
                INSERT INTO productos_mejor_calificados_mercado(nombre, rating)
                VALUES (%s, %s)
                """
                cursor.execute(insertar_datos_query, (row["nombre"], row["rating"]))

        dbConexion.commit()
        print("Datos insertados en productos mejor calificados mercado libre")
    except Error as e:
        print(e)
    finally:
        cursor.close()
        dbConexion.close()
def mostrar_top_10_mejor_calificados():
    # Conectar a la base de datos
    dbConexion, cursor = conectar()
    try:
        # Consulta para obtener los top 10 productos mejor calificados
        obtener_datos_query = """
        SELECT nombre, rating FROM productos_mejor_calificados_amazon
        ORDER BY rating DESC
        LIMIT 10
        """
        cursor.execute(obtener_datos_query)
        resultados = cursor.fetchall()

        # Convertir los resultados a un DataFrame de pandas para mostrar
        df = pd.DataFrame(resultados, columns=['nombre', 'rating'])
        print("Top 5 productos mejor calificados (de mayor a menor):")
        print(df)
    except Error as e:
        print(e)


def mostrar_top_10_mejor_calificados_mercado():
    # Conectar a la base de datos
    dbConexion, cursor = conectar()
    try:
        # Consulta para obtener los top 10 productos mejor calificados de mercado libre
        obtener_datos_query = """
        SELECT nombre, rating FROM productos_mejor_calificados_mercado
        ORDER BY rating DESC
        LIMIT 10
        """
        cursor.execute(obtener_datos_query)
        resultados = cursor.fetchall()

        # Convertir los resultados a un DataFrame de pandas para mostrar
        df = pd.DataFrame(resultados, columns=['nombre', 'rating'])
        print("Top 10 productos mejor calificados en Mercado Libre (de mayor a menor):")
        print(df)
    except Error as e:
        print(e)
    finally:
        cursor.close()
        dbConexion.close()



def crear_tabla_top_10_mejor_calificados_mercado():
    dbConexion, cursor = conectar()
    try:
        crear_tabla_query = """
        CREATE TABLE IF NOT EXISTS top_10_mejor_calificados_mercado (
            nombre VARCHAR(255),
            rating VARCHAR(255)
        )
        """
        cursor.execute(crear_tabla_query)
        dbConexion.commit()
        print("Tabla top_10_mejor_calificados_mercado creada")
    except Error as e:
        print(e)
    finally:
        cursor.close()
        dbConexion.close()


def top_10_mejor_calificados_amazon():
    dbConexion, cursor = conectar()
    try:
        crear_tabla_query = """
        CREATE TABLE IF NOT EXISTS top_10_mejor_calificados_amazon (
            nombre VARCHAR(255),
            rating varchar(255)
        )
        """
        cursor.execute(crear_tabla_query)
        dbConexion.commit()
        print("Tabla top_10_mejor_calificados creada")
    except Error as e:
        print(e)
    finally:
        cursor.close()
        dbConexion.close()

def insertar_10_mejor_calificados_mercado():
    dbConexion, cursor = conectar()
    try:
        # Consulta para obtener los top 10 productos mejor calificados de mercado libre
        obtener_datos_query = """
        SELECT nombre, rating FROM productos_mejor_calificados_mercado
        ORDER BY rating DESC
        LIMIT 10
        """
        cursor.execute(obtener_datos_query)
        resultados = cursor.fetchall()

        # Insertar los datos en la nueva tabla
        insertar_datos_query = """
        INSERT INTO top_10_mejor_calificados_mercado (nombre, rating)
        VALUES (%s, %s)
        """
        cursor.executemany(insertar_datos_query, resultados)
        dbConexion.commit()
        print("Top 10 productos mejor calificados de mercado libre insertados")
    except Error as e:
        print(e)
    finally:
        cursor.close()
        dbConexion.close()
def insertar_10_mejor_calificados_amazon():
    dbConexion, cursor = conectar()
    try:
        # Consulta para obtener los top 5 productos mejor calificados
        obtener_datos_query = """
        SELECT nombre, rating FROM productos_mejor_calificados_amazon
        ORDER BY rating DESC
        LIMIT 10
        """
        cursor.execute(obtener_datos_query)
        resultados = cursor.fetchall()

        # Insertar los datos en la nueva tabla
        insertar_datos_query = """
        INSERT INTO top_10_mejor_calificados_amazon (nombre, rating)
        VALUES (%s, %s)
        """
        cursor.executemany(insertar_datos_query, resultados)
        dbConexion.commit()
        print("Top 5 productos mejor calificados amazon insertados")
    except Error as e:
        print(e)
    finally:
        cursor.close()
        dbConexion.close()

def crear_tabla_comparativa_precios():
    dbConexion, cursor = conectar()
    try:
        crear_tabla_query = """
        CREATE TABLE IF NOT EXISTS comparativa_precios (
            plataforma VARCHAR(255),
            promedio_precio decimal(10,2)
        )
        """
        cursor.execute(crear_tabla_query)
        dbConexion.commit()
        print("Tabla comparativa_precios creada")
    except Error as e:
        print(e)


def calcular_e_insertar_promedios():
    dbConexion, cursor = conectar()
    try:
        # Calcular promedio de precios en Amazon
        cursor.execute("SELECT AVG(CAST(precio AS DECIMAL(10, 2))) FROM amazon")
        promedio_amazon = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(CAST(REPLACE(precio, '$', '') AS DECIMAL(10, 2))) FROM mercado_libre")
        promedio_mercado = cursor.fetchone()[0]

        # Insertar los promedios en la tabla comparativa
        insertar_datos_query = """
        INSERT INTO comparativa_precios (plataforma, promedio_precio)
        VALUES (%s, %s)
        """
        cursor.executemany(insertar_datos_query, [("Amazon", promedio_amazon), ("Mercado Libre", promedio_mercado)])
        dbConexion.commit()
        print("Promedios de precios insertados en tabla comparativa")
    except Error as e:
        print(e)


if __name__ == "__main__":
    archivo_csv_amazon = "C:/Users/abelc/PycharmProjects/Programacion Para La Extraccion De Datos/Datasets/productos_amazon2.csv"
    archivo_csv_mercado = "C:/Users/abelc/PycharmProjects/Programacion Para La Extraccion De Datos/Datasets/productos_mercadolibre.csv"

    # Creación de tablas para Amazon
    crear_tabla_amazon()
    crear_tabla_productos_mejor_calificados_amazon()
    top_10_mejor_calificados_amazon()

    # Insertar datos en tablas de Amazon
    insertar_datos_desde_csv(archivo_csv_amazon)
    insertar_datos_desde_csv_3(archivo_csv_amazon)

    # Mostrar y almacenar los top 10 productos mejor calificados de Amazon
    mostrar_top_10_mejor_calificados()
    insertar_10_mejor_calificados_amazon()

    # Creación de tablas para Mercado Libre
    crear_tabla_mercado()
    crear_tabla_productos_mejor_calificados_mercado()
    crear_tabla_top_10_mejor_calificados_mercado()

    # Insertar datos en tablas de Mercado Libre
    insertar_datos_desde_csv_2(archivo_csv_mercado)
    insertar_datos_desde_csv_4(archivo_csv_mercado)

    # Mostrar y almacenar los top 10 productos mejor calificados de Mercado Libre
    mostrar_top_10_mejor_calificados_mercado()
    insertar_10_mejor_calificados_mercado()

    crear_tabla_comparativa_precios()
    calcular_e_insertar_promedios()
