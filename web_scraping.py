import requests
import pandas as pd
import boto3
from datetime import datetime
from bs4 import BeautifulSoup
from io import StringIO
import logging

bucket_name = 'de-mercadolibre-scrap'
date = datetime.now().date()
file_key = f'data_{date}'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_html(url):
    """
    Realiza una solicitud HTTP GET a la URL proporcionada y devuelve el HTML de la página.
    """
    response = requests.get(url)
    return response.text

def extract_lego_data(soup):
    """
    Extrae los datos de la página de productos LEGO.
    """
    lego_data = []
    for producto in soup.find_all('div', class_="andes-card ui-search-result ui-search-result--core andes-card--flat andes-card--padding-16"):
        titulo = producto.find('h2', class_="ui-search-item__title").text
        precio = producto.find('span', class_='andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript').text
        cuotas = producto.find('div', class_='ui-search-item__group__element ui-search-installments ui-search-color--BLACK')
        date = datetime.now().strftime("%Y-%m-%d")
        lego_data.append([titulo, precio, cuotas, date])
    return lego_data

def extract_car_data(soup):
    """
    Extrae los datos de la página de productos de automóviles.
    """
    car_data = []
    for producto in soup.find_all('div', class_="ui-search-layout ui-search-layout--grid"):
        titulo_elementos = producto.find_all('h2', class_="ui-search-item__title")
        precio_elementos = producto.find_all('span', class_= "andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript")
        atributos_elementos = producto.find_all('ul', class_="ui-search-card-attributes ui-search-item__group__element")
        ubicacion_elementos = producto.find_all('span', class_ ='ui-search-item__group__element ui-search-item__location')
        for titulo, precio, atributos, ubicacion in zip(titulo_elementos, precio_elementos, atributos_elementos, ubicacion_elementos):
            titulo_texto = titulo.text
            precio_texto = precio.text
            atributos_texto = atributos.text
            year_texto, kilometraje_texto = None, None
            lines = atributos_texto.strip().split('\n')
            for line in lines:
                if line.strip().isdigit() and len(line.strip()) == 4:
                    year_texto = line.strip()
                    break
            if 'Km' in atributos_texto:
                kilometraje_texto = atributos_texto.split('Km')[0].strip()
            # Elimina los primeros 4 caracteres del kilometraje y los asigna a year_texto
            if year_texto is None and kilometraje_texto:
                year_texto = kilometraje_texto[:4]
                kilometraje_texto = kilometraje_texto[4:].strip()
            ubicacion_texto = ubicacion.text if ubicacion else None
            date = datetime.now().strftime("%Y-%m-%d")
            car_data.append([titulo_texto, precio_texto, date, year_texto, kilometraje_texto, ubicacion_texto])
    return car_data

def scrape_mercadolibre(url):
    """
    Extrae datos de la página de MercadoLibre según la URL proporcionada.
    """
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    data = []
    if 'lego' in url:
        data.extend(extract_lego_data(soup))
    else:
        data.extend(extract_car_data(soup))
    return data


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

df['year'] = df['year'].astype('int')
df['kilometraje'] = df['kilometraje'].str.replace('.','', regex=False).astype('int')

print(df)

#Convertir el df a csv en memoria
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)

#Conectar a S3
s3 = boto3.resource('s3')

#Subir al bucket del S3
try:
    s3.Object(bucket_name, file_key).put(Body=csv_buffer.getvalue())
    print(f'El DataFrame se ha subido exitosamente a S3 en s3://{bucket_name}/{file_key}')
except Exception as e:
    logger.warning(e)