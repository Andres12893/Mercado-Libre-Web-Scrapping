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
            ubicacion_elementos = producto.find_all('span', class_ ='ui-search-item__group__element ui-search-item__location')
            for titulo, precio, ubicacion in zip(titulo_elementos, precio_elementos, ubicacion_elementos):
                titulo = titulo.text
                precio = precio.text
                ubicacion = ubicacion.text if ubicacion else None
                date = datetime.now().strftime("%Y-%m-%d")
                cuotas = None
                data.append([titulo, precio, cuotas, date, ubicacion])

    return data


# Lista de URLs a raspar
urls = [
    'https://listado.mercadolibre.com.ar/lego-bonzai#D[A:lego%20bonzai]',
    'https://autos.mercadolibre.com.ar/ford/ford-ecosport-2016_NoIndex_True',
    'https://autos.mercadolibre.com.ar/ford/ford-ecosport-2016_Desde_49_NoIndex_True',
    'https://autos.mercadolibre.com.ar/ford/ford-ecosport-2016_Desde_97_NoIndex_True'
    # Agrega aquí más URLs si lo deseas
]

all_data = []
for url in urls:
    data = scrape_mercadolibre(url)
    all_data.extend(data)


# Crear DataFrame
df = pd.DataFrame(all_data, columns=['titulo', 'precio', 'cuotas', 'date', 'ubicacion'])

# Filtrar por títulos que contengan 'Bons'
# df = df[df['titulo'].str.contains('Bons')]

print(df)
