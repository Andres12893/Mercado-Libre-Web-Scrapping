from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime


def scrape_mercadolibre(url):
    # Obtener el HTML
    pedido_obtenido = requests.get(url)
    html_obtenido = pedido_obtenido.text

    # Parsear el HTML
    soup = BeautifulSoup(html_obtenido, "html.parser")

    data = []

    if 'lego' in url:
        for producto in soup.find_all('div', class_="andes-card ui-search-result ui-search-result--core andes-card--flat andes-card--padding-16"):
            titulo = producto.find('h2', class_="ui-search-item__title").text
            precio = producto.find('span', class_='andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript').text
            cuotas = producto.find('div', class_='ui-search-item__group__element ui-search-installments ui-search-color--BLACK')
            ubicacion = None
            date = datetime.now().strftime("%Y-%m-%d")
            data.append([titulo, precio, cuotas, date, ubicacion])
    else:  # Otro tipo de página
        for producto in soup.find_all('div', class_="ui-search-layout ui-search-layout--grid"):
            titulo_elementos = producto.find_all('h2', class_="ui-search-item__title")
            precio_elementos = producto.find_all('span', class_= "andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript")
            atributos_elementos = producto.find_all('ul', class_="ui-search-card-attributes ui-search-item__group__element")
            ubicacion_elementos = producto.find_all('span', class_ ='ui-search-item__group__element ui-search-item__location')
            for titulo, precio, atributos, ubicacion in zip(titulo_elementos, precio_elementos, atributos_elementos, ubicacion_elementos):
                titulo_texto = titulo.text
                precio_texto = precio.text
                atributos_texto = atributos.text
                year_texto = None
                kilometraje_texto = None
                lines = atributos_texto.strip().split('\n')
                for line in lines:
                    if line.strip().isdigit() and len(line.strip()) == 4:
                        year_texto = line.strip()  
                        break  # Salir del bucle una vez que se encuentra el año
                # Extraer el kilometraje solo si hay algún valor
                if 'Km' in atributos_texto:
                    kilometraje_texto = atributos_texto.split('Km')[0].strip()
                ubicacion_texto = ubicacion.text if ubicacion else None
                date = datetime.now().strftime("%Y-%m-%d")
                # Eliminar los primeros 4 caracteres de kilometraje y asignarlos a year
                if year_texto is None and kilometraje_texto:
                    year_texto = kilometraje_texto[:4]
                    kilometraje_texto = kilometraje_texto[4:].strip()
                data.append([titulo_texto, precio_texto, date, year_texto, kilometraje_texto, ubicacion_texto])

    return data



"""
Ideas: Puedo hacer un for, que vaya generando urls
"""

# Lista de URLs a raspar
urls = [
    #'https://listado.mercadolibre.com.ar/lego-bonzai#D[A:lego%20bonzai]',
    'https://autos.mercadolibre.com.ar/ford/ford-ecosport-2016_NoIndex_True',
    'https://autos.mercadolibre.com.ar/ford/ford-ecosport-2016_Desde_49_NoIndex_True',
    'https://autos.mercadolibre.com.ar/ford/ford-ecosport-2016_Desde_97_NoIndex_True',
    'https://autos.mercadolibre.com.ar/volkswagen/gol/gol-power_NoIndex_True',
    'https://autos.mercadolibre.com.ar/volkswagen/gol/gol-power_Desde_49_NoIndex_True'

    # Agrega aquí más URLs si lo deseas
]

all_data = []
for url in urls:
    data = scrape_mercadolibre(url)
    all_data.extend(data)


# Crear DataFrame
df = pd.DataFrame(all_data, columns=['titulo', 'precio','date','year','kilometraje', 'ubicacion'])

print(df)
