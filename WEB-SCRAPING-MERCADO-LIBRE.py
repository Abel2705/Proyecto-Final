import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def crear_navegador(url):
    driver = ChromeDriverManager()
    s = Service(driver.install())
    opc = Options()
    opc.add_argument("--window-size=1500,1200")
    navegador = webdriver.Chrome(service=s, options=opc)
    navegador.get(url)
    return navegador


def buscar_producto_mercadolibre(producto, cantidad_paginas):
    navegador2 = crear_navegador("https://www.mercadolibre.com.mx/")

    buscador2 = navegador2.find_element(By.ID, "cb1-edit")
    buscador2.send_keys(producto)
    time.sleep(1)

    botonbuscar = navegador2.find_element(By.CLASS_NAME, "nav-search-btn")
    botonbuscar.click()
    time.sleep(1)

    datos2 = {"nombre": [], "precio": [], "rating": []}

    for i in range(cantidad_paginas):
        soup2 = BeautifulSoup(navegador2.page_source, "html5lib")
        nombres = soup2.find_all("h2", class_="ui-search-item__title")
        ratings = soup2.find_all("span", class_="andes-visually-hidden")
        precios = soup2.find_all("span", class_="andes-money-amount")

        for nombre, precio, rating, in zip(nombres, precios, ratings):
            datos2["nombre"].append(nombre.text)
            datos2["precio"].append(precio.text)
            datos2["rating"].append(rating.text)

        try:
            boton_siguiente = WebDriverWait(navegador2, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "andes-pagination__button--next"))
            )
            # Desplazar la página para que el botón "Siguiente" esté dentro del área visible
            navegador2.execute_script("arguments[0].scrollIntoView();", boton_siguiente)

            # Hacer clic en el botón "Siguiente"
            boton_siguiente.click()
        except:
            print("No se pudo hacer clic en el botón 'Siguiente'.")
            time.sleep(1)

    df = pd.DataFrame(datos2)

    # filtrar los datos
    df1 = df[~df['rating'].str.contains("Más relevantes|,")]
    df2 = df1.dropna()  # eliminar filas con valores vacíos
    df2.to_csv("C:/Users/abelc/PycharmProjects/Programacion Para La Extraccion De Datos/Datasets/productos_mercadolibre.csv")


if __name__ == "__main__":
    buscar_producto_mercadolibre("tenis adidas", 4)