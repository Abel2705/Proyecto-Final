import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

def crear_navegador(url):
    driver = ChromeDriverManager()
    s = Service(driver.install())
    opc = Options()
    opc.add_argument("--window-size=1500,1200")
    navegador = webdriver.Chrome(service=s, options=opc)
    navegador.get(url)
    return navegador

def buscar_producto_amazon(producto, cantidad_paginas):

    navegador=crear_navegador("https://www.amazon.com.mx/")
    time.sleep(20)

    buscador = navegador.find_element(By.ID, "twotabsearchtextbox")
    buscador.send_keys(producto)
    time.sleep(3)
    boton_buscar = navegador.find_element(By.ID, "nav-search-submit-button")
    boton_buscar.click()
    time.sleep(3)

    datos = {"nombre":[],"precio":[],"rating":[],"fecha_entrega":[]}

    for i in range(cantidad_paginas):
        soup = BeautifulSoup(navegador.page_source, "html5lib")

        nombres = soup.find_all("span", class_="a-size-base-plus a-color-base a-text-normal")
        ratings = soup.find_all("span", class_="a-icon-alt")
        precios = soup.find_all("span", class_="a-price-whole")
        fechas_entrega = soup.find_all("span", class_="a-color-base a-text-bold")
        for nombre, precio, rating, fecha_entrega in zip(nombres, precios, ratings, fechas_entrega):
            datos["nombre"].append(nombre.text)
            datos["rating"].append(rating.text)
            datos["precio"].append(precio.text)
            datos["fecha_entrega"].append(fecha_entrega.text)
        boton_siguiente = navegador.find_element(By.LINK_TEXT, "Siguiente")
        boton_siguiente.click()
        time.sleep(2)

    df = pd.DataFrame(datos)
    # filtrar los datos
    df1 = df[~df['rating'].str.contains("Más relevantes|Previous page|Next page|,")]
    df2 = df1.dropna()  # eliminar filas con valores vacíos
    df2.to_csv("C:/Users/abelc/PycharmProjects/Programacion Para La Extraccion De Datos/Datasets/productos_amazon2.csv")




if __name__ == "__main__":
    buscar_producto_amazon("tenis adidas", 4)
